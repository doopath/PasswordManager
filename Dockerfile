FROM python:3.12.3

ENV PYTHONUNBUFFERED 1

WORKDIR /doopass

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /doopass/doopass

EXPOSE 7240

CMD python manage.py makemigrations && python manage.py migrate && gunicorn --bind 0.0.0.0:7240 doopass.wsgi
