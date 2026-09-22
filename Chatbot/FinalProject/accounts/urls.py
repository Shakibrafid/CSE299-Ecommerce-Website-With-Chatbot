from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, RegisterView


router = DefaultRouter()

router.register(
    r'profiles',
    ProfileViewSet,
    basename='profile'
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]

urlpatterns += router.urls