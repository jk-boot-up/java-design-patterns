# Table Data Gateway with JdbcTemplate, Explained

## The pattern in one sentence

With JdbcTemplate, a table data gateway keeps one table's SQL in one class
while Spring handles connections, row mapping and error translation.

## The 5 acts

### 1. Hand-written JDBC that leaks

A product page writes its own JDBC and forgets to close the connection it
borrowed from the pool. The pool holds two connections. The page works twice,
and the third time it waits a quarter of a second for a connection that will
never come back, and fails.

### 2. A gateway on JdbcTemplate

Now all the product SQL lives in one gateway built on JdbcTemplate. The
product page is asked four times on the same pool of two, and works every
time, because JdbcTemplate always returns the connection. The stock report
finds one product out of stock, and the cheaper-than-£10 list is the mug and
the tea towel, each row mapped to a Row record by column name.

### 3. Errors that mean something

The column is renamed behind the gateway's back, and the next query fails
with Spring's BadSqlGrammarException rather than a vendor's error code. A
second product with the key MUG-1 fails with DuplicateKeyException. The same
exception types come back whatever database is used, so callers can react to
them.

### 4. Stock in one statement

Four customers try for the two desk lamps. The gateway takes stock in one
statement, UPDATE ... WHERE quantity > 0, and reports whether a row changed.
Two are taken, stock ends at zero, and it can never go below.

### 5. The bill

A Row is only data: whether a product is low on stock is still decided by
each caller. The gateway grows a method for every question anyone asks the
table. And its SQL is still text, checked only when it runs.

## The verdict

Use a JdbcTemplate gateway when several parts of the code share a table and
you want plain SQL with safe plumbing. Map to records, catch Spring's
exceptions, and keep business rules out of the gateway.

## How to recognise this in code you did not write

- `@Repository` classes holding `JdbcTemplate` calls.
- `jdbc.query(sql, params, rowMapper)`.
- `catch (DuplicateKeyException e)`.

## Where you have already met this

- Spring `@Repository` classes built on `JdbcTemplate`.
- Spring Data JDBC and jOOQ, which generate or type the SQL.
- DAO classes, the older name for the same idea.
