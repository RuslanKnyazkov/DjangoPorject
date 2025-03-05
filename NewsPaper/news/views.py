from django.core.cache import cache
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, DetailView,
                                  CreateView,UpdateView,
                                  DeleteView)
from .filters import PostFilter
from .forms import PostForm
from .mixin import (AuthorMixin, PostMixin,
                    SingleCategoryPostView,
                    PostApiMixin)
from .models import Post, Comment, Author, Category



class NewsApiView(PostApiMixin):
    queryset = Post.objects.filter(choice_categories = 'новость')


class ArticleApiView(PostApiMixin):
    queryset = Post.objects.filter(choice_categories = 'статья')



class NewsView(PostMixin):
    template_name = 'news.html'
    queryset = Post.objects.filter(choice_categories='новость')


class ArticleView(PostMixin):
    template_name = 'article.html'
    queryset = Post.objects.filter(choice_categories='статья')


class NewsCategoryView(SingleCategoryPostView):
    template_name = 'news_category.html'


class ArticleCategoryView(SingleCategoryPostView):
    template_name = 'article_category.html'


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

    def get_object(self, queryset=None):
        obj = cache.get(f'news-{self.kwargs['pk']}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)

        return obj

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


class ActicleCreated(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    permission_denied_message = 'Вы не можете создавать статьи.'
    form_class = PostForm
    model = Post
    template_name = 'create_article.html'

    def form_valid(self, form):
        form.instance.author_post = Author.objects.get(name_id=self.request.user.id)
        test = form.save(commit=False)
        test.choice_categories = 'article'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'


class DeletePost(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    success_url = reverse_lazy('news')
    template_name = 'delete_post.html'


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    form_class = PostForm
    template_name = 'update_article.html'


class DeleteArticle(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    success_url = reverse_lazy('news')
    template_name = 'delete_article.html'


class AuthorView(ListView):
    model = Author
    template_name = 'all_authors.html'
    context_object_name = 'authors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

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

        return JsonResponse(data={'user': request.user.username,
                                  'status': request.user.categorysubscribers_set.filter(category_id=category_id
                                                                                        ).exists(),
                                  })

    if request.method == 'GET':
        sub_or_not = request.user.categorysubscribers_set.all().values()
        return JsonResponse(data={'all_subscribe_category': list(sub_or_not),
                                  'user_id': request.user.id})

