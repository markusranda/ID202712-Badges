from django.urls import path
from . import views

app_name = 'create_badge'

urlpatterns = [
    # function view url
    # path('', views.create_badge, name='create_badge'),
    # class view url
    # path('', views.CreateBadgeView.as_view(), name="create_badge"),
    # generic class view url
    path('', views.BadgeCreate.as_view(), name='create_badge'),
]
