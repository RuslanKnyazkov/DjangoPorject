from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post
# Create your views here.


class PostView(TemplateView):
    template_name = 'index.html'
    extra_context = {'posts': Post.objects.all()}

    def get_context_data(self, **kwargs):
        return self.extra_context