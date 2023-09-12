FROM python:3

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#CMD ["python", "manage.py", "runserver"]  - если с этим то получается полностью приложение 