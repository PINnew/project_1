# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Flower, Order, OrderItem
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
    cart = request.session.get('cart', {})

    # Преобразуем ключ flower_id в строку, так как Django сохраняет ключи в виде строк
    flower_id_str = str(flower_id)

    if flower_id_str in cart:
        cart[flower_id_str]['quantity'] += 1
    else:
        cart[flower_id_str] = {
            'name': flower.name,
            'color': flower.color,
            'price': float(flower.price),
            'quantity': 1
        }

    # Обновляем сессию
    request.session['cart'] = cart
    request.session.modified = True  # Помечаем сессию как изменённую
    return redirect('view_cart')


@login_required
def view_cart(request):
    """Просмотр содержимого корзины"""
    cart = request.session.get('cart', {})
    print("Содержимое корзины:", request.session.get('cart', {}))
    cart_items = []

    total_price = 0
    for flower_id, item in cart.items():
        item_total = item['price'] * item['quantity']
        total_price += item_total
        cart_items.append({
            'id': flower_id,
            'name': item['name'],
            'color': item['color'],
            'price': item['price'],
            'quantity': item['quantity'],
            'item_total': item_total
        })

    return render(request, 'orders/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def checkout(request):
    """Оформление заказа"""
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('flower_catalog')

    order = Order.objects.create(user=request.user, total_price=0)
    total_price = 0

    for flower_id, item in cart.items():
        flower = Flower.objects.get(id=int(flower_id))  # Преобразуем flower_id обратно в int
        item_total = item['quantity'] * flower.price
        OrderItem.objects.create(order=order, flower=flower, quantity=item['quantity'], price=item_total)
        total_price += item_total

    order.total_price = total_price
    order.save()

    # Очистка корзины
    request.session['cart'] = {}
    return redirect('order_success')


