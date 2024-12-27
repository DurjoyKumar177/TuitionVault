from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class TuitionPost(models.Model):
    class GroupChoices(models.TextChoices):
        SCIENCE = 'Science', _('Science')
        ARTS = 'Arts', _('Arts')
        COMMERCE = 'Commerce', _('Commerce')
        OTHER = 'Other', _('Other')

    class DayChoices(models.TextChoices):
        SUNDAY = 'Sunday', _('Sunday')
        MONDAY = 'Monday', _('Monday')
        TUESDAY = 'Tuesday', _('Tuesday')
        WEDNESDAY = 'Wednesday', _('Wednesday')
        THURSDAY = 'Thursday', _('Thursday')
        FRIDAY = 'Friday', _('Friday')
        SATURDAY = 'Saturday', _('Saturday')

    title = models.CharField(max_length=200, verbose_name=_("Tuition Title"))
    image = models.ImageField(upload_to='tutions/images/', verbose_name=_("Image"))
    class_name = models.CharField(max_length=100, verbose_name=_("Class"))
    subjects = models.TextField(verbose_name=_("Subjects"))  # List of subjects as text
    group = models.CharField(
        max_length=20,
        choices=GroupChoices.choices,
        default=GroupChoices.OTHER,
        verbose_name=_("Group"),
    )
    routine = models.TextField(verbose_name=_("Routine"))  # Comma-separated day names
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Monthly Payment"))
    location = models.CharField(max_length=255, verbose_name=_("Location"))
    google_map_link = models.URLField(max_length=500, verbose_name=_("Google Map Link"), null=True, blank=True)
    availability = models.BooleanField(default=True, verbose_name=_("Availability"))
    details = models.TextField(verbose_name=_("Details"))
    experience = models.PositiveIntegerField(verbose_name=_("Experience (Years)"), null=True, blank=True)
    required_skills = models.TextField(verbose_name=_("Required Skills"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def get_routine_buttons(self):
        """Parse routine into a list of day buttons."""
        return self.routine.split(',')  # Example: "Sunday,Monday" -> ['Sunday', 'Monday']

    def get_subject_buttons(self):
        """Parse subjects into a list of buttons."""
        return self.subjects.split(',')  # Example: "Math,Science" -> ['Math', 'Science']

    def __str__(self):
        return f'{self.title} ({self.class_name}) - {self.location}'


class TuitionApplication(models.Model):
    tuition_post = models.ForeignKey(
        TuitionPost,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name=_("Tuition Post"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Applicant"),
    )
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Applied At"))
    is_approved = models.BooleanField(default=False, verbose_name=_("Is Approved"))

    class Meta:
        unique_together = ('tuition_post', 'user')  # Ensure a user applies only once per post

    def save(self, *args, **kwargs):
        if self.is_approved:
            # Mark tuition post as unavailable if approved
            self.tuition_post.availability = False
            self.tuition_post.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} applied for {self.tuition_post.title}"
