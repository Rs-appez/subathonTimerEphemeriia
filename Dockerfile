ARG PYTHON_VERSION=3.13-alpine

FROM python:${PYTHON_VERSION}

ENV TZ="Europe/Brussels"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt 

COPY . /code

WORKDIR /code/subathonTimerEphemeriia

ENV SECRET_KEY="non-secret-key-for-building-purposes"

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "subathonTimerEphemeriia.asgi:application"]
