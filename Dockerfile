# Используем официальный образ Python 3.13 как базовый
FROM python:3.13-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только pyproject.toml и requirements.txt
COPY ./pyproject.toml ./requirements.txt ./

# Устанавливаем uv и зависимости
RUN pip install uv && \
    uv venv && \
    . .venv/bin/activate && \
    uv pip install -r requirements.txt

# Копируем остальной код проекта
COPY . .

# Экспорт переменных окружения
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Создаем том для статических файлов
VOLUME ["/app/staticfiles"]

# Порт по умолчанию для Uvicorn
EXPOSE 8000

# Команда запуска
CMD ["sh", "-c", ". .venv/bin/activate && python manage.py migrate && uvicorn spirit.settings.asgi:application --host 0.0.0.0 --port 8000"]
