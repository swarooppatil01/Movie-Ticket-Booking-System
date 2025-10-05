from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    RegisterView, MovieListView, ShowListView, BookSeatView,
    CancelBookingView, MyBookingsListView
)

urlpatterns = [
    # Auth
    path('signup/', RegisterView.as_view(), name='signup'), # POST /signup [cite: 18]
    path('login/', TokenObtainPairView.as_view(), name='login'), # POST /login [cite: 19]

    # Movies & Shows
    path('movies/', MovieListView.as_view(), name='movie-list'), # GET /movies/ [cite: 20]
    path('movies/<int:movie_id>/shows/', ShowListView.as_view(), name='show-list'), # GET /movies/<id>/shows/ [cite: 21]

    # Booking
    path('shows/<int:show_id>/book/', BookSeatView.as_view(), name='book-seat'), # POST /shows/<id>/book/ [cite: 22]
    path('bookings/<int:booking_id>/cancel/', CancelBookingView.as_view(), name='cancel-booking'), # POST /bookings/<id>/cancel/ [cite: 24]
    path('my-bookings/', MyBookingsListView.as_view(), name='my-bookings'), # GET /my-bookings/ [cite: 25]
]