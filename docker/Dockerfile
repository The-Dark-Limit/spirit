# Ну пока так ...

FROM archlinux:latest

ENV PYTHONUNBUFFERED=1

RUN pacman -Syyu python python-pdm python-pip python-setuptools --noconfirm

ADD . /app
WORKDIR /app

COPY app /app
COPY pdm.lock pdm.lock
COPY pyproject.toml pyproject.toml

RUN pdm install

CMD ["python", "main.py"]
