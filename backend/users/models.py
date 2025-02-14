import uuid
import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from cryptography.fernet import Fernet
from users.managers import CustomUserManager

# Generate a secret key for encryption
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
cipher = Fernet(ENCRYPTION_KEY.encode())

class User(AbstractUser):
    USER_TYPES = (
        ("Doctor", "Doctor"),
        ("Patient", "Patient"),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
class PatientDoctorAssignment(models.Model):
    patient = models.OneToOneField(User, on_delete=models.CASCADE, related_name="assigned_doctor")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patients")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} → {self.doctor.name}"
    
    
class DoctorNote(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_notes")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_notes")
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_encrypted_note(self, note_text):
        self.note = cipher.encrypt(note_text.encode())

    def get_decrypted_note(self):
        return cipher.decrypt(self.note).decode()

    def __str__(self):
        return f"Note by {self.doctor.name} for {self.patient.name} on {self.created_at}"
    

    
class ActionableStep(models.Model):
    CHECKLIST = "Checklist"
    PLAN = "Plan"

    STEP_TYPES = [
        (CHECKLIST, "Checklist"),
        (PLAN, "Plan"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.ForeignKey(DoctorNote, on_delete=models.CASCADE, related_name="steps")
    frequency = models.CharField(max_length=220, null=True, blank=True)
    duration = models.CharField(max_length=200, null=True, blank=True)
    step_type = models.CharField(max_length=10, choices=STEP_TYPES)
    description = models.TextField()
    scheduled_date = models.DateTimeField(null=True, blank=True) 
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def reduce_duration_on_checkin(self):
        """Reduces duration by 1 when a patient checks in."""
        if self.step_type == "Plan" and self.duration and self.duration > 0:
            self.duration -= 1
            self.save()
            return True  
        return False  

    def __str__(self):
        return f"{self.step_type} - {self.description[:30]}"


class Reminder(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reminders")
    actionable_step = models.ForeignKey(ActionableStep, on_delete=models.CASCADE, related_name="reminders")
    scheduled_time = models.DateTimeField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder for {self.patient.email} at {self.scheduled_time}"
