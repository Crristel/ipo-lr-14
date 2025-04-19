from django.shortcuts import render
import json
from django.http import JsonResponse
def home_page(request):
    return render(request, 'home_page.html') #render возвращает шаблон html на запрос пользователя

def about_me(request):
    return render(request,'about_me.html')
def game_store(request):
    return render(request,'game_store.html')



    
    
