from django.urls import path
from .views import AllPostView, DetailNews


urlpatterns = [
    path('', AllPostView.as_view(), name = 'news'),
    path('<int:pk>', DetailNews.as_view(), name='single_news')
]