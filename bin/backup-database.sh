#!/bin/bash

# Prepare environment
shopt -s expand_aliases
source $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh

BACKUP_HOME=${PROJECT_HOME}/backup
ensure_directory ${BACKUP_HOME}

source ${PROJECT_HOME}/.env > /dev/null 2>&1

rotate ${BACKUP_HOME}/identity-0.sql.gz

info "Backup keycloak database."
PGPASSWORD=${DATABASE_USER_PASSWORD}
db exec -T db pg_dump --username=phex identity > ${BACKUP_HOME}/identity-0.sql
gzip ${BACKUP_HOME}/identity-0.sql

cp ${BACKUP_HOME}/identity-0.sql.gz ${PROJECT_HOME}/appliance/database/initdb.d/10-identity.sql.gz
