from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from news.forms import *
from news.models import *


def news_list(request):
    context = {
        'title': 'Новости',
        'articles': Article.objects.all().order_by('-date_published')
    }

    return render(request=request,
                  template_name='articles_list.html',
                  context=context)


def article(request, article_slug):
    article_details = get_object_or_404(Article, slug=article_slug)
    context = {
        'title': article_details.title,
        'article': article_details
    }

    return render(request=request,
                  template_name='article.html',
                  context=context)


def add_article(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('main_page')

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.author = request.user
            new_article.save()
            return redirect('news_list')
        else:
            messages.error(request, 'Ошибка в форме. Пожалуйста, проверьте введенные данные.')
    else:
        form = ArticleForm()

    context = {
        'title': 'Добавить новость',
        'form': form
    }

    return render(request=request,
                  template_name='add_article.html',
                  context=context)
