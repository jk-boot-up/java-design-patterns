# Secrets Manager, Explained

## The pattern in one sentence

A Secrets Manager keeps secrets in one guarded store, grants each service only
what it needs, logs every read, and rotates secrets without rebuilds.

## The 5 acts

### 1. A key in the code

The payment key is written in a configuration file that is committed with the
code and built into checkout, refunds and subscriptions. All forty people who
can read the repository can read the key, and every old copy of it stays in
the history. Changing it means editing, rebuilding and redeploying three
services.

### 2. A key in the manager

Now the key lives in a secrets manager, granted to the three payment services
only. Checkout reads it when it runs and charges 20.00. The catalog service
asks for the same key and is refused: it was never granted it. The key is in
no source file and no build.

### 3. Rotation without a rebuild

The key is rotated to version 2, and the payment company accepts both for a
while. At minute 2, checkout is still using its cached version 1, which still
works. At minute 5, its five-minute cache runs out and it fetches version 2.
At minute 10, version 1 is cancelled, and checkout carries on charging. No
code changed, nothing was rebuilt.

### 4. A leak

Version 2 leaks. It is rotated to version 3 and cancelled at once, with no
grace period. The attacker's charge is refused. Checkout's cached copy is
refused too, so on a refusal it fetches again straight away, gets version 3,
and charges. No code change, no rebuild, no redeploy.

### 5. The bill

Every read is logged: five so far, including catalog's refusal. But every
service now depends on the manager: if it is down when a service starts, the
service cannot get its keys. And each service still needs one first
credential to reach the manager, best given by the platform itself rather
than stored as yet another password.

## The verdict

Take every real secret out of code and builds. Grant per service, log reads,
cache for minutes, fetch again on refusal, rotate regularly, and give services
a platform identity to reach the manager.

## How to recognise this in code you did not write

- Configuration like `${vault:secret/payment-key}`.
- Startup code calling a secrets client.
- Rotation schedules and audit logs in a vault console.

## Where you have already met this

- HashiCorp Vault, AWS Secrets Manager, Azure Key Vault and Google Secret Manager.
- Kubernetes Secrets, often fed from one of the above.
- Spring Cloud Vault, which loads secrets into Spring configuration.
