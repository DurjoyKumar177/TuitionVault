from django.db import models
from django.contrib.auth.models import User


class PersonalInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="personal_info")
    phone_number_1 = models.CharField(max_length=11)
    phone_number_2 = models.CharField(max_length=11, blank=True, null=True)
    date_of_birth = models.DateField()
    address = models.TextField()
    achieved_degree = models.CharField(max_length=100)
    running_degree = models.CharField(max_length=100, blank=True, null=True)
    current_organization = models.CharField(max_length=100, blank=True, null=True)
    degree_certificate = models.ImageField(upload_to="accounts/certificates/")
    personal_photo = models.ImageField(upload_to="accounts/photos/")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.email})'
