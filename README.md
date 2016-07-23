# Media-Hub
A Django based Web application that indexes all movies in your computer and fetches information from Imdb and save it in a Database.  
**After initial setup requires no internet connection can be accesed when offline.**

###Installations
```
sudo apt-get install python-django
sudo pip install imdbpy
```

###Setting Up
```
Inside Media-Hub
python Shelf.py "Media Directory(Suggested) or leave blank to search the whole hard drive"
python manage.py populate
```
Shelf.py goes through the given directory or the whole hard drive(depending on choice) looking for potential movie files and then stores the movie object returned by Imdbpy in a file.  
This file is then accesed by populate command which then populates the database with relevent entires  
  
**Note:**  
1. Once Shelf.py starts indexing do not stop the program or else next time it'll start indexing from the start.The     process will take a lot of time depending upon movie files present in the specified directory and the net speed.    
**(Can run it multiple times on smaller directories before proceeding to next step too)**  
2.The populate command will take time depending on net speed as it fetches movie Posters.This task need not be done in one go you can stop the program and when you run it again it will not process movies that have already been put in Database.

##Let's Start
```
python manage.py runserver
go to 127.0.0.1:8000
```

##Demo:
![](/extras/main.png?raw=true)

Click on any Movie to know more **Details** or **Play** it.

![](/extras/details.png?raw=true)

Users can watch/unwatch movies also and then filter their results based on it too.

**Search:**  
User can search movies based on Title,Year and Genre.  
Add **-w** after the search item and the search would give results filtering through all the **unwatched movies**.  
Only **-w** without any search item will display all the **unwatched movies**.

##Admin Access
Movies can be deleted or edited through the admin panel at **127.0.0.1:8000/admin**
But for that you will need to set up a superuser

```
python manage.py createsuperuser
```
And now you can delete or edit movies from the admin panel using the username and password you set. 
