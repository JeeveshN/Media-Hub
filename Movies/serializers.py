from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        #fields = '__all__' for all of them
        fields = ('Name','Year','Plot','Plot_outline','Imdb_rating')
