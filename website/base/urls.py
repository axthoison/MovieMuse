from django.urls import path, include
from .views import authView, home
from .views import movie_list, movie_create, movie
from .views import like_movie
from .views import my_liked_movies
from .views import remove_from_liked
urlpatterns = [
 path("", home, name="home"),
 path("signup/", authView, name="authView"),
 path("accounts/", include("django.contrib.auth.urls")),
 path('movies/', movie_list, name="movie_list" ),
 path('movies/create/', movie_create, name='movie_create'),
 path('movies/<int:pk>/', movie, name='movie_detail'),
 path('like_movie/', like_movie, name='like_movie'),
 path('my-liked-movies/', my_liked_movies, name='my_liked_movies'),
 path('remove_from_liked/', remove_from_liked, name='remove_from_liked'),
]