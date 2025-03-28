ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

ENV SECRET_KEY "Lxdhj3dF7xSIyO8qkVwly63Qg55c95i9qfFbMwewxZn0n3TQRV"
ENV DJANGO_SETTINGS_MODULE="task_manager.settings"
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn","--bind","0.0.0.0:8000","--workers","2","--worker-class","uvicorn.workers.UvicornWorker","task_manager.asgi:application"]
