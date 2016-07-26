from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Movie
from bs4 import BeautifulSoup
import threading
import urllib
import os
import re

def get_youtube_link(movie):
    query = urllib.quote_plus(movie.Name)
    f = urllib.urlopen('https://www.youtube.com/results?search_query='+query+'+trailer').read()
    soup=BeautifulSoup(f,'lxml')
    item = soup.find_all('ol',{'class':'item-section'})
    for itm in item:
        a = item[0].find_all('a',{'class':'yt-uix-sessionlink'})[0]
    a = re.findall('=(.*)',a.get('href'))
    print a
    link= 'http://www.youtube.com/embed/'+a[0]
    movie.trailer=link
    movie.save()

def index(request):
    if 'user' in request.session:
        movies=Movie.objects.all()
        return render(request,'main.html',{'movies':movies})
    return render(request,'login.html')

def logged_in(request):
    if 'user' in request.session and request.user.is_authenticated():
        movies=Movie.objects.all()
        return render(request,'main.html',{'movies':movies})
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        if not User.objects.filter(username=username).exists():
            return render(request,'login.html',{'error_message':'Please Register First'})
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                request.session['user']=username
                movies=Movie.objects.all()
                return render(request,'main.html',{'movies':movies})
            else:
                return render(request,'login.html',{'error_message':'Your Account Has Been Suspended'})
        return render(request,'login.html',{'error_message':'Wrong Credentials'})
    return render(request,'login.html')

def register(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        rep_password=request.POST['rep_password']
        e_mail=request.POST['email']
        if User.objects.filter(email=e_mail).exists():
            return render(request,'register.html',{'error_message':'E-mail already registered'})
        elif User.objects.filter(username=username).exists():
            return render(request,'register.html',{'error_message':'Username not available'})
        elif(password!=rep_password):
            return render(request,'register.html',{'error_message':'Passwords Dont match'})
        else:
            user=User(username=username,email=e_mail)
            user.set_password(password)
            user.save()
            user=authenticate(username=username,password=password)
            login(request,user)
            request.session['user']=username
            movies=Movie.objects.all()
            return render(request,'main.html',{'movies':movies})
    return render(request,'register.html')


def log_out(request):
    if 'user' in request.session:
        del request.session['user']
        logout(request)
        return redirect('logged_in')

def detail(request,movie_id):
    if not request.user.is_authenticated():
        return redirect('logged_in')
    threadobj= threading.Thread(target=get_youtube_link,args=[])
    movie=get_object_or_404(Movie,id=movie_id)
    print movie.trailer
    if not movie.trailer:
        try:
            get_youtube_link(movie)
        except:
            pass
    return render(request,'details.html',{'movie':movie})

def search_movie(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            if not request.POST['search']:
                return redirect('logged_in')
            if '-w' in request.POST['search']:
                Q=re.findall('(.*)\s+-w',request.POST['search'])
                if not Q:
                    movies=Movie.objects.filter(Watched=False)
                    return render(request,'main.html',{'movies':movies})
                else:
                    Q=Q[0]
                    list1=Movie.objects.filter(Name__contains=Q,Watched=False)
                    list2=Movie.objects.filter(Year__contains=Q,Watched=False)
                    list3=Movie.objects.filter(Genre__contains=Q,Watched=False)
            else:
                Q=request.POST['search']
                list1=Movie.objects.filter(Name__contains=Q)
                list2=Movie.objects.filter(Year__contains=Q)
                list3=Movie.objects.filter(Genre__contains=Q)
            res=list(set(list1)^set(list2)^set(list3))
            context={
                'movies':res,
            }
            return render(request,'main.html',context)
    return redirect('logged_in')
def Play_movie(request,movie_id):
    if request.user.is_authenticated():
        movie=get_object_or_404(Movie,id=movie_id)
        os.system('xdg-open '+'"'+movie.Path+'"')
        return render(request,'details.html',{'movie':movie})
    return redirect('logged_in')

def Watched(request,movie_id):
    if request.user.is_authenticated():
        movie=get_object_or_404(Movie,id=movie_id)
        if movie.Watched:
            movie.Watched=False
        else:
            movie.Watched=True
        movie.save()
    return redirect('logged_in')

def Watched_stay(request,movie_id):
    if request.user.is_authenticated():
        movie=get_object_or_404(Movie,id=movie_id)
        if movie.Watched:
            movie.Watched=False
        else:
            movie.Watched=True
        movie.save()
        return render(request,'details.html',{'movie':movie})
    return redirect('logged_in')
