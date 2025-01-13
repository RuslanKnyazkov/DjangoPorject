
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import PostForm
from .models import Post, Comment, Author, Category, CategorySubscribers
from .filters import PostFilter
from .mixin import AuthorMixin, CategoryMixin


class NewsView(CategoryMixin, ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-create_date'
    paginate_by = 10
    queryset = Post.objects.filter(choice_categories='news')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['cat'] = self.get_category()
        return context


class NewsCategoryView(CategoryMixin, DetailView):
    model = Post
    template_name = 'news_category.html'
    paginate_by = 5

    def get_object(self, queryset=None):
        return Category.objects.get(id=self.kwargs['pk'])

    def get_queryset(self):
        queryset = Post.objects.filter(test=self.object)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['queryset'] = self.get_queryset()
        context['is_subscribe'] = self.object.subscribers.filter(id=self.request.user.id).exists()
        context['cat'] = self.get_category()
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


class NewsCreated(PermissionRequiredMixin, AuthorMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'create_post.html'

    def form_valid(self, form):
        form.instance.author_post = Author.objects.get(name_id=self.request.user.id)
        form.save(commit=False)
        form.choice_categories = 'news'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['create'] = self.check_created(self.request)
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'


class DeletePost(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
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
        return context


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse





@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        category_id = int(request.POST.get('cat_id'))
        if not request.user.categorysubscribers_set.filter(category_id=category_id).exists():
            subscribe = Category.objects.get(id=category_id)
            subscribe.subscribers.add(request.user)
        else:
            cat_subscribe = request.user.categorysubscribers_set.get(category_id=category_id)
            cat_subscribe.delete()
        return JsonResponse(data={'user': request.user.username})

    if request.method == 'GET':
        sub_or_not = request.user.categorysubscribers_set.all().values()
        return JsonResponse(data={'all_subscribe_category': list(sub_or_not)
                                  })
