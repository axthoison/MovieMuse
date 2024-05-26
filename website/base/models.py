
from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):

    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('science_fiction', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('top50','Top 50'),
        ('python','Python')
    ]

    uu_id = models.UUIDField(default=uuid.uuid4) #unique id
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    length = models.CharField(max_length=20)
    rating = models.CharField(max_length=10)
    description = models.TextField()
    image_url = models.URLField()
    image2_url = models.URLField()
    director = models.CharField(max_length=255)
    stars = models.TextField()

    
    def __str__(self):
        return self.title

class UserLikedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} likes {self.movie.title}"