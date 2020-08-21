#!/bin/bash

set -e

curl -o /tmp/github-workflow.json https://raw.githubusercontent.com/Logerfo/schemastore/master/src/schemas/json/github-workflow.json

for i in */.github/workflows/*.yml
do
    name=$(basename "$i")
    cat $i | python3 -c 'import json, sys; from ruamel import yaml ; y=yaml.safe_load(sys.stdin.read()) ; json.dump(y, sys.stdout)' > /tmp/workflow-lint-$name.json
    echo "Validating GitHub workflow $i"
    jsonschema -i /tmp/workflow-lint-$name.json /tmp/github-workflow.json
done
