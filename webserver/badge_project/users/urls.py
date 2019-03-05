from django.urls import path
from . import views

current_app = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<username>/profile_page/', views.ProfilePage.as_view(), name='profile_page'),
    path('<username>/profile_page/edit', views.ProfileUpdate.as_view(), name='edit_profile'),
]
