FROM archlinux:latest

RUN pacman -Syyu python python-poetry tzdata python-pip python-setuptools --noconfirm

ADD . /app
WORKDIR /app

COPY app /app
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry update

ENV PYTHONPATH /app

CMD ["poetry", "run", "python", "main.py"]
