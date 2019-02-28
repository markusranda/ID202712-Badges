from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy

from create_badge.forms import CreateBadgeForm


# Generic class based view
class BadgeCreate(LoginRequiredMixin, CreateView):
    model = Badges
    form_class = CreateBadgeForm
    success_url = reverse_lazy('home')
    template_name = 'create_badge.html'

