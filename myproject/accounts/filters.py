from django_filters import rest_framework as filters
from .models import UserNotification

NOTIFICATION_TYPE_MAPPING = {
    'system': 1,
    'push': 2,
}

STATUS_MAPPING = {
    'unread': 0,
    'read': 1,
}


class UserNotificationFilter(filters.FilterSet):
    NOTIFICATION_TYPE_CHOICES = [
        ('system', 'System Notification'),
        ('push', 'Push Notification'),
    ]

    STATUS_CHOICES = [
        ('read', 'Read'),
        ('unread', 'Unread'),
    ]

    notification_type = filters.ChoiceFilter(choices=NOTIFICATION_TYPE_CHOICES, method='filter_notification_type')
    status = filters.ChoiceFilter(choices=STATUS_CHOICES, method='filter_status')
    ordering = filters.OrderingFilter(fields=('created',))

    class Meta:
        model = UserNotification
        fields = ['notification_type', 'status']

    def filter_notification_type(self, queryset, name, value):
        notification_type_id = NOTIFICATION_TYPE_MAPPING.get(value.lower())
        if notification_type_id:
            return queryset.filter(notification_type=notification_type_id)
        return queryset.none()

    def filter_status(self, queryset, name, value):
        status_id = STATUS_MAPPING.get(value.lower())
        if status_id is not None:
            return queryset.filter(status=status_id)
        return queryset.none()
