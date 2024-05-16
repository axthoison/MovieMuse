from django.urls import path, include
from .views import authView, home
from .views import movie_list, movie_create, movie

urlpatterns = [
 path("", home, name="home"),
 path("signup/", authView, name="authView"),
 path("accounts/", include("django.contrib.auth.urls")),
 path('movies/', movie_list, name="movie_list" ),
 path('movies/create/', movie_create, name='movie_create'),
 path('movies/<int:pk>/', movie, name='movie_detail')
]