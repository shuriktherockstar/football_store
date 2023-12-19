from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from orders.models import *
from products.utils import get_filtered_and_paginated_products


def all_categories(request):
    categories = Category.objects.all()

    context = {
        'title': 'Все категории',
        'categories': categories
    }

    return render(request=request,
                  template_name='all_categories.html',
                  context=context)


def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategories = Subcategory.objects.filter(category=category)
    products = Product.objects.filter(subcategory__in=subcategories)

    context = get_filtered_and_paginated_products(request, products)

    context.update({
        'title': category.name,
        'category': category,
    })

    return render(request=request,
                  template_name='products_list.html',
                  context=context)


def subcategory_products(request, subcategory_slug):
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
    products = Product.objects.filter(subcategory=subcategory)

    context = get_filtered_and_paginated_products(request, products)

    context.update({
        'title': subcategory.name,
        'subcategory': subcategory,
    })

    return render(request=request,
                  template_name='products_list.html',
                  context=context)


def product_details(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    product_units = ProductUnit.objects.filter(product=product).filter(quantity__gt=0)
    cart = get_object_or_404(Cart, user=request.user)
    cart_objects = CartItem.objects.filter(cart=cart)

    properties_values = {}
    valid_properties = set()

    for product_unit in product_units:
        properties_for_unit = Property.objects.filter(productunitproperty__product_unit=product_unit)
        values_dict = {}

        for prop in properties_for_unit:
            try:
                value = ProductUnitProperty.objects.get(
                    product_unit=product_unit,
                    property=prop
                ).property_value
                values_dict[prop] = value
                valid_properties.add(prop)
            except ProductUnitProperty.DoesNotExist:
                pass

        properties_values[product_unit.id] = values_dict

    valid_properties = Property.objects.filter(id__in=[prop.id for prop in valid_properties])

    in_cart = any(cart_object.product_unit.product == product for cart_object in cart_objects)

    context = {
        'title': product.name,
        'product': product,
        'properties_values': properties_values,
        'valid_properties': valid_properties,
        'product_units': product_units,
        'reviews': Review.objects.filter(product=product),
        'in_cart': in_cart,
    }

    return render(request=request,
                  template_name='product_details.html',
                  context=context)


def add_to_cart(request):
    if request.method == 'POST':
        product_unit_id = request.POST.get('product_unit_id')
        quantity = int(request.POST.get('quantity', 1))

        product_unit = get_object_or_404(ProductUnit, id=product_unit_id)
        cart = Cart.objects.get(user=request.user)

        new_cart_item = CartItem.objects.create(
            product_unit=product_unit,
            quantity=quantity,
            cart=cart
        )

        new_cart_item.quantity = quantity
        new_cart_item.save()
        cart.calculate_total_price()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def search_products(request):
    query = request.GET.get('search-input', '')
    query_capitalized = query.capitalize()
    query_uppered = query.upper()
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(club__name__icontains=query) |
        Q(club__league__name__icontains=query) |
        Q(club__league__country__name__icontains=query) |
        Q(name__icontains=query_capitalized) |
        Q(club__name__icontains=query_capitalized) |
        Q(club__league__name__icontains=query_capitalized) |
        Q(club__league__country__name__icontains=query_capitalized) |
        Q(name__icontains=query_uppered) |
        Q(club__name__icontains=query_uppered) |
        Q(club__league__name__icontains=query_uppered) |
        Q(club__league__country__name__icontains=query_uppered)
    )

    context = get_filtered_and_paginated_products(request, products, default_sort='price_asc')

    context.update({
        'title': f'Товары по запросу: {query}',
        'query': query,
    })

    return render(request=request,
                  template_name='products_list.html',
                  context=context)


def my_reviews(request):
    if not request.user.is_authenticated:
        return redirect('sign_in')

    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    user_reviews = Review.objects.filter(profile=user_profile).order_by('-created_at')

    context = {
        'title': 'Мои отзывы',
        'user': user,
        'profile': user_profile,
        'reviews': user_reviews
    }

    return render(request=request,
                  template_name='my_reviews.html',
                  context=context)
