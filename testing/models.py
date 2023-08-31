from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    # Use email as the unique identifier
    username = None
    email = models.EmailField(unique=True)
    mobile = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r"^\d{11}$",
                message="Mobile number must be 11 digits long.",
            )
        ],
        help_text="Required. Your 11-digit mobile number.",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Project(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    details = models.TextField(max_length=100)
    target = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    amount_donated = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.start_time >= self.end_time:
            raise ValueError("End time must be after start time")
        super().save(*args, **kwargs)

    def is_owner(self, user):
        return self.owner == user

    def can_edit(self, user):
        return self.is_owner(user)

    def can_delete(self, user):
        return self.is_owner(user) and timezone.now() < self.start_time

    def __str__(self):
        return self.title + self.details
