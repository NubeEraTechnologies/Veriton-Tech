from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from bootcampapp.models import School, Grade, Division

class Command(BaseCommand):
    help = 'Create Student Logins in bulk'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        self.stdout.write(self.style.WARNING('Creating Students...'))

        school_id = School.objects.values_list('id', flat=True).first()
        grade_id = Grade.objects.values_list('id', flat=True).first()
        division_id = Division.objects.values_list('id', flat=True).first()

        password = '123456'  # same password for all users (you can change this)

        created_count = 0
        skipped_count = 0

        for i in range(101, 151):
            username = f'VB260{i}'
            email = f'{username.lower()}@example.com'

            if User.objects.filter(username=username).exists():
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" already exists. Skipping.')
                )
                continue

            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                status=True,
                utype='student',   # or 'principle' if that’s really intended
                school_id=school_id,
                grade_id=grade_id,
                division_id=division_id,
            )

            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'User "{username}" created.'))

        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Created {created_count} users, skipped {skipped_count}.'
            )
        )
