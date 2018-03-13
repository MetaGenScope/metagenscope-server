#!/bin/bash

# Usage:
#     startup.sh [host:port[, host:port, ...]] -- [command]
#
# Iterate through arguments before '--', waiting for each
# service to accept TCP connections. Finally, execute
# everything after '--'.
#
# Ex.
#     Wait for Postgres and Mongo DBs running on localhost
#     before starting the application would look like this.
#
#     startup.sh localhost:5435 localhost:27020 -- python manage.py runserver

echoerr() { if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }

# '$#' is equal to the number of positional parameters
while [[ $# -gt 0 ]]
do
    case "$1" in
        *:* )
            ./wait-for-it.sh "$1"
            RC=$?
            if [[ $RC != 0 ]]; then
                exit $RC;
            fi
            shift 1
            ;;
        --)
            shift
            CLI=("$@")
            if [[ $CLI != "" ]]; then
                exec "${CLI[@]}"
            fi
            echoerr "No CLI argument provided!"
            exit 1
            ;;
        *)
            echoerr "Unknown argument: $1"
            exit 1
            ;;
    esac
done
