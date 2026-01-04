import os
from bootcampapp import models as MyModels
from django.contrib import messages
from django.core.files.storage import default_storage
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.db.models import Exists, OuterRef,Case, When, Value, IntegerField,F, Value, Q, Sum, Max
from django.db.models.functions import Coalesce
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from bootcampapp.apicalls import make_api_request,update_data,handle_api_request,create_data
ROMAN_NUMERAL_MAP = {
                        'V': 5,
                        'VI': 6,
                        'VII': 7,
                        'VIII': 8,
                        'IX': 9,
                        'X': 10,
                    }


# Display list of schools
@login_required
def school_list(request):
    if str(request.session['u']) == 'staff':
        schools = MyModels.School.objects.all()
        return render(request, 'staff/school/school_list.html', {'schools': schools})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Create a new school
@login_required
def school_create(request):
    if str(request.session['u']) == 'staff':
        if request.method == 'POST':
            school_name = request.POST.get('school_name')
            contact_person = request.POST.get('contact_person')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')

            if school_name:
                MyModels.School.objects.create(
                                                school_name=school_name,
                                                contact_person=contact_person,
                                                email=email,
                                                address=address,
                                                phone_number=phone_number
                                                )
                messages.success(request, 'School created successfully!')
                return redirect('school_create')
        return render(request, 'staff/school/school_create.html')
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Update an existing school
@login_required
def school_update(request, id):
    if str(request.session['u']) == 'staff':
        school = get_object_or_404(MyModels.School, id=id)
        if request.method == 'POST':
            school_name = request.POST.get('school_name')
            contact_person = request.POST.get('contact_person')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            if school_name:
                school.school_name = school_name
                school.contact_person = contact_person
                school.email = email
                school.address = address
                school.phone_number = phone_number
                school.save()
                return redirect('school_list')
        return render(request, 'staff/school/school_update.html', {'school': school})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Delete a school
@login_required
def school_delete(request, id):
    if str(request.session['u']) == 'staff':
        school = get_object_or_404(MyModels.School, id=id)
        school.delete()
        return redirect('school_list')
    else:
        return render(request,'loginrelated/diffrentuser.html')

  
# Display list of grades
@login_required
def grade_list(request):
    if str(request.session['u']) == 'staff':
        # Fetch grades using the decrypted password
        grades = handle_api_request(request, "grades", method="GET")
        if "error" in grades:
            return JsonResponse(grades, status=400)
        return render(request, 'staff/grade/grade_list.html', {'grades': grades})
    else:
        return render(request, 'loginrelated/diffrentuser.html')

# Create a new grade
@login_required
def grade_create(request):
    if str(request.session['u']) == 'staff':
        if request.method == "POST":
            created_data = {
                "grade_name": request.POST.get("grade_name"),
            }
            response = create_data(request, "grades", created_data)
            if "error" in response:
                return JsonResponse(response, status=400)  # Return error response
            messages.success(request, 'Grade created successfully!')
            return redirect('grade_create')
        return render(request, 'staff/grade/grade_create.html')
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Update an existing grade
@login_required
def grade_update(request, id):
    if str(request.session['u']) == 'staff':
        if request.method == "POST":
            updated_data = {
                "grade_name": request.POST.get("grade_name"),
            }
            response = update_data(request, "grades", id, updated_data)
            if "error" in response:
                return JsonResponse(response, status=400)  # Return error response
            return redirect('grade_list')
        grade = handle_api_request(request, "grades", method="GET", object_id=id)
        return render(request, 'staff/grade/grade_update.html', {'grade': grade})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Delete a grade
@login_required
def grade_delete(request, id):
    if str(request.session['u']) == 'staff':
        grade = get_object_or_404(MyModels.Grade, id=id)
        grade.delete()
        return redirect('grade_list')
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Display list of divisions
@login_required
def division_list(request):
    if str(request.session['u']) == 'staff':
        divisions = MyModels.Division.objects.all()
        return render(request, 'staff/division/division_list.html', {'divisions': divisions})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Create a new division
