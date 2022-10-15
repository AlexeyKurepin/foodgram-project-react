import json
import os

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'loading ingredients from data in json'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredients.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(os.path.join(r'data', options['filename']), 'r',
                      encoding='utf-8') as f:
                data = json.load(f)
                for ingredient in data:
                    Ingredient.objects.get_or_create(
                        name=ingredient["name"],
                        measurement_unit=ingredient[
                            "measurement_unit"])
        except FileNotFoundError:
            raise CommandError('Файл отсутствует в директории data')
        except PermissionError:
            raise CommandError('Отказано в доступе, недостаточно прав')
        else:
            print('Данные загружены в базу')
