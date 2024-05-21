from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Movie, UserLikedMovie
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import MovieSerializer
from django.http import JsonResponse
import numpy as np
import pandas as pd

@login_required
def home(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, "home.html", context)

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("base:login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def movie_create(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    else:
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def movie(request, pk):
    if request.method == 'GET':
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie)
            return JsonResponse(serializer.data)
        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Movie not found'}, status=404)
    elif request.method == 'PUT':
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            else:
                return JsonResponse(serializer.errors, status=400)
        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Movie not found'}, status=404)
    elif request.method == 'DELETE':
        try:
            movie = Movie.objects.get(pk=pk)
            movie.delete()
            return JsonResponse({'message': 'Movie deleted successfully!'})
        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Movie not found'}, status=404)

@login_required
def like_movie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie = get_object_or_404(Movie, id=movie_id)
        user_liked_movie, created = UserLikedMovie.objects.get_or_create(user=request.user, movie=movie)
        if created:
            message = 'Movie added to your liked list.'
        else:
            message = 'Movie already in your liked list.'
        return JsonResponse({'message': message})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def my_liked_movies(request):
    liked_movies = UserLikedMovie.objects.filter(user=request.user).select_related('movie')

    all_movies = Movie.objects.all()
    recommendations = generate_recommendations(liked_movies, all_movies)

    context = {
        'liked_movies': liked_movies,
        'recommendations': recommendations
    }
    
    return render(request, 'my_liked_movies.html', context)

import pandas as pd

def generate_recommendations(liked_movies, all_movies):
    #combina genres
    unique_movies = {}
    for movie in all_movies:
        if movie.title in unique_movies:
            unique_movies[movie.title]['genre'].append(movie.genre)
        else:
            unique_movies[movie.title] = {'id': movie.id, 'genre': [movie.genre]}

    # Convert unique_movies to DataFrame
    unique_movies_df = pd.DataFrame(list(unique_movies.values()))

    # Create genre vectors
    genre_list = np.unique([genre for genres in unique_movies_df['genre'] for genre in genres])

    def create_genre_vector(genres):
        return np.array([1 if genre in genres else 0 for genre in genre_list])

    unique_movies_df['genre_vector'] = unique_movies_df['genre'].apply(create_genre_vector)

    #unique movies test file
    unique_movies_df.to_csv('unique_movies.csv', index=False)

    # convert liked movies to DataFrame
    liked_movies_df = pd.DataFrame([{
        'id': lm.movie.id,
        'genre': lm.movie.genre,
        'genre_vector': create_genre_vector(lm.movie.genre)
    } for lm in liked_movies])

    #similarity scores
    recommendations = []
    for liked_movie in liked_movies_df.itertuples():
        for movie in unique_movies_df.itertuples():
            if liked_movie.id != movie.id:
                similarity_score = np.dot(liked_movie.genre_vector, movie.genre_vector)
                recommendations.append({
                    'movieId': movie.id,
                    'genre': movie.genre,
                    'similarity_score': similarity_score
                })

    recommendations_df = pd.DataFrame(recommendations)
    recommendations_df = recommendations_df.sort_values(by='similarity_score', ascending=False)

    return recommendations_df.to_dict(orient='records')