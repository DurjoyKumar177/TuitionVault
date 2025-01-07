from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import PersonalInformation
import re 
from . import models

class UserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.PersonalInformation
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    conform_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'conform_password']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        conform_password = self.validated_data['conform_password']

        # Validate password match
        if password != conform_password:
            raise serializers.ValidationError({'error': 'Password does not match'})

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})

        # Create new user instance but don't activate it yet
        account = User(username=username, email=email, first_name=first_name, last_name=last_name)
        account.set_password(password)
        account.is_active = False  # Account is inactive until confirmed
        account.save()
        return account

class PersonalInformationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PersonalInformation
        fields = [
            'user', 'phone_number_1', 'phone_number_2', 'date_of_birth',
            'address', 'achieved_degree', 'running_degree',
            'current_organization', 'degree_certificate', 'personal_photo'
        ]

    def validate_phone_number_1(self, value):
        # Check if phone number 1 is in the correct format (e.g., only digits and 10-15 characters long)
        if PersonalInformation.objects.filter(phone_number_1=value).exists():
            raise serializers.ValidationError("Phone number 1 already exists.")
        return value

    def validate_phone_number_2(self, value):
        # Optional phone number, so we don't need to enforce any format if it's not provided
        if PersonalInformation.objects.filter(phone_number_2=value).exists():
            raise serializers.ValidationError("Phone number 2 already exists.")
        return value

    def validate_date_of_birth(self, value):
        # Example: Ensure the user is at least 18 years old
        from datetime import date
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("You must be at least 18 years old.")
        return value

    def validate_address(self, value):
        # Example: Ensure the address is not too short
        if len(value) < 10:
            raise serializers.ValidationError("Address must be at least 10 characters long.")
        return value

    def validate_achieved_degree(self, value):
        # Example: Ensure the achieved degree is not empty
        if not value:
            raise serializers.ValidationError("Achieved degree cannot be empty.")
        return value

    def save(self):
        user = self.context['user']  # User comes from the context
        if not user:
            raise serializers.ValidationError("No user found.")
        
        # Creating PersonalInformation instance and saving
        personal_info = PersonalInformation(
            user=user,
            phone_number_1=self.validated_data['phone_number_1'],
            phone_number_2=self.validated_data.get('phone_number_2'),
            date_of_birth=self.validated_data['date_of_birth'],
            address=self.validated_data['address'],
            achieved_degree=self.validated_data['achieved_degree'],
            running_degree=self.validated_data['running_degree'],
            current_organization=self.validated_data['current_organization'],
            degree_certificate=self.validated_data['degree_certificate'],
            personal_photo=self.validated_data['personal_photo'],
        )
        personal_info.save()
        return personal_info

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    degree_certificate = serializers.ImageField(required=False)
    personal_photo = serializers.ImageField(required=False)

    class Meta:
        model = PersonalInformation
        fields = [
            'user', 'phone_number_1', 'phone_number_2', 'date_of_birth',
            'address', 'achieved_degree', 'running_degree',
            'current_organization', 'degree_certificate', 'personal_photo'
        ]
    
    def update(self, instance, validated_data):
        # Update fields that are passed in the request
        instance.phone_number_1 = validated_data.get('phone_number_1', instance.phone_number_1)
        instance.phone_number_2 = validated_data.get('phone_number_2', instance.phone_number_2)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.address = validated_data.get('address', instance.address)
        instance.achieved_degree = validated_data.get('achieved_degree', instance.achieved_degree)
        instance.running_degree = validated_data.get('running_degree', instance.running_degree)
        instance.current_organization = validated_data.get('current_organization', instance.current_organization)
        instance.degree_certificate = validated_data.get('degree_certificate', instance.degree_certificate)
        instance.personal_photo = validated_data.get('personal_photo', instance.personal_photo)
        instance.save()
        return instance

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Check if the new password matches the confirmation
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "The new passwords do not match."})

        return data

    def save(self, user):
        # Check if the old password is correct
        if not user.check_password(self.validated_data['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})

        # Set new password and save
        user.set_password(self.validated_data['new_password'])
        user.save()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Ensure the email exists in the system
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is not registered.")
        return value