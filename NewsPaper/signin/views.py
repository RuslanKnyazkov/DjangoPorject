from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .forms import BaseRegisterForm, BaseUserForm
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .models import Profile


class BaseRegisterView(CreateView):
    form_class = BaseRegisterForm

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(self.request, new_user)
            Profile.objects.create(user=new_user, firstname=form.cleaned_data['first_name'],
                                   lastname=form.cleaned_data['last_name'])

        return redirect('post')


class ProfileView(DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'user_id'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user_id=self.request.user.pk)


class UpdateProfile(UpdateView):
    form_class = BaseUserForm
    template_name = 'update_user_profile.html'
    pk_url_kwarg = 'user_id'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Profile, user_id=self.request.user.pk)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = self.form_class(instance=self.object)
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('post')


def logout_page(request):
    return render(request, template_name='logout.html')