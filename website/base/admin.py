from django.contrib import admin
from .models import Movie
from .models import UserLikedMovie

admin.site.register(UserLikedMovie)
admin.site.register(Movie)
