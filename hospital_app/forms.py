
from .models import  Patient, Doctor, Appointment

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


#admin form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists! Please use another email.")
        return email


#admin forgot password
class AdminPasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


#------------------------------------------------------------------------------------------------------------------------
#from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient

# forms.py

# ✅ Patient User Form (Handles only user-related fields)
class PatientRegisterForm(UserCreationForm):  # No need for confirm_password
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Django's built-in password confirmation

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


# ✅ Patient Profile Form (Handles patient-specific details like gender, age, contact, etc.)
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['age', 'gender', 'contact', 'medical_history']  # ✅ Added 'contact' field

        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Number'}),  # ✅ Contact Field
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Medical History', 'rows': 3}),
        }


#patient forgot password
class PatientPasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

#-----------------------------------------------------------------------------------------------------------------------
# Doctor Form
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'schedule']
        widgets = {
            'specialization':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your  specialization'}),
            'schedule':forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Your Available Schedule Days  Ex: monday,tuesday.....'}),
            }

#-----------------------------------------------------------------------------------------------------------------------
from django import forms
from .models import Appointment, Doctor

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        empty_label="Select a Doctor",
        label="Doctor"
    )

    date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time']

# Password Reset Form
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
