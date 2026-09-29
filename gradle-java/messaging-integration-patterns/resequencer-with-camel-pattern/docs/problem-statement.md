# Problem Statement

## The scenario

Order-status updates travel different paths and reach the tracking page out
of order.

## The naive version

Applying them as they arrive leaves the page on the wrong final status.

## What this project must deliver

- Out-of-order updates applied as they arrive.
- Camel's stream resequencer, and its first-message delay.
- Camel's batch resequencer, and its wait for a full batch.
- Two orders' updates sorted in batch mode.
- A lost update given up after a timeout.
- Every printed result asserted by a test.
