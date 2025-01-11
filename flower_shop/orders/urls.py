from django.urls import path
from .views import flower_catalog, create_order, register, add_to_cart, view_cart, checkout


urlpatterns = [
    path('', flower_catalog, name='flower_catalog'),
    path('order/<int:flower_id>/', create_order, name='create_order'),
    path('register/', register, name='register'),  # Маршрут для регистрации
    path('cart/add/<int:flower_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
]
