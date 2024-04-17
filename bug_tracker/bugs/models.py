from django.conf import settings
from django.db import models


class Bug(models.Model):
    title = models.CharField(max_length=255, blank=False)
    severity_type = models.TextChoices(
        "severity_type", "Blocker Critical Major Minor Trivial"
    )
    severity = models.CharField(
        max_length=8, choices=severity_type.choices, blank=False
    )
    status_type = models.TextChoices("status_type", "Open Closed")
    status = models.CharField(max_length=6, choices=status_type.choices, blank=False)
    description = models.TextField(blank=False)
    bug_created = models.DateTimeField(verbose_name="created at", auto_now_add=True)
    bug_creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="creator",
        on_delete=models.SET_NULL,
        related_name="bug_creator",
        null=True,
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assignee",
        null=True,
    )

    def __str__(self):
        return self.title
