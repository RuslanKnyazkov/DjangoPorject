from django.urls import path
from .views import (AllPostView, DetailNews, NewsCreated,
                    PostSearchView, PostUpdate, DeletePost)
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(AllPostView.as_view()), name = 'post'),
    path('<int:pk>/', DetailNews.as_view(), name='single_news'),
    path('create/', NewsCreated.as_view(), name ='create_news'),
    path('search/', PostSearchView.as_view(), name = 'search_news'),
    path('delete/<int:pk>/', DeletePost.as_view(), name='delete_post'),
    path('update/<int:pk>/', PostUpdate.as_view(), name='update_news'),
]