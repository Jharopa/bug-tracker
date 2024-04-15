from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    MANAGER = "M"
    DEVELOPER = "D"

    USER_TYPES = [(MANAGER, "Manager"), (DEVELOPER, "Developer")]

    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=225, null=False)
    last_name = models.CharField(max_length=225, null=False)
    user_type = models.CharField(max_length=1, choices=USER_TYPES, default=DEVELOPER)
    account_created = models.DateTimeField(
        verbose_name="account created", auto_now_add=True
    )
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_first_name(self):
        return self.first_name

    @property
    def is_manager(self):
        return self.user_type == self.MANAGER

    @property
    def is_developer(self):
        return self.user_type == self.DEVELOPER
