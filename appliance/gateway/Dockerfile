FROM nginx:mainline

COPY ./conf.d/default.conf \
    ./conf.d/api.phex.local.crt ./conf.d/api.phex.local.key \
    ./conf.d/identity.phex.local.crt ./conf.d/identity.phex.local.key \
    ./conf.d/phex.local.crt ./conf.d/phex.local.key \
    /etc/nginx/conf.d/
