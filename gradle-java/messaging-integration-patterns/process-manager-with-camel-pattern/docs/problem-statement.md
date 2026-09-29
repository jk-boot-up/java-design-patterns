# Problem Statement

## The scenario

Orders pass through reserve stock, payment and shipping, each a separate
service.

## The naive version

Steps handing on to each other leave reserved stock stranded when payment
fails, and nobody knows where an order is.

## What this project must deliver

- A chain that strands stock on a declined card.
- A saga route owning each journey.
- A branch to a partner warehouse.
- Compensation releasing stock, and a cancellation route.
- A status for every order, and the costs.
- Every printed result asserted by a test.
