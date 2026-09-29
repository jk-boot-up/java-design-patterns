# Problem Statement

## The scenario

The phone app draws an order screen from five facts and changes deliveries
over a slow mobile network.

## The naive version

A call per fact costs five round trips, and a change split over two calls can
fail halfway.

## What this project must deliver

- Five round trips measured.
- One JSON summary from a record.
- An all-or-nothing delivery change with a 422 problem report.
- Business rules kept on the fine-grained Order.
- The over-fetching cost.
- Every printed result asserted by a test.
