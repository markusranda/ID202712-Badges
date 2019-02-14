from django.urls import path

from . import views

app_name = 'badges'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('create_badge/', views.get_badge_name, name='create_badge'),
]
