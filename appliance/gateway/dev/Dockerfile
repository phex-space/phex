FROM alpine:3.15

RUN  apk update && apk upgrade --available && sync \
    && mkdir -p /run/nginx \
    && apk add --no-cache nginx-mod-http-lua

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./conf.d/ /etc/nginx/conf.d/

CMD ["nginx"]
