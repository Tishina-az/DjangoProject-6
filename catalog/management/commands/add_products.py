from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Load test data from fixture'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command('loaddata', 'catalog.json')
        self.stdout.write(self.style.SUCCESS('Successfully load data from fixture!'))
