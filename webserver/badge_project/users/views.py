from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import CustomUser, Attendees, UserBadges
from django.shortcuts import get_object_or_404

from .forms import CustomUserCreationForm
from badges.models import Badges
from events.models import Events
# from users.models import CustomUser


from .forms import CustomUserCreationForm, ChangeProfilePageForm, LoginForm
from users.models import CustomUser


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class ProfilePage(generic.ListView):
    model = Badges
    template_name = 'users/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parameter_username = self.kwargs['username']
        object_user = CustomUser.objects.filter(username=parameter_username).get()

        '''Obtain all events from the '''
        attendants_qs = Attendees.objects.filter(user_id=object_user.id)
        events_list = []
        for attendants_qs in attendants_qs:
            if attendants_qs.event.active:
                event = attendants_qs.event
                events_list.append(event)

        context['showcase_list'] = object_user.user.filter(is_showcase=1)
        context['event_badge_list'] = object_user.event_badge.all()
        context['event_active_list'] = events_list
        context['about_me'] = object_user.about_me
        context['profile_owner'] = parameter_username

        # User stats
        context['badge_count'] = object_user.event_badge.all().count()
        context['event_count'] = Attendees.objects.filter(user_id=object_user.id).count()
        context['date_joined'] = object_user.date_joined


        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = ChangeProfilePageForm
    template_name = 'users/profile_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        object_user = self.request.user
        context['user_badge_list'] = object_user.user.all()
        return context

    def get_success_url(self):
        username = self.kwargs['username']
        return reverse('profile_page', kwargs={'username': username})

    def post(self, request, *args, **kwargs):
        form = ChangeProfilePageForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            cd = form.cleaned_data
            userbadge_list_all = UserBadges.objects.filter(user_id=self.request.user.id)
            userbadge_list_add = cd.pop('userbadge_list')

            user = self.request.user
            about_me = cd.pop('about_me')
            user.about_me = about_me
            user.save()

            for userbadge in userbadge_list_all:

                if str(userbadge.id) in userbadge_list_add:
                    new_userbadge = UserBadges.objects.get(id=userbadge.id)
                    new_userbadge.is_showcase = 1
                    new_userbadge.save()
                else:
                    userbadge.is_showcase = 0
                    userbadge.save()

        return HttpResponseRedirect(self.get_success_url())

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


class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


