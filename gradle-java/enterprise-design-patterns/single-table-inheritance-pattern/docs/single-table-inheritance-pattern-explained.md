# Single Table Inheritance, Explained

## The pattern in one sentence

Single table inheritance stores every subclass in one table with a type
column and a column for every field, leaving unused columns empty.

## The 5 acts

### 1. A table per type

`TablePerType` keeps `book`, `food` and `electronics` in separate tables. To
list everything under £10 it asks all three: three queries for breakfast tea
and a desk lamp. A fourth product type means a fourth table, and every
question about all products grows again.

### 2. One table for all

`ProductTable` keeps every product in one table: shared columns for code,
name and price, a `type` column, and one column for each type-specific field.
Everything under £10 is now one query on one table.

### 3. Each row becomes its own class

When rows are loaded, the type column decides which class to build. `BOOK-1`
becomes a `Book` whose packing note shows its ISBN; `KETTLE-1` becomes
`Electronics` with a 2-year warranty card; `TEA-1` becomes `Food` with its
best-before date.

### 4. A new type

Gift cards are added with a `GiftCard` class and one new column,
`value_pence`, added to the same table. Existing rows are untouched; they
simply leave the new column empty. `GIFT-1` loads as a `GiftCard`.

### 5. The bill

With five products and four type-specific columns, 15 of 20 cells are empty.
And the database can no longer keep type rules: the ISBN column cannot be
`NOT NULL`, because food and kettles leave it empty, so a book with no ISBN is
saved without complaint.

## The verdict

Use it when subclasses share most of their fields and are often queried
together. Keep type-specific fields few, add CHECK constraints for type rules,
and switch to another inheritance mapping when the table fills with empty
columns.

## How to recognise this in code you did not write

- A `type`, `kind` or `dtype` column in a table.
- `@Inheritance(strategy = SINGLE_TABLE)` in JPA code.
- Many nullable columns that are filled only for some rows.

## Where you have already met this

- JPA's `@Inheritance(strategy = SINGLE_TABLE)` with `@DiscriminatorColumn`.
- Ruby on Rails' `type` column on ActiveRecord models.
- Product tables in shop platforms with a `product_type` column.
