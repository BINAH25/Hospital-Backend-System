from django.urls import path
from users import views

app_label = "users"

urlpatterns = [
    # USER URLS
    path("", views.SignInAPI.as_view()),
    path("register/", views.RegistrationAPI.as_view()),  
    path("get/all/doctors/", views.GetAllDoctorsAPI.as_view()),
    path("assign/doctor/", views.AssignDoctorAPI.as_view()),
    path("doctor-patients/", views.GetDoctorPatientsAPI.as_view()),
    path("doctor-notes/", views.DoctorNoteAPI.as_view()),
    path("get-pationt-action-steps/", views.PatientActionableStepsAPI.as_view()),
    path("get-pationt-reminders/", views.PatientRemindersAPI.as_view()),

    
]
