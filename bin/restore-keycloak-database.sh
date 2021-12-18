#!/bin/bash

# Prepare environment
shopt -s expand_aliases
source $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh

source ${PROJECT_HOME}/.env > /dev/null 2>&1

PGPASSWORD=${DATABASE_USER_PASSWORD}
db exec -T db psql --username=phex identity < ${PROJECT_HOME}/appliance/database/initdb.d/10-identity.sql.gz
