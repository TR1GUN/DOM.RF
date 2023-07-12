#Делаем образ
FROM python:3.10.5-buster
# Определяем парматеры
ENV GIT_SSL_NO_VERIFY 1
ENV TZ="Europe/Moscow"

#Определяем рабочую директорию
WORKDIR /app

#Копируем в наш список зависимостей
COPY requirements.txt requirements.txt

#Обновляем все внутри докер контейнера
RUN apt-get update -y

#Устанавливаем зависимости
RUN pip3 install --no-cache-dir -r requirements.txt

# Копируем проект в нашу директорию
COPY . /app