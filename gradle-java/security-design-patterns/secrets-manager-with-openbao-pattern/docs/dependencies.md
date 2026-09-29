# Dependencies

This project uses OpenBao, which the plain Java version of Secrets Manager
does not. Skipping it loses none of the pattern: the plain version teaches all
of it with nothing installed.

## What OpenBao is

OpenBao is an open-source secrets manager, a fork of HashiCorp Vault run by the Linux Foundation, with the same HTTP API. The KV version 2 engine stores secrets at paths such as secret/data/payment-key, keeping every version. A policy is a set of rules over paths, such as read on that one path. A token is what a service presents with each request, in the X-Vault-Token header; it carries policies, and can be revoked. Development mode runs everything in memory, already unsealed, with a root token: for learning only.

## What Why not Vault is

HashiCorp Vault changed its licence in 2023 to the Business Source License, which is not an open-source licence. OpenBao continues the open-source code, so what you learn here applies to Vault too.

## What Testcontainers is

Testcontainers is a Java library that starts a container, here OpenBao, from inside a program, and removes it afterwards.

## Why this project uses them

The plain version shows the idea. This version shows the concepts every real
secrets manager shares: paths, policies, tokens, versions and revocation.

## What to install

Only a JDK, version 21, and a running Docker. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Docker | running; 24 or later |
| OpenBao image | openbao/openbao:2.7.0 |
| Testcontainers | 2.0.5 |

## What it costs

- A container runtime, and a first run that downloads the OpenBao image.
- A highly available secrets server to run in production.
