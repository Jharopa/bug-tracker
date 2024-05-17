from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from .forms import CustomUserAuthenticationForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = CustomUserAuthenticationForm
    redirect_authenticated_user = True


def logout_view(request):
    logout(request)

    return redirect("users:login")
