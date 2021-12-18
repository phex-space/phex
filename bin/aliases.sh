#!/bin/bash
echo "$0"
SCRIPT_HOME="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_HOME="$( cd "$SCRIPT_HOME/.." >/dev/null 2>&1 ; pwd -P )"

alias gw="docker-compose -f ${PROJECT_HOME}/docker-compose.gateway.yml --env-file ${PROJECT_HOME}/.env -p gateway"
alias db="docker-compose -f ${PROJECT_HOME}/docker-compose.data.yml --env-file ${PROJECT_HOME}/.env -p data"
alias idp="docker-compose -f ${PROJECT_HOME}/docker-compose.identity.yml --env-file ${PROJECT_HOME}/.env -p identity"
alias api="docker-compose -f ${PROJECT_HOME}/docker-compose.api.yml --env-file ${PROJECT_HOME}/.env -p api"
