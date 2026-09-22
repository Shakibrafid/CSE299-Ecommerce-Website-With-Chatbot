import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings
from store.models import Category, Product, ProductImage, Inventory
from django.contrib.auth import get_user_model

User = get_user_model()

PLACEHOLDER_PNG = (
    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
    b'\x00\x00\x00\x0cIDATx\x9cc`\x00\x00\x00\x02\x00\x01\xe2!\xbc\x33\x00\x00\x00\x00IEND\xaeB`\x82'
)


def ensure_media_file(relative_path):
    absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
    if not os.path.exists(absolute_path):
        with open(absolute_path, 'wb') as image_file:
            image_file.write(PLACEHOLDER_PNG)
    return relative_path


def seed_store():
    Category.objects.all().delete()
    Product.objects.all().delete()
    ProductImage.objects.all().delete()
    Inventory.objects.all().delete()

    categories = [
        {
            'name': 'Electronics',
            'slug': 'electronics',
            'description': 'Latest gadgets and smart devices.',
            'is_active': True,
            'image': ensure_media_file('categories/electronics.jpg'),
        },
        {
            'name': 'Fashion',
            'slug': 'fashion',
            'description': 'Trendy clothing and accessories.',
            'is_active': True,
            'image': ensure_media_file('categories/fashion.jpg'),
        },
        {
            'name': 'Home & Living',
            'slug': 'home-living',
            'description': 'Furniture and home essentials.',
            'is_active': True,
            'image': ensure_media_file('categories/home-living.jpg'),
        },
        {
            'name': 'Sports',
            'slug': 'sports',
            'description': 'Performance gear and outdoor essentials.',
            'is_active': True,
            'image': ensure_media_file('categories/sports.jpg'),
        },
    ]

    created_categories = []
    for data in categories:
        category, _ = Category.objects.get_or_create(slug=data['slug'], defaults=data)
        category.image = data['image']
        category.save()
        created_categories.append(category)

    products = [
        {
            'category': 'Electronics',
            'name': 'Wireless Earbuds',
            'slug': 'wireless-earbuds',
            'description': 'Noise-cancelling earbuds with 24-hour battery life.',
            'price': '4990.00',
            'compare_price': '5990.00',
            'stock': 25,
            'is_active': True,
            'is_featured': True,
            'image': ensure_media_file('products/main/wireless-earbuds.jpg'),
            'gallery_images': [
                ensure_media_file('products/gallery/wireless-earbuds-1.jpg'),
                ensure_media_file('products/gallery/wireless-earbuds-2.jpg'),
            ],
        },
        {
            'category': 'Electronics',
            'name': 'Smart Watch',
            'slug': 'smart-watch',
            'description': 'Track your health and stay connected everywhere.',
            'price': '7590.00',
            'compare_price': '8990.00',
            'stock': 18,
            'is_active': True,
            'is_featured': True,
            'image': ensure_media_file('products/main/smart-watch.jpg'),
            'gallery_images': [
                ensure_media_file('products/gallery/smart-watch-1.jpg'),
            ],
        },
        {
            'category': 'Fashion',
            'name': 'Classic Denim Jacket',
            'slug': 'classic-denim-jacket',
            'description': 'Comfortable denim jacket for everyday wear.',
            'price': '3290.00',
            'compare_price': '3990.00',
            'stock': 30,
            'is_active': True,
            'is_featured': False,
            'image': ensure_media_file('products/main/classic-denim-jacket.jpg'),
            'gallery_images': [
                ensure_media_file('products/gallery/classic-denim-jacket-1.jpg'),
            ],
        },
        {
            'category': 'Fashion',
            'name': 'Leather Crossbody Bag',
            'slug': 'leather-crossbody-bag',
            'description': 'Premium leather bag with multiple compartments.',
            'price': '5890.00',
            'compare_price': '6990.00',
            'stock': 12,
            'is_active': True,
            'is_featured': True,
            'image': ensure_media_file('products/main/leather-crossbody-bag.jpg'),
            'gallery_images': [
                ensure_media_file('products/gallery/leather-crossbody-bag-1.jpg'),
            ],
        },
        {
            'category': 'Home & Living',
            'name': 'Ergonomic Office Chair',
            'slug': 'ergonomic-office-chair',
            'description': 'Comfortable chair for work-from-home setups.',
            'price': '12990.00',
            'compare_price': '14990.00',
            'stock': 10,
            'is_active': True,
            'is_featured': False,
            'image': ensure_media_file('products/main/ergonomic-office-chair.jpg'),
            'gallery_images': [
                ensure_media_file('products/gallery/ergonomic-office-chair-1.jpg'),
            ],
        },
        {
            'category': 'Home & Living',
            'name': 'Ambient Table Lamp',
            'slug': 'ambient-table-lamp',
            'description': 'Soft lighting with a modern minimalist design.',
            'price': '2490.00',
            'compare_price': '2990.00',
            'stock': 22,
            'is_active': True,
            'is_featured': False,
            'image': ensure_media_file('products/main/ambient-table-lamp.jpg'),
            'gallery_images': [
                ensure_media_file('products/gallery/ambient-table-lamp-1.jpg'),
            ],
        },
        {
            'category': 'Sports',
            'name': 'Running Shoes',
            'slug': 'running-shoes',
            'description': 'Lightweight running shoes built for comfort.',
            'price': '4590.00',
            'compare_price': '5490.00',
            'stock': 20,
            'is_active': True,
            'is_featured': True,
            'image': ensure_media_file('products/main/running-shoes.jpg'),
            'gallery_images': [
                ensure_media_file('products/gallery/running-shoes-1.jpg'),
            ],
        },
        {
            'category': 'Sports',
            'name': 'Yoga Mat',
            'slug': 'yoga-mat',
            'description': 'Non-slip yoga mat for home or studio use.',
            'price': '1890.00',
            'compare_price': '2290.00',
            'stock': 35,
            'is_active': True,
            'is_featured': False,
            'image': ensure_media_file('products/main/yoga-mat.jpg'),
            'gallery_images': [
                ensure_media_file('products/gallery/yoga-mat-1.jpg'),
            ],
        },
    ]

    category_lookup = {category.name: category for category in created_categories}
    for data in products:
        category = category_lookup[data['category']]
        product, created = Product.objects.get_or_create(slug=data['slug'], defaults={
            'category': category,
            'name': data['name'],
            'description': data['description'],
            'price': data['price'],
            'compare_price': data['compare_price'],
            'stock': data['stock'],
            'is_active': data['is_active'],
            'is_featured': data['is_featured'],
            'image': data['image'],
        })
        if not created:
            product.image = data['image']
            product.save()

        for gallery_image in data['gallery_images']:
            ProductImage.objects.get_or_create(product=product, image=gallery_image)

        Inventory.objects.get_or_create(
            product=product,
            defaults={
                'quantity_change': data['stock'],
                'reason': 'Initial stock',
                'note': 'Seeded inventory',
                'created_by': None,
            },
        )

    print('Seeded categories, products, and image paths successfully.')


if __name__ == '__main__':
    seed_store()
