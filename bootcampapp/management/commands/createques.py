from django.core.management.base import BaseCommand
from bootcampapp import models as MyModels
import random
class Command(BaseCommand):
    help = 'Create a Demo Question'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Creating Question...'))
        for i in range (9):
            MyModels.ModuleQuestion.objects.create(
                grade_id = 1,
                module_id = 2,
                question = f'Question {i+1}',
                option1 = f'Option 1',
                option2 = f'Option 2',
                option3 = f'Option 3',
                option4 = f'Option 4',
                answer = random.randint(1, 4),
                marks = 1
            ).save()
        self.stdout.write(self.style.SUCCESS('Question created successfully...'))
        