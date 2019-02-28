from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from badges.models import Badges
from events.models import Events
from users.models import CustomUser

from .forms import CustomUserCreationForm, ChangeProfilePageForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class ProfilePage(generic.ListView, FormMixin):
    form_class = ChangeProfilePageForm
    model = Badges
    template_name = 'users/profile_page.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['badges_list'] = Badges.objects.filter(user=self.request.user)
        context['showcase_list'] = Badges.objects.filter(is_showcase_of_id=self.request.user)
        context['event_active_list'] = Events.objects.all().filter(active=1).filter(created_by=self.request.user)
        return context


class ProfileUpdate(generic.UpdateView):
    form_class = ChangeProfilePageForm
    template_name = 'users/profile_update_form.html'
    success_url = reverse_lazy('home')

    def get_object(self, **kwargs):
        return get_object_or_404(CustomUser, pk=self.request.user.id)
