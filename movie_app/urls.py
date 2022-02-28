from django.urls import path     
from . import views
urlpatterns = [
    path('', views.main),   
    path('favorite/', views.favorite),
    path('movie/<movie_id>', views.movie),   
    path('watch_list/', views.watch_list),
    path('adding_form', views.adding_form),
    path('add_movie', views.add_movie),
    path('rate/<movie_id>', views.rate),
    path('add_to_watchlist/<movie_id>', views.add_to_watchlist),
    path('add_to_favorites/<movie_id>', views.add_to_favorites),
    path('remove_from_watchlist/<movie_id>', views.remove_from_watchlist),
    path('remove_from_favorites/<movie_id>', views.remove_from_favorites),
    path('category/<categ>', views.classify),
    path('movies/search', views.search),
    path('movies/search_result', views.search_result, name="search_result"),
    path('rate/<movie_id>', views.rate),
    path('my_movies', views.my_movies),
    path('logout', views.logout),
    path('comment/<movie_id>', views.comment),
    path('about_us', views.about_us)
]