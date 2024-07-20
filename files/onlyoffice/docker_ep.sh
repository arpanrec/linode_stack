#!/bin/bash

python3 /pg_cert_updater.py

echo "Replacing ALLOW_CONFIG_MUTATIONS in /etc/supervisor/conf.d/ds-converter.conf and /etc/supervisor/conf.d/ds-docservice.conf"
sed -i '/^ALLOW_CONFIG_MUTATIONS=/d' /etc/supervisor/conf.d/ds-converter.conf
sed -i '/^ALLOW_CONFIG_MUTATIONS=/d' /etc/supervisor/conf.d/ds-docservice.conf

echo "ALLOW_CONFIG_MUTATIONS=true" >>/etc/supervisor/conf.d/ds-converter.conf
echo "ALLOW_CONFIG_MUTATIONS=true" >>/etc/supervisor/conf.d/ds-docservice.conf

supervisorctl restart all

/app/ds/run-document-server.sh
