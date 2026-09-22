from rest_framework.routers import DefaultRouter
from .views import ChatSessionViewSet, ChatMessageViewSet, HumanSupportSessionViewSet

router = DefaultRouter()
router.register(r'sessions', ChatSessionViewSet, basename='chatsession')
router.register(r'messages', ChatMessageViewSet, basename='chatmessage')
router.register(r'human-support', HumanSupportSessionViewSet, basename='humansupport')

urlpatterns = router.urls