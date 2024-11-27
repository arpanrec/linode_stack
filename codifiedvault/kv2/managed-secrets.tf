resource "vault_mount" "secmanaged-secretsret" {
  path        = "managed-secrets"
  type        = "kv-v2"
  description = "managed-secrets"
  options = {
    version              = 2
    cas_required         = false
    max_versions         = 20
    delete_version_after = "0s"
  }
}
