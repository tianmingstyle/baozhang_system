# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from repository import models
from utilities.my_paginator import CustomPaginator
from django.core.paginator import  EmptyPage, PageNotAnInteger

def index(request, *args, **kwargs):
    if not kwargs:
        kwargs["article_type_id"] = None
        article_list = models.Article.objects.all()
    else:
        kwargs["article_type_id"] = int(kwargs["article_type_id"])
        article_list = models.Article.objects.filter(**kwargs)

    article_type_list = models.Article.type_choices

    current_page = request.GET.get('p', None)
    if not current_page:
        current_page = 1
    paginator = CustomPaginator(current_page, 11, article_list, 3)
    try:
        posts = paginator.page(current_page)

    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'index.html',
                  {'posts': posts,
                   'article_type_list': article_type_list,
                   'kwargs':kwargs
                   }
                  )


def get_content(request):
    art_id = request.GET.get("article_id")
    content_obj = models.Article.objects.filter(id=art_id).first()

    return render(request, 'content.html', locals())