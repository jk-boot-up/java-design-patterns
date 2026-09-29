# Problem Statement

## The scenario

The product page, stock report and checkout each wrote their own JDBC.

## The naive version

Hand-written JDBC leaks connections when a close is forgotten, and scatters
SQL that breaks together on a schema change.

## What this project must deliver

- A connection leak draining a real pool.
- A gateway on JdbcTemplate with row mapping.
- Spring's translated exceptions.
- An atomic stock update.
- The cost of rows without rules.
- Every printed result asserted by a test.
