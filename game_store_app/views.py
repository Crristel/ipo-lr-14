from django.shortcuts import render
import json
from django.http import JsonResponse
def home_page(request):
    return render(request, 'home_page.html') #render возвращает шаблон html на запрос пользователя

def about_me(request):
    return render(request,'about_me.html')
def game_store(request):
    return render(request,'game_store.html')

def speciality(request):
    specialties = []  
    with open("data/dump.json", 'r', encoding='utf-8') as file:
        read_file = json.load(file)
        
    for specialty in read_file:
        if specialty.get("model") == "data.specialty":
            specialty_data = {
                "code": specialty["fields"].get("code"),
                "pk": specialty.get("pk"),
                "title": specialty["fields"].get("title"),
                "educational": specialty["fields"].get("c_type"),
            }
            specialties.append(specialty_data)  
   

    
    return render(request, 'speciality.html',{'specialties': specialties})

def speciality_found(request):
    code = request.GET.get('code')
    speciality = []  
    with open("data/dump.json", 'r', encoding='utf-8') as file:
        read_file = json.load(file)
        for specialty in read_file:
            if specialty.get("model") == "data.specialty":
                if specialty["fields"].get("code") == code:
                    specialty_data = {
                        "code": specialty["fields"].get("code"),
                        "pk": specialty.get("pk"),
                        "title": specialty["fields"].get("title"),
                        "educational": specialty["fields"].get("c_type"),
                    }
                    speciality.append(specialty_data)  

    return render(request, "speciality_found.html", {'speciality': speciality}) 

def speciality_id(request,id):
    speciality = []  
    with open("data/dump.json", 'r', encoding='utf-8') as file:
        read_file = json.load(file)
        for specialty in read_file:
            if specialty.get("model") == "data.specialty":
                if int(specialty.get("pk")) == int(id):
                    specialty_data = {
                        "code": specialty["fields"].get("code"),
                        "pk": specialty.get("pk"),
                        "title": specialty["fields"].get("title"),
                        "educational": specialty["fields"].get("c_type"),
                    }
                    speciality.append(specialty_data)  

    return render(request, "speciality_found.html", {'speciality': speciality})

    
    
