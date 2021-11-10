FROM python:3.9-slim-buster
WORKDIR /django-blog-api
EXPOSE 8000
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt update
ENV PYTHONUNBUFFERED=1
ENV SECRET_KEY="django-insecure--n6t$=^+p+(b188e-5phqheprmpikg-sidiyu8hgrbe64u)akh"
ENV EMAIL_USE_SSL=True
ENV EMAIL_HOST=smtpout.secureserver.net
ENV EMAIL_PORT=465
ENV EMAIL_HOST_USER=admin@prodev.pro
ENV EMAIL_HOST_PASSWORD=Rehan876685$
ENV DEFAULT_FROM_EMAIL="Rehan <admin@prodev.pro>"
COPY . .
RUN ["python3", "manage.py", "makemigrations"]
RUN ["python3", "manage.py", "migrate", "--run-syncdb"]
RUN ["python3", "manage.py", "collectstatic", "--no-input"]
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
