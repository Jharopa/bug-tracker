from django import forms

from .models import Bug


class BugFormManager(forms.ModelForm):
    class Meta:
        model = Bug
        exclude = ("bug_creator",)


class BugFormDeveloper(forms.ModelForm):
    class Meta:
        model = Bug
        exclude = (
            "bug_creator",
            "assignee",
        )
