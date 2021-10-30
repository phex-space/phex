FROM postgres:13-alpine

RUN apk add tzdata && \
    cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \
    echo "Europe/Berlin" >  /etc/timezone \
    apk del tzdata
ENV TZ Europe/Berlin
ENV LANG en_US.utf8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# COPY ./init.d/ /docker-entrypoint-initdb.d/
