FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# COPY /.env .env

EXPOSE 8000

# CMD ["sh", "-c", "python manage.py migrate;gunicorn --config gunicorn-cfg.py core.wsgi"]
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]