# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файлы зависимостей и устанавливаем их
COPY uv.toml .
RUN pip install --no-cache-dir -U uv && \
    uv install

# Копируем остальной код проекта
COPY . .

# Запуск приложения
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
