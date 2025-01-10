# Create your views here.
from django.shortcuts import render, redirect
from .models import Flower, Order
from django.contrib.auth.decorators import login_required

# Просмотр каталога цветов
def flower_catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'orders/catalog.html', {'flowers': flowers})

# Оформление заказа
@login_required
def create_order(request, flower_id):
    flower = Flower.objects.get(id=flower_id)
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        address = request.POST['address']
        comments = request.POST.get('comments', '')
        order = Order.objects.create(
            user=request.user,
            flower=flower,
            quantity=quantity,
            address=address,
            comments=comments
        )
        return redirect('order_success')
    return render(request, 'orders/create_order.html', {'flower': flower})
