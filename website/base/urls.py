from django.urls import path, include
from .views import authView, home
from .views import movie_list, movie_create, movie, movie_list_by_genre, director_list
from .views import like_movie
from .views import my_liked_movies
from .views import remove_from_liked
from .views import action
from .views import comedy
from .views import drama
from .views import horror
from .views import romance
from .views import SF
from .views import fantasy
from .views import lists,liked_list_api




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