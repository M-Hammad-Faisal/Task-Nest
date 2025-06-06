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

ENV SECRET_KEY "pxIo8w7Stbz8vhFIBRCJgYhIs1zoRD5kAa7mQmnqTGureqbh5D"
RUN python manage.py collectstatic --noinput

EXPOSE 8000
RUN pip install daphne

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "task_manager.asgi:application"]
