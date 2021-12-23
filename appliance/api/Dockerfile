FROM python:3.10-alpine3.15 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PATH=$PATH:/venv/bin

RUN apk add zlib libjpeg

WORKDIR /opt/phex/api

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.12

RUN apk add --no-cache build-base libffi-dev musl-dev postgresql-dev jpeg-dev zlib-dev
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY ./packages /opt/packages
COPY ./appliance/api/pyproject.toml ./appliance/api/poetry.lock ./
RUN poetry export --without-hashes -f requirements.txt | /venv/bin/pip install -r /dev/stdin

FROM base as final

RUN apk add --no-cache libffi libpq
COPY --from=builder /venv /venv

COPY ./appliance/api .

EXPOSE 8080
CMD hypercorn --bind 0.0.0.0:8080 --reload main:server
# CMD sleep 900