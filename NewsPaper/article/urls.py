from django.urls import path
from .views import ArticleUpdate, ArticleCreated, DeleteArticle


urlpatterns = [
    path('create/', ArticleCreated.as_view(), name = 'create_article'),
    path('update/<int:pk>/', ArticleUpdate.as_view(), name='update_article'),
    path('delete/<int:pk>/', DeleteArticle.as_view(), name='delete_article'),
]