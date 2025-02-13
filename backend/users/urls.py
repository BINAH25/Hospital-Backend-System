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


    # path("auth/verify/", views.EmailVerificationAPI.as_view()),  
    # path("auth/logout/", views.LogOutAPI.as_view()),  
    # path("auth/change-password/", views.ChangePasswordAPI.as_view()),  
    # path("auth/reset-password/", views.ResetPasswordAPI.as_view()),  
    # path("auth/reset-password-done/", views.ResetPasswordDoneAPI.as_view()),  
    # path("auth/delete-account/", views.DeleteAccountAPI.as_view()),  
     
    
]
