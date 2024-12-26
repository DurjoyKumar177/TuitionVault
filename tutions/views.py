from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import TuitionPost, TuitionApplication
from .serializers import TuitionPostSerializer

class TuitionPostListAPIView(ListAPIView):
    queryset = TuitionPost.objects.filter(availability=True)
    serializer_class = TuitionPostSerializer

class TuitionPostDetailAPIView(RetrieveAPIView):
    queryset = TuitionPost.objects.all()
    serializer_class = TuitionPostSerializer

class ApplyForTuitionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tuition_post_id):
        tuition_post = get_object_or_404(TuitionPost, id=tuition_post_id)

        if not tuition_post.availability:
            return Response(
                {"error": "This tuition post is no longer available."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the user has already applied
        if TuitionApplication.objects.filter(tuition_post=tuition_post, user=request.user).exists():
            return Response(
                {"error": "You have already applied for this tuition post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the application
        application = TuitionApplication.objects.create(tuition_post=tuition_post, user=request.user)

        # Send notification email
        self.send_notification_email(request.user, tuition_post)

        return Response(
            {"message": "You have successfully applied for this tuition post."},
            status=status.HTTP_201_CREATED
        )

    def send_notification_email(self, user, tuition_post):
        """
        Sends an email notification to the user and admin after an application is submitted.
        """
        # User email
        user_email_subject = f"Application Submitted for {tuition_post.title}"
        user_email_body = f"Dear {user.username},\n\nYou have successfully applied for the tuition post: {tuition_post.title}.\n\nThank you for your interest!\n\nBest regards,\nTuition Platform Team"

        send_mail(
            user_email_subject,
            user_email_body,
            'admin@tuitionplatform.com',  # Sender's email
            [user.email],
            fail_silently=False,
        )

        # Admin email
        admin_email_subject = f"New Application for {tuition_post.title}"
        admin_email_body = f"Dear Admin,\n\nA new application has been submitted by {user.username} for the tuition post: {tuition_post.title}.\n\nPlease review the application at your earliest convenience.\n\nBest regards,\nTuition Platform System"

        send_mail(
            admin_email_subject,
            admin_email_body,
            'admin@tuitionplatform.com',  # Sender's email
            ['admin@tuitionplatform.com'],  # Admin's email
            fail_silently=False,
        )
