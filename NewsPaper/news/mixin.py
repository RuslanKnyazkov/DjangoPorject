from .models import Author, Category, Post, Comment
from datetime import datetime, timedelta
from django.views.generic import ListView

class AuthorMixin:
    """ Simple mixin for other class ."""

    def check_created(self, request):
        """ Check all the created records of the current user for the day."""

        author = Author.objects.get(name_id=request.user.id)
        today_post = author.post_set.filter(create_date__gt=datetime.today() - timedelta(hours=24)).count()
        return True if today_post < 3 else False


class CategoryMixin:
    """ Simple class for show categories. """

    def get_category(self):
        """ This function get all avaliable categories in context other class. """
        return Category.objects.all()


class PostMixin(CategoryMixin, ListView):
    model = Post
    context_object_name = 'news'
    ordering = '-create_date'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['cat'] = self.get_category()
        return context


class SingleCategoryPostView(CategoryMixin, ListView):
    model = Post

    def get(self, request, *args, **kwargs):
        self.category = Category.objects.get(pk=kwargs['pk'])
        return super().get(request, args, kwargs)

    def get_queryset(self):
        return Post.objects.filter(test=self.kwargs['pk'], choice_categories=self.kwargs['category'])

    def get_context_data(self, **kwargs):
        return super().get_context_data(cat=self.get_category(),
                                        queryset=self.get_queryset(),
                                        cat_id=self.category)
