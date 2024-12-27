from django.urls import path, include
from rest_framework import routers
from accounts import views
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationApiview, ActivateUserView, PersonalInformationView

router = DefaultRouter()
router.register('list', views.accountsViewset)

urlpatterns = [
    path('', include(router.urls)), 
    path('login/', views.UserLoginApiview.as_view(), name='login'),
    path('logout/', views.UserLogoutApiview.as_view(), name='logout'),
    path('register/', UserRegistrationApiview.as_view(), name='register'),
    path('verify/<uid>/<token>/', ActivateUserView.as_view(), name='activate-user'),
    path('personal-info/', PersonalInformationView.as_view(), name='personal_info'),
]
