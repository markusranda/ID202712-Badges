# Generic class based view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreateBadgeForm
from .models import Badges


class BadgeCreate(LoginRequiredMixin, CreateView):
    model = Badges
    form_class = CreateBadgeForm
    success_url = reverse_lazy('home')
    template_name = 'badges/create_badge.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['badge_list'] = Badges.objects.all()

        return context