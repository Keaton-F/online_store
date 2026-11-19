from typing import Any

from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Создает группу 'Модератор продуктов' и назначает ей необходимые права."

    def handle(self, *args: Any, **options: Any) -> None:
        group, created = Group.objects.get_or_create(name="Модератор продуктов")

        # Ищем право на отмену публикации и стандартное право на удаление продукта
        unpublish_perm = Permission.objects.get(codename="can_unpublish_product")
        delete_perm = Permission.objects.get(codename="delete_product")

        group.permissions.add(unpublish_perm, delete_perm)

        self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' успешно настроена и получила все права."))
