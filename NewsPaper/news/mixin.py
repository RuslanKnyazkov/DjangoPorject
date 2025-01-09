from .models import Author, Category
from datetime import datetime, timedelta


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