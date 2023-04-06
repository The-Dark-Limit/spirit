FROM archlinux:latest

RUN pacman -Syyu python python-poetry --noconfirm

ADD . /app
WORKDIR /app

COPY app /app
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry update

ENV PYTHONPATH /app

CMD ["python", "main.py"]
