from django.shortcuts import render
from django.views import generic

from .models import Users


def index(request):
    all_users_list = Users.objects.all()
    context = {'all_users_list': all_users_list}
    return render(request, 'badges/index.html', context)


class DetailView(generic.DetailView):
    model = Users
    template_name = 'badges/detail.html'

    '''
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Users.objects.all()
    '''


class IndexView(generic.ListView):
    template_name = 'badges/index.html'
    context_object_name = 'all_users_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Users.objects.all
