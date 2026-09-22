from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ProfileViewSet, RegisterAPIView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
	path('register/', RegisterAPIView.as_view(), name='register'),
]

# Append the router-generated URLs (profiles list/detail/create/etc.)
urlpatterns += router.urls