from django.conf.urls import url
from django.urls import path

from . import views
from .views import LoginView

current_app = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<username>/profile_page/', views.ProfilePage.as_view(), name='profile_page'),
    path('<username>/profile_page/edit', views.ProfileUpdate.as_view(), name='edit_profile'),
    path('<int:pk>/profile_page/delete/', views.DeleteUser.as_view(), name='delete_profile'),
    url(r'^login/$', LoginView.as_view(), name='login'),
]