@login_required
def division_create(request):
    if str(request.session['u']) == 'staff':
        if request.method == 'POST':
            division_name = request.POST.get('division_name')
            if division_name:
                MyModels.Division.objects.create(division_name=division_name)
                messages.success(request, 'Division created successfully!')
                return redirect('division_create')
        return render(request, 'staff/division/division_create.html')
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Update an existing division
@login_required
    
def division_update(request, id):
    if str(request.session['u']) == 'staff':
        division = get_object_or_404(MyModels.Division, id=id)
        if request.method == 'POST':
            division_name = request.POST.get('division_name')
            if division_name:
                division.division_name = division_name
                division.save()
                return redirect('division_list')
        return render(request, 'staff/division/division_update.html', {'division': division})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Delete a division
@login_required
def division_delete(request, id):
    if str(request.session['u']) == 'staff':
        division = get_object_or_404(MyModels.Division, id=id)
        division.delete()
        return redirect('division_list')
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Display list of modules
@login_required
def module_list(request):
    if str(request.session['u']) == 'staff':
        modules = MyModels.Module.objects.all()
        return render(request, 'staff/module/module_list.html', {'modules': modules})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Create a new module
@login_required
def module_create(request):
    if str(request.session['u']) == 'staff':
        if request.method == 'POST':
            grade = request.POST.get('grade')
            module_name = request.POST['module_name']
            description = request.POST['description']
            module_pic = request.FILES.get('module_pic')  # Fetch the file if uploaded
            if module_name:
                mode = MyModels.Module.objects.create(grade_id=grade,module_name=module_name,description=description)

                if module_pic:
                    # Generate the custom file name: username_userid.extension
                    file_extension = os.path.splitext(module_pic.name)[1]  # Get the file extension
                    new_file_name = f"{mode.module_name}_{mode.id}_{grade}{file_extension}"
                    
                    # Define the path where the file will be saved
                    file_path = mode.module_pic.storage.path(new_file_name)
                    
                    # Check if a file with the same name exists and delete it
                    if default_storage.exists(new_file_name):
                        default_storage.delete(new_file_name)

                    # Save the new profile pic with the new file name
                    mode.module_pic.save(new_file_name, module_pic)
                mode.save()
                messages.success(request, 'Module created successfully!')
                return redirect('module_create')
        grade = MyModels.Grade.objects.filter(id__isnull=False)\
                        .values('id','grade_name')
        grade = sorted(
                            grade,
                            key=lambda x: (ROMAN_NUMERAL_MAP.get(x['grade_name'], 0))
                        )
        return render(request, 'staff/module/module_create.html',{'grades':grade})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Update an existing module
@login_required
    
def module_update(request, id):
    if str(request.session['u']) == 'staff':
        if request.method == 'POST':
            grade = request.POST.get('grade')
            module_name = request.POST['module_name']
            description = request.POST['description']
            module_pic = request.FILES.get('module_pic')  # Fetch the file if uploaded

            
            mode = get_object_or_404(MyModels.Module, id=id)
            mode.grade_id = grade
            mode.module_name = module_name
            mode.description = description
            
            if module_pic:
                # Generate the custom file name: username_userid.extension
                file_extension = os.path.splitext(module_pic.name)[1]  # Get the file extension
                new_file_name = f"{mode.module_name}_{mode.id}_{grade}{file_extension}"
                
                # Define the path where the file will be saved
                file_path = mode.module_pic.storage.path(new_file_name)
                
                # Check if a file with the same name exists and delete it
                if default_storage.exists(new_file_name):
                    default_storage.delete(new_file_name)

                # Save the new profile pic with the new file name
                mode.module_pic.save(new_file_name, module_pic)
            mode.save()
            messages.success(request, 'Module updated successfully!' if id else 'Module created successfully!')
            return redirect('module_list')

        # Load the module details if updating
        module = None
        module = get_object_or_404(MyModels.Module, id=id)

        grades = MyModels.Grade.objects.filter(id__isnull=False).values('id', 'grade_name')
        grades = sorted(grades, key=lambda x: (ROMAN_NUMERAL_MAP.get(x['grade_name'], 0)))

        return render(request, 'staff/module/module_update.html', {
            'grades': grades,
            'module': module,
        })
    else:
        return render(request, 'loginrelated/diffrentuser.html')

