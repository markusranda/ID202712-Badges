from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventView.as_view(), name='events'),
    path('create_event/', views.CreateEvent.as_view(), name='create_event'),
]