from django.core.management import BaseCommand

from users.models import Administrator


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--email')
        parser.add_argument('--password')
        parser.add_argument('--first_name')
        parser.add_argument('--last_name')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        password = kwargs['password']
        first_name = kwargs['first_name']
        last_name = kwargs['last_name']
        admin = Administrator.objects.create_superuser(email, password)
        admin.first_name = first_name
        admin.last_name = last_name
        admin.save()
        self.stdout.write(self.style.SUCCESS(
            f'Admin {admin} created.'
        ))
