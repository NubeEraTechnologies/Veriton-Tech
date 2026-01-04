from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
import random
from django.contrib import messages
from bootcampapp import models as MyModels
from django.core.paginator import Paginator
from django.http import HttpResponse
from bootcampapp.models import User
from django.db import IntegrityError
import csv
from django.http import JsonResponse
from django.db.models import  F, Value, Q
from django.db.models import Count, F, Case, When, IntegerField
from django.db.models.functions import Coalesce
ROMAN_NUMERAL_MAP = {
                        'V': 5,
                        'VI': 6,
                        'VII': 7,
                        'VIII': 8,
                        'IX': 9,
                        'X': 10,
                    }
def roman_to_int(roman):
    roman_values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    prev_value = 0
    total = 0
    for char in reversed(roman):
        value = roman_values[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total

def student_list(request):
    if str(request.session['u']) == 'teacher':
        # Get the 'search' and 'grade_id' parameters from the GET request
        query = request.GET.get('search', '')
        grade_id = request.GET.get('grade_id')
        division_id = request.GET.get('division_id')

        # Get all grades to populate the dropdown
        grades = MyModels.Grade.objects.all()

        # Get all division to populate the dropdown
        divisions = MyModels.Division.objects.all()

        # Filter students by 'student' type and the current teacher's school
        students = User.objects.filter(
            utype='student',
            school_id=request.user.school.id,
            status=True
        )

        # Apply search filter
        if query:
            students = students.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(username__icontains=query) |
                Q(grade__grade_name__icontains=query) |
                Q(division__division_name__icontains=query)
            )

        # Apply grade filter if a grade is selected
        if grade_id:
            students = students.filter(grade_id=grade_id)
        
        # Apply division filter if a grade is selected
        if division_id:
            students = students.filter(division_id=division_id)

        # Annotate the students queryset with progress data
        students_with_data = students.annotate(
            total_lessons=Count('grade__lesson', distinct=True),
            total_watched_lessons=Count('lessonwatched', distinct=True),
            watched_percentage=Case(
                When(total_lessons__gt=0, then=F('total_watched_lessons') * 100 / F('total_lessons')),
                default=0,
                output_field=IntegerField()
            )
        ).select_related('grade', 'division')

        # Paginate the results
        paginator = Paginator(students_with_data, 50)
        page_number = request.GET.get('page')
        students_paginated = paginator.get_page(page_number)

        return render(request, 'teacher/user/student_list.html', {
            'users': students_paginated,
            'grades': grades,  # Pass grades to the template for the dropdown
            'selected_grade': grade_id,  # Preserve the selected grade
            'divisions': divisions,  # Pass divisions to the template for the dropdown
            'selected_division': division_id,  # Preserve the selected division
            'query': query  # Preserve the search query
        })
    else:
        return render(request, 'loginrelated/diffrentuser.html')
    
def student_attendance(request):
    if str(request.session['u']) == 'teacher':
        # Get the 'search' and 'grade_id' parameters from the GET request
        query = request.GET.get('search', '')
        grade_id = request.GET.get('grade_id')
        division_id = request.GET.get('division_id')

        # Get all grades to populate the dropdown
        grades = MyModels.Grade.objects.all()

        # Get all division to populate the dropdown
        divisions = MyModels.Division.objects.all()

        # Filter students by 'student' type and the current teacher's school
        students = User.objects.filter(
            utype='student',
            school_id=request.user.school.id,
            status=True
        )

        # Apply search filter
        if query:
            students = students.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(username__icontains=query) |
                Q(grade__grade_name__icontains=query) |
                Q(division__division_name__icontains=query)
            )

        # Apply grade filter if a grade is selected
        if grade_id:
            students = students.filter(grade_id=grade_id)
        
        # Apply division filter if a grade is selected
        if division_id:
            students = students.filter(division_id=division_id)

        # Annotate the students queryset with progress data
        students_with_data = students.annotate(
            total_lessons=Count('grade__lesson', distinct=True),
            total_watched_lessons=Count('lessonwatched', distinct=True),
            watched_percentage=Case(
                When(total_lessons__gt=0, then=F('total_watched_lessons') * 100 / F('total_lessons')),
                default=0,
                output_field=IntegerField()
            )
        ).select_related('grade', 'division')

        # Paginate the results
        paginator = Paginator(students_with_data, 50)
        page_number = request.GET.get('page')
        students_paginated = paginator.get_page(page_number)

        return render(request, 'teacher/user/student_attendance.html', {
            'users': students_paginated,
            'grades': grades,  # Pass grades to the template for the dropdown
            'selected_grade': grade_id,  # Preserve the selected grade
            'divisions': divisions,  # Pass divisions to the template for the dropdown
            'selected_division': division_id,  # Preserve the selected division
            'query': query  # Preserve the search query
        })
    else:
        return render(request, 'loginrelated/diffrentuser.html')
    
    
