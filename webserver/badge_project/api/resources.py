# api/resources.py
from tastypie import fields
from tastypie.constants import ALL
from tastypie.resources import ModelResource, Resource
from datetime import datetime

from users.models import CustomUser
from events.models import JoinedEventActivity, EarnedBadgeActivity
from badges.models import Badges
from events.models import Events


class UserResource(ModelResource):
    class Meta:
        queryset = CustomUser.objects.all()
        resource_name = 'user'
        fields = ['username']
        allowed_methods = ['get']


class EventResource(ModelResource):
    class Meta:
        queryset = Events.objects.all()
        resource_name = 'event'
        fields = ['id']
        allowed_methods = ['get']


class BadgeResource(ModelResource):
    class Meta:
        queryset = Badges.objects.all()
        resource_name = 'badge'
        allowed_methods = ['get']


class JoinedEventActivityResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    event_id = fields.ForeignKey(EventResource, 'event')

    class Meta:
        queryset = JoinedEventActivity.objects.order_by('datetime_earned')
        resource_name = 'joined_event_activities'
        allowed_methods = ['get']
        filtering = {
            'id': ALL,
            'event_id': ALL,
        }

    def dehydrate_datetime_earned(self, bundle):
        oldValue = bundle.data['datetime_earned']
        newValue = oldValue.strftime("%H:%M:%S")
        return newValue


class EarnedBadgeActivityResource(ModelResource):
    badge = fields.ForeignKey(BadgeResource, 'badge')

    class Meta:
        queryset = EarnedBadgeActivity.objects.order_by('datetime_earned')
        resource_name = 'earned_badge_activities'
        allowed_methods = ['get']

    def dehydrate_datetime_earned(self, bundle):
        oldValue = bundle.data['datetime_earned']
        newValue = oldValue.strftime("%H:%M:%S")
        return newValue
