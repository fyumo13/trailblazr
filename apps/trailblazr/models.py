from django.db import models
from datetime import datetime
from ..login_registration.models import User
from enum import Enum

class TrailManager(models.Manager):
    def add_trail(self, user_id, trail_id, trail_name, trail_location, trail_lat, trail_lon, trail_length, trail_ascent, trail_descent, trail_difficulty):
        user = User.objects.get(id=user_id)
        trail_id = trail_id
        trail_name = trail_name
        trail_location = trail_location
        trail_lat = trail_lat
        trail_lon = trail_lon
        trail_length = trail_length
        trail_ascent = trail_ascent
        trail_descent = trail_descent
        trail_difficulty = trail_difficulty
        trail = Trail.objects.create(user=user, trail_id=trail_id, name=trail_name, location=trail_location, lat=trail_lat, lon=trail_lon, length=trail_length, ascent=trail_ascent, descent=trail_descent, difficulty=trail_difficulty)
        return trail

class Trail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trail_id = models.IntegerField()
    name = models.CharField(max_length=255, default='')
    location = models.CharField(max_length=255, default='')
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    length = models.FloatField(default=0)
    ascent = models.FloatField(default=0)
    descent = models.FloatField(default=0)
    class DifficultyOptions(Enum):
        BEGINNER = 'Beginner'
        INTERMEDIATE = 'Intermediate'
        ADVANCED = 'Advanced'

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]
    difficulty = models.CharField(max_length=12, choices=DifficultyOptions.choices(), default='Beginner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TrailManager()

    def __str__(self):
        return "{}".format(self.trail_id)