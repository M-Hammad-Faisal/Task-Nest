from django import forms
from .models import Task, Comment, Attachment
from ..users.models import CustomUser


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "status", "due_date", "assignee", "team", "tags"]
        widgets = {
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["assignee"].queryset = CustomUser.objects.filter(teams__in=user.teams.all()).distinct()
            self.fields["team"].queryset = user.teams.all()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ["file"]
