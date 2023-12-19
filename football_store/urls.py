from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from core.views import *
from news.views import *
from orders.views import *
from products.views import *
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main_page'),

    path('news/', news_list, name='news_list'),
    path('news/<slug:article_slug>/', article, name='article'),
    path('add_article/', add_article, name='add_article'),

    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('create_profile/', create_profile, name='create_profile'),
    path('logout/', logout, name='logout'),
    path('my_profile/', my_profile, name='my_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('add_address/', add_address, name='add_address'),
    path('delete_address/', delete_address, name='delete_address'),

    path('my_cart/', my_cart, name='my_cart'),
    path('update_quantity/', update_quantity, name='update_quantity'),
    path('delete_cart_item/', delete_cart_item, name='delete_cart_item'),

    path('confirm_order/', confirm_order, name='confirm_order'),
    path('create_order/', create_order, name='create_order'),
    path('thanks_for_order/<str:order_number>', thanks_for_order, name='thanks_for_order'),
    path('my_orders/', my_orders, name='my_orders'),
    path('order/<str:order_number>/', order_details, name='order_details'),
    path('my_reviews', my_reviews, name='my_reviews'),

    path('all_categories', all_categories, name='all_categories'),
    path('category/<slug:category_slug>', category_products, name='category_products'),
    path('subcategories/<slug:subcategory_slug>/', subcategory_products, name='subcategory_products'),
    path('search_products/', search_products, name='search_products'),
    path('products/<slug:product_slug>/', product_details, name='product_details'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),

    path('all_orders/', all_orders, name='all_orders'),
    path('manage_order/<str:order_number>', manage_order, name='manage_order'),

    re_path(r'^.*/$', not_found, name='not_found')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
