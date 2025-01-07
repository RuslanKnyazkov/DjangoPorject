from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from news.models import Post, Author
from news.forms import PostForm


class ArticleView(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = '-create_date'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        news = Post.objects.all().filter(choice_categories='article')
        context = super().get_context_data(object_list=news)
        return context


class ArticleCreated(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    permission_denied_message = 'Вы не можете создавать статьи.'
    form_class = PostForm
    model = Post
    template_name = 'create_article.html'

    def form_valid(self, form):
        form.instance.author_post = Author.objects.get(id=self.request.user.id)
        test = form.save(commit=False)
        test.choice_categories = 'article'
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    form_class = PostForm
    template_name = 'update_article.html'


class DeleteArticle(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    success_url = reverse_lazy('post')
    template_name = 'delete_article.html'