# Delete a module
@login_required
def module_delete(request, id):
    if str(request.session['u']) == 'staff':
        module = get_object_or_404(MyModels.Module, id=id)
        
        # Check if there is a module_pic and delete the file if it exists
        if module.module_pic:
            # Construct the full file path
            file_path = os.path.join(settings.MEDIA_ROOT, str(module.module_pic))
            
            # Delete the file if it exists
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        # Now delete the module instance
        module.delete()
        
        return redirect('module_list')
    else:
        return render(request,'loginrelated/diffrentuser.html')
    
def get_modules(request):
    grade_id = request.GET.get('grade_id')
    modules = MyModels.Module.objects.filter(grade_id=grade_id).values('id', 'module_name')
    return JsonResponse(list(modules), safe=False)

# Display list of lessons
@login_required
def lesson_list(request):
    if str(request.session['u']) == 'staff':
        lessons = MyModels.Lesson.objects.all().order_by('grade', 'module', 'serialno')
        return render(request, 'staff/lesson/lesson_list.html', {'lessons': lessons})
    else:
        return render(request,'loginrelated/diffrentuser.html')

@login_required
@csrf_exempt  # Temporarily allowing POST without CSRF token for simplicity
def update_lesson_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Group lessons by grade and module
            lessons_by_grade_module = {}

            for item in data['order']:
                grade_id = item['grade']   # Capture the grade ID
                module_id = item['module']  # Capture the module ID
                heading = item['heading']   # Capture the heading
                new_position = item['new_position']  # New position after drag-and-drop

                key = f'{grade_id}-{module_id}'

                if key not in lessons_by_grade_module:
                    lessons_by_grade_module[key] = []

                # Append the current lesson info
                lessons_by_grade_module[key].append((heading, new_position))

            # Update serialno for each group of lessons based on heading
            for key, lessons in lessons_by_grade_module.items():
                grade_id, module_id = key.split('-')

                # Update each lesson based on new position
                for heading, new_position in lessons:
                    # Fetch the lesson object by grade, module, and heading
                    lesson_obj = MyModels.Lesson.objects.get(
                        grade__id=grade_id,
                        module__id=module_id,
                        heading=heading
                    )
                    # Update the serial number
                    lesson_obj.serialno = new_position
                    lesson_obj.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def lesson_preview(request, id):
    if str(request.session['u']) == 'staff':
        les = get_object_or_404(MyModels.Lesson, id=id)
        grade = les.grade_id
        module = les.module_id
        heading = les.heading
        about =  les.about 
        reqmaterial = les.reqmaterial 
        digram = les.digram
        code = les.code
        process = les.process
        get = les.get
        video = les.video
        return render(request, 'staff/lesson/lesson_preview.html', {
            'grade': grade,
            'module': module,
            'heading': heading,
            'about': about,
            'reqmaterial': reqmaterial,
            'digram': digram,
            'code': code,
            'process': process,
            'get': get,
            'video': video,
        })
    else:
        return render(request, 'loginrelated/diffrentuser.html')

