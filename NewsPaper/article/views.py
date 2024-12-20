from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from news.models import Post, Author
from news.forms import PostForm

class ArticleCreated(CreateView):  # LoginRequiredMixin
    form_class = PostForm
    model = Post
    template_name = 'create_article.html'
    #login_url = 'login'

    def form_valid(self, form):
        form.instance.author_post = Author.objects.get(id=self.request.user.id)
        test = form.save(commit=False)
        test.choice_categories = 'article'
        return super().form_valid(form)

class ArticleUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update_article.html'


class DeleteArticle(DeleteView):
    model = Post
    success_url = reverse_lazy('post')
    template_name = 'delete_article.html'
