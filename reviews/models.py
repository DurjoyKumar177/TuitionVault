from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from tutions.models import TuitionApplication

class TuitionReview(models.Model):
    application = models.OneToOneField(
        TuitionApplication,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name=_("Tuition Application"),
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Reviewer"),
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name=_("Rating"),
        choices=[(i, str(i)) for i in range(1, 6)],  # Ratings between 1-5
    )
    comment = models.TextField(verbose_name=_("Comment"), null=True, blank=True)
    reviewed_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Reviewed At"))

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.application.tuition_post.title}"
