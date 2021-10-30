FROM python:3.7-alpine

MAINTAINER phex-space

RUN apk update && apk add --no-cache git openssh-client \
        && addgroup -S -g 1001 phex \
        && adduser -S -D -h /opt/phex_api -u 1001 -G phex phex

USER phex

ENV PATH="/opt/phex_api/.local/bin:$PATH"

RUN pip install pipenv --upgrade --user

WORKDIR /opt/phex_api
ENV PYTHONPATH="$PYTHONPATH:/opt/phex_api"

COPY Pipfile Pipfile.lock ./
RUN pipenv install

COPY phex phex

EXPOSE 8080
CMD ["pipenv", "run", "hypercorn", "--bind", "0.0.0.0:8080", "--reload", "phex:app"]
#CMD tail -f /dev/null
