from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Удаляет суперпользователя'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Имя суперпользователя')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь {username} удален'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Суперпользователь {username} не найден'))
