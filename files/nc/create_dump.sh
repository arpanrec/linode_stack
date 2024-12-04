#!/usr/bin/env bash
set -euo pipefail

backup_id=$(date +%Y-%m-%d-%H-%M-%S)
current_dir="${CS_NC_EXTERNAL_DRIVE_MOUNT_DATA_DUMP_PATH}/current"

mkdir -p "${current_dir}"

echo "${backup_id}:: Backup ID: ${backup_id}"

echo "${backup_id}:: Turning on maintenance mode"
sudo -u "${CS_NC_RUN_USER}" php "${CS_NC_WEB_DIR}/occ" maintenance:mode --on

echo "${backup_id}:: Syncing data directory"
rsync --acls --archive --one-file-system --progress \
    --verbose --delete-before --recursive "${CS_NC_ROOT_DIR}/" "${current_dir}/"

echo "${backup_id}:: Creating database dump in tar format"
docker run --rm \
    -v "${CS_NC_DB_CHAIN_PEM_FILE}":/ca-certificates.crt:ro \
    -v "${CS_NC_DB_CERT_PEM_FILE}":/client-cert.pem:ro \
    -v "${CS_NC_DB_PRIVKEY_PEM_FILE}":/client-key.pem:ro \
    -v "${current_dir}:/backup" \
    -e PGPASSWORD="${CS_NC_DB_PASSWORD}" -e PGSSLMODE=verify-full -e PGDATABASE="${CS_NC_DB_DATABASE}" \
    -e PGSSLROOTCERT=/ca-certificates.crt -e PGSSLCERT=/client-cert.pem -e PGSSLKEY=/client-key.pem \
    -e PGUSER="${CS_NC_DB_USER}" -e PGHOST="${CS_NC_DB_HOST}" -e PGPORT="${CS_NC_DB_PORT}" \
    --entrypoint "" \
    "${CS_NC_DB_DOCKER_IMAGE}":"${CS_NC_DB_VERSION}" pg_dump -F tar -f /backup/pgsql-db.tar

echo "${backup_id}:: Creating database dump in plain text"
docker run --rm \
    -v "${CS_NC_DB_CHAIN_PEM_FILE}":/ca-certificates.crt:ro \
    -v "${CS_NC_DB_CERT_PEM_FILE}":/client-cert.pem:ro \
    -v "${CS_NC_DB_PRIVKEY_PEM_FILE}":/client-key.pem:ro \
    -v "${current_dir}:/backup" \
    -e PGPASSWORD="${CS_NC_DB_PASSWORD}" -e PGSSLMODE=verify-full -e PGDATABASE="${CS_NC_DB_DATABASE}" \
    -e PGSSLROOTCERT=/ca-certificates.crt -e PGSSLCERT=/client-cert.pem -e PGSSLKEY=/client-key.pem \
    -e PGUSER="${CS_NC_DB_USER}" -e PGHOST="${CS_NC_DB_HOST}" -e PGPORT="${CS_NC_DB_PORT}" \
    --entrypoint "" \
    "${CS_NC_DB_DOCKER_IMAGE}":"${CS_NC_DB_VERSION}" pg_dump -f /backup/pgsql-db.sql

echo "${backup_id}:: Turning off maintenance mode"
sudo -u "${CS_NC_RUN_USER}" php "${CS_NC_WEB_DIR}/occ" maintenance:mode --off

echo "${backup_id}:: Creating tarball"
tar --use-compress-program=zstdmt -cf "${CS_NC_EXTERNAL_DRIVE_MOUNT_DATA_DUMP_PATH}/${backup_id}.tar" \
    -C "${current_dir}" .

echo "${backup_id}:: Truncating log file"
truncate -s 0 "${CS_NC_LOG_FILE}"

echo "${backup_id}:: Changing ownership of the dump directory"
chown -R "${CS_NC_RUN_USER}":"${CS_NC_RUN_GROUP}" "${CS_NC_EXTERNAL_DRIVE_MOUNT_DATA_DUMP_PATH}"

echo "${backup_id}:: Done"

exit 0
