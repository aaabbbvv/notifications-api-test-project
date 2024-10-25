from rest_framework import serializers
from accounts import models as acc_models
from accounts.notification_helper import fetch_notification_txt


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class NotificationSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = acc_models.UserNotification
        fields = (
            "id",
            "notification_type",
            "status",
            "text",
            "created",
        )

    def get_text(self, obj):
        language_id = self.context.get("language_id")
        if language_id:
            return fetch_notification_txt(obj, language_id)
        return None


class BulkNotificationStatusUpdateSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )