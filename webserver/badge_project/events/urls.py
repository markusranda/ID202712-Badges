from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventView.as_view(), name='events'),
    path('<username>/create_event/', views.)
]
