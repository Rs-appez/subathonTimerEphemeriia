ARG PYTHON_VERSION=3.13-alpine

FROM python:${PYTHON_VERSION}

ENV TZ="Europe/Brussels"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache supervisor;

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt 

COPY . /code
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /code/logs
WORKDIR /code/subathonTimerEphemeriia

ENV SECRET_KEY="non-secret-key-for-building-purposes"

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
