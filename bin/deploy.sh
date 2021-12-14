#!/bin/bash

# Prepare environment
shopt -s extglob
shopt -s expand_aliases
source $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh

source ${PROJECT_HOME}/.env > /dev/null 2>&1

PHEX_DIST=${PROJECT_HOME}/dist

ensure_directory ${PHEX_DIST}
ensure_directory ${PHEX_DIST}/bin
ensure_directory ${PHEX_DIST}/appliance/gateway
ensure_directory ${PHEX_DIST}/appliance/database

info "Aktualisiere Shell-Skripte"
rsync -r --verbose ${PROJECT_HOME}/bin/ ${PHEX_DIST}/bin/
info "Aktualisiere Docker Compose Dateien"
cp -fv ${PROJECT_HOME}/*.yml ${PHEX_DIST}

info "Aktualisiere Datenbank Konfiguration"
rsync -r --verbose --exclude *.gz ${PROJECT_HOME}/appliance/database/ ${PHEX_DIST}/appliance/database/
# info "Aktualisiere Monitoring Konfiguration"
# rsync -r --verbose --delete ${PROJECT_HOME}/appliance/monitoring/ ${PHEX_DIST}/appliance/monitoring/

info "Aktualisiere Services im Produktionssystem"
rsync -azP ${PHEX_DIST}/ ${DEPLOYMENT_HOST}:/opt/phex/
