#!/bin/sh
sudo update-ca-certificates
JSON_BIN=/var/www/${COMPANY_NAME}/documentserver/npm/json
${JSON_BIN} -f /etc/onlyoffice/documentserver/default.json -I \
    -e 'this.services.CoAuthoring.requestDefaults.agentOptions={}'
ca_content=$(awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' /usr/local/share/ca-certificates/ownca.crt)
${JSON_BIN} -f /etc/onlyoffice/documentserver/default.json -I \
    -e 'this.services.CoAuthoring.requestDefaults.agentOptions.ca="'"${ca_content}"'"'
/app/ds/run-document-server.sh
