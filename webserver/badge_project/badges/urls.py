from django.urls import path

from . import views

app_name = 'badges'
urlpatterns = [
    path('create_new_badge/', views.BadgeCreate.as_view(), name='create_new_badge'),
]
