from rest_framework import viewsets, permissions
from backend.permissions import IsOwnerOrStaff
from .models import Order, Payment, Invoice
from .serializers import OrderSerializer, PaymentSerializer, InvoiceSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, 'is_support_agent', False):
            return Order.objects.all()
        return Order.objects.filter(user=user)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, 'is_support_agent', False):
            return Payment.objects.all()
        return Payment.objects.filter(order__user=user)

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or getattr(user, 'is_support_agent', False):
            return Invoice.objects.all()
        return Invoice.objects.filter(order__user=user)