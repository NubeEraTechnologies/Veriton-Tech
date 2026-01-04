from bootcampapp import models as MyModels
from django.contrib import messages
from django.db.models import Sum, F, Value, Q, Count, F, Case, When, IntegerField
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
import os
from django.db.models.functions import TruncDate
from django.core.files.storage import default_storage
from django.shortcuts import render, get_object_or_404,redirect
from bootcampapp import models
from django.http import HttpResponseRedirect
from bootcampapp.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
login_time = datetime.now()
logout_time  = datetime.now()
from django.http import HttpResponse
from django.contrib.auth import logout
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as userlogin
from django.db import IntegrityError
from django.core.files.storage import default_storage
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .encryption_utils import encrypt_password
from django.db.models import Exists, OuterRef, Value, Q, Sum,  Count
import json
from itertools import groupby
from operator import itemgetter

ROMAN_NUMERAL_MAP = {
                        'V': 5,
                        'VI': 6,
                        'VII': 7,
                        'VIII': 8,
                        'IX': 9,
                        'X': 10,
                    }

def login(request):
    return redirect('userlogin')
    # return render(request, 'bootcampapp/index.html')

def logout_view(request):
    logout(request)
    return redirect('userlogin')

@login_required
def switch_user_view(request):
    logout(request)
    return redirect('userlogin')

def check_username(request):
    if request.method == "GET":
        username = request.GET.get('username', None)
        is_taken = User.objects.filter(username=username).exists()
        return JsonResponse({'is_taken': is_taken})
    
def validate_old_password(request):
    if request.method == "GET":
        old_password = request.GET.get('old_password')
        user = request.user

        # Check if the provided old password is correct
        if user.check_password(old_password):
            return JsonResponse({"is_valid": True})
        else:
            return JsonResponse({"is_valid": False})
        
def signup(request):
    if request.method == "POST":
        # Get form data
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        username = request.POST['username'].strip()
        password = request.POST['password']
        profile_pic = request.FILES.get('profile_pic')  # Fetch the file if uploaded
        banner_pics = request.FILES.get('banner_pic')  # Fetch the file if uploaded
        mobile = request.POST['mobile'].strip()
        whatsappno = request.POST['whatsappno'].strip()
        
        # Create user
        try:
            newuser = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                mobile=mobile,
                whatsappno=whatsappno,
                username=username,
                password=password
            )

            # If a profile picture was uploaded
            if profile_pic:
                # Generate the custom file name: username_userid.extension
                file_extension = os.path.splitext(profile_pic.name)[1]  # Get the file extension
                new_file_name = f"{username}_{newuser.id}{file_extension}"

                # Save the profile pic with the new file name
                newuser.profile_pic.save(new_file_name, profile_pic)

            # If a banner picture was uploaded
            if banner_pics:
                # Generate the custom file name: username_userid.extension
                file_extension = os.path.splitext(banner_pics.name)[1]  # Get the file extension
                new_file_name = f"{username}_{newuser.id}{file_extension}"

                # Save the profile pic with the new file name
                newuser.banner_pic.save(new_file_name, banner_pics)

            # Save the user instance (if banner_pics is updated)
            newuser.save()

            users = User.objects.all().filter(is_superuser = False)
            return HttpResponseRedirect('/admin-view-user-list',{'users':users})
            
        except IntegrityError:
            return HttpResponse("A user with that username already exists.")
        except Exception as e:
            return HttpResponse(f"Something went wrong: {e}")

    return render(request, 'loginrelated/signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            userlogin(request, user)
            request.session['yono'] = encrypt_password(password)
            return redirect('home')  # Redirect to a success page.
        else:
            return render(request, 'loginrelated/userlogin.html', {'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'loginrelated/userlogin.html')
def session_expire_view(request):
    A = models.LastUserLogin.objects.all()
    if A:
        for x in A:
            id = x.id
            logout_time = datetime.now()
            dur = str( logout_time - login_time).split(".")[0]
            userlog = models.UserLog.objects.create(
                    user_id = id,
                    login = login_time,
                    logout = logout_time,
                    dur = dur
                    )
            userlog.save()
    models.LastUserLogin.objects.all().delete()
    return render(request, 'loginrelated/user_session_expire.html')

@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    if not user.is_staff:
        pic = "UserSocialAuth.objects.only('pic').get(user_id=user.id).pic"
    login_time = datetime.now()

@receiver(user_logged_out)
def post_logout(sender, user, request, **kwargs):
    logout_time = datetime.now()
    dur = str( logout_time - login_time).split(".")[0]
    userlog = models.UserLog.objects.create(
              user = user,
              login = login_time,
              logout = logout_time,
              dur = dur
            )
    userlog.save()
    models.LastUserLogin.objects.all().delete()

@login_required
def user_change_password_view(request):
    try:    
        if request.method == 'POST':
            u = request.user
            u.set_password(request.POST['passid'])
            u.save() # Add this line
            update_session_auth_hash(request, u)
            return HttpResponseRedirect('indexpage')  
        return render(request, 'loginrelated/changepassword.html')
    except:
        return render(request,'loginrelated/diffrentuser.html')

@require_POST
@csrf_exempt
def reset_user_password(request, user_id):
    print('entered')
    try:
        user = User.objects.get(id=user_id)
        # Logic to reset the user's password
        user.set_password('bootcamp123')  # Replace with your password logic
        user.profile_updated = False
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})
@login_required
def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('indexpage'))
    return render(request,'bootcampapp/404page.html')

