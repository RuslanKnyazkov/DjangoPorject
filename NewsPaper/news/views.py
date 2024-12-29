from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from .forms import PostForm
from .models import Post, Comment, Author
from .filters import PostFilter


# Create your views here.


class NewsView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-create_date'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        news = Post.objects.all().filter(choice_categories='news')
        context = super().get_context_data(object_list=news)
        return context


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


class NewsCreated(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

    def form_valid(self, form):
        form.instance.author_post = Author.objects.get(id=self.request.user.id)
        form.save(commit=False)
        form.choice_categories = 'news'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post')
    template_name = 'delete_post.html'


class AuthorView(ListView):
    model = Author
    template_name = 'all_authors.html'
    context_object_name = 'authors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        print(context)
        return context