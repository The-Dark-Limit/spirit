# Ну пока так ...

FROM archlinux:latest

ENV PYTHONUNBUFFERED=1

RUN pacman -Syyu python python-poetry python-pip python-setuptools --noconfirm

ADD . /app
WORKDIR /app

COPY app /app
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry export -f requirements.txt --output requirements.txt
RUN --mount=type=cache,target=/root/.cache
RUN pip install -r requirements.txt --break-system-packages

CMD ["poetry", "run", "python", "main.py"]