def afterlogin_view(request):
    user = User.objects.all().filter(id = request.user.id)
    if user:
        for xx in user:
            if xx.is_superuser:
                request.session['u'] = 'admin'
                return redirect('user-dashboard')
            elif not xx.status:
                request.session['u'] = xx.utype
                return render(request,'loginrelated/wait_for_approval.html')
            elif xx.status:
                request.session['u'] = xx.utype
                return redirect('user-dashboard')
            elif not xx.profile_updated:
                request.session['u'] = xx.utype
                return redirect('user-profile')
            
            else:
                return render(request,'loginrelated/wait_for_approval.html')
    else:
        return render(request, 'loginrelated/userlogin.html')

@login_required
def user_dashboard_view(request):
    if str(request.session['u']) == 'admin':
        school_student = User.objects.filter(utype='student', grade__isnull=False)\
                        .values('school__school_name', 'grade__grade_name')\
                        .annotate(
                            grade_count=Count('grade'),  # Count students by grade
                            active_count=Count('id', filter=Q(status=True)),  # Count active users
                            on_hold_count=Count('id', filter=Q(status=False))  # Count users on hold
                        )\
                        .order_by('school__school_name', 'grade__grade_name')
        
        school_student_grade = User.objects.filter(utype='student', grade__isnull=False)\
                        .values('grade__grade_name')\
                        .annotate(
                            grade_count=Count('grade'),  # Count students by grade
                            active_count=Count('id', filter=Q(status=True)),  # Count active users
                            on_hold_count=Count('id', filter=Q(status=False))  # Count users on hold
                        )\
                        .order_by('grade__grade_name')
        school_student_grade = sorted(
                            school_student_grade,
                            key=lambda x: (ROMAN_NUMERAL_MAP.get(x['grade__grade_name'], 0))
                        )
        
        school_student_count = User.objects.filter(utype='student', grade__isnull=False)\
                            .values('school__school_name')\
                            .annotate(student_count=Count('id'))\
                            .order_by('school__school_name')  # Order by school name
        # Prepare data for the chart
        
        school_student_chart = User.objects.filter(utype='student', grade__isnull=False)\
        .annotate(date=TruncDate('created'))\
        .values('date')\
        .annotate(student_count=Count('id'))\
        .order_by('date')  # Order by date

        # Prepare data for Chart.js
        data = {}
        for entry in school_student_chart:
            date_str = entry['date'].isoformat()  # Format date as string
            student_count = entry['student_count']
            
            data[date_str] = student_count  # Store student count by date

        # Create lists for labels and counts
        labels = list(data.keys())
        counts = list(data.values())
        
        
        school_student = sorted(
                            school_student,
                            key=lambda x: (x['school__school_name'], ROMAN_NUMERAL_MAP.get(x['grade__grade_name'], 0))
                        )
        
        dict={
        'total_schools':    models.School.objects.exclude(id=None).count(),
        'total_grades':     models.Grade.objects.exclude(id=None).count(),
        'total_principles':   models.User.objects.exclude(id=None).filter(utype = 'principle', status = True).count(),
        'total_principles_pending':   models.User.objects.exclude(id=None).filter(utype = 'principle', status = False).count(),
        'total_teachers':   models.User.objects.exclude(id=None).filter(utype = 'teacher', status = True).count(),
        'total_teachers_pending':   models.User.objects.exclude(id=None).filter(utype = 'teacher', status = False).count(),
        'total_students':   models.User.objects.exclude(id=None).filter(utype = 'student', status = True).count(),
        'total_students_pending':   models.User.objects.exclude(id=None).filter(utype = 'student', status = False).count(),
        'school_student':school_student,
        'school_student_count':school_student_count,
        'labels': json.dumps(labels),  # Pass labels as JSON
        'counts': json.dumps(counts),  # Pass counts as JSON
        'school_student_grade':school_student_grade,
        }
        return render(request,'bootcampapp/admin_dashboard.html',context=dict)
    
    elif str(request.session['u']) == 'principle':
        dict={
        'total_schools':0,
        'total_exam':0,
        'total_shortExam':0, 
        'total_question':0,
        'total_short':0,
        'total_learner':0,
        }
        return render(request,'principle/principle_dashboard.html',context=dict)
    elif str(request.session['u']) == 'student':
            # total_lessons = MyModels.Lesson.objects.filter(
            #             module__grade__user__id=request.user.id,
            #             module__grade__user__grade_id=request.user.grade.id,
            #             module__grade__user__school_id=request.user.school.id,
            #             module__grade_id=request.user.grade.id
            #             ).count()
                        
            # watched_lessons = MyModels.LessonWatched.objects.filter(
            #                 student=request.user,
            #                 grade=request.user.grade
            #                 ).count()

            # watched_percentage = 0
            # # Calculate the percentage of watched lessons
            # if total_lessons > 0:  # Avoid division by zero
            #     watched_percentage = (watched_lessons / total_lessons) * 100
        
            # dict={
            # 'total_lessons': total_lessons,
            # 'watched_lessons': watched_lessons,
            # 'watched_percentage':watched_percentage
            # }
            # return render(request,'student/student_dashboard.html',context=dict)

            # Create a subquery to check if the lesson has been watched
        watched_lessons_subquery = MyModels.LessonWatched.objects.filter(
            lesson=OuterRef('id'),
            student=request.user
        )
        has_question_subquery = MyModels.ModuleQuestion.objects.filter(
            module=OuterRef('module__id')
        )

        # Get all lessons with their watched_status
        lessons = list(MyModels.Lesson.objects.filter(
            module__grade__user__id=request.user.id,
            module__grade__user__grade_id=request.user.grade.id,
            module__grade__user__school_id=request.user.school.id,
            module__grade_id=request.user.grade.id
        ).distinct().annotate(
            watched_status=Exists(watched_lessons_subquery),
            has_ques=Exists(has_question_subquery)
        ).values(
            'id', 
            'module__id', 
            'module__module_name', 
            'heading',
            'mints',
            'watched_status',
            'has_ques'
        ).order_by('module__module_name', 'serialno'))
        
        # Iterate through the lessons and set the first NO to YES after the last YES
        found_first_no = False  # Flag to track if we've found the first NO
        js = json.dumps(lessons)
        for i, lesson in enumerate(lessons):
            if i == 0 and not lesson['watched_status']:  # First lesson in the list
                lesson['watched_status_display'] = 'YES'
                lesson['watched_status'] = True
            if lesson['watched_status']:  # If we encounter a YES
                found_first_no = True  # Allow subsequent NOs to be changed to YES
                lesson['watched_status_display'] = 'YES'
            elif found_first_no and not lesson['watched_status']:  # If we encounter the first NO after a YES
                lesson['watched_status'] = True  # Change the first NO to YES
                lesson['watched_status_display'] = 'YES'
                break  # Exit after changing the first NO


        
        
        total_lessons = MyModels.Lesson.objects.filter(
            module__grade__user__id=request.user.id,
            module__grade__user__grade_id=request.user.grade.id,
            module__grade__user__school_id=request.user.school.id,
            module__grade_id=request.user.grade.id
        ).count()

        # Count watched lessons from LessonWatched model
        watched_lessons = MyModels.LessonWatched.objects.filter(
            student=request.user,
            grade=request.user.grade
        ).count()

        watched_percentage = 0
        # Calculate the percentage of watched lessons
        if total_lessons > 0:  # Avoid division by zero
            watched_percentage = (watched_lessons / total_lessons) * 100
        
        
        grouped_lessons = {key: list(group) for key, group in groupby(lessons, key=itemgetter('module__module_name'))}
        
        return render(request, 'student/studykit/studykit.html', 
                      {'grouped_lessons': grouped_lessons,
                       'total_lessons': total_lessons,
                       'watched_lessons': watched_lessons,
                       'watched_percentage':watched_percentage
                       })
    elif str(request.session['u']) == 'teacher':
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        # Filter schedulers for the current month and the sum of associated statuses < 100
        schedulers = MyModels.Scheduler.objects.filter(
            teacher_id=request.user.id,
            start__gte=start_of_month,  # Filter for start date >= first day of the month
            start__lte=end_of_month,    # Filter for start date <= last day of the month
        ).annotate(
            status_sum=Coalesce(Sum('schedulerstatus__status'), Value(0))
        ).filter(
            status_sum__lt=100  # Only include schedulers where the status sum is less than 100
        )

        # Create the context dictionary
        dict = {
            'schedulers': schedulers
        }
        return render(request,'teacher/teacher_dashboard.html',context=dict)
    elif str(request.session['u']) == 'staff':
        dict={
        'total_course':0,
        'total_exam':0,
        'total_shortExam':0, 
        'total_question':0,
        'total_short':0,
        'total_learner':0,
        }
        return render(request,'staff/staff_dashboard.html',context=dict)
    return render(request,'loginrelated/diffrentuser.html')

