from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import *


from .forms import EventPinForm
from .models import Events


class EventView(LoginRequiredMixin, generic.ListView):
    model = Events
    template_name = 'events/my_events.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['event_historic_list'] = Events.objects.filter(created_by=self.request.user)
        context['event_active_list'] = Events.objects.all().filter(active=1).filter(created_by=self.request.user)
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
        else:
            print("----------------------------------- Triggered -----------------------------------")
        return render(request, self.template_name, context)


