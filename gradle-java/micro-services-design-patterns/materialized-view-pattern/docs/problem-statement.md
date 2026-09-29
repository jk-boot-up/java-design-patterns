# Problem Statement

## The scenario

The "my orders" page shows each order's product, quantity and shipping status.
Orders, shipping and product names live in three separate services.

## The naive version

`QueryOnRead` asks all three services on every visit: one call for the orders,
then two per order. Seven calls for three orders, and the page fails if any
service is down.

## What this project must deliver

- The call count and waiting time for the page built on every visit (7 calls, about 280 ms).
- The same page served from a view with 0 service calls, while the catalogue is down.
- The lag shown: a shipped order still reading placed until its event arrives.
- A view rebuilt from the event log that matches the original.
- The costs shown: a rename rewriting 2 rows, and every row stored twice.
- Every printed number asserted by a test.
