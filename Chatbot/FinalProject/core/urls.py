from rest_framework.routers import DefaultRouter
from .views import SettingViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'settings', SettingViewSet, basename='setting')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = router.urls