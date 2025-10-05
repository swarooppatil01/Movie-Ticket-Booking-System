from rest_framework import serializers
from .models import Movie, Show, Booking
from django.contrib.auth.models import User

# --- Authentication Serializers ---
class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}} # Password shouldn't be returned

    def create(self, validated_data):
        # Hash the password when creating the user for security
        user = User.objects.create_user(**validated_data)
        return user

# --- Core Models Serializers ---
class MovieSerializer(serializers.ModelSerializer):
    """Serializer for the Movie model."""
    class Meta:
        model = Movie
        fields = '__all__'

class ShowSerializer(serializers.ModelSerializer):
    """Serializer for the Show model, including calculated available seats."""
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = ['id', 'movie', 'movie_title', 'screen_name', 'date_time', 'total_seats', 'available_seats']

    # Calculates available seats: total_seats - currently booked seats
    def get_available_seats(self, obj):
        # Count only 'booked' status to represent seats currently taken
        booked_count = obj.booking_set.filter(status='booked').count()
        return obj.total_seats - booked_count

class BookingSerializer(serializers.ModelSerializer):
    """Serializer for the Booking model."""
    username = serializers.CharField(source='user.username', read_only=True)
    # Use the ShowSerializer to display detailed show information when viewing a booking
    show_details = ShowSerializer(source='show', read_only=True) 

    class Meta:
        model = Booking
        fields = ['id', 'username', 'show', 'show_details', 'seat_number', 'status', 'created_at']
        read_only_fields = ['user', 'status']