# Create a new lesson
@login_required
def lesson_create(request):
    if str(request.session['u']) == 'staff':
        if request.method == 'POST':
            grade = request.POST.get('grade')
            module = request.POST.get('module')
            serialno = request.POST['serialno']
            mints = request.POST['mints']
            heading = request.POST['heading']
            about = request.POST['about']
            reqmaterial = request.POST['reqmaterial']
            digram = request.POST['digram']
            code = request.POST['code']
            process = request.POST['process']
            get = request.POST['get']
            video = request.POST['video']
            mode = MyModels.Lesson.objects.create(grade_id=grade,
                                                  module_id=module,
                                                  serialno = serialno,
                                                  mints=mints,
                                                  heading=heading,
                                                  about=about,
                                                  reqmaterial=reqmaterial,
                                                  digram=digram,
                                                  code=code,
                                                  process=process,
                                                  get=get,
                                                  video=video
                                                  )
            mode.save()
            messages.success(request, 'Lesson created successfully!')
            return redirect('lesson_create')
        grade = MyModels.Grade.objects.filter(id__isnull=False)\
                        .values('id','grade_name')
        grade = sorted(
                            grade,
                            key=lambda x: (ROMAN_NUMERAL_MAP.get(x['grade_name'], 0))
                        )
        
        return render(request, 'staff/lesson/lesson_create.html',{'grades':grade})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Update an existing lesson
@login_required
    
def lesson_update(request, id):
    if str(request.session['u']) == 'staff':
        if request.method == 'POST':
            grade = request.POST.get('grade')
            module = request.POST.get('module')
            serialno = request.POST['serialno']
            mints = request.POST['mints']
            heading = request.POST['heading']
            about = request.POST['about']
            reqmaterial = request.POST['reqmaterial']
            digram = request.POST['digram']
            code = request.POST['code']
            process = request.POST['process']
            get = request.POST['get']
            video = request.POST['video']
            
            les = get_object_or_404(MyModels.Lesson, id=id)
            les.grade_id = grade
            les.module = module
            les.serialno = serialno
            les.mints = mints
            les.heading = heading
            les.about = about
            les.reqmaterial = reqmaterial
            les.digram = digram
            les.code = code
            les.process = process
            les.get = get
            les.video = video
            les.save()
            messages.success(request, 'Lesson updated successfully!' if id else 'Lesson created successfully!')
            return redirect('lesson_list')

        grades = MyModels.Grade.objects.filter(id__isnull=False).values('id', 'grade_name')
        grades = sorted(grades, key=lambda x: (ROMAN_NUMERAL_MAP.get(x['grade_name'], 0)))

        les = get_object_or_404(MyModels.Lesson, id=id)
        grade = les.grade_id
        module = les.module_id
        serialno = les.serialno
        mints = les.mints
        heading = les.heading
        about =  les.about 
        reqmaterial = les.reqmaterial 
        digram = les.digram
        code = les.code
        process = les.process
        get = les.get
        video = les.video
        return render(request, 'staff/lesson/lesson_update.html', {
            'grades': grades,
            'grade': grade,
            'module': module,
            'serialno' :serialno,
            'mints': mints,
            'heading': heading,
            'about': about,
            'reqmaterial': reqmaterial,
            'digram': digram,
            'code': code,
            'process': process,
            'get': get,
            'video': video,
        })
    else:
        return render(request, 'loginrelated/diffrentuser.html')

# Delete a lesson
@login_required
def lesson_delete(request, id):
    if str(request.session['u']) == 'staff':
        lesson = get_object_or_404(MyModels.Lesson, id=id)
        # Now delete the lesson instance
        lesson.delete()
        
        return redirect('lesson_list')
    else:
        return render(request,'loginrelated/diffrentuser.html')


# Display list of modulequestion
@login_required
def modulequestion_list(request):
    if str(request.session['u']) == 'staff':
        modulequestion = MyModels.ModuleQuestion.objects.all().order_by('grade', 'module')
        return render(request, 'staff/modulequestion/modulequestion_list.html', {'modulequestion': modulequestion})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Create a new modulequestion
