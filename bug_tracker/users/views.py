from django.contrib.auth.views import LoginView

from .forms import CustomUserAuthenticationForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = CustomUserAuthenticationForm
    redirect_authenticated_user = True
