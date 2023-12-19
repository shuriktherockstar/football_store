from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from orders.models import *
from products.models import Review
from users.forms import *


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('my_profile')
    else:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)

                Cart.objects.create(user=user)
                return redirect('create_profile')
        else:
            form = UserRegistrationForm()

        context = {
            'title': 'Регистрация',
            'form': form
        }

        return render(request=request,
                      template_name='sign_up.html',
                      context=context)


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('my_profile')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                email = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=email, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('main_page')
        else:
            form = UserAuthenticationForm()

        context = {
            'title': 'Авторизация',
            'form': form
        }

        return render(request=request,
                      template_name='sign_in.html',
                      context=context)


def create_profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = user
            user_profile.save()

            return redirect('main_page')
    else:
        form = ProfileForm()

    context = {
        'title': 'Создать профиль',
        'form': form
    }

    return render(request=request,
                  template_name='create_profile.html',
                  context=context)


def my_profile(request):
    if not request.user.is_authenticated:
        return redirect('sign_in')

    user = request.user
    user_profile = get_object_or_404(Profile, user=user)

    try:
        latest_order = Order.objects.filter(user=user).latest('created_at')
        latest_order_info = {
            'order': latest_order,
            'order_items': OrderItem.objects.filter(order=latest_order)
        }
    except ObjectDoesNotExist:
        latest_order_info = None

    try:
        latest_review = Review.objects.filter(profile=user_profile).latest('created_at')
    except ObjectDoesNotExist:
        latest_review = None

    context = {
        'title': 'Мой профиль',
        'user': user,
        'profile': user_profile,
        'latest_order': latest_order_info,
        'addresses': Address.objects.filter(profile=user_profile),
        'latest_review': latest_review,
    }

    return render(request=request,
                  template_name='my_profile.html',
                  context=context)


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('sign_in')
    else:
        profile = Profile.objects.get(user=request.user)

        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('my_profile')
        else:
            form = ProfileUpdateForm(instance=profile)

        context = {
            'title': 'Редактировать профиль',
            'form': form
        }

        return render(request=request,
                      template_name='edit_profile.html',
                      context=context)


@require_POST
def delete_address(request):
    address_id = request.POST.get('address_id')
    address = get_object_or_404(Address, id=address_id)
    address.delete()
    return JsonResponse({'message': 'Address deleted successfully'})


def add_address(request):
    if request.method == 'POST':
        address_text = request.POST.get('address')
        Address.objects.create(profile=request.user.profile, address=address_text)
        return redirect('my_profile')

    return render(request=request,
                  template_name='my_profile.html')


def logout(request):
    if request.user.is_authenticated:
        request.session.flush()

    return redirect('main_page')
