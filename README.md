Добавлен Dockerfile и описание развертывания его 

FROM python:3  # выбор версии питона

WORKDIR /app  # выбор рабочей директории

COPY ./requirements.txt .  # из какого файла копировать и в какую директорию

RUN pip install -r requirements.txt  # установка зависимостей

COPY . .  # копировать все из основной директории в основную рабочую 

#CMD ["python", "manage.py", "runserver"] # если с этим то получается полностью приложение 

Добавлены настройки для docker.yml

version: "_"  - версия

services:
  db:
    image: "_" название бд
    environment:
        POSTGRES_PASSWORD: "_" ее пароль
        PGDATA: /ver/lib/postgresql/data/pgdata  # где она будет находиться 


  app:  # эта команда производит сбор приложения с перенаправлением порта и запуском нашей бд
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "8000:8000"
    depends_on:
      - db