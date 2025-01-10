from django.urls import path
from .views import flower_catalog, create_order

urlpatterns = [
    path('', flower_catalog, name='flower_catalog'),
    path('order/<int:flower_id>/', create_order, name='create_order'),
]
