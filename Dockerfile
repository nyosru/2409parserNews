# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install -r requirements.txt
#RUN pip install watchdog

# Копируем исходный код в контейнер
COPY . .

# Открываем порт для приложения (если нужно)
# EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]
#CMD ["watchmedo", "auto-restart", "--recursive", "--patterns=*.py", "python3", "app.py"]
#CMD ["watchmedo", "auto-restart", "--recursive", "--patterns=*.py", "python", "app.py"]
