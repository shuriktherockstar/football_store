from django.db.models import Count
from django.shortcuts import render

from products.models import *


def main_page(request):
    latest_products = Product.objects.all().order_by('-id')[:5]

    products_with_reviews = Product.objects.annotate(num_reviews=Count('review'))
    most_reviewed_products = products_with_reviews.order_by('-num_reviews')[:5]

    products_with_orders = Product.objects.annotate(num_orders=Count('productunit__cartitem__cart'))
    most_ordered_products = products_with_orders.order_by('-num_orders')[:5]

    context = {
        'title': 'Главная',
        'latest_products': latest_products,
        'most_ordered_products': most_ordered_products,
        'most_reviewed_products': most_reviewed_products,
    }

    return render(request=request,
                  template_name='main_page.html',
                  context=context)


def not_found(request):
    return render(request=request,
                  template_name='not_found.html',
                  context={'title': '404 - Не найдено'})
