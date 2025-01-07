from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts import views

router = DefaultRouter()
router.register('list', views.accountsViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginApiview.as_view(), name='login'),
    path('logout/', views.UserLogoutApiview.as_view(), name='logout'),
    path('register/', views.UserRegistrationApiview.as_view(), name='register'),
    path('verify/<uid>/<token>/', views.ActivateUserView.as_view(), name='activate-user'),
    path('personal-info/', views.PersonalInformationView.as_view(), name='personal_info'),

    # User profile related paths
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', views.UpdateUserProfileView.as_view(), name='update-profile'),

    # Change password and Forgot password paths
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<uid>/<token>/', views.ResetPasswordView.as_view(), name='reset-password'),
]
