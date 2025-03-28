# src/apps/notifications/tests.py
from django.test import TestCase
from django.urls import reverse
from src.apps.users.models import CustomUser
from src.apps.tasks.models import Task
from src.apps.notifications.models import Notification


class NotificationTests(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username="user1", email="user1@example.com", password="pass123")
        self.user2 = CustomUser.objects.create_user(username="user2", email="user2@example.com", password="pass123")
        self.task = Task.objects.create(
            title="Test Task",
            creator=self.user1,
            assignee=self.user2,
            status="todo",
            priority="medium",
        )
        self.client.login(username="user1", password="pass123")

    def test_notification_on_comment(self):
        response = self.client.post(reverse("task_detail", args=[self.task.id]), {
            "comment": "1",
            "content": "Test comment",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Notification.objects.filter(
            user=self.user2,
            task=self.task,
            message="user1 commented on 'Test Task'"
        ).exists())

    def test_notification_list(self):
        Notification.objects.create(user=self.user1, task=self.task, message="Test notification")
        self.client.login(username="user1", password="pass123")
        response = self.client.get(reverse("notification_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test notification")
