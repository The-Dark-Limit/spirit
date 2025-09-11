FROM pytorch/pytorch:2.8.0-cuda12.9-cudnn9-runtime

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей (именно в таком порядке!)
COPY pyproject.toml ./
COPY requirements-ml.txt ./
COPY requirements.txt ./

# Устанавливаем ML-зависимости (они редко меняются, поэтому кэшируются)
RUN pip install -r requirements-ml.txt

# Устанавливаем остальные зависимости
RUN pip install -r requirements.txt

COPY . .

# Экспорт переменных окружения
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Создаем том для статических файлов
VOLUME ["/app/staticfiles"]

# Порт по умолчанию для Uvicorn
EXPOSE 8000

# Команда запуска
CMD ["sh", "-c", "python manage.py migrate && uvicorn spirit.settings.asgi:application --host 0.0.0.0 --port 8000"]
