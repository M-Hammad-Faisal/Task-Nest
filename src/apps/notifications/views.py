from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required(login_url="login")
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notifications/notification_list.html", {"notifications": notifications})


@login_required(login_url="login")
def notification_read(request, notification_id=None):
    notification = Notification.objects.filter(user=request.user, id=notification_id, is_read=False).first()
    if notification:
        notification.is_read = True
        notification.save()
        return redirect("task_detail", notification.task.id)
    return redirect("notification_list")
