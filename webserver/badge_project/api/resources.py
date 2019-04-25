# api/resources.py
from tastypie import fields
from tastypie.constants import ALL
from tastypie.resources import ModelResource, Resource
from datetime import datetime

from users.models import CustomUser
from events.models import JoinedEventActivity, EarnedBadgeActivity
from badges.models import Badges
from events.models import Events
from badges.models import Images


class UserResource(ModelResource):
    class Meta:
        queryset = CustomUser.objects.all()
        resource_name = 'user'
        fields = ['username', 'personal_color']
        allowed_methods = ['get']


class EventResource(ModelResource):
    class Meta:
        queryset = Events.objects.all()
        resource_name = 'event'
        fields = ['id']
        allowed_methods = ['get']


class ImageResource(ModelResource):
    class Meta:
        queryset = Images.objects.all()
        resource_name = 'image'
        allowed_methods = ['get']


class BadgeResource(ModelResource):
    image = fields.ForeignKey(ImageResource, 'image')

    class Meta:
        queryset = Badges.objects.all()
        resource_name = 'badge'
        fields = ['name', 'description', "image_url"]
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

    def dehydrate(self, bundle):
        if bundle.request.GET.get('attach_dynamic_fields'):
            event_id = bundle.request.GET.get('event_id')
            bundle.data['attach_dynamic_fields_get_count'] = JoinedEventActivity.objects.filter(event_id=event_id).count()
        return bundle


class EarnedBadgeActivityResource(ModelResource):
    badge = fields.ForeignKey(BadgeResource, 'badge')
    user = fields.ForeignKey(UserResource, 'user')
    event_id = fields.ForeignKey(EventResource, 'event')

    class Meta:
        queryset = EarnedBadgeActivity.objects.order_by('datetime_earned')
        resource_name = 'earned_badge_activities'
        allowed_methods = ['get']
        filtering = {
            'id': ALL,
            'event_id': ALL,
        }

    def dehydrate_datetime_earned(self, bundle):
        oldValue = bundle.data['datetime_earned']
        newValue = oldValue.strftime("%H:%M:%S")
        return newValue

    def dehydrate(self, bundle):
        if bundle.request.GET.get('attach_dynamic_fields'):
            event_id = bundle.request.GET.get('event_id')
            bundle.data['attach_dynamic_fields_get_count'] = EarnedBadgeActivity.objects.filter(event_id=event_id).count()
        return bundle

