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

def remove_from_liked(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        user_liked_movie = get_object_or_404(UserLikedMovie, user=request.user, movie__id=movie_id)
        user_liked_movie.delete()
        return redirect('my_liked_movies')
    return redirect('home')  # Redirect to home page if not a POST request

import pandas as pd
def generate_recommendations(liked_movies, all_movies):
    
    liked_movie_ids = set(liked_movie.movie.id for liked_movie in liked_movies)
    
    #combine genres for movies with same title
    unique_movies = {}
    for movie in all_movies:
        if movie.id not in liked_movie_ids:  #skip movies already liked
            if movie.title in unique_movies:
                unique_movies[movie.title]['genre'].append(movie.genre)
            else:
                unique_movies[movie.title] = {'id': movie.id, 'genre': [movie.genre]}

    
    unique_movies_df = pd.DataFrame(list(unique_movies.values()))

    #genre vecors
    genre_list = np.unique([genre for genres in unique_movies_df['genre'] for genre in genres])

    def create_genre_vector(genres):
        return np.array([1 if genre in genres else 0 for genre in genre_list])

    unique_movies_df['genre_vector'] = unique_movies_df['genre'].apply(create_genre_vector)

    #liked movies to DF
    liked_movies_df = pd.DataFrame([{
        'id': lm.movie.id,
        'genre': lm.movie.genre,
        'genre_vector': create_genre_vector(lm.movie.genre)
    } for lm in liked_movies])

    #calculate user_vector based on liked movies
    user_vector = np.sum(liked_movies_df['genre_vector'], axis=0)
    user_vector_norm = user_vector / np.linalg.norm(user_vector)  # Normalize user_vector

    #calculate similarity with dot product
    recommendations = []
    for movie in unique_movies_df.itertuples():
        similarity_score = np.dot(user_vector_norm, movie.genre_vector)
        recommendations.append({
            'movieId': movie.id,
            'genre': movie.genre,
            'similarity_score': similarity_score
        })

    recommendations_df = pd.DataFrame(recommendations)
    recommendations_df = recommendations_df.sort_values(by='similarity_score', ascending=False)
   
    recommended_movies_with_details = []
    for movie_id in recommendations_df['movieId']:
        recommended_movie = Movie.objects.filter(id=movie_id).first()
        if recommended_movie:
            #append details for the movie id that has the same title so we can display from database
            similarity_score = recommendations_df.loc[recommendations_df['movieId'] == movie_id]['similarity_score'].iloc[0]
            recommended_movies_with_details.append({
                'id': recommended_movie.id,
                'title': recommended_movie.title,
                'image_url': recommended_movie.image_url,
                'length': recommended_movie.length,
                'rating': recommended_movie.rating,
                'similarity_score': similarity_score
            })

    return recommended_movies_with_details
def action(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, "action.html", context)
def comedy(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, "comedy.html", context)
def drama(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, "drama.html", context)
def horror(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, "horror.html", context)
def romance(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, "romance.html", context)
def SF(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, "science_fiction.html", context)
def fantasy(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, "fantasy.html", context)