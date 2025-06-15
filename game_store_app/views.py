from django.shortcuts import render
import json
# from django.db.models import Q
from .models import Product,Category,Maker,Basket,Basket_element
from .forms import Filter
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
# from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm

from django.contrib import messages

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
        if specialty.get("model") == "data.speciality":
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
    
def product_list(request):
    products = Product.objects.all()
    form = Filter(request.GET or None)
    if form.is_valid(): #Сохраняются в cleaned_data автоматически
        if form.cleaned_data['category']:
            products = products.filter(category__name__iexact=form.cleaned_data['category']) # Модификатор сравнения, который означает: i - case-insensitive (регистронезависимый) и exact - точное совпадение

        if form.cleaned_data['maker']:
            products = products.filter(maker__name__iexact=form.cleaned_data['maker'])
        if form.cleaned_data['search']:
            products = products.filter(name__icontains=form.cleaned_data['search']) # регистронезависимый поиск подстроки
    
    return render(request, 'shop/product_list.html', {'products': products, 'form': form})

def product_detail(request,id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
            messages.error(request, "Товар не найден.")
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist or  UnboundLocalError :
        messages.error(request, "Товар не найден.")
        return redirect('cart_view')
    basket, created = Basket.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    basket_element, created = Basket_element.objects.get_or_create(
        basket=basket,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        basket_element.quantity += quantity
        basket_element.save()
        messages.success(request, "Количество товара обновлено в корзине.")
    else:
        messages.success(request, "Товар добавлен в корзину.")
    return redirect('cart_view')   

@login_required
@require_POST
def update_cart(request, item_id):
    try:
        basket_element = Basket_element.objects.get(id=item_id, basket__user=request.user)
    except Basket_element.DoesNotExist:
        messages.error(request, "Не удалось обновить корзину")
        return redirect('cart_view')

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity <= 0:
        basket_element.delete()
        messages.success(request, "Товар удалён из корзины")
    elif quantity <= basket_element.product.stok_quantity:
        basket_element.quantity = quantity
        basket_element.save()
        messages.success(request, "Количество обновлено")
    else:
        messages.error(request, "Недостаточно товара на складе")

    return redirect('cart_view')

@login_required
def remove_from_cart(request, item_id):
    try:
        basket_element = Basket_element.objects.get(id=item_id, basket__user=request.user)
        basket_element.delete()
        messages.success(request, "Товар удалён из корзины")
    except Basket_element.DoesNotExist:
        messages.error(request, "Товар не найден в корзине")
    return redirect('cart_view')

@login_required
def cart_view(request):
    basket, created = Basket.objects.get_or_create(user=request.user)
    basket_elements = basket.basket_elements.select_related('product').all()
    total = sum(item.element_cost() for item in basket_elements)
    context = {
        'cart_items': basket_elements,
        'total': total,
    }
    return render(request, 'shop/cart.html', context)





def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cart_view')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cart_view')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})