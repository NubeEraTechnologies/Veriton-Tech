from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from bootcampapp.models import School
class Command(BaseCommand):
    help = 'Create a superuser and a teacher with predefined credentials'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Creating the superuser
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'  # Change this to your desired password

        self.stdout.write(self.style.WARNING(f'Creating Admin'))

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))

        self.stdout.write(self.style.WARNING(f'Creating Principle'))
        # Creating the teacher (non-superuser)
        school_id = School.objects.values('id')[0]['id']
        username = 'principle'
        email = 'imran@example.com'
        password = 'principle'  # Change this to your desired password



        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
        else:
            # Using create_user instead of create_superuser
            User.objects.create_user(username=username, email=email, password=password, status=True, utype='principle',school_id=school_id)
            self.stdout.write(self.style.SUCCESS(f'Principle "{username}" created successfully.'))
        

        self.stdout.write(self.style.WARNING(f'Creating Staff'))
        # Creating the teacher (non-superuser)
        school_id = School.objects.values('id')[0]['id']
        username = 'staff'
        email = 'imran@example.com'
        password = 'staff'  # Change this to your desired password



        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
        else:
            # Using create_user instead of create_superuser
            User.objects.create_user(username=username, email=email, password=password, status=True, utype='staff',school_id=school_id)
            self.stdout.write(self.style.SUCCESS(f'Staff "{username}" created successfully.'))
        

        self.stdout.write(self.style.WARNING(f'Creating Teacher'))
        # Creating the teacher (non-superuser)
        username = 'teacher'
        email = 'imran@example.com'
        for i in range (1):
            self.stdout.write(self.style.NOTICE(f'Creating teacher {i+1}'))
            username = f'teacher{i+1}'
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
            else:
                # Using create_user instead of create_superuser
                User.objects.create_user(username=username, email=email, password=username, status=True, utype='teacher',school_id=i+1)
                self.stdout.write(self.style.SUCCESS(f'Teacher "{username}" created successfully.'))
