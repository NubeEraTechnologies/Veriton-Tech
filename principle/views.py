from django.shortcuts import render, redirect
from bootcampapp import models
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from bootcampapp.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from bootcampapp import models as MyModels

def teacher_list(request):
    if str(request.session['u']) == 'principle':
        users = User.objects.all().filter(utype = 'teacher', school_id = request.user.school.id, status = True)
        return render(request,'principle/user/teacher_list.html',{'users':users})
    else:
        return render(request,'loginrelated/diffrentuser.html')
    
def teacher_list_pending(request):
    if str(request.session['u']) == 'principle':
        users = User.objects.all().filter(utype = 'teacher', school_id = request.user.school.id, status = False)
        return render(request,'principle/user/teacher_list_pending.html',{'users':users})
    else:
        return render(request,'loginrelated/diffrentuser.html')
    
def create_teacher(request):
    if str(request.session['u']) == 'principle':

        if request.method == "POST":
            # Get form data
            username = request.POST['username'].strip()
            password = 'bootcamp123'
            
            # Create user
            try:
                newuser = User.objects.create_user(
                    username=username,
                    password=password,
                    utype = 'teacher',
                    school_id = request.user.school.id,
                )

                newuser.save()
                return redirect('teacher-list')
                
            except IntegrityError:
                return HttpResponse("A user with that username already exists.")
            except Exception as e:
                return HttpResponse(f"Something went wrong: {e}")
        return render(request, 'principle/user/create_teacher.html')
    else:
        return render(request,'loginrelated/diffrentuser.html')
    
@login_required
def all_teacher_attendance_reportmonthwise_view(request):
    if str(request.session['u']) != 'principle':
        return render(request,'loginrelated/diffrentuser.html')
    today = datetime.today()
    teacher_attendance = {}
    current_month_days = []
    search_date = None

    if request.method == 'POST':
        # Get the selected month
        search_date = request.POST.get('date', None)

        # Default to the current month if no date is provided
        if search_date:
            try:
                year, month = map(int, search_date.split('-'))
                first_day_of_month = datetime(year, month, 1).date()
                if month == 12:
                    first_day_of_next_month = datetime(year + 1, 1, 1).date()
                else:
                    first_day_of_next_month = datetime(year, month + 1, 1).date()
                last_day_of_month = first_day_of_next_month - timedelta(days=1)
            except ValueError:
                search_date = None
                first_day_of_month = today.replace(day=1).date()
                last_day_of_month = today.date()
        else:
            first_day_of_month = today.replace(day=1).date()
            if today.month == 12:
                last_day_of_month = (datetime(today.year + 1, 1, 1) - timedelta(days=1)).date()
            else:
                last_day_of_month = (datetime(today.year, today.month + 1, 1) - timedelta(days=1)).date()

        # Generate a list of all days in the current month
        current_month_days = [
            first_day_of_month + timedelta(days=i)
            for i in range((last_day_of_month - first_day_of_month).days + 1)
        ]

        # Fetch all teachers from the same school
        teachers = User.objects.filter(utype='teacher', school_id=request.user.school_id)

        # Retrieve attendance data for all teachers in the selected month
        attendance_data = MyModels.SchedulerStatus.objects.filter(
            date__range=[first_day_of_month, last_day_of_month]
        )

        # Organize attendance data by teacher and day
        attendance_dict = {}
        for record in attendance_data:
            if record.teacher_id not in attendance_dict:
                attendance_dict[record.teacher_id] = {}
            attendance_dict[record.teacher_id][record.date] = record.status

        # Populate teacher attendance for each day of the month
        for teacher in teachers:
            teacher_attendance[teacher.id] = {
                'name': teacher.get_full_name() or teacher.username,
                'attendance': [
                    'Y' if attendance_dict.get(teacher.id, {}).get(day, 0) > 0 else 'N'
                    for day in current_month_days
                ]
            }

            # Mark as 'N' (absent) if no records exist for the teacher
            if teacher.id not in attendance_dict:
                teacher_attendance[teacher.id]['attendance'] = ['N'] * len(current_month_days)

    return render(request, 'principle/user/teacher_attendance_report_month.html', {
        'report': teacher_attendance,
        'current_month_days': current_month_days,
        'search_date': search_date,
    })    