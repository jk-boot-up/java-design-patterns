# Problem Statement

## The scenario

Order confirmation emails wait on a queue while the email provider is slow.

## The naive version

Messages the broker holds only in memory vanish when it restarts.

## What this project must deliver

- Transient messages lost on a durable queue.
- Persistent messages with publisher confirms surviving a restart.
- Manual acknowledgements so each email is sent once.
- A crash before acknowledging, and the redelivered flag.
- The cost named.
- Every printed result asserted by a test, skipped without Docker.
