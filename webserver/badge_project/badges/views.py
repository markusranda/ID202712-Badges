from django.shortcuts import render

from .models import Users


def index(request):
    all_users_list = Users.objects.all()
    context = {'all_users_list': all_users_list}
    return render(request, 'badges/index.html', context)
