# Problem Statement

## The scenario

The store sells books, food and electronics, each with shared fields and one
field of its own.

## The naive version

`TablePerType` keeps a table per type, so every question about all products
asks every table.

## What this project must deliver

- Three queries for one question with a table per type.
- One table with a type column, and one query.
- Rows loaded as the right class.
- A new type added with one class and one column.
- Empty cells and a missing NOT NULL rule shown.
- Every printed result asserted by a test, against a real in-memory database.
