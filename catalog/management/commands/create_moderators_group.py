from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает ей необходимые разрешения'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана.'))

            unpublish_permission = Permission.objects.get(codename='can_unpublish_product')
            delete_permission = Permission.objects.get(codename='delete_product')
            group.permissions.add(unpublish_permission, delete_permission)
            self.stdout.write(self.style.SUCCESS('Группе "Модератор продуктов" успешно назначены разрешения'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует.'))
