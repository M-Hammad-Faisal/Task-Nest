from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages

import task_manager.settings
from .models import Task, Comment
from .forms import TaskForm, CommentForm, AttachmentForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from src.apps.notifications.models import Notification


def home(request):
    return render(request, "home.html")


@login_required(login_url="login")
def dashboard(request):
    tasks = Task.objects.filter(assignee=request.user) | Task.objects.filter(creator=request.user)
    teams = request.user.teams.all()

    # Search and Filter
    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")
    priority_filter = request.GET.get("priority", "")
    team_filter = request.GET.get("team", "")
    category_filter = request.GET.get("category", "")

    if query:
        tasks = tasks.filter(title__icontains=query)
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if team_filter:
        tasks = tasks.filter(team_id=team_filter)
    if category_filter:
        tasks = tasks.filter(tags__icontains=category_filter)

    stats = {
        "open": tasks.filter(status="open").count(),
        "in_progress": tasks.filter(status="in_progress").count(),
        "resolved": tasks.filter(status="resolved").count(),
        "closed": tasks.filter(status="closed").count(),
        "reopened": tasks.filter(status="reopened").count(),
        "overdue": tasks.filter(due_date__lt=timezone.now()).count(),
    }
    team_stats = [{"name": team.name, "total": team.tasks.count(), "closed": team.tasks.filter(status="closed").count()}
                  for team in teams]
    categories = tasks.values_list("tags", flat=True).distinct()
    context = {
        "tasks": tasks,
        "teams": teams,
        "stats": stats,
        "team_stats": team_stats,
        "categories": categories,
        "query": query,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "category_filter": category_filter,
        "status_choices": Task.STATUS_CHOICES,
        "priority_choices": Task.PRIORITY_CHOICES,
    }
    return render(request, "tasks/dashboard.html", context)


@login_required(login_url="login")
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    channel_layer = get_channel_layer()

    if request.method == "POST":
        if "comment" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.task = task
                comment.user = request.user
                comment.save()
                if task.assignee and task.assignee != request.user:
                    Notification.objects.create(
                        user=task.assignee,
                        task=task,
                        message=f"{request.user.username} commented on '{task.title}'"
                    )
                    send_mail(
                        subject=f"New Comment on {task.title}",
                        message=f"{request.user.username} commented: {comment.content}",
                        from_email=task_manager.settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[task.assignee.email],
                        fail_silently=True,
                    )
                async_to_sync(channel_layer.group_send)(
                    f"task_{task_id}",
                    {
                        "type": "broadcast_update",
                        "message": {
                            "type": "comment",
                            "comment": {"user": str(request.user), "content": comment.content,
                                        "created_at": comment.created_at.isoformat()},
                        },
                    },
                )
                return redirect("task_detail", task_id=task.id)
        elif "status" in request.POST:
            status = request.POST.get("status")
            task.status = status
            task.save()
            if task.assignee and task.assignee != request.user:
                Notification.objects.create(
                    user=task.assignee,
                    task=task,
                    message=f"{request.user.username} updated '{task.title}' to {status}"
                )
                send_mail(
                    subject=f"Task Status Updated: {task.title}",
                    message=f"{request.user.username} changed the status to {status}",
                    from_email=task_manager.settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[task.assignee.email],
                    fail_silently=True,
                )
            async_to_sync(channel_layer.group_send)(
                f"task_{task_id}",
                {
                    "type": "broadcast_update",
                    "message": {"type": "task_update", "task": {"status": status}},
                },
            )
            return redirect("task_detail", task_id=task.id)
        elif "attachment" in request.POST:
            attachment_form = AttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.task = task
                attachment.uploaded_by = request.user
                attachment.save()
                if task.assignee and task.assignee != request.user:
                    Notification.objects.create(
                        user=task.assignee,
                        task=task,
                        message=f"{request.user.username} added an attachment to '{task.title}'"
                    )
                    send_mail(
                        subject=f"New Attachment on {task.title}",
                        message=f"{request.user.username} uploaded a file: {attachment.file.name}",
                        from_email=task_manager.settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[task.assignee.email],
                        fail_silently=True,
                    )
                return redirect("task_detail", task_id=task.id)
    else:
        form = CommentForm()
        attachment_form = AttachmentForm()
    return render(request, "tasks/task_detail.html", {"task": task, "form": form, "attachment_form": attachment_form})


@login_required(login_url="login")
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            return redirect("dashboard")
    else:
        form = TaskForm(user=request.user)
    return render(request, "tasks/task_create.html", {
        "form": form,
    })


@login_required(login_url="login")
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.creator != request.user and task.assignee != request.user:
        messages.error(request, "You don’t have permission to edit this task.")
        return redirect("dashboard")

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            updated_task = form.save()
            if updated_task.assignee and updated_task.assignee != request.user:
                Notification.objects.create(
                    user=updated_task.assignee,
                    task=updated_task,
                    message=f"{request.user.username} updated '{updated_task.title}'"
                )
                send_mail(
                    subject=f"Task Updated: {updated_task.title}",
                    message=f"{request.user.username} made changes to your assigned task.",
                    from_email="your-email@gmail.com",
                    recipient_list=[updated_task.assignee.email],
                    fail_silently=True,
                )
            messages.success(request, "Task updated successfully!")
            return redirect("task_detail", task_id=task.id)
    else:
        form = TaskForm(instance=task, user=request.user)
    return render(request, "tasks/task_edit.html", {"form": form, "task": task})


@login_required(login_url="login")
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.creator != request.user:
        messages.error(request, "Only the creator can delete this task.")
        return redirect("dashboard")
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect("dashboard")
    return render(request, "tasks/task_delete.html", {"task": task})


@login_required(login_url="login")
def task_list(request):
    tasks = Task.objects.filter(team__members=request.user)
    context = {"tasks": tasks}
    return render(request, "tasks/task_list.html", context)
