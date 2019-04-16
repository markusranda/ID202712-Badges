# api/resources.py
from tastypie import fields
from tastypie.resources import ModelResource

from users.models import CustomUser
from events.models import JoinedEventActivity


class UserResource(ModelResource):
    class Meta:
        queryset = CustomUser.objects.all()
        resource_name = 'user'
        fields = ['username']
        allowed_methods = ['get']


class ActivityResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = JoinedEventActivity.objects.all()
        resource_name = 'joined_event_activities'
        allowed_methods = ['get']
