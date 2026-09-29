# Problem Statement

## The scenario

Customers add 2 MB photos to reviews, and the app server carries every byte.

## The naive version

Proxying uploads through the app wastes its bandwidth and memory on data it
never needs to see.

## What this project must deliver

- Uploads carried through the app server.
- An S3 presigned PUT URL used directly by the browser.
- Refusals for the wrong method, object and size.
- An expired URL refused.
- A leaked URL, and an emulator's limit, named honestly.
- Every printed result asserted by a test, skipped without Docker.
