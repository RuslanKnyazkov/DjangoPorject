from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from .forms import LoginForm, RegisterForm
from django.views.generic import FormView
from django.contrib.auth import authenticate

def logout_view(request):
    logout(request)
    return redirect('login')

class User_Logit_View(FormView):
    form_class = LoginForm
    template_name = 'login_user.html'
    success_url = '/news/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username = username, password = password)
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('')