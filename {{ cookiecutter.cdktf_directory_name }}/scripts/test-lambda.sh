#!/usr/bin/env bash

set -euo pipefail


json_input=$(cat <<EOF
{
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
}
EOF
)

payload=$(echo "$json_input" | jq --compact-output '{body: (tojson), IsBase64Encoded: false}')

curl -vvv -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
    --data-binary "$payload"
