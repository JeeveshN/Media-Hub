from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import MovieSerializer
from .models import Movie

#/movies/api
@api_view(['GET','POST'])
def API_res(request,name,year):
    if request.method == 'GET':
        if year and name:
            movies=Movie.objects.filter(Name__contains=name,Year=year)
        elif name:
            movies=Movie.objects.filter(Name__contains=name)
        else:
            movies=Movie.objects.filter(Year=year)
        serializer = MovieSerializer(movies,many=True)
        return Response(serializer.data)
