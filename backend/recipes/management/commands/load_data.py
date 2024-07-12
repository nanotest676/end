import csv
from django.conf import settings
from django.core.management import BaseCommand
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#E26C2D', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#49B64E', 'slug': 'dinner'},
            {'name': 'Ужин', 'color': '#8775D2', 'slug': 'supper'}
        ]
        
        for tag in data:
            Tag.objects.get_or_create(
                name=tag['name'], defaults={'color': tag['color'], 'slug': tag['slug']}
            )
        
        with open(
            f'{settings.BASE_DIR}/data/ingredients.csv',
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    name, measurement_unit = row
                    Ingredient.objects.get_or_create(
                        name=name, defaults={'measurement_unit': measurement_unit}
                    )
                else:
                    self.stderr.write(self.style.ERROR(f"Incorrect data format: {row}"))
