import re

from django.db import transaction
from datetime import datetime
from accounts import models as acc_models
from typing import List, Dict, Union, Optional
from django.db.models import Q, OuterRef, Subquery, Exists


def get_user_notifications(user: acc_models.User):
    settings_subquery = acc_models.UserNotificationSetting.objects.filter(
        user=user,
        notification_template=OuterRef('notification_template')
    )

    notifications = acc_models.UserNotification.objects.filter(user=user).annotate(
        has_settings=Exists(settings_subquery)
    ).filter(
        Q(has_settings=False) |
        (
            Q(notification_template__usernotificationsetting__user=user) &
            (
                (Q(notification_type=1) & Q(notification_template__usernotificationsetting__system_notification=1)) |
                (Q(notification_type=2) & Q(notification_template__usernotificationsetting__push_notification=1))
            )
        )
    ).select_related('notification_template').prefetch_related('usernotificationoption_set')

    return notifications


Option = Dict[str, Union[str, int]]


def create_notification(
        user: acc_models.User,
        notification_template: acc_models.NotificationTemplate,
        notification_type: int,
        options: Optional[List[Option]]
) -> Optional[acc_models.UserNotification]:

    notification_settings = acc_models.UserNotificationSetting.objects.filter(
        user=user,
        notification_template=notification_template
    )

    if notification_settings:
        if any([
            notification_type == 1 and notification_settings.system_notification == 0,
            notification_type == 2 and notification_settings.push_notification == 0
        ]):
            return None

    notification = acc_models.UserNotification.objects.create(
        user=user,
        notification_template=notification_template,
        notification_type=notification_type,
        status=0,
        created=datetime.now()
    )
    if options:
        notification_options = [
            acc_models.UserNotificationOption(
                user_notification=notification,
                field_id=option['field_id'],
                txt=option['txt']
            )
            for option in options
        ]
        with transaction.atomic():
            acc_models.UserNotificationOption.objects.bulk_create(notification_options)

    return notification


def fetch_notification_txt(
        notification: acc_models.UserNotificationOption,
        language_id: int
) -> str:
    def replacer(match):
        field_id = int(match.group(1))
        option = notification.usernotificationoption_set.filter(field_id=field_id).last()
        return option.txt if option else match.group(0)

    content_type = acc_models.DjangoContentType.objects.filter(
        app_label="user",
        model="notificationtemplate"
    ).last()

    translation = acc_models.TranslationString.objects.filter(
        content_type=content_type,
        object_id=notification.notification_template.id,
        language_id=language_id
    ).last()

    pattern = re.compile(r'\{(\d+)\}')
    result = pattern.sub(replacer, translation.text)
    return result


