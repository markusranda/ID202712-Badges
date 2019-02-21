from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView
from .forms import CustomUserCreationForm
from django.db import connection

from badges.models import Badges
from badges.models import UserBadges
from badges.models import Events


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class ProfilePage(generic.ListView):
    model = Badges
    template_name = 'users/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['badges_list'] = Badges.objects.filter(user=self.request.user)
        context['event_active_list'] = Events.objects.all().filter(active=1).filter(created_by=self.request.user)
        return context
