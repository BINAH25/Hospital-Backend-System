from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import *
# from utils.function import *
from django.contrib.auth import get_user_model
from users.models import *
from django.conf import settings
import re
User = get_user_model()
# Create your views here.


def get_auth_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'user':UserLoginSerializer(user).data,
        # 'permission':get_all_user_permissions(user),
        'refresh': str(refresh),
        'token': str(refresh.access_token) 
    }
    
    
class SignInAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CodeEmailSerializer
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PatientDoctorAssignmentSerializer

    def post(self, request, *args, **kwargs):
        patient = request.user
        doctor_email = request.data.get("doctor_email")
        
        if patient.user_type != "Patient":
            return Response({"error": "Only patients can assign doctors."}, status=status.HTTP_403_FORBIDDEN)

        doctor = get_object_or_404(User, email=doctor_email, user_type="Doctor")

        assignment, created = PatientDoctorAssignment.objects.update_or_create(
            patient=patient, defaults={"doctor": doctor}
        )

        return Response(PatientDoctorAssignmentSerializer(assignment).data, status=status.HTTP_201_CREATED)


    
class GetDoctorPatientsAPI(generics.GenericAPIView):
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

# class SubmitDoctorNoteAPI(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = DoctorNoteSerializer

#     def post(self, request, *args, **kwargs):
#         doctor = request.user
#         patient_id = request.data.get("patient_id")
#         note = request.data.get("note")

#         if doctor.user_type != "Doctor":
#             return Response({"error": "Only doctors can submit notes."}, status=status.HTTP_403_FORBIDDEN)

#         patient = get_object_or_404(User, id=patient_id, user_type="Patient")
        
#         # Save the note
#         doctor_note = DoctorNote.objects.create(doctor=doctor, patient=patient, note=note)

#         # Extract actionable steps using an LLM (e.g., OpenAI GPT, Google Gemini)
#         extracted_steps = self.extract_actionable_steps(note)

#         # Save actionable steps
#         for step in extracted_steps:
#             ActionableStep.objects.create(
#                 patient=patient,
#                 doctor_note=doctor_note,
#                 step_type=step["step_type"],
#                 description=step["description"],
#                 schedule_date=step.get("schedule_date"),
#             )

#         return Response(DoctorNoteSerializer(doctor_note).data, status=status.HTTP_201_CREATED)

#     def extract_actionable_steps(self, note):
#         """
#         Simulating LLM Extraction of actionable steps from doctor notes.
#         You can replace this with an actual API call to OpenAI or Google Gemini.
#         """
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[{"role": "system", "content": "Extract actionable medical steps."},
#                       {"role": "user", "content": note}]
#         )

#         extracted_steps = response["choices"][0]["message"]["content"]

#         # Mock response parsing
#         return [
#             {"step_type": "checklist", "description": "Buy paracetamol"},
#             {"step_type": "plan", "description": "Take medicine daily for 7 days", "schedule_date": timezone.now() + timedelta(days=1)}
#         ]











