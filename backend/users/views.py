from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import *
from users.utils import *
from django.contrib.auth import get_user_model
from users.models import *
from django.conf import settings
import re
from datetime import timedelta
from django.utils import timezone
from users.tasks import *
User = get_user_model()
# Create your views here.


def get_auth_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'user':UserLoginSerializer(user).data,
        'refresh': str(refresh),
        'token': str(refresh.access_token) 
    }
    
    
class SignInAPI(generics.GenericAPIView):
    """
    authenticate and login the user.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    def post(self, request,*args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            email = serializers.data["email"]
            password = serializers.data["password"]
            if User.objects.filter(email=email): 
                user = authenticate(email=email,password=password)
                if not user:
                    response_data = {'message':'Invalid Credential'}
                    return Response(response_data, status=400)
                
                user_data = get_auth_for_user(user)
                return Response(user_data, status=200)
            else:
                return Response(
                    {
                        "status": "error",
                        "detail": "User Not Found",
                    },
                    status=404,
                )
        else:
            return Response(
                {"status": "failure", "detail": serializers.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
class RegistrationAPI(generics.GenericAPIView):
    """" Validate  and register the user"""
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
    def post(self, request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            name = serializer.validated_data["name"]
            user_type = serializer.validated_data["user_type"]
            
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return Response(
                    {"status": "failure", "detail": "Invalid email address format"},
                    status=400,
                )
            
            user = User.objects.create_user(username=email, email=email, password=password,name=name,user_type=user_type)
            user.save()
            user_data = get_auth_for_user(user)
            return Response(user_data, status=200) 
            
        else:
            return Response(
                {"status": "failure", "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
            
class GetAllDoctorsAPI(generics.GenericAPIView):
    """ Get all doctors """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserRegistrationSerializer

    def get(self, request,*args, **kwargs):
        doctors = User.objects.filter(user_type="Doctor").all()
        serializers = self.serializer_class(doctors,many=True)
        return Response(
            {"status": "success", "success_message": serializers.data},
            status=200
        )       
        

class AssignDoctorAPI(generics.GenericAPIView):
    """ Assign A Patient to a Doctor"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DoctormailSerializer

    def post(self, request, *args, **kwargs):
        patient = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            doctor_email = serializers.data["doctor_email"]
        
            if patient.user_type != "Patient":
                return Response({"error": "Only patients can assign doctors."}, status=status.HTTP_403_FORBIDDEN)

            doctor = get_object_or_404(User, email=doctor_email, user_type="Doctor")

            assignment, created = PatientDoctorAssignment.objects.update_or_create(
                patient=patient, defaults={"doctor": doctor}
            )

            return Response(PatientDoctorAssignmentSerializer(assignment).data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"status": "failure", "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    
class GetDoctorPatientsAPI(generics.GenericAPIView):
    """ Get All Patients of a Doctor"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DoctorPatientSerializer

    def get(self, request,*args, **kwargs):
        user = self.request.user
        if user.user_type != "Doctor":
            return PatientDoctorAssignment.objects.none()
        
        patients = PatientDoctorAssignment.objects.filter(doctor=user)
        serializers = self.serializer_class(patients,many=True)
        return Response(
            {"status": "success", "success_message": serializers.data},
            status=200
        )       

class DoctorNoteAPI(generics.GenericAPIView):
    """ For Submitting doctor notes and processing actionable steps."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NoteSerializer

    def post(self, request, *args, **kwargs):
        doctor = request.user

        if doctor.user_type != "Doctor":
            return Response({"error": "Only doctors can submit notes."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            patient_email = serializers.data["patient_email"]
            note_text = serializers.data["note"]


            patient = get_object_or_404(User, email=patient_email, user_type="Patient")

            # Encrypt and save the note
            note = DoctorNote.objects.create(doctor=doctor, patient=patient)
            note.set_encrypted_note(note_text)
            note.save()

            # Cancel existing actionable steps
            ActionableStep.objects.filter(note__patient=patient).delete()

            checklist, plan = extract_actionable_steps(note_text)

            # Save Checklist Tasks (Immediate One-Time Actions)
            for task in checklist:
                ActionableStep.objects.create(note=note, step_type="Checklist", description=task)

            # Process Plan Tasks (Scheduled Actions) using the helper function
            if plan:
                process_plan_steps(note, plan)

            return Response(DoctorNoteSerializer(note).data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(
                {"status": "failure", "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    
class PatientActionableStepsAPI(generics.GenericAPIView):
    """For Retrieving actionable steps of Patients"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActionableStepSerializer

    def get(self, request, *args, **kwargs):
        patient = request.user
        if patient.user_type != "Patient":
            return Response({"error": "Only patients can access this."}, status=status.HTTP_403_FORBIDDEN)

        steps = ActionableStep.objects.filter(note__patient=patient, completed=False)
        return Response(ActionableStepSerializer(steps, many=True).data, status=status.HTTP_200_OK)
    
    
class PatientRemindersAPI(generics.GenericAPIView):
    """ For Getting Patients reminders"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        patient = request.user
        if patient.user_type != "Patient":
            return Response({"error": "Only patients can view reminders."}, status=status.HTTP_403_FORBIDDEN)

        reminders = get_upcoming_reminders(patient)
        return Response(ReminderSerializer(reminders, many=True).data, status=status.HTTP_200_OK)


class PatientCheckInAPI(generics.GenericAPIView):
    """ Reduce the dynamic schedules plan"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        patient = request.user

        if patient.user_type != "Patient":
            return Response({"error": "Only patients can check in."}, status=status.HTTP_403_FORBIDDEN)

        steps = ActionableStep.objects.filter(note__patient=patient, step_type="Plan")

        updated_steps = []
        for step in steps:
            if step.reduce_duration_on_checkin():  
                updated_steps.append(step.description)

        if updated_steps:
            return Response({"message": "Check-in successful. Updated steps:", "steps": updated_steps}, status=status.HTTP_200_OK)
        return Response({"message": "Check-in successful. No steps updated."}, status=status.HTTP_200_OK)
