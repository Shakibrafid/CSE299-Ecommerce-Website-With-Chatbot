from django.urls import path

from .views import AdminChatView, CustomerChatView


urlpatterns = [
    path(
        "chat/",
        CustomerChatView.as_view(),
        name="customer-ai-chat",
    ),
    path(
        "admin-chat/",
        AdminChatView.as_view(),
        name="admin-ai-chat",
    ),
]