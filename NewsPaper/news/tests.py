from django.test import TestCase
from .models import Author


# Create your tests here.
class AuthorTestCase(TestCase):

    def check_value_rating_author_post(self):
        authors = Author.objects.all()
        for author in authors:
            self.assertEquals(author.rating_user, int)
            assert author.rating_user >= 0