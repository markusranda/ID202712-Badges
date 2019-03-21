from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict
from django.views import generic
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user
from django.views.generic.edit import ModelFormMixin

from .models import Events
from .forms import CreateEventForm


class EventView(LoginRequiredMixin, generic.ListView):
    model = Events
    template_name = 'events/my_events.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['event_historic_list'] = Events.objects.filter(created_by=self.request.user)
        context['event_active_list'] = Events.objects.all().filter(active=1).filter(created_by=self.request.user)
        return context


class CreateEvent(LoginRequiredMixin, CreateView):
    model = Events
    form_class = CreateEventForm
    success_url = reverse_lazy('events:events')
    template_name = 'events/create_event_form.html'

    # Retrieves the form before it's been successfully posted
    # Adds a new field to the form name "created_by_id"
    # Saves the value with current user's id
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by_id = self.request.user.id
        self.object.save()

        return super(ModelFormMixin, self).form_valid(form)