@login_required
def user_profile(request):
    if request.method == 'POST':
        user = User.objects.get(id = request.user.id)
        user.first_name = request.POST['first_name'].strip()
        user.last_name = request.POST['last_name'].strip()
        user.user_full_name = request.POST['user_full_name'].strip()
        user.email = request.POST['email'].strip()
        user.mobile = request.POST['mobile'].strip()
        user.whatsappno = request.POST['whatsappno']
        profile_pic = request.FILES.get('profile_pic')
        
        # If a profile picture was uploaded
        if profile_pic:
            # Generate the custom file name: username_userid.extension
            file_extension = os.path.splitext(profile_pic.name)[1]  # Get the file extension
            new_file_name = f"{user.username}_{user.id}{file_extension}"
            
            # Define the path where the file will be saved
            file_path = user.profile_pic.storage.path(new_file_name)
            
            # Check if a file with the same name exists and delete it
            if default_storage.exists(new_file_name):
                default_storage.delete(new_file_name)

            # Save the new profile pic with the new file name
            user.profile_pic.save(new_file_name, profile_pic)
        user.save
        if not user.profile_updated:
            old_password = request.POST['old_password']
            password = request.POST['confirm_password']
            password1 = request.POST['new_password']
            
            
            if user.check_password(old_password):
                if password != password1:
                    messages.warning(request, 'New password and confirm password does not matched')
                    return redirect('user-profile') 
                user.set_password(password)
                user.profile_updated = True  
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Profile Updated')

            else:
                messages.warning(request, 'invalid old password')
        return redirect('user-profile') 

    return render(request,'bootcampapp/users/user_profile.html')


