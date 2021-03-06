from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import forms
from django.http import HttpResponseRedirect, QueryDict, request
from django.shortcuts import render, render_to_response
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import *
from django.views.generic.detail import SingleObjectMixin, BaseDetailView
from django.views.generic.edit import ModelFormMixin, FormMixin
from django.contrib.auth import get_user
from django.views.generic.edit import ModelFormMixin

from users.models import CustomUser
from users.models import Attendees
from users.models import CustomUser
from users.models import UserBadges

from badges.models import Badges
from .multiforms import MultiFormsView
from .forms import EventPinForm, CreateEventForm, BadgeRequestForm, BadgeApprovalForm, DeleteBadgeRequestForm, \
    BadgeApprovalModeratorForm, RemoveBadgeFromUserForm, EndEventForm
from .models import Events, BadgeRequests, EventBadges, EarnedBadgeActivity, JoinedEventActivity
from .models import random

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

    def get(self, request, *args, **kwargs):
        form = EventPinForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EventPinForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            cd = form.cleaned_data
            event_pin = cd.pop('event_field')
            current_event_id = Events.objects.filter(pin=event_pin).get().id
            current_user = request.user.id
            attendee = Attendees(event_id=current_event_id, user_id=current_user)
            attendee.save()
            JoinedEventActivity.objects.create(event_id=current_event_id, user_id=current_user)
            return HttpResponseRedirect(self.get_success_url(current_event_id))
        return render(request, self.template_name, context)

    def get_success_url(self, pk):
        return reverse('events:event_profile', kwargs={'pk': pk})


class CreateEvent(LoginRequiredMixin, CreateView):
    model = Events
    form_class = CreateEventForm
    success_url = reverse_lazy('events:events')
    template_name = 'events/create_event_form.html'

    # Retrieves the form before it's been successfully posted
    # Adds a new field to the form name "created_by_id"
    # Saves the value with current user's id
    def post(self, request, *args, **kwargs):
        form = CreateEventForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            cd = form.cleaned_data
            name = cd.pop('name')
            description = cd.pop('description')
            badges = cd.pop('badge')
            user_id = request.user.id

            event = Events.objects.create(name=name, description=description, active=1,
                                          created_by_id=user_id, pin=random())

            for badge in badges:
                EventBadges.objects.create(badge_id=badge.id, event_id=event.id)

            Attendees.objects.create(event_id=event.id, user_id=user_id)
            JoinedEventActivity.objects.create(event_id=event.id, user_id=user_id)

            return HttpResponseRedirect(self.get_success_url(event.id))

        return render(request, self.template_name, context)

    def get_success_url(self, pk):
        return reverse('events:event_profile', kwargs={'pk': pk})


class EventProfile(MultiFormsView):
    template_name = 'events/event_profile.html'
    model = Events
    form_classes = {'request_badge': BadgeRequestForm,
                    'approve_badge': BadgeApprovalForm,
                    'delete_badge_request': DeleteBadgeRequestForm,
                    'remove_badge_from_user': RemoveBadgeFromUserForm,
                    'end_event': EndEventForm,
                    'approve_badge_mod': BadgeApprovalModeratorForm,
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
        if self.request.user.id == event_object.created_by_id:
            user_is_moderator = True

        event_badge_list = event_object.event.all()
        user_badge_list = []
        for event_badge in event_badge_list:
            user_badge_qs = event_badge.user_badges.all()
            for user_badge in user_badge_qs:
                    user_badge_list.append(user_badge)

        context['user_is_moderator'] = user_is_moderator
        context['people_joined'] = Attendees.objects.filter(event=event_object.id).count()
        context['attendees'] = Attendees.objects.filter(event=event_object.id)
        context['earned'] = event_object.badge.all().count()
        context['event_name'] = event_object.name
        context['event_desc'] = event_object.description
        context['event_id'] = event_object.id
        context['badge_requests'] = badge_request_qs
        context['requestable_badge'] = event_object.badge.all()
        context['event_pin'] = event_object.pin
        context['user_badge_list'] = user_badge_list
        context['event_active'] = event_object.active


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

    def end_event_form_valid(self, form):
        event_id = form.cleaned_data.get('event_id')
        event = Events.objects.get(id=event_id)
        event.active = 0
        event.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        pk = self.kwargs['pk']
        return reverse('events:event_profile', kwargs={'pk': pk})

    def delete_badge_request_form_valid(self, form):
        badge_id = form.cleaned_data.get('badge_id')
        event_id = self.kwargs['pk']
        user_id = self.request.user.id
        b = BadgeRequests.objects.filter(badge_id=badge_id, event_id=event_id, user_id=user_id).get()
        b.delete()

        return HttpResponseRedirect(self.get_success_url())

    def remove_badge_from_user_form_valid(self, form):
        badge_id = form.cleaned_data.get('badge_id')
        event_id = self.kwargs['pk']
        user_id = form.cleaned_data.get('user_id')
        event_badge = EventBadges.objects.get(badge_id=badge_id, event_id=event_id)
        userbadge = UserBadges.objects.filter(event_badge=event_badge, user_id=user_id).get()
        userbadge.delete()

        return HttpResponseRedirect(self.get_success_url())

    def approve_badge_mod_form_valid(self, form):
        badge_id = form.cleaned_data.get('badge_id')
        event_id = self.kwargs['pk']
        user_id = form.cleaned_data.get('user_id')
        event_badge = EventBadges.objects.get(badge_id=badge_id, event_id=event_id)
        UserBadges.objects.create(event_badge=event_badge, user_id=user_id)
        badgeRequest = BadgeRequests.objects.filter(badge_id=badge_id, event_id=event_id, user_id=user_id).get()
        EarnedBadgeActivity.objects.create(badge_id=badge_id, event_id=event_id, user_id=user_id)
        badgeRequest.delete()

        return HttpResponseRedirect(self.get_success_url())
