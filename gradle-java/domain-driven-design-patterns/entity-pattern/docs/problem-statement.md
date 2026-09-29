# Problem Statement

## The scenario

Customers change their details over time, and some share names and emails.

## The naive version

`CustomerRecord` compares all fields. An email change makes a "new" customer
whose orders cannot be found, and two look-alike people become one.

## What this project must deliver

- A value-compared customer losing its orders after an email change.
- An entity with an ID, compared by ID only.
- Look-alike customers kept apart.
- A history of changes under one ID.
- The cost shown: a stale copy that is still equal.
- Every printed result asserted by a test.
