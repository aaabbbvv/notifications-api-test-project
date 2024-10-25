from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import CustomLoginView, NotificationView, NotificationsView, UnreadNotificationsView,\
    BulkUpdateUserNotificationView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="Test API",
      default_version='v1',
      description="Test description",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

doc_urls = [
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns = [
    path("api/", include(doc_urls)),
    path("api/notifications/", NotificationsView.as_view(), name='list_notifications'),
    path("api/notifications/bulk-update/", BulkUpdateUserNotificationView.as_view(), name='bulk_update'),
    path("api/notifications/unread-number/", UnreadNotificationsView.as_view(), name='list_notifications'),
    path("api/notifications/<int:pk>/", NotificationView.as_view(), name='get_notification'),
    path("admin/", admin.site.urls),
    path("api/login/", CustomLoginView.as_view(), name='custom_login'),
    # path("api/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
