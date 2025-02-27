from django.urls import path
from .views import upgrade_me, BaseRegisterView, SignIn
from django.contrib.auth.views import LoginView, LogoutView
from .views import logout_page, ProfileView, UpdateProfile, FollowerCategoryView

urlpatterns = [
    path('login/', SignIn.as_view(), name='login'),
    path('logout/', logout_page, name='logout'),
    path('logout/success', LogoutView.as_view(), name='success_logout'),
    path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
    path('profile/<int:user_id>', ProfileView.as_view(), name = 'profile'),
    path('upgrade', upgrade_me, name='upgrade'),
    path('profile/update/<int:user_id>', UpdateProfile.as_view(), name='update_profile'),
    path('profile/follower/<int:pk>', FollowerCategoryView.as_view(), name='follower')

]
