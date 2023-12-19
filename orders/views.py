from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from orders.models import *
from users.models import *
from .forms import OrderUpdateForm


def my_cart(request):
    if not request.user.is_authenticated:
        return redirect('sign_in')

    user_cart = Cart.objects.get(user=request.user)
    cart_items = user_cart.get_cart_items()

    for item in cart_items:
        properties = item.product_unit.productunitproperty_set.all().order_by('property__name')
        item.product_properties_string = ", ".join(
            [f"{product_property.property.name}: {product_property.property_value}"
             for product_property in properties]
        )

    context = {
        'title': 'Моя корзина',
        'cart_items': cart_items,
        'total_price': user_cart.total_price
    }

    return render(request=request,
                  template_name='my_cart.html',
                  context=context)


@require_POST
def update_quantity(request):
    new_quantity = int(request.POST.get('new_quantity'))
    cart_item_id = int(request.POST.get('cart_item_id'))

    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.quantity = new_quantity
        cart_item.save()

        cart = cart_item.cart
        cart.calculate_total_price()

        return JsonResponse({
            'success': True,
            'total_price': cart.total_price
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def delete_cart_item(request):
    if request.method == 'POST':
        cart_item_id = int(request.POST.get('cart_item_id'))
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.delete()
        print('Удалено')

        cart = cart_item.cart
        cart.calculate_total_price()

        response_data = {
            'status': 'success',
            'message': 'Элемент корзины успешно удален',
            'total_price': cart.total_price
        }

        return JsonResponse(response_data)


def confirm_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    user_cart = Cart.objects.get(user=request.user)
    cart_items = user_cart.get_cart_items()

    addresses = Address.objects.filter(profile=user_profile)
    if not cart_items:
        return redirect('my_cart')

    for item in cart_items:
        properties = item.product_unit.productunitproperty_set.all().order_by('property__name')
        item.product_properties_string = ", ".join(
            [f"{product_property.property.name}: {product_property.property_value}"
             for product_property in properties]
        )

    context = {
        'title': 'Оформление заказа',
        'addresses': addresses,
        'cart_items': cart_items,
        'total_price': user_cart.total_price
    }

    return render(request=request,
                  template_name='confirm_order.html',
                  context=context)


def create_order(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        selected_address = Address.objects.get(pk=selected_address_id)

        user = request.user
        user_cart = Cart.objects.get(user=user)
        cart_items = user_cart.get_cart_items()

        order = Order.objects.create(
            user=user,
            status=OrderStatus.accepted.value,
            shipping_address=selected_address
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                product_unit=cart_item.product_unit,
                quantity=cart_item.quantity,
                order=order
            )

            cart_item.product_unit.quantity -= cart_item.quantity
            cart_item.product_unit.save()

        user_cart.clear_cart()
        return redirect(
            to='thanks_for_order',
            order_number=order.order_number
        )
    else:
        messages.error(request, 'Что-то пошло не так при создании заказа.')
        return redirect('confirm_order')


def thanks_for_order(request, order_number):
    context = {
        'title': 'Спасибо за заказ!',
        'order_number': order_number
    }

    return render(
        request=request,
        template_name='thanks_for_order.html',
        context=context
    )


def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('sign_in')

    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'title': 'Мои заказы',
        'user': user,
        'profile': user_profile,
        'orders': user_orders
    }

    return render(request=request,
                  template_name='my_orders.html',
                  context=context)


def order_details(request, order_number: str):
    if not request.user.is_authenticated:
        return redirect('sign_in')

    order = Order.objects.get(order_number=order_number)
    order_items = order.get_order_items()

    for item in order_items:
        properties = item.product_unit.productunitproperty_set.all().order_by('property__name')
        item.product_properties_string = ", ".join(
            [f"{product_property.property.name}: {product_property.property_value}"
             for product_property in properties]
        )

    context = {
        'title': f'Заказ {order_number}',
        'order': order,
        'order_items': order_items
    }

    return render(request=request,
                  template_name='order_details.html',
                  context=context)


def all_orders(request):
    if not request.user.is_authenticated:
        return redirect('sign_in')
    else:
        user = get_object_or_404(User, id=request.user.id)
        if not user.is_manager:
            return redirect('my_orders')
        else:
            orders = Order.objects.all().order_by('-created_at')

            context = {
                'title': 'Все заказы',
                'user': user,
                'orders': orders
            }

            return render(request=request,
                          template_name='all_orders.html',
                          context=context)


def manage_order(request, order_number: str):
    user = get_object_or_404(User, id=request.user.id)
    if not user.is_manager:
        return redirect('my_orders')
    else:
        order = get_object_or_404(Order, order_number=order_number)

        if request.method == 'POST':
            form = OrderUpdateForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect('order_details', order_number=order_number)
        else:
            form = OrderUpdateForm(instance=order)

            context = {
                'title': f'Редактирование заказа {order_number}',
                'order': order,
                'form': form
            }

            return render(request=request,
                          template_name='manage_order.html',
                          context=context)
