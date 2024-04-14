from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email address")
        elif not first_name:
            raise ValueError("User must have a first name")
        elif not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.is_active = True

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email=email, first_name=first_name, last_name=last_name, password=password
        )

        user.is_staff = True
        user.is_superuser = True

        user.save()

        return user