@login_required
def user_password(request):
    if request.method == 'POST':
        user = User.objects.get(id = request.user.id)
        
        old_password = request.POST['old_password']
        password = request.POST['confirm_password']
        password1 = request.POST['new_password']
            
            
        if user.check_password(old_password):
            if password != password1:
                messages.warning(request, 'New password and confirm password does not matched')
                return redirect('user-password') 
            user.set_password(password)
            user.profile_updated = True  
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Updated')

        else:
            messages.warning(request, 'invalid old password')
        return redirect('user-password') 

    return render(request,'bootcampapp/users/user_password.html')

@login_required
def admin_view_user_list_view(request):
    #try:    
        if str(request.session['u']) == 'admin':
            query = request.GET.get('search', '')
            users = User.objects.all().filter(is_superuser = False)

            if query:
                users = users.filter(
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(username__icontains=query)
                )

            # Pagination
            paginator = Paginator(users, 50)  # Show 10 users per page
            page_number = request.GET.get('page')
            users_paginated = paginator.get_page(page_number)
            return render(request,'bootcampapp/users/admin_view_user_list.html',{'users': users_paginated, 'query': query})
    #except:
        return render(request,'loginrelated/diffrentuser.html')


def admin_view_user_log_details_view(request,user_id):
    try:    
        if str(request.session['u']) == 'admin':
            users = models.UserLog.objects.all().filter(user_id = user_id)
            return render(request,'bootcampapp/users/admin_view_user_log_details.html',{'users':users})
    except:
        return render(request,'loginrelated/diffrentuser.html')

