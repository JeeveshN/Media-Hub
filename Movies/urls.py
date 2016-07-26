from django.conf.urls import url
from Movies import views,api
from rest_framework.urlpatterns import format_suffix_patterns

app_name='Movies'

urlpatterns = [
    #movies/<movie_id>
    url(r'^(?P<movie_id>[0-9]+)/$',views.detail,name="detail"),
    #movies/<movie_id>/play/
    url(r'^(?P<movie_id>[0-9]+)/play/$',views.Play_movie,name="play"),
    #movies/<movie_id>/watched/
    url(r'^(?P<movie_id>[0-9]+)/watched/$',views.Watched,name="watched"),
    #movies/<movie_id>/watched/
    url(r'^(?P<movie_id>[0-9]+)/watched/stay=True$',views.Watched_stay,name="watched_stay"),
    #movies/api/name=<name>
    url(r'^api/name=(?P<name>[A-Z,a-z," ",""]+|)?&y=(?P<year>[0-9]+|)$',api.API_res,name="api"),
]
