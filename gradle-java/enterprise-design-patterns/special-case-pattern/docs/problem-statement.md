# Problem Statement

## The scenario

Checkout serves registered customers, guests without accounts, and old orders
from deleted accounts.

## The naive version

The lookup returns `null` for guests and deleted accounts, and checkout checks
for null in four places. The points line forgot, and the first guest crashed
checkout.

## What this project must deliver

- The crash shown: a NullPointerException for a guest.
- A Guest special case with no discount, no points and no newsletter.
- An Unknown special case for deleted accounts that keeps the old ID.
- Checkout with no null checks and no type checks.
- The cost shown: a mistyped ID hidden as a former customer.
- Every printed result asserted by a test.
