from django.test import TestCase
from django.urls import reverse
from src.apps.users.models import CustomUser, Team


class UserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.team = Team.objects.create(
            name="Test Team", owner=self.user, invite_code="TEST1234"
        )
        self.team.members.add(self.user)

    def test_signup(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "testing@example.com",
                "first_name": "Test",
                "last_name": "User",
                "role": "admin",
                "password1": "newpass123",
                "password2": "newpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username="newuser").exists())

    def test_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_team_create(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("team_create"), {"name": "New Team"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Team.objects.filter(name="New Team").exists())

    def test_team_join(self):
        CustomUser.objects.create_user(
            username="joiner", email="join@example.com", password="joinpass123"
        )
        self.client.login(username="joiner", password="joinpass123")
        response = self.client.post(reverse("team_join"), {"invite_code": "TEST1234"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Team.objects.get(invite_code="TEST1234")
            .members.filter(username="joiner")
            .exists()
        )
