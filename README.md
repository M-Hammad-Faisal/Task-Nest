# Task-Nest

A sleek, minimalist task management web application built with Django, designed for individual and team collaboration.
Featuring a professional yet cool UI with real-time updates, team-based task assignments, notifications, and a clean,
responsive design, Task Manager streamlines workflows with simplicity and style.

## Features

- __Task Management__: Create, edit, delete, and track tasks with statuses (Open, In Progress, Resolved, Closed,
  Reopened) and priorities (Low, Medium, High).
- __Team Collaboration__: Assign tasks to team members, manage teams with invite codes, and filter tasks by team or
  category (derived from tags).
- __Real-Time Updates__: WebSocket-powered live comment and status updates on task detail pages.
- __Notifications__: In-app notifications for task updates, with unread highlighting.
- __Minimalist UI__: Clean, professional design with a deep blue (`#1E3A8A`) and emerald green (`#10B981`) palette,
  small typography, and subtle hover effects.
- __Attachments__: Upload and view files per task.
- __Responsive__: Mobile-friendly layout with Bootstrap 5.
- __User Authentication__: Secure signup, login, and logout functionality.

## Tech Stack

- __Backend__: Django 5.1.7, Python 3.12.3
- __Frontend__: HTML, CSS (custom minimalist styles), Bootstrap 5, Chart.js (for dashboard stats)
- __Real-Time__: Django Channels, WebSockets
- __Database__: SQLite (default, configurable for PostgreSQL)
- __Dependencies__: See `requirements.txt`

## Installation

### Prerequisites

- Python 3.12+
- pip
- Virtualenv (recommended)
- Redis (for WebSocket support)

### Setup

1. Clone the Repository

  ```bash
  git clone https://github.com/M-Hammad-Faisal/Task-Nest.git
  cd Task-Nest
  ```

2. Create a Virtual Environment

  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

3. Install Dependencies

  ```bash
  pip install -r requirements.txt
  ```

4. Set Up Environment Variables Create a .env file in the project root:

  ```text
  DEBUG=True
  SECRET_KEY=your-secret-key-here
  DATABASE_URL=sqlite:///db.sqlite3
  EMAIL_HOST_USER=your-email@gmail.com
  EMAIL_HOST_PASSWORD=your-email-password
  ```

5. Apply Migrations

  ```bash
  python manage.py migrate
  ```

6. Create a Superuser

  ```bash
  python manage.py createsuperuser
  ```

7. Install Redis
    - On macOS: `brew install redis`
    - On Ubuntu: `sudo apt-get install redis-server`
    - On Windows: Use WSL or a Redis Docker container
    - Start Redis: `redis-server`

8. Run the Development Server

      ```bash
      python manage.py runserver 
      ```

   Visit http://localhost:8000 in your browser.

9. Run WebSocket Server Ensure Redis is running, then:
    ```bash
    python manage.py runserver  # Channels handles WebSockets automatically 
    ```

## Usage

- __Dashboard__: View your tasks, team stats, and filter by status, priority, team, or category (`/dashboard/`).
- __Task List__: See all tasks (`/tasks/`).
- __Task Details__: Update status, add comments or attachments in real-time (`/tasks/<id>/`).
- __Teams__: Create or join teams with invite codes (`/teams/`).
- __Notifications__: Check task updates (`/notifications/`).
- __Admin__: Manage users, tasks, and teams at `/admin/` (superuser only).

## Screenshots

[Homepage](./static/Homepage.png)
[Dashboard](./static/dashboard.png)

## Testing

Run the test suite:

```bash
python manage.py test
```

Tests cover task CRUD, team functionality, and notifications.

## Contributing

- Fork the repo.
- Create a branch: `git checkout -b feature/your-feature`.
- Commit changes: `git commit -m "Add your feature"`.
- Push: `git push origin feature/your-feature`.
- Open a pull request.

## Future Enhancements

- Overdue task alerts via email or in-app.
- Task dependencies and Gantt chart view.
- Dark mode toggle.
- API endpoints for third-party integration.

## License

MIT License—feel free to use, modify, and distribute.