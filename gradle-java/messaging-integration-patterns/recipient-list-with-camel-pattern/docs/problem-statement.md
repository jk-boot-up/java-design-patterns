# Problem Statement

## The scenario

Five orders must reach the warehouses holding their items, plus fraud review
and gift wrap when rules say so.

## The naive version

Sending every order to every warehouse made twenty deliveries, most of them
useless.

## What this project must deliver

- Every order multicast to four warehouses.
- A recipient list asking a routing table per order.
- Rules adding fraud review and gift wrap.
- The table changed while routes run.
- A failed recipient reported, with the half-sent order shown.
- Every printed result asserted by a test.
