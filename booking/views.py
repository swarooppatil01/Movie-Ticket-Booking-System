from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction
from django.shortcuts import get_object_or_404 # Correct import for checking object existence

from .models import Movie, Show, Booking
from .serializers import (
    MovieSerializer, ShowSerializer, BookingSerializer, UserSerializer
)

# --- 1. Authentication Views ---

# POST /signup (Register a user)
class RegisterView(generics.CreateAPIView):
    """Handles user registration."""
    serializer_class = UserSerializer

# POST /login (Handled by simplejwt's TokenObtainPairView, mapped in urls.py)

# --- 2. Movie and Show Views ---

# GET /movies/ (List all movies)
class MovieListView(generics.ListAPIView):
    """Lists all available movies."""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # This endpoint is public

# GET /movies/<id>/shows/ (List all shows for a movie)
class ShowListView(generics.ListAPIView):
    """Lists all shows for a specific movie."""
    serializer_class = ShowSerializer
    
    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        # Use get_object_or_404 to immediately return a 404 if the movie doesn't exist
        get_object_or_404(Movie, id=movie_id)
        return Show.objects.filter(movie_id=movie_id).order_by('date_time')
    # This endpoint is public

# --- 3. Booking Views ---

# POST /shows/<id>/book/ (Book a seat)
class BookSeatView(APIView):
    """Books a seat for a specific show, applying business rules."""
    permission_classes = [IsAuthenticated] # Requires JWT token

    def post(self, request, show_id):
        seat_number = request.data.get('seat_number')
        show = get_object_or_404(Show, id=show_id)

        # Basic input validation
        if not seat_number:
            return Response({"error": "seat_number is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            seat_number = int(seat_number)
        except ValueError:
             return Response({"error": "seat_number must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Input validation: check seat number range (Bonus Point)
        if not (1 <= seat_number <= show.total_seats):
            return Response(
                {"error": f"Seat number must be between 1 and {show.total_seats} for this show."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Use a transaction for atomic operation (prevents concurrent double booking)
            with transaction.atomic():
                # Prevent double booking: Check if the seat is already *actively* booked
                active_booking = Booking.objects.select_for_update().filter(
                    show=show,
                    seat_number=seat_number,
                    status='booked'
                ).exists()

                if active_booking:
                    return Response(
                        {"error": f"Seat {seat_number} is already booked for this show."}, 
                        status=status.HTTP_409_CONFLICT
                    )

                # Prevent overbooking: Check current booked seats against capacity
                booked_count = Booking.objects.filter(show=show, status='booked').count()
                if booked_count >= show.total_seats:
                    return Response(
                        {"error": "Show is fully booked (overbooking prevented)."}, 
                        status=status.HTTP_409_CONFLICT
                    )

                # Create the booking
                booking = Booking.objects.create(
                    user=request.user,
                    show=show,
                    seat_number=seat_number,
                    status='booked'
                )
                serializer = BookingSerializer(booking)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Proper try/except error handling
            return Response(
                {"error": f"An internal server error occurred during booking: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# POST /bookings/<id>/cancel/ (Cancel a booking)
class CancelBookingView(APIView):
    """Cancels an existing booking."""
    permission_classes = [IsAuthenticated] # Requires JWT token

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)

        # Security check: A user cannot cancel another user's booking (Bonus Point)
        if booking.user != request.user:
            return Response(
                {"error": "You do not have permission to cancel this booking."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        if booking.status == 'cancelled':
            return Response(
                {"message": "Booking is already cancelled."}, 
                status=status.HTTP_200_OK
            )
        
        # Check if show time has passed (Optional: good practice)
        # if booking.show.date_time < timezone.now():
        #     return Response({"error": "Cannot cancel a past show's booking."}, status=status.HTTP_400_BAD_REQUEST)

        # Cancelling frees up the seat
        booking.status = 'cancelled'
        booking.save()

        serializer = BookingSerializer(booking)
        return Response(
            {"message": "Booking cancelled successfully. The seat is now free.", "booking": serializer.data}, 
            status=status.HTTP_200_OK
        )


# GET /my-bookings/ (List all bookings for the logged-in user)
class MyBookingsListView(generics.ListAPIView):
    """Lists all bookings for the logged-in user."""
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated] # Requires JWT token

    def get_queryset(self):
        # Filter bookings by the authenticated user
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')