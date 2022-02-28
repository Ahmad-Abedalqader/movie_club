from django.shortcuts import render, redirect
from django.http import JsonResponse
from login_app.models import *
from movie_app.models import *
from django.contrib import messages


def main(request):
    # Autocomplete jquerry for search box 
    if "term" in request.GET:
        sr = Movie.objects.filter(title__contains = request.GET.get('term'))
        titles = []
        for movie in sr:
            titles.append(movie.title)
            print(movie.title)
        return JsonResponse(titles, safe=False)
    if 'userid' in request.session:
        context = {
        'all_movies' : Movie.objects.all().order_by('-release_date')[1:6],
        'most_popular' : Movie.objects.all().order_by('-likes')[:10],
        'first_movies' : Movie.objects.all().order_by('-release_date')[0],
        'this_user' : User.objects.get(id=request.session['userid'])
        }
        return render(request,"main_page.html" , context)
    else :
        context = {
            'all_movies' : Movie.objects.all().order_by('-release_date')[1:6],
            'most_popular' : Movie.objects.all().order_by('-likes')[:10],
            'first_movies' : Movie.objects.all().order_by('-release_date')[0],
        }
        return render(request,"main_page.html" , context)


def favorite(request):
    this_user=User.objects.get(id= request.session['userid'])
    context = { 
        'movies' : this_user.favorites.all(),
        'this_user' : this_user
    }
    return render(request,"favorites.html",context)

def add_to_favorites(request,movie_id):
    this_user=User.objects.get(id= request.session['userid'])
    this_movie=Movie.objects.get(id=movie_id)
    this_movie.liked_by.add(this_user)
    this_movie.likes += 1 
    this_movie.save()
    return redirect (f'/movie/{movie_id}')

def remove_from_favorites(request,movie_id):
    this_movie = Movie.objects.get(id=movie_id)
    this_user=User.objects.get(id= request.session['userid'])
    this_movie.liked_by.remove(this_user)
    this_movie.likes -= 1 
    this_movie.save()
    return redirect (f'/movie/{movie_id}')

def movie(request,movie_id):
    # Autocomplete jquerry for search box 
    if "term" in request.GET:
        sr = Movie.objects.filter(title__contains = request.GET.get('term'))
        titles = []
        for movie in sr:
            titles.append(movie.title)
        return JsonResponse(titles, safe=False)
    this_movie = Movie.objects.get(id=movie_id)
    x= this_movie.rates.all()
    sum = 0
    avg = 0
    for i in x:
        sum=sum+i.rate
    if len(x) == 0 :
        avg == 'no ranks yet'
    else :
        avg = sum / len(x)
    if 'userid' in request.session:
        context = {
            'avg' : avg,
            'this_movie' : this_movie,
            'this_user' : User.objects.get(id=request.session['userid']),
            'comments' : this_movie.comments.all()
        }
        return render(request,"movie.html",context)
    else:
        context = {
            'avg' : avg,
            'this_movie' : this_movie,
            'comments' : this_movie.comments.all()
        }
        return render(request,"movie.html",context)

def watch_list(request):
    # Autocomplete jquerry for search box 
    if "term" in request.GET:
        sr = Movie.objects.filter(title__contains = request.GET.get('term'))
        titles = []
        for movie in sr:
            titles.append(movie.title)
        return JsonResponse(titles, safe=False)

    this_user=User.objects.get(id= request.session['userid'])
    context = {
        'this_user': this_user,
        'movies' : this_user.movies_to_watch.all()
    }
    return render(request,"watch_list.html",context)

def add_to_watchlist(request,movie_id):
    this_user=User.objects.get(id= request.session['userid'])
    this_movie=Movie.objects.get(id=movie_id)
    this_movie.to_watch_by.add(this_user)
    return redirect (f'/movie/{movie_id}')

def remove_from_watchlist(request,movie_id):
    this_movie = Movie.objects.get(id=movie_id)
    this_user=User.objects.get(id= request.session['userid'])
    this_user.movies_to_watch.remove(this_movie)
    return redirect (f'/movie/{movie_id}')

def adding_form(request):
    return render(request, "add_movie.html")

def add_movie(request):
    errors = Movie.objects.movie_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/adding_form')
    user_id = request.session['userid']
    this_user = User.objects.get(id = user_id)
    this_movie = Movie.objects.create(
        title = request.POST['title'],
        release_date = request.POST['rel_date'],
        desc = request.POST['desc'],
        trailer_url = request.POST['trailer_url'],
        uplode_image = request.FILES['image'],
        added_by = this_user,
        )
    categories = request.POST.getlist('categ')
    for categ in categories:
        this_categ = Category.objects.get(name = categ)
        this_movie.categories.add(this_categ)
    return redirect("/")

def classify(request, categ):
    # Autocomplete jquerry for search box 
    if "term" in request.GET:
        sr = Movie.objects.filter(title__contains = request.GET.get('term'))
        titles = []
        for movie in sr:
            titles.append(movie.title)
        return JsonResponse(titles, safe=False)

    this_category = Category.objects.get(name = categ)
    categ_movies = this_category.movies.all()
    if "userid" in request.session:
        this_user = User.objects.get(id = request.session['userid'])
        context={
            "user": this_user,
            "movies": categ_movies
            }
    else:
        context={
                "movies": categ_movies
                }
    return render(request, "categ_movies.html", context)

def search(request):
    request.session["search"] = request.POST["search"]
    print(request.session["search"])
    return redirect("/movies/search_result")

def search_result(request):
        
    if "term" in request.GET:
        sr = Movie.objects.filter(title__contains = request.GET.get('term'))
        titles = []
        for movie in sr:
            titles.append(movie.title)
        return JsonResponse(titles, safe=False)
    
    result = Movie.objects.filter(title__contains = request.session["search"])
    if "userid" in request.session:
        this_user = User.objects.get(id = request.session['userid'])
        context={
                "user": this_user,
                "result": result
                }    
    else:
        context={
                "result": result
                }
    return render(request,"search_result.html", context)

def rate(request,movie_id):
    this_user=User.objects.get(id= request.session['userid'])
    this_movie=Movie.objects.get(id=movie_id)
    Rate.objects.create(rate=request.POST['range'],movie=this_movie,user=this_user)
    return redirect(f'/movie/{movie_id}')

def my_movies(request):
    # Autocomplete jquerry for search box 
    if "term" in request.GET:
        sr = Movie.objects.filter(title__contains = request.GET.get('term'))
        titles = []
        for movie in sr:
            titles.append(movie.title)
        return JsonResponse(titles, safe=False)
    if "userid" in request.session:
        this_user=User.objects.get(id= request.session['userid'])
        my_movies = this_user.added_movies.all()
        context={
            "user": this_user,
            "movies": my_movies
            }
        return render(request,"my_movies.html", context)
    else:
        return redirect("/login_form")



def logout(request):
    del(request.session['userid'])
    del(request.session['from'])
    return redirect('/')

def comment(request,movie_id):
    this_user=User.objects.get(id=request.session['userid'])
    this_movie=Movie.objects.get(id=movie_id)
    Comment.objects.create(movie=this_movie,user=this_user,comment=request.POST['comment'])
    return redirect(f'/movie/{movie_id}')

def about_us(request):
    if "userid" in request.session:
        this_user = User.objects.get(id = request.session['userid'])
        context={
                "user": this_user,
                }
        return render(request,'about_us.html', context)
    else:
        return render(request,'about_us.html')