def student_list_pending(request):
    if str(request.session['u']) == 'teacher':
        query = request.GET.get('search', '')
        users = User.objects.all().filter(utype = 'student', school_id = request.user.school.id, status = False)
        if query:
                users = users.filter(
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(username__icontains=query)
                )
        paginator = Paginator(users, 50)  # Show 10 users per page
        page_number = request.GET.get('page')
        users_paginated = paginator.get_page(page_number)
        
        return render(request,'teacher/user/student_list_pending.html',{'users':users_paginated})
    else:
        return render(request,'loginrelated/diffrentuser.html')
    
def create_student(request):
    if str(request.session['u']) == 'teacher':

        if request.method == "POST":
            # Get form data
            username = request.POST['username'].strip()
            grade = request.POST['grade'].strip()
            division = request.POST['division'].strip()
            roll_no = request.POST['roll_no'].strip()
            password = 'bootcamp123'
            
            # Create user
            try:
                newuser = User.objects.create_user(
                    username=username,
                    password=password,
                    utype = 'student',
                    school_id = request.user.school.id,
                    grade_id = grade,
                    division_id = division,
                    roll_no = roll_no,
                )

                newuser.save()
                return redirect('student-list-pending')
                
            except IntegrityError:
                return HttpResponse("A user with that username already exists.")
            except Exception as e:
                return HttpResponse(f"Something went wrong: {e}")
        divisions = MyModels.Division.objects.all().order_by('division_name')                
        # Fetch all grades
        grades = list(MyModels.Grade.objects.all())

        # Sort grades using the custom roman_to_int function
        grades_sorted = sorted(grades, key=lambda grade: roman_to_int(grade.grade_name))                
        return render(request, 'teacher/user/create_student.html', {'grades': grades_sorted, 'divisions': divisions})
    else:
        return render(request,'loginrelated/diffrentuser.html')
    
def check_username_exist(request, username, fname, lname):
    # Check if the provided username exists
    if User.objects.filter(username=username).exists():
        # Username exists, so generate a new one
        while True:
            # Generate a random 4-digit number and create a new username
            random_number = random.randint(1000, 9999)
            new_username = f"{fname}_{lname}_{random_number}"
            
            # Check if the newly generated username exists
            if not User.objects.filter(username=new_username).exists():
                return new_username  # Unique username found, return it

    # Username does not exist, it's available
    return username


@login_required
def upload_student_csv(request):
    if str(request.session['u']) == 'teacher':
        if request.method == 'POST':
            if 'select_file' not in request.FILES or request.FILES['select_file'] == '':
                messages.info(request, 'Please select a CSV file for upload')
            else:
                csv_file = request.FILES['select_file']

                # Check if file is CSV
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'File is not CSV type')
                    return render(request, 'teacher/user/upload_user_csv.html')

                school = request.user.school.id
                file_data = csv_file.read().decode('utf-8').splitlines()

                csv_reader = csv.reader(file_data)
                next(csv_reader)  # Skip header row

                oldgr = ''
                olddiv = ''
                grid = 0
                divid = 0
                for row in csv_reader:
                    fname, lname, grade, division, rollno = [col.strip() for col in row]

                    # Fetch or create Grade
                
                    gr , created = MyModels.Grade.objects.get_or_create(grade_name=grade)
                    grid = gr.id

                    # Fetch or create Division
                    
                    dv , created  = MyModels.Division.objects.get_or_create(division_name=division)
                    divid = dv.id

                    # Ensure username is unique
                    username = fname + '_' + lname
                    username = check_username_exist(request, username, fname, lname)

                    # Create new User object
                    newuser = User.objects.create_user(
                        first_name=fname,
                        last_name=lname,
                        username=username,
                        password='bootcamp123',
                        school_id=school,
                        grade_id=grid,
                        division_id=divid,
                        roll_no=rollno
                    )
                    newuser.save()  # Corrected to call the save method

                messages.success(request, 'CSV upload successful')
        return render(request, 'teacher/user/upload_student_csv.html')
    else:
        return render(request, 'loginrelated/diffrentuser.html')
