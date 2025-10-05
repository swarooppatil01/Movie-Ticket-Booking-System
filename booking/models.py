# booking/models.py

from django.db import models
from django.contrib.auth.models import User # Required for the Booking model's FK

class Movie(models.Model):
    """Model to store movie details."""
    title = models.CharField(max_length=255) # Movie: title [cite: 13]
    duration_minutes = models.IntegerField() # Movie: duration_minutes [cite: 13]

    def __str__(self):
        return self.title

class Show(models.Model):
    """Model to store show timings and screen information."""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE) # Show: movie (FK) [cite: 14]
    screen_name = models.CharField(max_length=100) # Show: screen_name [cite: 14]
    date_time = models.DateTimeField() # Show: date_time [cite: 14]
    total_seats = models.IntegerField() # Show: total_seats [cite: 14]

    def __str__(self):
        return f"{self.movie.title} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    """Model to store individual seat bookings."""
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE) # Booking: user (FK) [cite: 15]
    show = models.ForeignKey(Show, on_delete=models.CASCADE) # Booking: show (FK) [cite: 15]
    seat_number = models.IntegerField() # Booking: seat_number [cite: 15]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked') # Booking: status [cite: 15]
    created_at = models.DateTimeField(auto_now_add=True) # Booking: created_at [cite: 15]
    
    # We add a unique constraint here to prevent double booking in the database layer.
    # Note: While handled in the view logic for cleaner error messages, this is robust.
    class Meta:
        # A single seat number for a show can only be 'booked' once.
        constraints = [
            models.UniqueConstraint(
                fields=['show', 'seat_number'], 
                condition=models.Q(status='booked'), 
                name='unique_active_seat_booking'
            )
        ]

    def __str__(self):
        return f"Booking for {self.show.movie.title} by {self.user.username} (Seat {self.seat_number})"