from django.shortcuts import render, get_object_or_404
from django.views import generic

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


