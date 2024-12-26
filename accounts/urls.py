from django.urls import path
from .views import UserRegistrationApiview, ActivateUserView, PersonalInformationView

urlpatterns = [
    path('register/', UserRegistrationApiview.as_view(), name='register'),
    path('verify/<uid>/<token>/', ActivateUserView.as_view(), name='activate-user'),
    path('personal-info/', PersonalInformationView.as_view(), name='personal_info'),
]