@login_required
def admin_view_user_activity_details_view(request,user_id):
    #try:    
        if str(request.session['u']) == 'admin':
            users = models.UserActivity.objects.all().filter(user_id = user_id)
            return render(request,'bootcampapp/users/admin_view_user_activity_details.html',{'users':users})
    #except:
        return render(request,'loginrelated/diffrentuser.html')

@login_required
def update_user_view(request, pk):
    if str(request.session['u']) == 'admin':
        if request.method == 'POST':
            first_name = request.POST['first_name'].strip()
            last_name = request.POST['last_name'].strip()
            profile_pic = request.FILES.get('profile_pic')  # Fetch the file if uploaded
            banner_pic = request.FILES.get('banner_pic')  # Fetch the file if uploaded
            mobile = request.POST['mobile'].strip()
            whatsappno = request.POST['whatsappno'].strip()

            user = User.objects.get(id=pk)
            user.first_name = first_name
            user.last_name = last_name
            user.mobile = mobile
            user.whatsappno = whatsappno

            # Handle profile picture update
            if profile_pic:
                # Delete the old profile picture if it exists
                if user.profile_pic:
                    if default_storage.exists(user.profile_pic.name):
                        default_storage.delete(user.profile_pic.name)
                # Generate the custom file name: username_userid.extension
                file_extension = os.path.splitext(profile_pic.name)[1]  # Get the file extension
                new_file_name = f"{user.username}_{pk}{file_extension}"

                # Save the new profile picture
                user.profile_pic.save(new_file_name, profile_pic)

            # Handle banner picture update
            if banner_pic:
                # Delete the old banner picture if it exists
                if user.banner_pic:
                    if default_storage.exists(user.banner_pic.name):
                        default_storage.delete(user.banner_pic.name)
                # Generate the custom file name: username_userid.extension
                file_extension = os.path.splitext(banner_pic.name)[1]  # Get the file extension
                new_file_name = f"{user.username}_{pk}{file_extension}"

                # Save the new banner picture
                user.banner_pic.save(new_file_name, banner_pic)

            user.save()
            
            users = User.objects.filter(is_superuser=False)
            return HttpResponseRedirect('/admin-view-user-list', {'user': users})
        
        users = User.objects.get(id=pk)
        return render(request, 'bootcampapp/users/admin_update_user.html', {'users': users})

    return render(request,'loginrelated/diffrentuser.html')
