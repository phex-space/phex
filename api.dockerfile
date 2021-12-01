FROM python:3.9-alpine as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PATH=$PATH:/venv/bin

COPY phex.ca.pem /opt/phex.ca.pem
RUN  apk --no-cache add ca-certificates \
    && cat /opt/phex.ca.pem >> /etc/ssl/certs/ca-certificates.crt \
    && update-ca-certificates
WORKDIR /opt/phex/api

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.12

RUN apk add --no-cache build-base libffi-dev musl-dev postgresql-dev
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY ["./appliance/api/pyproject.toml", "./appliance/api/poetry.lock", "./"]
COPY ./packages /opt/packages
RUN poetry export --without-hashes -f requirements.txt | /venv/bin/pip install -r /dev/stdin \
    && cat /opt/phex.ca.pem >> /venv/lib/python3.9/site-packages/certifi/cacert.pem

FROM base as final

RUN apk add --no-cache libffi libpq
COPY --from=builder /venv /venv

COPY ./appliance/api .

EXPOSE 8080
# CMD sleep 900
CMD hypercorn --bind 0.0.0.0:8080 --reload main:server
