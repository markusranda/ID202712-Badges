from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from create_badge.forms import CreateBadgeForm


# Create your views here.

def create_badge(request):
    if request.method == "POST":
        form = CreateBadgeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('')
            except:
                pass
    else:
        form = CreateBadgeForm()
    return render(request, 'create_badge.html', {'form': form})
