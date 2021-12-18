#!/bin/bash

export PATH=/bin:/usr/bin:/usr/local/bin:PATH

export SCRIPT_HOME="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PROJECT_HOME="$( cd "$SCRIPT_HOME/.." >/dev/null 2>&1 ; pwd -P )"

alias gw="docker-compose -f ${PROJECT_HOME}/docker-compose.gateway.yml --env-file ${PROJECT_HOME}/.env -p gateway"
alias db="docker-compose -f ${PROJECT_HOME}/docker-compose.data.yml --env-file ${PROJECT_HOME}/.env -p data"

info() { printf "%s [INFO] - %s\n" "$( date )" "$*" >&2; }

info "SCRIPT_HOME:  $SCRIPT_HOME"
info "PROJECT_HOME: $PROJECT_HOME"

rotate() {
    # usage: rotate /path/to/map-0.jpg
    local dest=$1
    local dest_dir=$(dirname "$dest")
    local dest_prefix=$(basename "${dest%-*}")
    local dest_ext=${dest#*.}
    local i
    for i in {6..0}; do
      if [ -f "$dest_dir/${dest_prefix}-$((i)).$dest_ext" ]
      then
        mv "$dest_dir/${dest_prefix}-$((i)).$dest_ext" "$dest_dir/${dest_prefix}-$((i+1)).$dest_ext"
      fi
    done
}

ensure_directory() {
  local target=$1
  if [ ! -d $target ]; then
    mkdir -p $target
  fi
}
