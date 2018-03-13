#!/bin/bash

echoerr() { if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }

# process arguments
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
