from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def get_filtered_and_paginated_products(request, products, default_sort='price_asc', items_per_page=15):
    sort_by = request.GET.get('sort_by', default_sort)

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    page = request.GET.get('page', 1)
    paginator = Paginator(products, items_per_page)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return {
        'products': products,
        'sort_by': sort_by,
    }
