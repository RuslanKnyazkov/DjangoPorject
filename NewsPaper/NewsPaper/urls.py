
from django.contrib import admin
from django.urls import path, include
from .settings import DEBUG, STATIC_URL, STATIC_ROOT
from .view import home_page, Index
from django.conf.urls.static import static

urlpatterns = [
    path('', home_page, name = 'home'),
    path('admin/', admin.site.urls),
    path('post/', include('news.urls')),
    path('user/', include('signin.urls')),
    path('accounts/', include('allauth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('time', Index.as_view(), name = 'time'),
] + static(STATIC_URL, document_root = STATIC_ROOT)

if DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

