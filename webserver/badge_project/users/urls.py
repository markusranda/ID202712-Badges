from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('<username>/profile_page/', views.ProfilePage.as_view(), name='profile_page'),
]
