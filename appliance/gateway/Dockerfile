FROM alpine:3.15

RUN  apk update && apk upgrade --available && sync \
    && mkdir -p /run/nginx \
    && apk add --no-cache nginx-mod-http-lua

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./mitigate-log4shell.conf /etc/nginx/mitigate-log4shell.conf
COPY ./conf.d/ /etc/nginx/conf.d/
COPY ./www /var/lib/nginx/html

CMD ["nginx"]
