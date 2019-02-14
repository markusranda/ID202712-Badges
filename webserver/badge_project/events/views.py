# Create your views here.
from django.shortcuts import render


def events(request):
    return render(request, 'events/my_events.html')



