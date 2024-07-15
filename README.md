# Core Services

## Nextcloud

Deploy a nextcloud storage server.

Deploy public facing core services on Linode.

Service: Mini0

## Requirements

- [Ansible](https://www.ansible.com/)
- [Linode API Token](https://www.linode.com/docs/guides/getting-started-with-the-linode-api/)
- GoDaddy Domain and API Key
- [Poetry](https://python-poetry.org/)

## Linode Domains

Creates a subdomain in linode to point to the server.

Add GoDaddy NS Records to point to Linode.

## Mini0

Creates a Linode instance with a extra volume attached to it.
Install Docker and deploy single kes and mini0 container.
Create a ACME certificate for the domain using acme `dns-01` challenge, Which automatically validates the domain by adding a TXT record to the Linode domains.

## Export Poetry dependencies

```bash
poetry export --without-hashes --format=requirements.txt --with dev > requirements-dev.txt
```