@login_required
def active_user_view(request, pk):
    if str(request.session['u']) == 'admin':
        try:
            user = User.objects.get(id=pk)
            user.status = not user.status  # Toggle status
            user.save()
            return JsonResponse({'success': True, 'status': user.status})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
    return JsonResponse({'success': False, 'error': 'Unauthorized'})

@login_required
def admin_view_user_list_school_view(request):
    if str(request.session['u']) == 'admin':
        query = request.GET.get('search', '')
        school_id = request.GET.get('school')
        selected_school_id = int(school_id) if school_id else None
        if request.method == 'POST':
            
            school_id = selected_school_id
            if school_id:
                users = User.objects.filter(school_id=school_id)
                if users.exists():
                    if 'active' in request.POST:
                        users.update(status=True)
                        messages.success(request, 'All users for selected school activated ')

                    elif 'hold' in request.POST:
                        users.update(status=False)
                        messages.success(request, 'All users for selected school holded ')

        users = User.objects.all().filter(is_superuser=False, utype__in=['student', 'teacher', 'principle'])

        # Filter by school if provided
        if school_id:
            users = users.filter(school_id=school_id)

        if query:
            users = users.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(username__icontains=query)
            )

        # Get the list of schools for the dropdown
        schools = MyModels.School.objects.all()  # Assuming your school model is called School

        # Pagination
        paginator = Paginator(users, 50)
        page_number = request.GET.get('page')
        users_paginated = paginator.get_page(page_number)

        return render(request, 'bootcampapp/users/admin_view_user_list_school.html', {
            'users': users_paginated,
            'query': query,
            'schools': schools,  # Pass schools to the template
            'selected_school_id': selected_school_id,  # Pass the selected school ID
        })

    return render(request, 'loginrelated/diffrentuser.html')

@login_required
def reset_user_view(request, pk):
    if str(request.session['u']) == 'admin':
        try:
            user = User.objects.get(id=pk)
            user.set_password('bootcampapp@123')
            user.save()
            update_session_auth_hash(request, user)
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})
    return JsonResponse({'success': False, 'error': 'Unauthorized'})
@login_required
def delete_user_view(request,pk):
    if str(request.session['u']) == 'admin':
        users = models.User.objects.get(id = pk)
        users.delete()
        users = User.objects.all().filter(is_superuser = False)
        return HttpResponseRedirect('/admin-view-user-list',{'users':users})
    else:
        return render(request,'loginrelated/diffrentuser.html')


def create_principle(request):
    if str(request.session['u']) == 'admin':

        if request.method == "POST":
            # Get form data
            username = request.POST['username'].strip()
            school = request.POST['school'].strip()
            password = 'bootcamp123'
            
            # Create user
            try:
                newuser = User.objects.create_user(
                    username=username,
                    password=password,
                    utype = 'principle',
                    school_id = school
                )

                newuser.save()

                schools = models.School.objects.all().order_by('school_name')
                return HttpResponseRedirect('/admin-view-user-list',{'schools':schools})
                
            except IntegrityError:
                return HttpResponse("A user with that username already exists.")
            except Exception as e:
                return HttpResponse(f"Something went wrong: {e}")
        schools = models.School.objects.all().order_by('school_name')
        return render(request, 'bootcampapp/users/create_principle.html',{'schools':schools})
    else:
        return render(request,'loginrelated/diffrentuser.html')
    
def create_staff(request):
    if str(request.session['u']) == 'admin':

        if request.method == "POST":
            # Get form data
            username = request.POST['username'].strip()
            password = 'bootcamp123'
            
            # Create user
            try:
                newuser = User.objects.create_user(
                    username=username,
                    password=password,
                    utype = 'staff',
                    status = True
                )

                newuser.save()

                schools = models.School.objects.all().order_by('school_name')
                return HttpResponseRedirect('/admin-view-user-list',{'schools':schools})
                
            except IntegrityError:
                return HttpResponse("A user with that username already exists.")
            except Exception as e:
                return HttpResponse(f"Something went wrong: {e}")
        return render(request, 'bootcampapp/users/create_staff.html')
    else:
        return render(request,'loginrelated/diffrentuser.html')