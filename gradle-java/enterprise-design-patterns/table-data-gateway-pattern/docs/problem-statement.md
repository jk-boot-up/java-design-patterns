# Problem Statement

## The scenario

Three parts of the store read and update the product table.

## The naive version

The product page, stock report and checkout each hold their own SQL. Renaming
one column breaks all three.

## What this project must deliver

- Scattered SQL shown failing after a column rename.
- A gateway class holding every statement for the table.
- The rename fixed in one place.
- A scan showing which classes mention the table.
- Every printed result asserted by a test, against a real in-memory database.
