from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PostForm
from .models import Post, Comment, Author
from .filters import PostFilter


# Create your views here.


class AllPostView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-create_date'
    paginate_by = 10


class PostSearchView(ListView):
    model = Post
    template_name = 'search_news.html'
    context_object_name = 'news'
    ordering = '-create_date'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class DetailNews(DetailView):
    model = Post
    template_name = 'single_news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            current_post=context['object']).order_by('-date_comment')
        return context


class NewsCreated(CreateView):  #LoginRequiredMixin - убран для проверки задания
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'
    #login_url = 'login'

    def form_valid(self, form):
        form.instance.author_post = Author.objects.get(id=self.request.user.id)
        form.save(commit=False)
        form.choice_categories = 'news'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'


class DeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('post')
    template_name = 'delete_post.html'


