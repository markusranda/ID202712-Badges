from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from .forms import CustomUserCreationForm

from badges.models import Badges
from events.models import Events
# from users.models import CustomUser

from .forms import CustomUserCreationForm, ChangeProfilePageForm
from users.models import CustomUser

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class ProfilePage(generic.ListView):
    model = Badges
    template_name = 'users/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        current_user = self.request.user
        context['badges_list'] = current_user.badge.all()
        '''context['showcase_list'] = CustomUser.objects.filter(is_showcase_badge=current_user)'''
        context['showcase_list'] = current_user.showcase_badge.all()
        context['event_active_list'] = Events.objects.all().filter(active=1).filter(created_by=self.request.user)
        context['about_me'] = current_user.about_me

        # User stats
        context['badge_count'] = Badges.objects.filter(user=self.request.user).count()
        context['event_count'] = Events.objects.all().filter(active=0).count()

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
        import pdb; pdb.set_trace()
        user_id = self.request.user.id
        username = CustomUser.objects.filter(id=user_id)
        return reverse_lazy('profile_page', kwargs={'username': username})

    def get_object(self, **kwargs):
        return get_object_or_404(CustomUser, pk=self.request.user.id)
