from django.conf.urls import url
from Movies import views

app_name='Movies'

urlpatterns = [
    #movies/<movie_id>
    url(r'^(?P<movie_id>[0-9]+)/$',views.detail,name="detail"),
    #movies/<movie_id>/play/
    url(r'^(?P<movie_id>[0-9]+)/play/$',views.Play_movie,name="play"),
    #movi#movies/<movie_id>/watched/
    url(r'^(?P<movie_id>[0-9]+)/watched/$',views.Watched,name="watched"),
    #movi#movies/<movie_id>/watched/
    url(r'^(?P<movie_id>[0-9]+)/watched/stay=True$',views.Watched_stay,name="watched_stay"),

]
