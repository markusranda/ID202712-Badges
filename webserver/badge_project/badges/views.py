from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect

from .models import Users
from .forms import CreateBadgeForm

def index(request):
    all_users_list = User.objects.all()
    context = {'all_users_list': all_users_list}
    return render(request, 'badges/index.html', context)


class DetailView(generic.DetailView):
    template_name = 'badges/detail.html'
    context_object_name = 'user'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return User.objects.filter()


def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'polls/detail.html', {'user': user})


class IndexView(generic.ListView):
    template_name = 'badges/index.html'
    context_object_name = 'all_users_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return User.objects.all()


def detail(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    return render(request, 'badges/detail.html', {'user': user})


def get_badge_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateBadgeForm(request.POST)
        # check if it's valid:
        if form.is_valid():
            return HttpResponseRedirect('/badges/')

    # if a GET (or any other method we'll create a blank form
    else:
        form = CreateBadgeForm()

    return render(request, 'badges/create_badge.html', {'form': form})