@login_required
def teacher_view_user_list_view(request):
    #try:    
        if str(request.session['u']) == 'teacher':
            query = request.GET.get('search', '')
            users = User.objects.all().filter(is_superuser = False, utype = 'student')

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
            return render(request,'teacher/studentrelated/teacher_view_user_list.html',{'users': users_paginated, 'query': query})
    #except:
        return render(request,'loginrelated/diffrentuser.html')

    
# Display list of exams
@login_required
def exam_list(request):
    if str(request.session['u']) == 'teacher':
        exams = MyModels.Exam.objects.all()
        return render(request, 'teacher/exam/exam_list.html', {'exams': exams})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Display list of exams
@login_required
def exam_student_top(request,exam_id):
    if str(request.session['u']) == 'teacher':
        # Get the top 10 students ordered by their marks in the most recent exam result
        students = MyModels.ExamResult.objects.filter(exam_id=exam_id).order_by('-marks')[:10].values(
            'student__user_full_name',  # Student's full name
            'marks',                    # Marks
            'exam__id',                  # Exam ID
            'student__id'                # Student ID
        )
        return render(request, 'teacher/exam/exam_student_top.html', {'students': students})
    else:
        return render(request,'loginrelated/diffrentuser.html')

@login_required
def exam_student_marks_list(request,exam_id):
    if str(request.session['u']) == 'teacher':
        # Query to get all students with their exam marks, or 0 if no result exists
        students = User.objects.filter(utype='student').annotate(
    marks=Coalesce(
        F('examresult__marks'),
        Value(0)  # Default to 0 if no ExamResult exists
    ),
    student_id=F('id'),
    exam_id=Coalesce(F('examresult__exam_id'), Value(0))  # Ensure a fallback value
).filter(
    Q(examresult__exam_id=exam_id) | Q(examresult__isnull=True)
)
        return render(request, 'teacher/exam/exam_student_result.html', {'students': students})
    else:
        return render(request,'loginrelated/diffrentuser.html')
    
@login_required
def exam_student_details_list(request,exam_id,student_id):
    #try:    
        if str(request.session['u']) == 'teacher':
            # Pre-fetch related ExamResult for each ExamResultDetail
            exams = MyModels.ExamResultDetails.objects.all().filter(
                examresult__student_id=student_id,
                examresult__exam_id=exam_id,
                question_id__in=MyModels.ExamQuestion.objects.all()
            ).select_related('examresult')  # This will fetch the related ExamResult
            return render(request,'teacher/exam/exam_student_details.html',{'exams':exams})
    #except:
        return render(request,'lxpapp/404page.html')
# Create a new exam
@login_required
def exam_create(request):
    if str(request.session['u']) == 'teacher':
        if request.method == 'POST':
            grade = request.POST.get('grade')
            exam_name = request.POST['exam_name']
            description = request.POST['description']
            if exam_name:
                mode = MyModels.Exam.objects.create(grade_id=grade,exam_name=exam_name,description=description)
                mode.save()
                messages.success(request, 'Exam created successfully!')
                return redirect('exam_create')
        grade = MyModels.Grade.objects.filter(id__isnull=False)\
                        .values('id','grade_name')
        grade = sorted(
                            grade,
                            key=lambda x: (ROMAN_NUMERAL_MAP.get(x['grade_name'], 0))
                        )
        return render(request, 'teacher/exam/exam_create.html',{'grades':grade})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Update an existing exam
@login_required
    
def exam_update(request, id):
    if str(request.session['u']) == 'teacher':
        if request.method == 'POST':
            grade = request.POST.get('grade')
            exam_name = request.POST['exam_name']
            description = request.POST['description']
            
            mode = get_object_or_404(MyModels.Exam, id=id)
            mode.grade_id = grade
            mode.exam_name = exam_name
            mode.description = description
            
            mode.save()
            messages.success(request, 'Exam updated successfully!' if id else 'Exam created successfully!')
            return redirect('exam_list')

        # Load the exam details if updating
        exam = None
        exam = get_object_or_404(MyModels.Exam, id=id)

        grades = MyModels.Grade.objects.filter(id__isnull=False).values('id', 'grade_name')
        grades = sorted(grades, key=lambda x: (ROMAN_NUMERAL_MAP.get(x['grade_name'], 0)))

        return render(request, 'teacher/exam/exam_update.html', {
            'grades': grades,
            'exam': exam,
        })
    else:
        return render(request, 'loginrelated/diffrentuser.html')

