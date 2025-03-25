# src/apps/tasks/tests.py
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from src.apps.users.models import CustomUser
from src.apps.tasks.models import Task, Comment, Attachment


class TaskTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.client.login(username="testuser", password="testpass123")
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            creator=self.user,
            status="open",
            priority="medium",
            tags="bug, urgent",
        )

    def test_dashboard(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_task_detail(self):
        response = self.client.get(reverse("task_detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_task_create(self):
        response = self.client.post(reverse("task_create"), {
            "title": "New Task",
            "description": "New Description",
            "priority": "high",
            "status": "in_progress",
            "tags": "feature, sprint1",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    def test_task_edit(self):
        response = self.client.post(reverse("task_edit", args=[self.task.id]), {
            "title": "Updated Task",
            "description": "Updated Description",
            "priority": "low",
            "status": "resolved",  # Changed from "done" to "resolved"
            "tags": "bug, fixed",
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")
        self.assertEqual(self.task.status, "resolved")

    def test_task_delete(self):
        response = self.client.post(reverse("task_delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_add_comment(self):
        response = self.client.post(reverse("task_detail", args=[self.task.id]), {
            "comment": "1",
            "content": "This is a test comment",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content="This is a test comment", task=self.task).exists())

    def test_add_attachment(self):
        file = SimpleUploadedFile("test.txt", b"Test content")
        response = self.client.post(reverse("task_detail", args=[self.task.id]), {
            "attachment": "1",
            "file": file,
        }, format="multipart")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Attachment.objects.filter(task=self.task, file__endswith="test.txt").exists())