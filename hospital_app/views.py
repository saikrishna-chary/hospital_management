from .forms import PatientForm, AppointmentForm, PatientPasswordResetForm, PatientRegisterForm
from .forms import UserRegisterForm, DoctorForm
from django.contrib.auth import logout

from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate

from django.urls import reverse
from django.shortcuts import  get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Doctor, Patient

# Home View
def home(request):
    return render(request, 'home.html')

# Removed register_admin function since it's no longer needed

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Attempting login - Username: {username}, Password: {password}")

        user = authenticate(request, username=username, password=password)

        if user:
            print(f"Authenticated: {user.username}, Role: {user.role}")  # Debugging print

            if user.role == 'Admin' or user.is_superuser:  # Allow superuser to login as admin
                login(request, user)
                print("Admin successfully logged in!")  # Debugging print
                return redirect('dashboard_admin')
            else:
                messages.error(request, "You are not authorized as an Admin.")
        else:
            messages.error(request, "Invalid username or password.")
            print("Authentication failed")  # Debugging print

    return render(request, 'admin_login.html')


@login_required
def admin_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')



User = get_user_model()  # ✅ Dynamically get the custom User model

def admin_forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "❌ Passwords do not match.")
            return render(request, "forgot_admin_password.html")

        try:
            # ✅ Ensure we are correctly querying the custom User model
            user = User.objects.filter(username=username, email=email).first()

            if user:
                user.set_password(new_password)  # ✅ Securely set the new password
                user.save()
                messages.success(request, "✅ Password reset successful. You can now log in.")
                return redirect("admin_login")
            else:
                messages.error(request, "❌ Invalid username or email.")

        except Exception as e:
            messages.error(request, f"❌ An error occurred: {e}")  # Debugging message
            print(f"Error resetting password: {e}")  # Log error for debugging

    return render(request, "forgot_admin_password.html")


from datetime import date
from django.utils.dateparse import parse_date


@login_required
def dashboard_admin(request):
    # Check if user is admin or superuser
    if not (request.user.role == 'Admin' or request.user.is_superuser):
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
        
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    selected_date_str = request.GET.get('date')
    selected_date = parse_date(selected_date_str) if selected_date_str else date.today()

    all_appointments = Appointment.objects.all()
    filtered_appointments = all_appointments.filter(date=selected_date)

    return render(request, 'dashboard_admin.html', {
        'doctors': doctors,
        'patients': patients,
        'appointments': filtered_appointments,  # 👈 filtered list!
        'total_doctors': doctors.count(),
        'total_appointments_on_date': filtered_appointments.count(),
        'scheduled_count': filtered_appointments.filter(status='Scheduled').count(),
        'completed_count': filtered_appointments.filter(status='Completed').count(),
        'cancelled_count': filtered_appointments.filter(status='Cancelled').count(),
        'selected_date': selected_date,
        'today': date.today(),
    })


#-----------------------------------------------------------------------------------------------------------------------



def register_doctor(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        doctor_form = DoctorForm(request.POST)

        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'Doctor'  # Set user role to Doctor
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.user = user  # Link doctor to user
            doctor.save()

            messages.success(request, "✅ Doctor registered successfully!")
            login(request, user)
            return redirect('doctor_login')  # FIXED: Redirect to correct dashboard

        else:
            messages.error(request, "❌ There were errors in the form!")
            print(f"❌ Doctor Form Errors: {doctor_form.errors.as_json()}")
            print(f"❌ User Form Errors: {user_form.errors.as_json()}")

    else:
        user_form = UserRegisterForm()
        doctor_form = DoctorForm()

    return render(request, 'register_doctor.html', {'user_form': user_form, 'doctor_form': doctor_form})


# Doctor Login View
def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and hasattr(user, 'doctor'):  # Ensuring only doctors can log in
            login(request, user)
            messages.success(request, '✅ Logged in successfully!')
            return redirect('doctor_dashboard')  # Redirecting to doctor dashboard

        else:
            messages.error(request, '❌ Invalid credentials or not a doctor!')
            return redirect('doctor_login')

    return render(request, 'doctor_login.html')



User = get_user_model()  # ✅ Correctly references 'hospital_app.User'


def doctor_forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = User.objects.get(username=username, email=email)  # Check if user exists

            if new_password == confirm_password:
                user.set_password(new_password)  # Securely set new password
                user.save()
                messages.success(request, "✅ Password reset successful. You can now log in.")
                return redirect("doctor_login")
            else:
                messages.error(request, "❌ Passwords do not match.")

        except User.DoesNotExist:
            messages.error(request, "❌ Invalid username or email.")

    return render(request, "doctor_forgot_password.html")

# Doctor Logout View
def logout_doctor(request):
    logout(request)  # This will log out the user
    return redirect('home')  # Redirect to the home page or any other page after logout



# Doctor Dashboard View
@login_required
def doctor_dashboard(request):
    if request.user.role != "Doctor":
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        messages.error(request, "Doctor profile not found.")
        return redirect('home')

    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, 'dashboard_doctor.html', {'doctor': doctor, 'appointments': appointments})


