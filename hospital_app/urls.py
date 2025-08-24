from .views import home, book_appointment, update_appointment, delete_appointment

from django.urls import path
from .views import admin_login, admin_logout, dashboard_admin,admin_forgot_password
from .views import doctor_forgot_password,doctor_login,register_doctor,doctor_dashboard,logout_doctor
from .views import patient_dashboard,register_patient,patient_login,patient_forgot_password,edit_appointment,logout_patient


urlpatterns = [
    path('', home, name='home'),  # Homepage
   # book appointment urls link
    path('patient-login/', patient_login, name='patient_login'),  # Custom login page
    path('book-appointment/', book_appointment, name='book_appointment'),

   #patient urls links
    path('register/patient/', register_patient, name='register_patient'),  # Patient registration form
    path('login/patient/', patient_login, name='patient_login'),
    path('patient/logout/', logout_patient, name='logout_patient'),

    path('patient-dashboard/', patient_dashboard, name='patient_dashboard'),
    path('patient/forgot-password/', patient_forgot_password, name='patient_forgot_password'),

    #doctor urls links
    path('register/doctor/', register_doctor, name='register_doctor'),  # Doctor registration form
    path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('login/doctor/', doctor_login, name='doctor_login'),
    path('doctor/logout/', logout_doctor, name='logout_doctor'),
    path('doctor/forgot-password/', doctor_forgot_password, name='doctor_forgot_password'),

    path('update-appointment/<int:appointment_id>/<str:status>/', update_appointment, name='update_appointment'),
    path('delete_appointment/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
    path('appointment/update/<int:appointment_id>/', edit_appointment, name='edit_appointment'),



    #admin urls links
    path('admin-login/', admin_login, name='admin_login'),
    path('logout/', admin_logout, name='admin_logout'),
    path('forgot-password/', admin_forgot_password, name='forgot_admin_password'),
    path('dashboard_admin/', dashboard_admin, name='dashboard_admin'),

]
