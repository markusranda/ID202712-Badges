from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import CustomUser, Attendees
from django.shortcuts import get_object_or_404

from .forms import CustomUserCreationForm
from create_badge.forms import CreateBadgeForm
from badges.models import Badges
from events.models import Events
# from users.models import CustomUser


from .forms import CustomUserCreationForm, ChangeProfilePageForm
from users.models import CustomUser

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class CreateBadge(LoginRequiredMixin, CreateView):
    model = Badges
    form_class = CreateBadgeForm
    success_url = reverse_lazy('home')
    template_name = 'badges/create_badge.html'


class ProfilePage(generic.ListView):
    model = Badges
    template_name = 'users/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        parameter_username = self.kwargs['username']
        object_user = CustomUser.objects.filter(username=parameter_username).get()

        '''Obtain all events from the '''
        attendants_qs = Attendees.objects.filter(user_id=object_user.id)
        events_list = []
        for attendants_qs in attendants_qs:
            if attendants_qs.event.active:
                event = attendants_qs.event
                events_list.append(event)

        context['showcase_list'] = object_user.showcase_badge.all()
        context['badges_list'] = object_user.badge.all()
        context['event_active_list'] = events_list
        context['about_me'] = object_user.about_me

        # User stats
        context['badge_count'] = object_user.badge.all().count()
        context['event_count'] = Attendees.objects.filter(user_id=object_user.id).count()
        context['date_joined'] = object_user.date_joined

        return context


class ProfileUpdate(generic.UpdateView, SingleObjectMixin):
    form_class = ChangeProfilePageForm
    template_name = 'users/profile_update_form.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['all_badges'] = Badges.objects.all()

        return context

    def get_success_url(self):
        username = self.kwargs['username']
        return reverse('profile_page', kwargs={'username': username})

    def get_object(self, **kwargs):
        return get_object_or_404(CustomUser, pk=self.request.user.id)


class DeleteUser(DeleteView):
    model = CustomUser
    template_name = 'users/profile_delete_form.html'

    def get_success_url(self):
        user_id = self.request.user.id
        user = CustomUser.objects.filter(id=user_id)
        user.delete()
        return reverse_lazy('login')
    #
    # def get_object(self, **kwargs):
    #     return get_object_or_404(CustomUser, pk=self.request.user.id)


class CreateNewBadge:
    form_class = ChangeProfilePageForm
    template_name = 'users/profile_update_form.html'


