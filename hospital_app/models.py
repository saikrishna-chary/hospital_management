from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User Model with Roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Patient')

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    medical_history = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)  # ✅ Add this field

    def __str__(self):
        return self.user.username

# Doctor Model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    schedule = models.TextField()

    def __str__(self):  # ✅ Show "Dr. [Name]"
        full_name = self.user.get_full_name()
        return f"Dr. {full_name}" if full_name else f"Dr. {self.user.username}"





class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Scheduled')

    def __str__(self):
        return f"{self.patient.user.username} - {self.doctor.user.username} ({self.status})"
