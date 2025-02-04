FROM python:3.10.13-slim-bullseye

WORKDIR /opt/app

COPY ["poetry.lock", "pyproject.toml", "./"]
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1
ENV PYTHONPATH .
ENV COOKING_CORE_SETTING_IN_DOCKER true

RUN set -xe \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        pkg-config \
        python3-dev \
        default-libmysqlclient-dev \
    && pip install --no-cache-dir virtualenvwrapper poetry==1.6.1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN poetry install --no-root
COPY myproject myproject
COPY /entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


