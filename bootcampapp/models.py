from django.db import models
from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
class Grade(models.Model):
    # Example fields
    grade_name = models.CharField(max_length=100)
    def __str__(self):
        return self.grade_name
    
class Division(models.Model):
    # Example fields
    division_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.division_name

class School(models.Model):
    school_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    enrollment_date = models.DateField(auto_now=True)
    def __str__(self):
        return self.school_name
    
class User(AbstractUser):
    school=models.ForeignKey(School,on_delete=models.SET_NULL, null=True)
    grade=models.ForeignKey(Grade,on_delete=models.SET_NULL, null=True)
    division=models.ForeignKey(Division,on_delete=models.SET_NULL, null=True)
    roll_no = models.CharField(max_length=200)
    user_full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    CAT = (
        ("principle", "principle"),
        ("teacher", "teacher"),
        ("student", "student"),
    )
    utype = models.CharField(max_length=200, choices=CAT, default="student")
    mobile = models.CharField(max_length=10)
    whatsappno = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    profile_updated = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created =  models.DateTimeField(default=timezone.now)


class UserLog(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    login =  models.DateTimeField(default=datetime.datetime.now)
    logout = models.DateTimeField(default=datetime.datetime.now)
    dur = models.CharField(default='',max_length=200)
    session_id = models.CharField(default='',max_length=200)

    
class IsFirstLogIn(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.user

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=2048)
    method = models.CharField(max_length=16)
    status_code = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username} accessed {self.url} ({self.status_code})'
    
class ErrorLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    url = models.CharField(max_length=2048)
    exception = models.TextField()
    traceback = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Error occurred while processing {self.url}'

class LastUserLogin(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

class Module(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    module_name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000,default='')
    module_pic = models.ImageField(upload_to='module_pic/', blank=True, null=True)
    def __str__(self):
        return self.module_name
    
class Lesson(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    serialno = models.PositiveIntegerField()
    mints = models.PositiveIntegerField(default=0)
    heading = RichTextField(default='')
    about = RichTextField(default='')
    reqmaterial =RichTextField(default='')
    video = models.CharField(max_length=1000,default='')
    digram = models.CharField(max_length=1000,default='')
    code = models.CharField(max_length=1000,default='')
    process = RichTextField(default='')
    get = RichTextField(default='')
    
    def __str__(self):  
        return self.heading
    
class LessonWatched(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    
class ModuleQuestion(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    question=RichTextField(default='')
    option1=RichTextField(default='')
    option2=RichTextField(default='')
    option3=RichTextField(default='')
    option4=RichTextField(default='')
    cat=(('1','Option1'),('2','Option2'),('3','Option3'),('4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)
    marks=models.IntegerField(default=1)

class ModuleResult(models.Model):
    student=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    marks = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    timetaken = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

class ModuleResultDetails(models.Model):
    moduleresult=models.ForeignKey(ModuleResult,on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(ModuleQuestion,on_delete=models.SET_NULL, null=True)
    selected=models.CharField(max_length=200)


class Exam(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    exam_name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000,default='')
    def __str__(self):
        return self.exam_name
    

class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    question=RichTextField(default='')
    option1=RichTextField(default='')
    option2=RichTextField(default='')
    option3=RichTextField(default='')
    option4=RichTextField(default='')
    cat=(('1','Option1'),('2','Option2'),('3','Option3'),('4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)
    marks=models.IntegerField(default=1)

class ExamResult(models.Model):
    student=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)
    marks = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    timetaken = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

class ExamResultDetails(models.Model):
    examresult=models.ForeignKey(ExamResult,on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(ExamQuestion,on_delete=models.SET_NULL, null=True)
    selected=models.CharField(max_length=200)

class StudentAttendance(models.Model):
    student=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    status = models.PositiveIntegerField(default=0)

class Scheduler(models.Model): 
    school=models.ForeignKey(School,on_delete=models.SET_NULL, null=True)
    teacher=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    all_day = models.BooleanField(default=False)
    
    def __str__(self):
        # Return a formatted string instead of a datetime object
        return f"Schedule on {self.start.strftime('%Y-%m-%d %H:%M:%S')}"
    
class SchedulerStatus(models.Model): 
    date = models.DateField()
    scheduler=models.ForeignKey(Scheduler,on_delete=models.SET_NULL, null=True)
    teacher=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    status=models.PositiveIntegerField(default=0)

class GradeFee(models.Model): 
    school=models.ForeignKey(School,on_delete=models.SET_NULL, null=True)
    grade=models.ForeignKey(Grade,on_delete=models.SET_NULL, null=True)
    fee=models.PositiveIntegerField(default=0)

class FeePaid(models.Model): 
    date = models.DateField()
    student=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    feepaid=models.PositiveIntegerField(default=0)