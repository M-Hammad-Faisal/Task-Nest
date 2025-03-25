from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=[("admin", "Admin"), ("manager", "Manager"), ("member", "Member")],
        default="member",
    )
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    invite_code = models.CharField(max_length=10, unique=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_teams")
    members = models.ManyToManyField(CustomUser, related_name="teams")

    def __str__(self):
        return self.name
