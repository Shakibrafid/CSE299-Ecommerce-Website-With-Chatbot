from django.conf import settings
from rest_framework import serializers

from .models import Category, Product, ProductImage, Inventory


class FlexibleImageField(serializers.ImageField):
    def to_representation(self, value):
        if not value:
            return None

        try:
            name = value.name
        except AttributeError:
            return super().to_representation(value)

        if isinstance(name, str) and (
            name.startswith('http://')
            or name.startswith('https://')
            or name.startswith('data:')
        ):
            return name

        media_url = settings.MEDIA_URL or '/media/'
        if not media_url.endswith('/'):
            media_url = f'{media_url}/'

        if isinstance(name, str) and name.startswith('/'):
            return name

        if isinstance(name, str) and name.startswith(media_url):
            return name

        return f'{media_url}{name}'


class CategorySerializer(serializers.ModelSerializer):
    image = FlexibleImageField(required=False, allow_null=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        required=False,
    )
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'parent',
            'subcategories',
            'products',
            'image',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProductImageSerializer(serializers.ModelSerializer):
    image = FlexibleImageField(required=False, allow_null=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'created_at']
        read_only_fields = ['created_at']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'product', 'quantity_change', 'reason', 'note', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    image = FlexibleImageField(required=False, allow_null=True)
    images = ProductImageSerializer(many=True, read_only=True)
    inventory_logs = InventorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'name',
            'slug',
            'description',
            'price',
            'compare_price',
            'stock',
            'image',
            'is_active',
            'is_featured',
            'views',
            'images',
            'inventory_logs',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['views', 'created_at', 'updated_at']
