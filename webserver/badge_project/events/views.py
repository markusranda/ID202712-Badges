from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user

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
    success_url = reverse_lazy('events')
    template_name = 'events/create_event_form.html'

    def get_form(self, **kwargs):
        form = super(CreateEvent, self).get_form(**kwargs)
        form.current_user = self.request.user.id
        return form

    def hop(self, form=form_class):
        new_event = form.save()
        event_profile = CreateEventForm.save(commit=False)
        if event_profile.current_user is None:
            event_profile.current_user = new_event.get_form()
        event_profile.save()