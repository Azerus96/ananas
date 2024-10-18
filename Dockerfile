# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей и устанавливаем библиотеки
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в образ
COPY . .

# Указываем переменную окружения для Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

# Открываем порт для приложения
EXPOSE 5000

# Запускаем Flask-приложение
CMD ["flask", "run"]
