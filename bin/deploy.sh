#!/bin/bash

# Prepare environment
shopt -s extglob
shopt -s expand_aliases
source $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/env.sh

source ${PROJECT_HOME}/.env > /dev/null 2>&1

PHEX_DIST=${PROJECT_HOME}/dist

ensure_directory ${PHEX_DIST}
ensure_directory ${PHEX_DIST}/bin
ensure_directory ${PHEX_DIST}/appliance/database
ensure_directory ${PHEX_DIST}/appliance/gateway
ensure_directory ${PHEX_DIST}/appliance/identity
ensure_directory ${PHEX_DIST}/appliance/api
ensure_directory ${PHEX_DIST}/packages

info "Aktualisiere Shell-Skripte"
rsync -r --verbose ${PROJECT_HOME}/bin/ ${PHEX_DIST}/bin/
info "Aktualisiere Docker Compose Dateien"
cp -fv ${PROJECT_HOME}/*.yml ${PHEX_DIST}

info "Aktualisiere Datenbank Konfiguration"
rsync -r --verbose --exclude *.gz ${PROJECT_HOME}/appliance/database/ ${PHEX_DIST}/appliance/database/
info "Aktualisiere Gateway Konfiguration"
rsync -r --verbose --exclude *.gz ${PROJECT_HOME}/appliance/gateway/ ${PHEX_DIST}/appliance/gateway/
info "Aktualisiere Identity Provider Konfiguration"
rsync -r --verbose --exclude *.gz ${PROJECT_HOME}/appliance/identity/ ${PHEX_DIST}/appliance/identity/
info "Aktualisiere API Konfiguration"
rsync -r --verbose --exclude .env.${USER} --exclude .env.development ${PROJECT_HOME}/appliance/api/ ${PHEX_DIST}/appliance/api/
rsync -r --verbose --exclude *.gz ${PROJECT_HOME}/packages/core/ ${PHEX_DIST}/packages/core/
rsync -r --verbose --exclude *.gz ${PROJECT_HOME}/packages/security/ ${PHEX_DIST}/packages/security/
# info "Aktualisiere Monitoring Konfiguration"
# rsync -r --verbose --delete ${PROJECT_HOME}/appliance/monitoring/ ${PHEX_DIST}/appliance/monitoring/

info "Aktualisiere Services im Produktivsystem"
rsync -azP ${PHEX_DIST}/ ${DEPLOYMENT_HOST}:/opt/phex/
