from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Comment


# Create your views here.


class AllPostView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-create_date'


class DetailNews(DetailView):
    model = Post
    template_name = 'single_news.html'
    # pk_url_kwarg = 'single_news'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            current_post=context['object']).order_by('-date_comment')
        return context
