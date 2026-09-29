# Problem Statement

## The scenario

Orders move through placed, paid, shipped and delivered, and can be cancelled,
refunded and, later, returned.

## The naive version

`IfElseOrder` checks the status inside each method, differently each time. A
delivered order can be cancelled and a refund can be paid twice, and nothing in
the code looks wrong.

## What this project must deliver

- The two scattered-if bugs shown with printed results.
- A transition table that prints its own rows.
- Moves not in the table refused with a message naming the move and the status.
- The allowed actions for a status, for showing buttons.
- A new rule (returns) added with two rows and no other change.
- Every printed result asserted by a test.
