from django.urls import path
from .views import home_page,about_me,game_store

urlpatterns = [
    path('', home_page, name='home_page'),
    path('about_me', about_me, name='about_me'),
    path('game_store', game_store, name='game_store'),

]