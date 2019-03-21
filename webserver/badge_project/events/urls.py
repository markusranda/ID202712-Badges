from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventView.as_view(), name='events'),
    path('event_pin/', views.EventPin.as_view(), name='event_pin'),
    path('<int:pk>/event_profile/', views.EventProfile.as_view(), name='event_profile'),
]
