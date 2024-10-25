FROM python:3.12.7-bullseye

COPY requirements/prod.txt /app/requirements/prod.txt
RUN --mount=type=cache,target=/var/lib/apt/lists --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/root/.cache \
    set -ex \
    && apt-get -qq update \
    && buildDeps=" \
        build-essential \
        " \
    && runDeps=" \
        # utils \
        gettext \
        curl \
        " \
    && DEBIAN_FRONTEND=noninteractive apt-get \
         install -y --no-install-recommends $buildDeps $runDeps \
    # change timezone
    && echo "Asia/Vladivostok" > /etc/timezone \
    # install requirements
    && pip install -r /app/requirements/prod.txt \
    # cleaning
    && if [ "${remove_build_deps}" = "true" ] ; \
       then \
         DEBIAN_FRONTEND=noninteractive apt-get \
           purge -y --auto-remove $buildDeps; \
       fi

COPY requirements/dev.txt /app/requirements/dev.txt
ARG installdev=true
RUN --mount=type=cache,target=/root/.cache \
    if [ "${installdev}" = "true" ] ; \
      then pip install -r /app/requirements/dev.txt ; \
    fi

WORKDIR /app
COPY . /app
#RUN python ./manage.py compilemessages
#RUN python ./manage.py collectstatic --noinput
