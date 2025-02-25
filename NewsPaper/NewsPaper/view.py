from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.conf.urls.i18n import set_language

@cache_page(60)
def home_page(request):
    """View main page"""
    return render(request, template_name='base.html', context={})


def change_language(request):
    if request.method == "POST":
        print(request.POST)