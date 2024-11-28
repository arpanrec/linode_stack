data "vault_policy_document" "minio-kes" {
  rule {
    path         = "kv/minio/kes/kms/*"
    capabilities = ["create", "read", "delete", "update", "list"]
    description  = "All operations on the minio/kes/kms path"
  }
  # https://developer.hashicorp.com/vault/tutorials/policies/policy-templating#challenge
  rule {
    path         = "managed-secrets/data/minio-kes/clusters/+/kms/*"
    capabilities = ["create", "read"]
    description  = "read and write credentials"
  }

  # https://developer.hashicorp.com/vault/tutorials/policies/policy-templating#challenge
  rule {
    path         = "managed-secrets/metadata/minio-kes/clusters/+/kms/*"
    capabilities = ["list", "delete"]
    description  = "delete and list credentials"
  }
}

resource "vault_policy" "minio-kes" {
  name   = "minio-kes"
  policy = data.vault_policy_document.minio-kes.hcl
}
