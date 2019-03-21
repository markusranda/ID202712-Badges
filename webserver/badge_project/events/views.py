from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import *
from users.models import CustomUser

from users.models import Attendees
from .forms import EventPinForm
from .models import Events


class EventView(LoginRequiredMixin, generic.ListView):
    model = Events
    template_name = 'events/my_events.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        current_user = self.request.user
        context['event_historic_list'] = current_user.event.values_list()
        context['event_active_list'] = Events.objects.filter(created_by=current_user)

        return context


class EventPin(LoginRequiredMixin, View):
    template_name = "events/event_pin.html"

    def get_form(self, request, **kwargs):
         form = super(EventPin, self).get_form(request, **kwargs)
         form.current_user = request.user
         return form

    def get(self, request,*args, **kwargs):
        form = EventPinForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request,*args, **kwargs):
        form = EventPinForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            cd = form.cleaned_data
            event_pin = cd.pop('event_field')
            current_event = Events.objects.filter(pin = event_pin).get()
            current_user = request.user
            current_user.event.add(current_event)
            return render(request, "events/event_profile.html", context)
        return render(request, self.template_name, context)


class EventProfile(generic.DetailView):
    template_name = 'events/event_profile.html'
    model = Events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parameter_event_id = self.kwargs['pk']
        context['people_joined'] = Attendees.objects.filter(event=1).count()
        # object_user = CustomUser.objects.filter(username=parameter_username).get()
        # context['showcase_list'] = object_user.showcase_badge.all()
        # context['badges_list'] = object_user.badge.all()
        # context['event_active_list'] = object_user.event.filter(active=1)
        # context['about_me'] = object_user.about_me
        #
        # # User stats
        # context['badge_count'] = object_user.badge.all().count()
        # context['event_count'] = object_user.event.all().count()
        # context['date_joined'] = object_user.date_joined
        return context



