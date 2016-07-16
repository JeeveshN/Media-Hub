from django.conf.urls import url
from Movies import views

app_name='Movies'

urlpatterns = [
    #movies/<movie_id>
    url(r'^(?P<movie_id>[0-9]+)/$',views.detail,name="detail"),
]
