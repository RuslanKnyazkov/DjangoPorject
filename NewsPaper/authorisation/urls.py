from django.urls import path
from .views import logout_view, User_Logit_View

urlpatterns = [
    path('', logout_view, name='logout'),
    path('login', User_Logit_View.as_view(), name='login')
]