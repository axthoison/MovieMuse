from rest_framework import serializers

from .models import Movie
class MovieSerializer(serializers.ModelSerializer):
    # Serializer class for converting Movie model instances to JSON and vice versa
    class Meta:
        model = Movie
        fields = '__all__'
