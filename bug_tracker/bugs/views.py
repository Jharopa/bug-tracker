from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView
from users.models import CustomUser

from .models import Bug


class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    template_name = "bugs/list.html"
    context_object_name = "bugs"

    paginate_by = 15

    login_url = settings.LOGIN_URL

    def get_queryset(self):
        if self.request.user.user_type == CustomUser.MANAGER:
            return self.model.objects.all().order_by("id")
        elif self.request.user.user_type == CustomUser.DEVELOPER:
            return self.model.objects.filter(
                Q(assignee__id=self.request.user.id)
            ).order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_manager:
            context["is_manager"] = True

        return context
