# Template Method with Spring, Explained

## The pattern in one sentence

In Spring, a template owns the fixed steps of a task, and you hand it a lambda for the one step that differs.

## What is new here

The pattern is [Template Method](../template-method-pattern). This page is only what Spring Boot adds.

### Plain JDBC Leaks

Plain JDBC closes on the happy path only. A typo in the SQL throws before the close, and one connection stays in use.

```
  a good query returns [ORD-000001, ORD-000002, ORD-000003]. connections in use afterwards: 0.
  a query with a typo throws JdbcSQLSyntaxErrorException. connections in use afterwards: 1.
  the pool has two connections, so a second typo leaves one, and a third waits for a connection that never comes back.
```

### The Template Closes On Every Path

The same query through JdbcTemplate closes on every path. The typo, three times, leaves nothing in use.

```
  a good query returns [ORD-000001, ORD-000002, ORD-000003]. connections in use afterwards: 0.
  the same typo, three times: connections in use afterwards: 0.
```

### What Is Ours

The only code that is ours is a lambda that turns a row into an order. Everything else is the template's.

```
  asha's orders: [Order[orderNumber=ORD-000001, customer=asha, totalPence=2499], Order[orderNumber=ORD-000003, customer=asha, totalPence=1250]]
  we wrote one lambda, which turns a row into an Order. The template opened the
  connection, prepared the statement, bound the customer, ran it, walked the rows,
  and closed everything.
```

### Exceptions, Translated

By hand, you catch a checked exception with a vendor state code. The template translates it into Spring's own unchecked hierarchy.

```
  by hand: JdbcSQLSyntaxErrorException, a checked exception, SQL state 42S02.
  template: BadSqlGrammarException, unchecked, the same on every database.
  a repeated order number: DuplicateKeyException.
```

### What The Template Decides

Ask for one row and the template treats none, and two, as errors. That is a decision the template made, and it is nowhere in your code.

```
  one row expected, none found: EmptyResultDataAccessException.
  one row expected, two found: IncorrectResultSizeDataAccessException.
  the fixed steps are the template's. What counts as a missing row is a decision it made for you.
```

### A Transaction Is A Template Too

A transaction template owns begin, commit and rollback. The failed checkout inserted an order row first, and it was undone when the stock update failed.

```
  before: 3 orders, 3 mugs on hand.
  after a good checkout: 4 orders, 1 mug on hand.
  a checkout for 4 mugs fails: DataIntegrityViolationException.
  after it: 4 orders, 1 mug on hand. the order row was rolled back.
```

## The verdict

Use the template, not the raw API. Learn what it decides for you. Keep the lambda small. Catch the translated exceptions, not vendor codes.

## How to recognise this in code you did not write

- `jdbcTemplate.query(sql, rowMapper)`.
- `transactionTemplate.execute(...)`.
- Other Spring `*Template` classes: `RestTemplate`, `KafkaTemplate`, `JmsTemplate`.

## Where you have already met this

Every Spring `*Template` class. Each owns the fixed steps of talking to something and asks for the step that differs.

## When this is too much

For one query in a script, plain JDBC with try-with-resources is fine. The template earns its place when many callers repeat the fixed steps.
