from django.contrib.auth.models import AbstractUser #для user

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.


class CustomUser(AbstractUser):
    about_yourself = models.TextField(blank=True, null=True,verbose_name="О себе", max_length=200)
    


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название") #verbose_name задает название конкретного поля
    description = models.TextField(blank=True, null=True,verbose_name="Описание") #blanck = true - настройка для форм ("можно не заполнять"). null = True - настройка для БД ("можно хранить NULL").

    def __str__(self): #нужен для строкового представления объекта иначе будет вот так <Product: Product object (1)> | self ссылка на текущий экземпляр объекта
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Категория" #задаёт название в целом для всей модели
        verbose_name_plural = "Категории"



class Maker(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    country = models.CharField(max_length=100,verbose_name="Страна")
    description = models.TextField(blank=True, null=True,verbose_name="Описание")
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
 


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(blank=True, null=True,upload_to="media", verbose_name="Фото товара") # upload_to - папка для загрузки
    price = models.DecimalField(decimal_places=2, max_digits=10,validators=[MinValueValidator(0)],verbose_name="Цена")
    stok_quantity = models.IntegerField(validators=[MinValueValidator(0)],verbose_name="Количество на складе")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name="Категория")
    maker = models.ForeignKey(Maker,on_delete=models.CASCADE,verbose_name="Производитель")
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    

class Basket(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,verbose_name="Пользователь")
    creation_date = models.DateTimeField(auto_now_add= True,verbose_name="Дата создания")

    def __str__(self):
        return f"Корзина пользователя <{self.user.username}>"
    
    def total_cost(self):
        return sum(item.element_cost() for item in self.basket_elements.all())
    
    total_cost.short_description ='Общая стоимость' # для нормального отображения в админке

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"



class Basket_element(models.Model):
    basket = models.ForeignKey(Basket,on_delete=models.CASCADE,verbose_name="Корзина",related_name='basket_elements') 
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name}({self.quantity} шт.)"
    
    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"
    
    def element_cost(self):
        return self.product.price * self.quantity
    
    element_cost.short_description ='Стоимость элемента'

    def clean(self):
        if self.quantity > self.product.stok_quantity:
            raise ValidationError(
                f"Недостаточно товара на складе. Доступно: {self.product.stok_quantity}"
            )




