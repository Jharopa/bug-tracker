from django.urls import path

# Bugs app imports.
from . import views

app_name = "bugs"

urlpatterns = [
    path("", views.BugListView.as_view(), name="bug_list"),
]
