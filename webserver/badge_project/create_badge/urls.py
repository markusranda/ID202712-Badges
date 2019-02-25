from django.urls import path
from . import views

app_name = 'create_badge'

urlpatterns = [
    path('', views.create_badge, name='create_badge'),
]
