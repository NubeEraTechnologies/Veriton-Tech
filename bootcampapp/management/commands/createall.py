from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs makemigrations, migrate, and createadmin commands sequentially.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Running makemigrations...'))
        call_command('makemigrations')

        self.stdout.write(self.style.NOTICE('Running migrate...'))
        call_command('migrate')

        self.stdout.write(self.style.NOTICE('Creating Demo data...'))
        call_command('createdemodata')
        
        self.stdout.write(self.style.NOTICE('Creating admin user...'))
        call_command('createadmin')  # No need to pass arguments since it's predefined

        self.stdout.write(self.style.SUCCESS('All commands executed successfully.'))