# Delete a exam
@login_required
def exam_delete(request, id):
    if str(request.session['u']) == 'teacher':
        exam = get_object_or_404(MyModels.Exam, id=id)
        exam.delete()
        
        return redirect('exam_list')
    else:
        return render(request,'loginrelated/diffrentuser.html')
    
def get_exams(request):
    grade_id = request.GET.get('grade_id')
    exams = MyModels.Exam.objects.filter(grade_id=grade_id).values('id', 'exam_name')
    return JsonResponse(list(exams), safe=False)    


# Display list of examquestion
@login_required
def examquestion_list(request):
    if str(request.session['u']) == 'teacher':
        examquestion = MyModels.ExamQuestion.objects.all().order_by('grade', 'exam')
        return render(request, 'teacher/examquestion/examquestion_list.html', {'examquestion': examquestion})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Create a new examquestion
@login_required
def examquestion_create(request):
    if str(request.session['u']) == 'teacher':
        if request.method == 'POST':
            grade = request.POST.get('grade')
            exam = request.POST.get('exam')
            question = request.POST['question']
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST['option3']
            option4 = request.POST['option4']
            answer = request.POST['answer']
            mode = MyModels.ExamQuestion.objects.create(grade_id=grade,
                                                  exam_id=exam,
                                                  question = question,
                                                  option1=option1,
                                                  option2=option2,
                                                  option3=option3,
                                                  option4=option4,
                                                  answer=answer,
                                                  marks=1
                                                  )
            mode.save()
            messages.success(request, 'ExamQuestion created successfully!')
            return redirect('examquestion_create')
        grade = MyModels.Grade.objects.filter(id__isnull=False)\
                        .values('id','grade_name')
        grade = sorted(
                            grade,
                            key=lambda x: (ROMAN_NUMERAL_MAP.get(x['grade_name'], 0))
                        )
        
        return render(request, 'teacher/examquestion/examquestion_create.html',{'grades':grade})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Update an existing examquestion
@login_required
    
def examquestion_update(request, id):
    if str(request.session['u']) == 'teacher':
        if request.method == 'POST':
            grade = request.POST.get('grade')
            exam = request.POST.get('exam')
            question = request.POST['question']
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST['option3']
            option4 = request.POST['option4']
            answer = request.POST['answer']
            
            les = get_object_or_404(MyModels.ExamQuestion, id=id)
            les.grade_id = grade
            les.exam = exam
            les.question = question
            les.option1 = option1
            les.option2 = option2
            les.option3 = option3
            les.option4 = option4
            les.answer = answer
            les.save()
            messages.success(request, 'ExamQuestion updated successfully!' if id else 'ExamQuestion created successfully!')
            return redirect('examquestion_list')

        grades = MyModels.Grade.objects.filter(id__isnull=False).values('id', 'grade_name')
        grades = sorted(grades, key=lambda x: (ROMAN_NUMERAL_MAP.get(x['grade_name'], 0)))

        les = get_object_or_404(MyModels.ExamQuestion, id=id)
        grade = les.grade_id
        exam = les.exam_id
        question = les.question
        option1 = les.option1
        option2 =  les.option2 
        option3 = les.option3 
        option4 = les.option4
        answer = les.answer
        return render(request, 'teacher/examquestion/examquestion_update.html', {
            'grades': grades,
            'grade': grade,
            'exam': exam,
            'question' :question,
            'option1': option1,
            'option2': option2,
            'option3': option3,
            'option4': option4,
            'answer': answer,
        })
    else:
        return render(request, 'loginrelated/diffrentuser.html')

# Delete a examquestion
@login_required
def examquestion_delete(request, id):
    if str(request.session['u']) == 'teacher':
        examquestion = get_object_or_404(MyModels.ExamQuestion, id=id)
        # Now delete the examquestion instance
        examquestion.delete()
        
        return redirect('examquestion_list')
    else:
        return render(request,'loginrelated/diffrentuser.html')
    