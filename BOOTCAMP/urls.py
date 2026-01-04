from django.urls import path,include
from django.contrib import admin
from bootcampapp import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-dashboard', views.user_dashboard_view,name='user-dashboard'),
    path('validate-old-password/', views.validate_old_password, name='validate_old_password'),
    path('check-username/', views.check_username, name='check_username'),
    path('signup/', views.signup, name='signup'),
    path('create-principle/', views.create_principle, name='create-principle'),
    path('create-staff/', views.create_staff, name='create-staff'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('switch-user', views.switch_user_view,name='switch-user'),
    path('reset-user/<int:pk>', views.reset_user_view,name='reset-user'),

    path("", views.home, name='home'),

    path('staff/',include('staff.urls')), 
    path('principle/',include('principle.urls')), 
    path('teacher/',include('teacher.urls')), 
    path('student/',include('student.urls')), 
    
    path('indexpage/', views.afterlogin_view,name='indexpage'),   
    path('user-profile/', views.user_profile,name='user-profile'),   
    path('user-password/', views.user_password,name='user-password'),   
    path('user-session-expired', views.session_expire_view,name='user-session-expired'),
    path('admin-view-user-log-details/<int:user_id>', views.admin_view_user_log_details_view,name='admin-view-user-log-details'),
    path('admin-view-user-activity-details/<int:user_id>', views.admin_view_user_activity_details_view,name='admin-view-user-activity-details'),
    path('admin-view-user-list', views.admin_view_user_list_view,name='admin-view-user-list'),
    path('admin-view-user-list-school', views.admin_view_user_list_school_view,name='admin-view-user-list-school'),
    path('update-user/<int:pk>', views.update_user_view,name='update-user'),
    path('active-user/<int:pk>', views.active_user_view,name='active-user'),
    path('delete-user/<userid>/<int:pk>', views.delete_user_view,name='delete-user'),
    
    path('userlogin/', views.user_login,name='userlogin'),
    path('register', LoginView.as_view(template_name='loginrelated/register.html'),name='register'),
    path('user-change-password', views.user_change_password_view,name='user-change-password'),
    path('reset-user/<int:user_id>/', views.reset_user_password,name='reset-user'),

    
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
    