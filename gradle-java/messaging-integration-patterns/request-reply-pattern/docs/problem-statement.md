# Problem Statement

## The scenario

Checkout reserves stock by sending requests to the inventory service over a
queue; the service works on several at once.

## The naive version

`InOrderRequester` takes replies in arrival order and matches them to
requests by position, swapping the kettle and mug answers.

## What this project must deliver

- Wrong matches shown when replies are taken in order.
- Unique IDs and correlation identifiers matching replies correctly.
- Return addresses separating two requesters' replies.
- Twenty requests in flight, all matched.
- A lost reply timing out and staying in the waiting table.
- Every printed result asserted by a test.
