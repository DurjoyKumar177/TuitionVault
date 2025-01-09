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
from rest_framework import generics

class TuitionPostListAPIView(ListAPIView):
    queryset = TuitionPost.objects.filter(availability=True).order_by('-created_at')
    serializer_class = TuitionPostSerializer

class TuitionPostDetailAPIView(RetrieveAPIView):
    queryset = TuitionPost.objects.all()
    serializer_class = TuitionPostSerializer
    
class TuitionPostFilterByClassAPIView(generics.ListAPIView):
    serializer_class = TuitionPostSerializer

    def get_queryset(self):
        class_name = self.request.query_params.get('class_name', None)
        if class_name:
            return TuitionPost.objects.filter(class_name__icontains=class_name, availability=True)
        return TuitionPost.objects.filter(availability=True)

# Filter Tuition Posts by Location
class TuitionPostFilterByLocationAPIView(generics.ListAPIView):
    serializer_class = TuitionPostSerializer

    def get_queryset(self):
        location = self.request.query_params.get('location', None)
        if location:
            return TuitionPost.objects.filter(location__icontains=location, availability=True)
        return TuitionPost.objects.filter(availability=True)

# Filter Tuition Posts by Monthly Payment
class TuitionPostFilterByPaymentAPIView(generics.ListAPIView):
    serializer_class = TuitionPostSerializer

    def get_queryset(self):
        min_payment = self.request.query_params.get('min_payment', None)
        max_payment = self.request.query_params.get('max_payment', None)
        if min_payment and max_payment:
            return TuitionPost.objects.filter(monthly_payment__gte=min_payment, monthly_payment__lte=max_payment, availability=True)
        elif min_payment:
            return TuitionPost.objects.filter(monthly_payment__gte=min_payment, availability=True)
        elif max_payment:
            return TuitionPost.objects.filter(monthly_payment__lte=max_payment, availability=True)
        return TuitionPost.objects.filter(availability=True)
    
class TuitionPostSearchByTitleAPIView(generics.ListAPIView):
    serializer_class = TuitionPostSerializer

    def get_queryset(self):
        title_query = self.request.query_params.get('title', None)
        if title_query:
            return TuitionPost.objects.filter(title__icontains=title_query, availability=True)
        return TuitionPost.objects.filter(availability=True)

class DropdownOptionsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        field = self.kwargs.get('field')
        if field not in ['class_name', 'location', 'group']:
            return Response({"error": "Invalid field name"}, status=400)

        values = TuitionPost.objects.filter(availability=True).values_list(field, flat=True).distinct()
        return Response(sorted(values))

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
