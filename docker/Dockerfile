# Ну пока так ...

FROM archlinux:latest

ENV PYTHONUNBUFFERED=1

RUN pacman -Syyu python python-poetry python-pip python-setuptools --noconfirm

ADD . /app
WORKDIR /app

COPY app /app
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry install

CMD ["poetry", "run", "python", "main.py"]
