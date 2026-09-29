# Problem Statement

## The scenario

The order service answered the internet directly and held the database
password.

## The naive version

Internal-only features, a spoofable admin header and a path to the admin
export, were reachable by anyone.

## What this project must deliver

- A directly exposed service leaking every order two ways.
- NGINX removing the internal header.
- An allow-list of locations and methods.
- Size and shape limits.
- A real check that the gate holds no secrets.
- Every printed result asserted by a test, skipped without Docker.
