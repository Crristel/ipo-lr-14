from django.urls import path
from .views import home_page,about_me,game_store,speciality,speciality_found,speciality_id

urlpatterns = [
    path('', home_page, name='home_page'),
    path('about_me', about_me, name='about_me'),
    path('game_store', game_store, name='game_store'),
    path('spec', speciality, name='speciality'),
    path('spec/<int:id>/', speciality_id, name='speciality_id'),
    path('speciality_found', speciality_found, name='speciality_found'),


]