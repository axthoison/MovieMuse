"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from base import views


schema_view = get_schema_view(
   openapi.Info(
      title="Movie API",
      default_version='v1',
      description="API for managing movies",
      terms_of_service="https://www.example.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('base.urls', 'base'), namespace='base')),
    path('api/v1/', include('base.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('likedlist/', views.liked_list_api, name='likedlist'),
    path('movies/', views.movie_list, name="movie_list"),
    path('movies/create/', views.movie_create, name='movie_create'),
    path('movies/<int:pk>/', views.movie, name='movie_detail'),
    path('like_movie/', views.like_movie, name='like_movie'),
    path('movies/genre/<str:genre>/', views.movie_list_by_genre, name='movie_list_by_genre'),
    path('directors/', views.director_list, name='director_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
