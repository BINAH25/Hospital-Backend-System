from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import *
User = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'user_type'
        ]
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'name',
            'user_type'
        ]
        extra_kwargs = {'password': {'write_only': True}}
        
class PatientDoctorAssignmentSerializer(serializers.ModelSerializer):
    patient = UserLoginSerializer()
    doctor = UserLoginSerializer()
    class Meta:
        model = PatientDoctorAssignment
        fields = ["id", "patient", "doctor", "created_at"]
        
class DoctorPatientSerializer(serializers.ModelSerializer):
    patient = UserLoginSerializer()
    class Meta:
        model = PatientDoctorAssignment
        fields = ["id", "patient", "created_at"]
        
        
class DoctorNoteSerializer(serializers.ModelSerializer):
    patient = UserLoginSerializer()
    doctor = UserLoginSerializer()
    class Meta:
        model = DoctorNote
        fields = ["id", "doctor", "patient", "note", "created_at"]

class ActionableStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionableStep
        fields = ["id", "note", "step_type", "description", "scheduled_date", "completed", "duration","frequency"]

class ReminderSerializer(serializers.ModelSerializer):
    patient = UserLoginSerializer()
    actionable_step = ActionableStepSerializer()
    class Meta:
        model = Reminder
        fields = ["id", "patient", "actionable_step", "scheduled_time", "sent"]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=254)
    
class DoctormailSerializer(serializers.Serializer):
    doctor_email = serializers.EmailField(max_length=254)
    
class NoteSerializer(serializers.Serializer):
    patient_email = serializers.EmailField(max_length=254)
    note = serializers.CharField(max_length=254)

