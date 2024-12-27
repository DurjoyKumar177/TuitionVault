from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import TuitionPost, TuitionApplication
from .serializers import TuitionPostSerializer
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

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
        email_subject = "Tuition Application Notification"
        email_body = render_to_string('applyNotification.html', {'username': user.username, 'tuition_title': tuition_post.title})

        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()
