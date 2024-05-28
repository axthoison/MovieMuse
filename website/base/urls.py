from django.urls import path, include
from .views import (
    authView, home, movie_list, movie_create, movie, 
    movie_list_by_genre, director_list, like_movie, 
    my_liked_movies, remove_from_liked, action, comedy, 
    drama, horror, romance, SF, fantasy, lists, liked_list_api
)




urlpatterns = [
 path("", home, name="home"),
 path("signup/", authView, name="authView"),
 path("accounts/", include("django.contrib.auth.urls")),
 path('movies/', movie_list, name="movie_list" ),
 path('movies/create/', movie_create, name='movie_create'),
 path('movies/<int:pk>/', movie, name='movie_detail'),
 path('like_movie/', like_movie, name='like_movie'),
 path('movies/genre/<str:genre>/', movie_list_by_genre, name='movie_list_by_genre'),
 path('directors/', director_list, name='director_list'),
 path('my-liked-movies/', my_liked_movies, name='my_liked_movies'),
 path('remove_from_liked/', remove_from_liked, name='remove_from_liked'),
 path('likedlist/', liked_list_api, name='likedlist'),
 path('action/', action , name='action'),
 path('comedy/', comedy , name='comedy'),
 path('drama/', drama , name='drama'),
 path('horror/', horror , name='horror'),
 path('romance/', romance , name='romance'),
 path('science_fiction/', SF , name='SF'),
 path('fantasy/', fantasy, name='fantasy'),
 path('lists/', lists, name='lists'),
]