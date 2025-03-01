from django.urls import path
from .views import (NewsView, DetailNews, NewsCreated,
                    PostSearchView, PostUpdate, DeletePost,
                    AuthorView, subscribe, NewsCategoryView,
                    ArticleView, ActicleCreated, ArticleUpdate,
                    DeleteArticle, ArticleCategoryView, get_top_rating_post,
                   )
from django.views.decorators.cache import cache_page


# urlpatterns = [
#     path('home/', get_top_rating_post, name='top'),
#     path('<int:pk>', cache_page(300)(DetailNews.as_view()), name='single_post'),
#     path('news/', cache_page(300)(NewsView.as_view()), name='news'),
#     path('news/<str:category>/<int:pk>', cache_page(300)(NewsCategoryView.as_view()), name='category_news'),
#     path('news/create/', NewsCreated.as_view(), name='create_news'),
#     path('search/', PostSearchView.as_view(), name='search_news'),
#     path('news/delete/<int:pk>/', DeletePost.as_view(), name='delete_post'),
#     path('news/update/<int:pk>/', PostUpdate.as_view(), name='update_news'),
#     path('article/', cache_page(300)(ArticleView.as_view()), name='article'),
#     path('article/create', ActicleCreated.as_view(), name='create_article'),
#     path('article/delete/<int:pk>', DeleteArticle.as_view(), name='delete_article'),
#     path('article/update<int:pk>', ArticleUpdate.as_view(), name='update_article'),
#     path('article/<str:category>/<int:pk>', cache_page(300)(ArticleCategoryView.as_view()), name='category_article'),
#     path('author/', cache_page(500)(AuthorView.as_view()), name='show_authors'),
#     path('subscribe/', subscribe, name='subscribe'),
# ]


urlpatterns = [
    #path('home/', get_top_rating_post, name='top'),
    path('<int:pk>', DetailNews.as_view(), name='single_post'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/<str:category>/<int:pk>', NewsCategoryView.as_view(), name='category_news'),
    path('news/create/', NewsCreated.as_view(), name='create_news'),
    path('search/', PostSearchView.as_view(), name='search_news'),
    path('news/delete/<int:pk>/', DeletePost.as_view(), name='delete_post'),
    path('news/update/<int:pk>/', PostUpdate.as_view(), name='update_news'),

    path('article/', ArticleView.as_view(), name='article'),
    path('article/create', ActicleCreated.as_view(), name='create_article'),
    path('article/delete/<int:pk>', DeleteArticle.as_view(), name='delete_article'),
    path('article/update<int:pk>', ArticleUpdate.as_view(), name='update_article'),
    path('article/<str:category>/<int:pk>', ArticleCategoryView.as_view(), name='category_article'),
    path('author/', AuthorView.as_view(), name='show_authors'),
    path('subscribe/', subscribe, name='subscribe'),
]