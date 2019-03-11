from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import *
from .utils import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q


def post_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        post = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        post = Post.objects.all()

    paginator = Paginator(post, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'next_url': next_url,
        'prev_url': prev_url,
        'is_paginated': is_paginated
    }
    return render(request, 'index.html', context )


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'post_create.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'post_delete_form.html'
    redirect_template = 'post_list_url'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'tag_create.html'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    context = {'tags': tags}
    return render(request, 'tags_list.html', context)


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'tag_delete_form.html'
    redirect_template = 'tags_list_url'
    raise_exception = True



