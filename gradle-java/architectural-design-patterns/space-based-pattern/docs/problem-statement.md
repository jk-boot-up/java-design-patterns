# Problem Statement

## The scenario

A kettle flash sale sends hundreds of orders at once, and every order checks
and updates stock.

## The naive version

Every app server asks one central database, one query at a time, so adding
servers does not add capacity.

## What this project must deliver

- Central-database timing that more servers do not improve.
- Processing units serving orders from memory.
- A data grid replicating changes between units.
- A background writer updating the database in batches.
- The cost shown: the last kettle sold twice.
- Every printed result asserted by a test.
