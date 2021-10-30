FROM python:3.9-buster

COPY ./phex.ca.pem /usr/local/share/ca-certificates/

RUN apt-get -y update && apt-get -y upgrade && \
    apt-get install -y build-essential && \
    apt-get install -y libpq-dev && \
    useradd --create-home --home-dir /opt/app phex && \
    chown -Rf phex.phex /opt/app && \
    update-ca-certificates

USER phex
ENV PATH="/opt/app/.local/bin:$PATH"

RUN pip install pipenv --upgrade --user

WORKDIR /opt/app
ENV PYTHONPATH="$PYTHONPATH:/opt/app"

# Install dependencies:
COPY Pipfile ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy && \
    cat /usr/local/share/ca-certificates/phex.ca.pem >> /opt/app/.venv/lib/python3.9/site-packages/certifi/cacert.pem

COPY phex phex

EXPOSE 8080
CMD ["pipenv", "run", "hypercorn", "--bind", "0.0.0.0:8080", "--reload", "phex:app"]
#CMD  tail -f /dev/null