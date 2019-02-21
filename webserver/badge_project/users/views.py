from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView
from .forms import CustomUserCreationForm

from badges.models import Badges
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
        #context['event_historic_list'] = Events.objects.filter(created_by=self.request.user)
        context['event_active_list'] = Events.objects.all().filter(active=1).filter(created_by=self.request.user)
        return context

    def get_queryset(self):
        return
