from django.urls import path
from .views import ArticleUpdate, ArticleCreated, DeleteArticle, ArticleView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(300)(ArticleView.as_view()), name = 'article'),
    path('create/', ArticleCreated.as_view(), name = 'create_article'),
    path('update/<int:pk>/', ArticleUpdate.as_view(), name='update_article'),
    path('delete/<int:pk>/', DeleteArticle.as_view(), name='delete_article'),
]