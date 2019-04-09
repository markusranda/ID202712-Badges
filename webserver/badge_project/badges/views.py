# Generic class based view
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
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

    def get(self, request,*args, **kwargs):
        form = CreateBadgeForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request,*args, **kwargs):
        form = CreateBadgeForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            cd = form.cleaned_data
            name = cd.pop('name')
            description = cd.pop('description')
            image_id = cd.pop('image_id')
            Badges.objects.create(name=name, description=description, image_id=image_id)
            return HttpResponseRedirect(self.get_success_url())
        return render(request, self.template_name, context)

    def get_success_url(self):
        return reverse('home')