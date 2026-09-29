# Problem Statement

## The scenario

Orders are immutable records three levels deep: order, customer, address.

## The naive version

Changing a postcode meant rebuilding all three by hand, and street and city
were swapped without any error.

## What this project must deliver

- A hand rebuild with swapped arguments.
- A `Lens` record with `get`, `set`, `modify` and `andThen`.
- Joined lenses from order to postcode.
- Modify with a function, and two lenses together.
- The cost, and structural sharing shown.
- The three lens laws checked by tests.
