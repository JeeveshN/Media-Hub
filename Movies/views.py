from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

from .models import Movie

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
    movie=get_object_or_404(Movie,id=movie_id)
    return render(request,'details.html',{'movie':movie})
