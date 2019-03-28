from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import forms
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render, render_to_response
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import *
from django.views.generic.detail import SingleObjectMixin, BaseDetailView
from django.views.generic.edit import ModelFormMixin, FormMixin

from users.models import Attendees

from badges.models import Badges

from .multiforms import MultiFormsView
from .forms import EventPinForm, CreateEventForm, BadgeRequestForm, BadgeApprovalForm
from .models import Events, BadgeRequests

from django.db import models


class EventView(LoginRequiredMixin, generic.ListView):
    model = Events
    template_name = 'events/my_events.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        current_user = self.request.user
        context['events_historic_list'] = current_user.attendingEvents.all()
        context['events_created_list'] = Events.objects.filter(created_by=current_user)

        return context


class EventPin(LoginRequiredMixin, View):
    template_name = "events/event_pin.html"

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
            current_event_id = Events.objects.filter(pin=event_pin).get().id
            current_user = request.user.id
            attendee = Attendees(event_id=current_event_id, user_id=current_user)
            attendee.save()

            return HttpResponseRedirect(self.get_success_url(current_event_id))
        return render(request, self.template_name, context)

    def get_success_url(self, pk):
        return reverse('events:event_profile_user', kwargs={'pk': pk})


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


class EventProfile(MultiFormsView):
    template_name = 'events/event_profile.html'
    model = Events
    form_classes = {'request_badge': BadgeRequestForm,
                    'approve_badge': BadgeApprovalForm,
                    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parameter_event_id = self.kwargs['pk']
        event_object = Events.objects.all().get(id=parameter_event_id)

        '''Obtain all badges from the relevant badge_requests'''
        badge_request_qs = BadgeRequests.objects.filter(event_id=event_object.id)
        badge_requests = []
        for badge_request in badge_request_qs:
            badge = badge_request.badge
            badge_requests.append(badge)

        user_is_moderator = False
        if self.request.user.id == event_object.created_by_id :
            user_is_moderator = True

        context['user_is_moderator'] = user_is_moderator
        context['people_joined'] = Attendees.objects.filter(event=event_object.id).count()
        context['event_name'] = event_object.name
        context['event_desc'] = event_object.description
        context['badge_requests'] = badge_request_qs
        context['requestable_badge'] = event_object.requestable_badges.all()
        context['event_pin'] = event_object.pin

        return context

    def request_badge_form_valid(self, form):
        badge_id = form.cleaned_data.get('badge_id')
        event_id = self.kwargs['pk']
        b = Badges.objects.all().get(id=badge_id)
        e = Events.objects.all().get(id=event_id)
        u = self.request.user
        br = BadgeRequests.objects.create(user=u, event=e, badge=b)
        return HttpResponseRedirect(self.get_success_url())

    def approve_badge_form_valid(self, form):
        badge_id_as_str = form.cleaned_data.get('badge_id_as_str')
        form_name = form.cleaned_data.get('action')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        pk = self.kwargs['pk']
        return reverse('events:event_profile', kwargs={'pk': pk})



