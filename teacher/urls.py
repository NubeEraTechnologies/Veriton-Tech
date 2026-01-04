from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('create-student', views.create_student,name='create-student'),
    path('student-list', views.student_list,name='student-list'),
    path('student-attendance', views.student_attendance,name='student-attendance'),
    path('attendance-report-daywise/', views.attendance_reportdaywise_view, name='attendance-report-daywise'),
    path('attendance-report-monthwise/', views.attendance_reportmonthwise_view, name='attendance-report-monthwise'),
    path('teacher-attendance-report-monthwise/', views.teacher_attendance_reportmonthwise_view, name='teacher-attendance-report-monthwise'),
    path('attendance/<int:grade_id>/<int:division_id>/<str:date>/', views.attendance_details, name='attendance_details'),

    path('student-list-pending', views.student_list_pending,name='student-list-pending'),
    path('uploadstud/', views.upload_student_csv, name='upload-student-csv'),

    path('exams/', views.exam_list, name='exam_list'),
    path('exams-student-marks/<int:exam_id>/', views.exam_student_marks_list, name='exams-student-marks'),
    path('exams-student-top/<int:exam_id>/', views.exam_student_top, name='exams-student-top'),
    path('exams-student-details/<int:exam_id>/<int:student_id>/', views.exam_student_details_list, name='exams-student-details'),
    path('exams/create/', views.exam_create, name='exam_create'),
    path('exams/update/<int:id>/', views.exam_update, name='exam_update'),
    path('exams/delete/<int:id>/', views.exam_delete, name='exam_delete'),
    path('get-exams/', views.get_exams, name='get_exams'),

    path('examquestion/', views.examquestion_list, name='examquestion_list'),
    path('examquestion/create/', views.examquestion_create, name='examquestion_create'),
    path('examquestion/update/<int:id>/', views.examquestion_update, name='examquestion_update'),
    path('examquestion/delete/<int:id>/', views.examquestion_delete, name='examquestion_delete'),

    path('teacher-calender/', views.teacher_calender, name='teacher-calender'),

    path('schedulerstatus/', views.schedulerstatus_list, name='schedulerstatus_list'),
    path('schedulerstatus/create/', views.schedulerstatus_create, name='schedulerstatus_create'),
    path('schedulerstatus/delete/<int:id>/', views.schedulerstatus_delete, name='schedulerstatus_delete'),
    path('get-scheduler-status-sum/', views.get_scheduler_status_sum, name='get_scheduler_status_sum'),
   
    path('fee-setting/', views.fee_setting, name='fee-setting'),
    path('feepaid/', views.feepaid_list, name='feepaid_list'),
    path('feepaid/create/', views.feepaid_create, name='feepaid_create'),
    path('feepaid/update/<int:id>/', views.feepaid_update, name='feepaid_update'),
    path('feepaid/delete/<int:id>/', views.feepaid_delete, name='feepaid_delete'),
    path('fee-report/', views.fee_report, name='fee-report'),
    path('fee-report-details/<int:student_id>/', views.fee_report_details, name='fee-report-details'),
    

]
