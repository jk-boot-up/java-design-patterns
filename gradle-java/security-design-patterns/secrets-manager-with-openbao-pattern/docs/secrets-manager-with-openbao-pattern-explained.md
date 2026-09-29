# Secrets Manager with OpenBao, Explained

## The pattern in one sentence

With OpenBao, secrets live at paths, policies decide who may read them, each
service holds a revocable token, and every change is a new version.

## The 5 acts

### 1. A key in the code

The payment key is written into the code as a constant and built into
checkout, refunds and subscriptions. Everyone who can read the repository can
read it, and every old copy stays in the history.

### 2. Policies and tokens

The key is stored in OpenBao's key-value store. A policy called payments
allows reading that one path. Checkout gets a token carrying the policy and
reads the key: HTTP 200. The catalog service gets a token without it and is
refused: HTTP 403, permission denied.

### 3. Versions and rotation

Writing a new value creates version 2 of the secret, and checkout now reads
pay-key-v2 with no rebuild. OpenBao keeps version 1, so it can still be read
while the payment company accepts both during the change-over.

### 4. Revoke a leaked token

Checkout's token appears in a log that leaked. It is revoked at once. The
attacker using it gets HTTP 403. Checkout is given a new token and reads the
key as before; the key itself can also be rotated, as in act three.

### 5. The bill

Every service still needs one first credential to get its token; the answer
is the platform's own identity, such as AppRole or Kubernetes auth. And this
demo's server runs in development mode: in memory, unsealed and with a root
token. Production needs real storage, unsealing and high availability,
because every service now depends on it to start.

## The verdict

Use a secrets manager for every real secret. Write narrow policies, give each
service its own token from a platform identity, rotate secrets as versions,
revoke leaks at once, and run the server for high availability.

## How to recognise this in code you did not write

- `X-Vault-Token` headers and `/v1/secret/data/...` paths.
- Policies written as `path "..." { capabilities = ["read"] }`.
- `spring.cloud.vault` settings in configuration.

## Where you have already met this

- HashiCorp Vault, whose API OpenBao keeps.
- AWS Secrets Manager, Azure Key Vault and Google Secret Manager.
- Spring Cloud Vault, which reads Vault-compatible servers into Spring configuration.
