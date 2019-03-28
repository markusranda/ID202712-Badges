# Generic class based view
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import CreateBadgeForm
from .models import Badges


class BadgeCreate(LoginRequiredMixin, FormView):
    form_class = CreateBadgeForm
    success_url = reverse_lazy('home')
    template_name = 'badges/create_badge.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return context

    def form_valid(self, form):
        return super().form_valid(form)