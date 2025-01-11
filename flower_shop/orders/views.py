# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Flower, Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('flower_catalog')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


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

# Оформление корзины
@login_required
def add_to_cart(request, flower_id):
    """Добавление цветка в корзину"""
    flower = get_object_or_404(Flower, id=flower_id)
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})

    if flower_id in cart:
        cart[flower_id]['quantity'] += quantity
    else:
        cart[flower_id] = {
            'name': flower.name,
            'color': flower.color,
            'price': float(flower.price),
            'quantity': quantity
        }

    request.session['cart'] = cart
    return redirect('flower_catalog')


@login_required
def view_cart(request):
    """Отображение корзины"""
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'orders/cart.html', {'cart': cart, 'total_price': total_price})


@login_required
def checkout(request):
    """Оформление заказа на все товары в корзине"""
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('flower_catalog')

    for flower_id, item in cart.items():
        flower = Flower.objects.get(id=flower_id)
        Order.objects.create(
            user=request.user,
            flower=flower,
            quantity=item['quantity'],
            address=request.POST['address'],
            comments=request.POST.get('comments', '')
        )

    request.session['cart'] = {}  # Очищаем корзину после оформления заказа
    return redirect('order_success')
