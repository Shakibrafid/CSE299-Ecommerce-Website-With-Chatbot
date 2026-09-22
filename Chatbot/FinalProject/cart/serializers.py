from rest_framework import serializers

from store.serializers import ProductSerializer

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.PrimaryKeyRelatedField(read_only=True)
    product_detail = ProductSerializer(source='product', read_only=True)
    price = serializers.DecimalField(source='price_at_add', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'cart',
            'product',
            'product_detail',
            'quantity',
            'price_at_add',
            'price',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['cart', 'price_at_add', 'price', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        if not user or not user.is_authenticated:
            raise serializers.ValidationError('Authentication required to add cart items.')

        cart, _ = Cart.objects.get_or_create(user=user)
        product = validated_data['product']
        quantity = validated_data.get('quantity', 1)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity': quantity,
                'price_at_add': product.price,
            },
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity')
        if quantity is not None:
            if quantity <= 0:
                instance.delete()
                return instance
            instance.quantity = quantity
            instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_id', 'items', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
