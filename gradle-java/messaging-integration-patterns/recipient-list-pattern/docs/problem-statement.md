# Problem Statement

## The scenario

Orders contain items from different categories, each shipped by a different
warehouse, and some need fraud review or gift wrap.

## The naive version

Every order is sent to every warehouse: twenty deliveries for five orders,
when eight were needed.

## What this project must deliver

- Broadcast deliveries counted against those needed.
- Recipients computed from each order's categories.
- Rules adding fraud review and gift wrap.
- A changed table rerouting kitchen items.
- A half-sent order when one recipient is down.
- Every printed result asserted by a test.
