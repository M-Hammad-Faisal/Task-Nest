from django.core.management.base import BaseCommand
from src.apps.users.models import CustomUser

class Command(BaseCommand):
    help = "Sets up an initial superuser"

    def handle(self, *args, **options):
        if not CustomUser.objects.filter(username="admin").exists():
            CustomUser.objects.create_superuser(
                username="admin",
                first_name="Admin",
                role="admin",
                email="admin@example.com",
                password="admin123",
                is_verified=True,
            )
            self.stdout.write(self.style.SUCCESS("Superuser created: admin/admin123"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))