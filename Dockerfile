FROM python:3.9-alpine3.14
WORKDIR /django-blog-api
CMD [ "python3 install python3-pip", "python3 -m pip install --upgrade pip" ]
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN ["python3 manage.py makemigrations"]
RUN ["python3 manage.py migrate --run-syncdb"]
RUN ["python3 manage.py collectstatic --no-input"]
EXPOSE 8000
RUN python3 manage.py runserver