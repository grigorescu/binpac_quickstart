#!/bin/bash

set -e

ZEEK_VER=$1

env

for i in /tmp/workflow-lint-*.json
do
    jq -c '.jobs.test.steps[].run' "$i" | egrep . | egrep -v "^null$" | while read -r cmd
    do
        cd telnet_analyzer
        cmd=$(echo "$cmd" | sed -e 's/$GITHUB_WORKSPACE/$PWD/g')
        cmd=$(echo "$cmd" | sed -e 's/${{ matrix.zeek }}/'$ZEEK_VER'/g')
        cmd=$(echo "$cmd" | sed -e 's/^"//' | sed -e 's/"$//')
        echo "Running command: $cmd"
        eval "$(printf "$cmd")"
        cd -
    done
done
