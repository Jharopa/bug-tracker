from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from lookup_property import L
from users.models import CustomUser

from .forms import BugFormDeveloper, BugFormManager
from .models import Bug


class BugCreateView(LoginRequiredMixin, CreateView):
    model = Bug
    template_name = "bugs/create.html"

    login_url = settings.LOGIN_URL

    def get_form_class(self):
        if self.request.user.is_manager:
            return BugFormManager
        else:
            return BugFormDeveloper

    def form_valid(self, form):
        form.instance.bug_creator = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("bugs:bug_list")


class BugDetailView(LoginRequiredMixin, DetailView):
    model = Bug
    template_name = "bugs/detail.html"
    context_object_name = "bug"

    login_url = settings.LOGIN_URL

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Bug, id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_manager:
            context["is_manager"] = True

        return context


class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    template_name = "bugs/list.html"
    context_object_name = "bugs"

    paginate_by = 15

    login_url = settings.LOGIN_URL

    def get_queryset(self):
        order_by = self.request.GET.get("order_by", "id")
        status = self.request.GET.get("status", "")
        assignee = self.request.GET.get("assignee", "")

        query = Q(status__contains=status) & L(assignee__full_name__contains=assignee)

        if self.request.user.user_type == CustomUser.MANAGER:
            return self.model.objects.all().filter(query).order_by(order_by)
        elif self.request.user.user_type == CustomUser.DEVELOPER:
            return self.model.objects.filter(
                Q(assignee__id=self.request.user.id) & query
            ).order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_manager:
            context["is_manager"] = True

        return context


class BugUpdateView(LoginRequiredMixin, UpdateView):
    model = Bug
    template_name = "bugs/update.html"
    context_object_name = "bug"

    login_url = settings.LOGIN_URL

    def get_form_class(self):
        if self.request.user.is_manager:
            return BugFormManager
        else:
            return BugFormDeveloper

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Bug, id=id)

    def get_success_url(self):
        return reverse("bugs:bug_list")


class BugDeleteView(LoginRequiredMixin, DeleteView):
    model = Bug
    template_name = "bugs/delete.html"
    context_object_name = "bug"

    login_url = settings.LOGIN_URL

    def get(self, request, *args, **kwargs):
        if request.user.is_developer:
            return redirect("bugs:bug_list")

        return super().get(request, *args, **kwargs)

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Bug, id=id)

    def get_success_url(self):
        return reverse("bugs:bug_list")


@login_required(login_url=settings.LOGIN_URL)
def close_bug_view(request: HttpRequest, id):
    bug = get_object_or_404(Bug, id=id)

    if request.user != bug.assignee and not request.user.is_manager:
        return redirect("bugs:bug_list")

    if request.method == "GET":
        return render(request, "bugs/close.html", {"bug": bug})

    if request.method == "POST":
        if bug.status == "Open":
            bug.status = "Closed"
            bug.save()

        return redirect("bugs:bug_list")
