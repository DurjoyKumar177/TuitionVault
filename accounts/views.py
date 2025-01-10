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
from django.http import JsonResponse

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
            request.session.save()
            return JsonResponse({
                "message": "Registration successful", 
                "status": "ok", 
                "user_id": user.id
                }, status=201)  # Redirect to the personal info form
        
        else:
            print(serializer.errors)
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
        # Check if the user is authenticated, else check the session ID
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
            confirm_link = f"https://durjoykumar177.github.io/TuitionVault_Frontend/active_account.html?uid={uid}&token={token}"  # Adjust the URL path

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

    def get(self, request):
        user = request.user
        personal_info = get_object_or_404(PersonalInformation, user=user)
        serializer = self.serializer_class(personal_info)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            serializer.save(user=request.user)
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            # Generate token and UID for password reset
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Generate reset link pointing to your frontend page
            reset_link = f"https://durjoykumar177.github.io/TuitionVault_Frontend/reset_pass.html?uid={uid}&token={token}"

            # Send email with the reset link
            email_subject = "Password Reset Request"
            email_body = render_to_string('password_reset_email.html', {'reset_link': reset_link})
            email_message = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email_message.attach_alternative(email_body, 'text/html')
            email_message.send()

            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid user or token."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the new password and confirm password from the request
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password:
            return Response({"error": "Both password fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)