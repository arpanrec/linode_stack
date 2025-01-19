#!/usr/bin/env bash
set -euo pipefail

__mysql_root_password="root@1234"

tee mysql-init.sql <<EOF
ALTER USER 'root'@'%' IDENTIFIED BY '$__mysql_root_password';
FLUSH PRIVILEGES;
EOF

docker volume create mysql_data || true

docker rm -f mysql-docker

docker run -d --name mysql-docker \
    -e MYSQL_ROOT_PASSWORD=$__mysql_root_password \
    -p 3306:3306 -v mysql_data:/var/lib/mysql \
    mariadb:10.11

sleep 10

docker rm -f mysql-docker

docker run -d --name mysql-docker \
    -e MYSQL_ROOT_PASSWORD=$__mysql_root_password \
    -p 3306:3306 -v mysql_data:/var/lib/mysql -v "$(pwd)/mysql-init.sql:/mysql-init.sql" \
    mariadb:10.11 mysqld --init-file=/mysql-init.sql

sleep 10
