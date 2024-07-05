# MinIO

Install the minio server on a single node.

## Requirements

Secrets in `.env` file:

```env
INIT_STORAGE_MINIO_DOMAIN='Hostname for minio'
INIT_STORAGE_MINIO_PROTOCOL=https
INIT_STORAGE_MINIO_PORT=9000
INIT_STORAGE_MINIO_CONSOLE_PORT=9001
INIT_STORAGE_MINIO_ROOT_USER=svc_minio_admin
INIT_STORAGE_MINIO_ROOT_PASSWORD='Password for root user (Not access key/secret credentials)'
INIT_STORAGE_MINIO_EMAIL='MinIO Admin email address'
INIT_STORAGE_MINIO_CERT_PRIV_KEY_BASE64='Base64 encoded private key'
INIT_STORAGE_MINIO_CERT_FULL_CHAIN_BASE64='Base64 encoded full certificate chain'
```

The first argument to [minio-install.sh](/minio-install.sh) is the path to the `.env` file.

raw script: <https://raw.githubusercontent.com/arpanrec/minio-install/main/minio-install.sh>

```bash
sudo -H -u root bash -c "/bin/bash <(curl https://raw.githubusercontent.com/arpanrec/minio-install/main/minio-install.sh) $(realpath .env)"
```

### Post-installation

In the MinIO Console Set the region to `ap-south-1`

## License

[GLWTS](/LICENSE)
