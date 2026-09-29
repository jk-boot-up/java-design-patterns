# Problem Statement

## The scenario

Customers upload photos to their product reviews; files live in a separate
storage service.

## The naive version

Every photo is uploaded to the app server and sent on to storage: 40 MB
through the app for ten photos.

## What this project must deliver

- Bytes carried by the app server counted.
- A signed key allowing one upload directly to storage.
- Wrong method, path and size refused.
- An expired key refused.
- The leaked-key risk shown.
- Every printed result asserted by a test, over real HTTP.
