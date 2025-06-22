# Register your models here.
from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

from .models import Category, Maker, Product, Basket,Basket_element,Order,OrderItem
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name","description")

@admin.register(Maker)
class MakerAdminModel(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name", "country")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo', 'price', 'stok_quantity', 'category', 'maker')
    list_filter = ('category', 'maker')
    search_fields = ('name', 'description')
    
    def display_photo(self, obj): # self это стандартный первый параметр любого метода класса в Python. Сам экземпляр класса 
        if obj.photo: #есть ли у товара загруженное фото (поле photo не пустое)
            return format_html( #безопасно создаёт HTML-код                                                                              
                '<img src="{}" width="70" height="70" style="object-fit: contain; background: #f0f0f0;" />', #object-fit: contain - сохраняет пропорции, помещая всё изображение в заданные размеры
                obj.photo.url # url фото вставляется в <img src= "{}" c помощью format_html
            )
        return "—"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email']
    # поля при редактировании 
    fieldsets = (
         # none это означает, что поля username и password будут отображаться без заголовка
        ('Персональная информация', {
            'fields': ('username','first_name', 'last_name','about_yourself','email','password')
        }),
        
    )
    # поля при создании
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date', 'total_cost',)
    list_filter = ('creation_date',)
    search_fields = ('user__username',)
    readonly_fields = ('creation_date', 'total_cost',) # readonly_fields нельзя редактировать только режим чтения
    fieldsets = (
            (None, {
                'fields': ('user', 'creation_date', 'total_cost')
            }),
        )


@admin.register(Basket_element)
class BasketElementAdmin(admin.ModelAdmin):
    list_display = ('basket', 'product', 'quantity', 'element_cost',)
    list_filter = ('basket__user', 'product',)
    search_fields = ('product__name', 'basket__user__username',)
    readonly_fields = ('element_cost',)
    
    fieldsets = (
        (None, {
            'fields': ('basket', 'product', 'quantity')
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'total_price',)
    list_filter = ('created',)
    search_fields = ('user__username',)
    readonly_fields = ('created', 'total_price',) # readonly_fields нельзя редактировать только режим чтения
    fieldsets = (
            (None, {
                'fields': ('user', 'created', 'total_price')
            }),
        )
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price',)
    list_filter = ('order__user', 'product',)
    search_fields = ('product__name', 'order__user__username',)
    readonly_fields = ('price',)
    
    fieldsets = (
        (None, {
            'fields': ('order', 'product', 'quantity')
        }),
    )