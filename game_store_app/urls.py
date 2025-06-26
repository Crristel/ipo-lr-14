from django.urls import path, include
from .views import (home_page,about_me,game_store,speciality,speciality_found,
speciality_id,product_list,product_detail,
add_to_cart,update_cart,remove_from_cart, 
cart_view,user_login,register,checkout,)


from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    CategoryViewSet,
    MakerViewSet,
    BasketViewSet,
    Basket_elementViewSet,
    OrderViewSet,
    OrderItemViewSet
)
router = DefaultRouter()
# Регистрация ViewSet в роутере
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'makers', MakerViewSet)
router.register(r'baskets', BasketViewSet)
router.register(r'basket-elements', Basket_elementViewSet) 
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)   


urlpatterns = [
     
    path('api', include(router.urls)),

    path('', home_page, name='home_page'), # name что бы можно было указывать только его в a href к примеру
    path('about_me', about_me, name='about_me'),
    path('game_store', game_store, name='game_store'),
    path('spec', speciality, name='speciality'),
    path('spec/<int:id>/', speciality_id, name='speciality_id'),
    path('speciality_found', speciality_found, name='speciality_found'),
    path('catalog',product_list, name='catalog'),
    path('catalog/<int:id>/',product_detail,name='product_detail'),

    path('cart/', cart_view,name= 'cart_view'),
    path('cart/add/<int:product_id>/',add_to_cart,name='add_to_cart'), #а вот здесь уже самого товара
    path('cart/update/<int:item_id>/',update_cart,name='update_cart'), #id элемента корзины а не самого товара
    path('cart/remove/<int:item_id>/',remove_from_cart,name='remove_from_cart'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('checkout/',checkout,name='checkout')
    
]