from django.contrib.auth.mixins import LoginRequiredMixin

from badges.models import Events
from django.views import generic
from django.views.generic import ListView


class EventView(LoginRequiredMixin, generic.ListView):
    model = Events
    template_name = 'events/my_events.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['event_historic_list'] = Events.objects.all()
        context['event_active_list'] = Events.objects.all().filter(active=1)
        return context


