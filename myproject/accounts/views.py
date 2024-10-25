import hashlib
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts import models as acc_models
from .filters import UserNotificationFilter
from .serializers import LoginSerializer, NotificationSerializer, BulkNotificationStatusUpdateSerializer
from rest_framework.permissions import AllowAny
from accounts.permisions import IsAuthenticatedUser
from django_filters.rest_framework import DjangoFilterBackend
from accounts.notification_helper import get_user_notifications
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def hash_password(password):
    salt = "salt"
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()[:45]


def check_password(password, current_password):
    return current_password == hash_password(password)


class CustomLoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = acc_models.User.objects.get(email=email)
            if check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except acc_models.User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UnreadNotificationsView(APIView):
    permission_classes = (IsAuthenticatedUser,)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of unread notifications'),
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        number = get_user_notifications(self.request.user).filter(status=0).count()
        return Response({'number': number})


class NotificationsView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedUser,)
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserNotificationFilter

    def get_queryset(self):
        return get_user_notifications(self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        language = self.request.user.language

        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"language_id": language.id})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={"language_id": language.id})
        return Response(serializer.data)


class NotificationView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedUser,)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return (
            acc_models.UserNotification.objects.filter(user_id=self.request.user.id)
                .select_related('notification_template')
                .prefetch_related('usernotificationoption_set')
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        language = self.request.user.language
        serializer = self.get_serializer(instance, context={"language_id": language.id})
        return Response(serializer.data)


class BulkUpdateUserNotificationView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticatedUser,)
    serializer_class = BulkNotificationStatusUpdateSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Successfully updated notifications",
                examples={"application/json": {"detail": "3 notifications updated successfully."}}
            )
        },
        operation_summary="Bulk update user notification statuses",
        operation_description="Update the status of multiple user notifications by providing a list of notification IDs."
    )
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data['ids']
        updated_count = get_user_notifications(self.request.user).filter(id__in=ids).update(status=1)
        return Response(
            {"detail": f"{updated_count} notifications updated successfully."},
            status=status.HTTP_200_OK
        )

