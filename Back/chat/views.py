import re
import uuid
from decimal import Decimal, InvalidOperation

from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.permissions import IsOwnerOrStaff, IsSupportAgentUser
from .models import ChatSession, ChatMessage, HumanSupportSession
from .serializers import ChatSessionSerializer, ChatMessageSerializer, HumanSupportSessionSerializer
from store.models import Product

class ChatSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_support_agent', False) or user.is_staff:
            return ChatSession.objects.filter(is_active=True)
        return ChatSession.objects.filter(user=user)

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_support_agent', False) or user.is_staff:
            return ChatMessage.objects.all()
        return ChatMessage.objects.filter(chat_session__user=user)

class HumanSupportSessionViewSet(viewsets.ModelViewSet):
    serializer_class = HumanSupportSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupportAgentUser]
    queryset = HumanSupportSession.objects.all()


def _product_payload(product):
    return {
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'description': product.description or '',
        'price': str(product.price),
        'compare_price': str(product.compare_price) if product.compare_price is not None else None,
        'stock': product.stock,
        'image': product.image.url if product.image else None,
        'category': product.category.name,
    }


def _budget_from_message(message):
    match = re.search(r'(?:under|below|within|budget(?:\s+is)?|less than)\s*[৳$]?\s*([\d,]+(?:\.\d+)?)', message)
    if not match:
        return None
    try:
        return Decimal(match.group(1).replace(',', ''))
    except InvalidOperation:
        return None


def _advisor_response(message):
    normalized = message.lower()
    products = list(Product.objects.filter(is_active=True, stock__gt=0).select_related('category'))
    if not products:
        return 'Our catalog is currently out of stock. Please check back soon.', [], 'recommendations'

    budget = _budget_from_message(normalized)
    if budget is not None:
        products = [product for product in products if product.price <= budget]

    mentioned = [
        product for product in products
        if product.name.lower() in normalized or product.slug.lower().replace('-', ' ') in normalized
    ]
    is_comparison = any(word in normalized for word in ('compare', 'comparison', 'versus', ' vs ', 'difference'))
    if is_comparison and len(mentioned) >= 2:
        selected = mentioned[:3]
        details = '; '.join(
            f'{product.name}: ৳{product.price}, {product.category.name}, {product.description or "no description"}'
            for product in selected
        )
        return f'Here is a side-by-side comparison: {details}. Choose {selected[0].name} for the first option, or {selected[1].name} if its features better match your needs.', [_product_payload(product) for product in selected], 'comparison'

    preference_terms = {
        'gaming': ('gaming', 'game', 'gpu', 'graphics'),
        'budget': ('cheap', 'budget', 'affordable', 'low price', 'inexpensive'),
        'premium': ('premium', 'best', 'high-end', 'professional'),
        'portable': ('portable', 'lightweight', 'travel', 'compact'),
        'office': ('office', 'work', 'business', 'productivity'),
    }
    requested = [name for name, terms in preference_terms.items() if any(term in normalized for term in terms)]

    def score(product):
        text = f'{product.name} {product.description or ""} {product.category.name}'.lower()
        value = sum(2 for preference in requested if any(term in text for term in preference_terms[preference]))
        if 'budget' in requested:
            value += max(0, 10 - int(product.price / max(budget or Decimal('100000'), Decimal('1')) * 10))
        if 'premium' in requested:
            value += int(product.price / max(budget or Decimal('1'), Decimal('1')))
        return value

    products.sort(key=lambda product: (-score(product), product.price))
    selected = products[:3]
    if requested or budget is not None:
        preference_text = ', '.join(requested) if requested else 'your budget'
        budget_text = f' under ৳{budget}' if budget is not None else ''
        reply = f'Based on {preference_text}{budget_text}, I recommend ' + ', '.join(product.name for product in selected) + '. '
        reply += f'{selected[0].name} is the strongest match because it is ৳{selected[0].price} and fits the available catalog details.'
    else:
        reply = 'Tell me what matters to you, such as your budget, preferred use, portability, or performance. These currently available products are a good starting point: ' + ', '.join(product.name for product in selected) + '.'
    return reply, [_product_payload(product) for product in selected], 'recommendations'


class AIChatAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        message_text = request.data.get('message')
        if not message_text:
            return Response({'detail': 'Missing message field.'}, status=400)

        session = ChatSession.objects.filter(user=user, is_active=True).first()
        if not session:
            session = ChatSession.objects.create(
                user=user,
                session_id=uuid.uuid4().hex,
                is_active=True,
            )

        chat_message = ChatMessage.objects.create(
            chat_session=session,
            sender_type='user',
            content=message_text,
        )

        reply_text, products, response_type = _advisor_response(message_text.strip())
        bot_message = ChatMessage.objects.create(
            chat_session=session,
            sender_type='bot',
            content=reply_text,
        )

        return Response({
            'session_id': session.session_id,
            'message_id': chat_message.id,
            'reply_message_id': bot_message.id,
            'reply': reply_text,
            'products': products,
            'response_type': response_type,
        }, status=201)
