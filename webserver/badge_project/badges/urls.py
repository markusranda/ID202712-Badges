from django.urls import path

from . import views

app_name = 'badges'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.login, name='login'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]