@login_required
def modulequestion_create(request):
    if str(request.session['u']) == 'staff':
        if request.method == 'POST':
            grade = request.POST.get('grade')
            module = request.POST.get('module')
            question = request.POST['question']
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST['option3']
            option4 = request.POST['option4']
            answer = request.POST['answer']
            mode = MyModels.ModuleQuestion.objects.create(grade_id=grade,
                                                  module_id=module,
                                                  question = question,
                                                  option1=option1,
                                                  option2=option2,
                                                  option3=option3,
                                                  option4=option4,
                                                  answer=answer,
                                                  marks=1
                                                  )
            mode.save()
            messages.success(request, 'ModuleQuestion created successfully!')
            return redirect('modulequestion_create')
        grade = MyModels.Grade.objects.filter(id__isnull=False)\
                        .values('id','grade_name')
        grade = sorted(
                            grade,
                            key=lambda x: (ROMAN_NUMERAL_MAP.get(x['grade_name'], 0))
                        )
        
        return render(request, 'staff/modulequestion/modulequestion_create.html',{'grades':grade})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Update an existing modulequestion
@login_required
    
def modulequestion_update(request, id):
    if str(request.session['u']) == 'staff':
        if request.method == 'POST':
            grade = request.POST.get('grade')
            module = request.POST.get('module')
            question = request.POST['question']
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST['option3']
            option4 = request.POST['option4']
            answer = request.POST['answer']
            
            les = get_object_or_404(MyModels.ModuleQuestion, id=id)
            les.grade_id = grade
            les.module = module
            les.question = question
            les.option1 = option1
            les.option2 = option2
            les.option3 = option3
            les.option4 = option4
            les.answer = answer
            les.save()
            messages.success(request, 'ModuleQuestion updated successfully!' if id else 'ModuleQuestion created successfully!')
            return redirect('modulequestion_list')

        grades = MyModels.Grade.objects.filter(id__isnull=False).values('id', 'grade_name')
        grades = sorted(grades, key=lambda x: (ROMAN_NUMERAL_MAP.get(x['grade_name'], 0)))

        les = get_object_or_404(MyModels.ModuleQuestion, id=id)
        grade = les.grade_id
        module = les.module_id
        question = les.question
        option1 = les.option1
        option2 =  les.option2 
        option3 = les.option3 
        option4 = les.option4
        answer = les.answer
        return render(request, 'staff/modulequestion/modulequestion_update.html', {
            'grades': grades,
            'grade': grade,
            'module': module,
            'question' :question,
            'option1': option1,
            'option2': option2,
            'option3': option3,
            'option4': option4,
            'answer': answer,
        })
    else:
        return render(request, 'loginrelated/diffrentuser.html')

# Delete a modulequestion
@login_required
def modulequestion_delete(request, id):
    if str(request.session['u']) == 'staff':
        modulequestion = get_object_or_404(MyModels.ModuleQuestion, id=id)
        # Now delete the modulequestion instance
        modulequestion.delete()
        
        return redirect('modulequestion_list')
    else:
        return render(request,'loginrelated/diffrentuser.html')


# Create Scheduler
@login_required
def create_scheduler(request):
    if request.method == 'POST':
        school_id = request.POST.get('school')
        teacher_id = request.POST.get('teacher')
        grade_id = request.POST.get('grade')
        division_id = request.POST.get('division')
        module_id = request.POST.get('module')
        lesson_id = request.POST.get('lesson')
        start = request.POST.get('start')
        end = request.POST.get('end')
        all_day = request.POST.get('all_day') == 'on'

        scheduler = MyModels.Scheduler(
            school=MyModels.School.objects.get(id=school_id),
            teacher=MyModels.User.objects.get(id=teacher_id),
            grade=MyModels.Grade.objects.get(id=grade_id),
            division=MyModels.Division.objects.get(id=division_id),
            module=MyModels.Module.objects.get(id=module_id),
            lesson=MyModels.Lesson.objects.get(id=lesson_id),
            start=start,
            end=end,
            all_day=all_day
        )
        scheduler.save()
        return redirect('scheduler_list')
    
    schools = MyModels.School.objects.all()
    grades = MyModels.Grade.objects.all()
    return render(request, 'staff/scheduler/create_scheduler.html', {'schools': schools,'grades': grades})


