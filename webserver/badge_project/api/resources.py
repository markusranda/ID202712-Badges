# api/resources.py
from tastypie import fields
from tastypie.resources import ModelResource

from users.models import CustomUser
from events.models import JoinedEventActivity, EarnedBadgeActivity
from badges.models import Badges


class UserResource(ModelResource):
    class Meta:
        queryset = CustomUser.objects.all()
        resource_name = 'user'
        fields = ['username']
        allowed_methods = ['get']


class BadgeResource(ModelResource):
    class Meta:
        queryset = Badges.objects.all()
        resource_name = 'badge'
        allowed_methods = ['get']


class JoinedEventActivityResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = JoinedEventActivity.objects.all()
        resource_name = 'joined_event_activities'
        allowed_methods = ['get']


class EarnedBadgeActivityResource(ModelResource):
    badge = fields.ForeignKey(BadgeResource, 'badge')

    class Meta:
        queryset = EarnedBadgeActivity.objects.all()
        resource_name = 'earned_badge_activities'
        allowed_methods = ['get']
