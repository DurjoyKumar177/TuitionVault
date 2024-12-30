from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import PersonalInformation
from .serializers import RegistrationSerializer, PersonalInformationSerializer,ProfileSerializer, PasswordChangeSerializer, ForgotPasswordSerializer,UserSerializer
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from . import serializers
from . import models
from rest_framework import viewsets

class accountsViewset(viewsets.ModelViewSet):
    queryset = models.PersonalInformation.objects.all()
    serializer_class = serializers.UserSerializer

class UserRegistrationApiview(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()  # Save user and get the instance
            request.session["temp_user_id"] = user.id  # Store user ID in the session
            return redirect('personal_info')  # Redirect to the personal info form

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateUserView(APIView):
    def get(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = get_object_or_404(User, pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)

class PersonalInformationView(APIView):
    serializer_class = PersonalInformationSerializer

    def post(self, request):
        user = None
        if request.user.is_authenticated:
            user = request.user
        elif request.session.get("temp_user_id"):
            user = get_object_or_404(User, id=request.session["temp_user_id"])

        if not user:
            return Response({"message": "Unauthorized."}, status=status.HTTP_401_UNAUTHORIZED)

        # Pass user in the context for serializer
        serializer = self.serializer_class(data=request.data, context={'request': request, 'user': user})

        if serializer.is_valid():
            # Save the personal information for the user
            serializer.save()

            # Send confirmation email to activate the account
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))  # User's unique ID
            confirm_link = f"http://localhost:8000/accounts/verify/{uid}/{token}"  # Adjust the URL path

            email_subject = "Please activate your account"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()

            # Remove temporary user ID from session
            if request.session.get("temp_user_id"):
                del request.session["temp_user_id"]

            return Response({"message": "Personal information saved and verification email sent."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginApiview(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password) #user authenticate function to verify username and password is currect or not
            
            if user :
                token,_ = Token.objects.get_or_create(user=user) #get_or_create function token thakle nibe ar na thakle create kore dibe. akhane create token er janno _ user kora hoice.
                login(request, user)
                return Response({'token':token.key, 'user_id':user.id})
            else:
                return Response({'error': 'Invalid credentials'})
        return Response(serializer.errors)
    
    
class UserLogoutApiview(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        personal_info = get_object_or_404(PersonalInformation, user=user)
        serializer = UserSerializer(personal_info)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def put(self, request):
        user = request.user
        personal_info = get_object_or_404(PersonalInformation, user=user)

        # Pass user data to the serializer to ensure we update the right record
        serializer = self.serializer_class(personal_info, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            # Generate token and send email for password reset
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://localhost:8000/accounts/reset-password/{uid}/{token}/"
            
            # Send email with the reset link
            email_subject = "Password Reset"
            email_body = render_to_string('password_reset_email.html', {'reset_link': reset_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