#-----------------------------------------------------------------------------------------------------------------------

def register_patient(request):
    if request.method == 'POST':
        user_form = PatientRegisterForm(request.POST)
        patient_form = PatientForm(request.POST)

        if user_form.is_valid() and patient_form.is_valid():
            # ✅ Save User with Hashed Password
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])  # Hash password
            user.save()

            # ✅ Save Patient and Link to User
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()

            # ✅ Success Message and Redirect
            messages.success(request, "✅ Registration successful! Please log in.")
            print("✅ Forms are valid. Redirecting to patient login...")  # Debugging
            return redirect('patient_login')

        else:
            # ❌ Print Errors for Debugging
            messages.error(request, "❌ There were errors in the form!")
            print(f"❌ User Form Errors: {user_form.errors.as_json()}")
            print(f"❌ Patient Form Errors: {patient_form.errors.as_json()}")

    else:
        user_form = PatientRegisterForm()
        patient_form = PatientForm()

    return render(request, 'register_patient.html', {'user_form': user_form, 'patient_form': patient_form})



def patient_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next", "patient_dashboard")  # 🔥 Default to dashboard

        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'patient'):
            login(request, user)
            messages.success(request, "✅ Login successful!")
            return redirect(next_url)  # 🔥 Redirect to Book Appointment or Dashboard
        else:
            messages.error(request, "❌ Invalid credentials or not a patient!")

    return render(request, "patient_login.html")

def patient_forgot_password(request):
    if request.method == 'POST':
        form = PatientPasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']

            try:
                user = User.objects.get(username=username, email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successfully! Please log in with your new password.")
                return redirect('patient_login')
            except User.DoesNotExist:
                messages.error(request, "Invalid username or email. Please try again.")

    else:
        form = PatientPasswordResetForm()

    return render(request, 'patient_forgot_password.html', {'form': form})
# Patient Dashboard View
@login_required
def patient_dashboard(request):
    if request.user.role != "Patient":
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')

    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, "Patient profile not found.")
        return redirect('home')

    appointments = Appointment.objects.filter(patient=patient)

    # 🔍 Debugging: Check appointment IDs and statuses
    print("Appointments:", appointments)
    for appt in appointments:
        print(f"ID: {appt.id}, Status: {appt.status}")

    return render(request, 'dashboard_patient.html', {'patient': patient, 'appointments': appointments})

# Patient Logout View
def logout_patient(request):
    logout(request)  # This will log out the user
    return redirect('home')  # Redirect to the home page or any other page after logout

#-----------------------------------------------------------------------------------------------------------------------
# Book Appointment (Only for Patients)






from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm

@login_required(login_url='patient_login')
def book_appointment(request):
    if not hasattr(request.user, 'patient'):  # ✅ Ensure only patients can book
        messages.error(request, "Only patients can book appointments.")
        return redirect('home')

    patient = request.user.patient  # ✅ Fetch patient profile
    success_message = None  # ✅ Variable to store acknowledgment message

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient  # ✅ Assign patient
            appointment.status = 'Scheduled'

            doctor = appointment.doctor
            if Appointment.objects.filter(doctor=doctor, date=appointment.date, time=appointment.time).exists():
                messages.error(request, "This doctor is already booked for the selected time.")
                return redirect('patient_dashboard')

            appointment.save()  # ✅ Save to database

            success_message = "Your booking is confirmed!"  # ✅ Set confirmation message

    else:
        form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form, 'success_message': success_message})


#------------------------------------------------------------------------------------------------------------------------

@login_required
def update_appointment(request, appointment_id, status):
    if request.user.role != "Doctor":
        return redirect('doctor_dashboard')

    try:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = status
        appointment.save()
        messages.success(request, "Appointment status updated successfully.")
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")

    return redirect('doctor_dashboard')

from .forms import AppointmentForm

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user.role != "Doctor":
        return redirect('doctor_dashboard')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully.")
            return redirect('doctor_dashboard')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'edit_appointment.html', {
        'form': form,
        'appointment': appointment  # Needed for the "Mark as Completed" button
    })





@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure only 'Completed' or 'Cancelled' appointments can be deleted
    if appointment.status in ['Completed', 'Cancelled']:
        appointment.delete()
        messages.success(request, "✅ Appointment deleted successfully.")
    else:
        messages.error(request, "❌ Only Completed or Cancelled appointments can be deleted.")

    return redirect('doctor_dashboard')  # Redirect to the doctor's dashboard