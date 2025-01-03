# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения
COPY . .
COPY ./models /app/models
COPY ./ИменаДебютов.txt /app/ИменаДебютов.txt
COPY ./инкеременткод.txt /app/инкеременткод.txt

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=main.py

# Открываем порт 3000
EXPOSE 3000

# Запускаем Flask приложение
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]