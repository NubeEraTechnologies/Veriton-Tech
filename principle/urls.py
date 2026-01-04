from django.urls import path
from principle import views

urlpatterns = [

    path('create-teacher', views.create_teacher,name='create-teacher'),
    path('teacher-list', views.teacher_list,name='teacher-list'),
    path('teacher-list-pending', views.teacher_list_pending,name='teacher-list-pending'),
    path('all-teacher-attendance-report-monthwise/', views.all_teacher_attendance_reportmonthwise_view, name='all-teacher-attendance-report-monthwise'),
   
]
