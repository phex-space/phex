#!/usr/bin/env bash

export SCRIPT_HOME="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PROJECT_HOME="$( cd "$SCRIPT_HOME/.." >/dev/null 2>&1 ; pwd -P )"

cd "${PROJECT_HOME}"
cp hooks/* .git/hooks
