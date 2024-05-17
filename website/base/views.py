from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Movie
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import MovieSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, UserLikedMovie

@login_required
def home(request):
 movies = Movie.objects.all()
 context = {
        'movies': movies,
    }
 return render(request, "home.html",context)


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


def my_liked_movies(request):
    # Retrieve the liked movies for the current user
    liked_movies = UserLikedMovie.objects.filter(user=request.user)
    
    context = {
        'liked_movies': liked_movies
    }
    
    return render(request, 'my_liked_movies.html', context)