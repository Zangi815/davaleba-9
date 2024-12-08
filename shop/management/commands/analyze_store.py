from django.core.management.base import BaseCommand
from shop.models import Item, Category  
from django.db.models import Count, Max, Min, Avg, Sum

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        category_item_count = Item.objects.filter(category__name="Electronics").count()
        price_stats = Item.objects.aggregate(
            max_price=Max('price'),
            min_price=Min('price'),
            avg_price=Avg('price')
        )
        print(category_item_count)
        print(price_stats)

        categories = Category.objects.annotate(
            items_count=Count('items'),
            items_price_sum=Sum('items__price')
        )
        for category in categories:
            print(category.name, category.items_count, category.items_price_sum)

        items = Item.objects.select_related('category').all()
        for item in items:
            print(item.name, item.category.name)

        items_with_tags = Item.objects.prefetch_related('tags').all()
        for item in items_with_tags:
            tags = item.tags.all()
            print(item.name, [tag.name for tag in tags])

