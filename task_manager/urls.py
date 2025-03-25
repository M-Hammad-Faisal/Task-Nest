from django.contrib import admin
from django.urls import path
from src.apps.users import views as user_views
from src.apps.tasks import views as task_views
from src.apps.notifications import views as notification_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", task_views.home, name="home"),
    path("admin/", admin.site.urls),
    path("signup/", user_views.signup, name="signup"),
    path("login/", user_views.login_view, name="login"),
    path("logout/", user_views.logout_view, name="logout"),
    path("dashboard/", task_views.dashboard, name="dashboard"),
    path("tasks/", task_views.task_list, name="task_list"),
    path("tasks/<int:task_id>/", task_views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/edit/", task_views.task_edit, name="task_edit"),
    path("tasks/<int:task_id>/delete/", task_views.task_delete, name="task_delete"),
    path("tasks/create/", task_views.task_create, name="task_create"),
    path("teams/", user_views.team_list, name="team_list"),
    path("teams/create/", user_views.team_create, name="team_create"),
    path("teams/join/", user_views.team_join, name="team_join"),
    path(
        "notifications/", notification_views.notification_list, name="notification_list"
    ),
    path(
        "notifications/<int:notification_id>/read",
        notification_views.notification_read,
        name="notification_read",
    ),
    path("profile/", user_views.profile, name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
