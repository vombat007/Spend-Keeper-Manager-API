from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django_app_api.models import Currency


class Command(BaseCommand):
    help = 'Populate the Currency model with popular currencies and their symbols.'

    def handle(self, *args, **kwargs):
        currencies = [
            {'name': 'USD', 'symbol': '$'},
            {'name': 'EUR', 'symbol': '€'},
            {'name': 'GBP', 'symbol': '£'},
            {'name': 'JPY', 'symbol': '¥'},
            {'name': 'AUD', 'symbol': 'A$'},
            {'name': 'CAD', 'symbol': 'C$'},
            {'name': 'CHF', 'symbol': 'CHF'},
            {'name': 'CNY', 'symbol': '¥'},
            {'name': 'SEK', 'symbol': 'kr'},
            {'name': 'NZD', 'symbol': 'NZ$'},
        ]

        for currency in currencies:
            try:
                Currency.objects.create(name=currency['name'], symbol=currency['symbol'])
                self.stdout.write(self.style.SUCCESS(f"Successfully added {currency['name']}"))
            except IntegrityError:
                self.stdout.write(self.style.WARNING(f"{currency['name']} already exists in the database."))
