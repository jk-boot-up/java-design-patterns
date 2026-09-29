# Table Data Gateway, Explained

## The pattern in one sentence

A table data gateway is one class per table that holds all of that table's
SQL, so the rest of the program asks plain questions and gets plain records
back.

## The 5 acts

### 1. SQL in every caller

`ProductPage`, `StockReport` and `CheckoutSql` each hold their own SQL for the
product table. They work: the kettle has 4 in stock, one product is out of
stock, checkout takes one kettle. Then the database team renames the `stock`
column to `quantity`, and all three fail with `Column "STOCK" not found`.

### 2. A table data gateway

`ProductGateway` holds every piece of SQL for the product table:
`findBySku`, `cheaperThan`, `countOutOfStock`, `takeStock`. The page, report
and checkout now call those methods and receive `Row` records. Everything
works as before, and one new question, products cheaper than £10, returns the
tea towel and the mug.

### 3. A rename, fixed once

The column is renamed again. This time the column's name lives in one place,
the gateway, which is told its new name once. The product page, the stock
report and checkout work without any change: 3 in stock, 1 out of stock, then
2 after checkout.

### 4. Where the SQL lives

Scanning the source: three classes in the old `scattered` package mention the
product table. In the new code, no caller does; only the gateway does. Callers
receive plain `Row` records, with no connections, result sets or SQL.

### 5. The bill

A `Row` is data only. A rule such as "low on stock means fewer than five" has
nowhere to live but the callers, where it will be written more than once. And
the gateway grows a method for every question anyone asks the table.

## The verdict

Use a gateway as soon as more than one part of a program touches a table. Keep
SQL, connections and result sets inside it, return records, and move to
Repository or Data Mapper when rows start needing behaviour.

## How to recognise this in code you did not write

- Classes named `...Dao`, `...Gateway` or `...Table`, one per table.
- Methods like `findBy...`, `insert`, `update`, `delete` returning records or DTOs.
- Callers with no `java.sql` imports.

## Where you have already met this

- DAO classes (Data Access Objects), such as `ProductDao`.
- Spring's `JdbcTemplate` wrapped in one class per table.
- MyBatis mapper interfaces, one per table.
