# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from badges.models import Events
from django.views import generic


class EventView(generic.ListView):
    model = Events
    template_name = 'events/my_events.html'
    event_historic_list = Events.objects.all()
    event_active_list = Events.objects.filter(active=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_name(self):
        return self.object.name()


def events(request):
    event_historic_list = Events.objects.all()
    event_active_list = Events.objects.filter(active=1)
    context = {
        'event_historic_list': event_historic_list,
        'event_active_list': event_active_list,
    }
    return render(request, 'events/my_events.html', context)

