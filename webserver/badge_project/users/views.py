from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView
from .forms import CustomUserCreationForm
from datetime import datetime

from badges.models import Badges
from events.models import Events
from users.models import CustomUser


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class ProfilePage(generic.ListView):
    model = Badges
    template_name = 'users/profile_page.html'

    #Logic follows the user signed in!!!
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['badges_list'] = Badges.objects.filter(user=self.request.user)
        context['event_active_list'] = Events.objects.all().filter(active=1).filter(created_by=self.request.user)

        # User stats
        context['badge_count'] = Badges.objects.filter(user=self.request.user).count()
        context['event_count'] = Events.objects.all().filter(active=0).count()

        return context