@login_required
def update_scheduler(request, scheduler_id):
    # Get the Scheduler object to be updated
    scheduler = get_object_or_404(MyModels.Scheduler, id=scheduler_id)
    
    if request.method == "POST":
        # Process the form data
        school_id = request.POST.get('school')
        teacher_id = request.POST.get('teacher')
        grade_id = request.POST.get('grade')
        division_id = request.POST.get('division')
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')
        all_day = 'all_day' in request.POST
        
        # Update the scheduler instance
        scheduler.school = MyModels.School.objects.get(id=school_id)
        scheduler.teacher = MyModels.User.objects.get(id=teacher_id)
        scheduler.grade = MyModels.Grade.objects.get(id=grade_id)
        scheduler.division = MyModels.Division.objects.get(id=division_id)
        scheduler.title = title
        scheduler.start = start
        scheduler.end = end if end else None
        scheduler.all_day = all_day
        
        scheduler.save()
        
        messages.success(request, 'Scheduler updated successfully!')
        return redirect('scheduler_list')  # Redirect to the scheduler list or another page as needed

    else:
        # GET request: Fetch data for the form
        schools = MyModels.School.objects.all()
        teachers = MyModels.User.objects.filter(school=scheduler.school)  # Assuming a user (teacher) is linked to a school
        grades = MyModels.Grade.objects.all()
        divisions = MyModels.Division.objects.all()

        # Return the form with current scheduler data
        context = {
            'scheduler': scheduler,
            'schools': schools,
            'teachers': teachers,
            'grades': grades,
            'divisions': divisions,
        }
        return render(request, 'staff/scheduler/update_scheduler.html', context)
    
# List all Schedulers
@login_required
def scheduler_list(request):
    schedulers = MyModels.Scheduler.objects.all()
    return render(request, 'staff/scheduler/scheduler_list.html', {'schedulers': schedulers})


# List scheduler_calender
@login_required
def scheduler_calender(request):
    # Get schedulers for the logged-in teacher and use Coalesce to replace None with 0 for status_sum
    schedulers = MyModels.Scheduler.objects.annotate(
        status_sum=Coalesce(Sum('schedulerstatus__status'), Value(0)),
        completion_date=Case(
            When(status_sum__gte=100, then=Max('schedulerstatus__date')),
            default=Value(None),
        )
    )
    return render(request, 'staff/scheduler/scheduler_calender.html', {'schedulers': schedulers})

# Get Teachers based on selected School
@login_required
def get_teachers(request, school_id):
    teachers = MyModels.User.objects.filter(school_id=school_id, utype='teacher')
    return JsonResponse([{'id': teacher.id, 'name': teacher.first_name + ' ' + teacher.last_name} for teacher in teachers], safe=False)

# Get Divisions based on selected Grade
@login_required
def get_divisions(request, grade_id):
    divisions = MyModels.Division.objects.all()  # Adjust logic if needed
    return JsonResponse([{'id': division.id, 'name': division.division_name} for division in divisions], safe=False)

# Get Module based on selected Grade
@login_required
def get_modulesbygrade(request, grade_id):
    modules = MyModels.Module.objects.all().filter(grade_id=grade_id)  # Adjust logic if needed
    return JsonResponse([{'id': module.id, 'name': module.module_name} for module in modules], safe=False)

# Get Lesson based on selected Grade and Module
@login_required
def get_lessons(request, module_id):
    lessons = MyModels.Lesson.objects.all().filter(module_id=module_id)  # Adjust logic if needed
    return JsonResponse([{'id': lesson.id, 'name': lesson.heading} for lesson in lessons], safe=False)

# Delete Scheduler
@login_required
def delete_scheduler(request, scheduler_id):
    scheduler = get_object_or_404(MyModels.Scheduler, id=scheduler_id)
    scheduler.delete()
    return redirect('scheduler_list')    
