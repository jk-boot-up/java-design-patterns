# Problem Statement

## The scenario

The online store has customers. A customer has a name, an email address,
a postal address and loyalty points, and needs to be stored and loaded.

## The naive version: Active Record

The object saves itself. `customer.save()`. It works, and this project
shows it working before it shows the cost, because for a simple
application it is the right answer.

```
ONE. Active Record — the object saves itself, and it works well.
    INSERT customers id=1
    SELECT customers id=1
    UPDATE customers id=1
  3 operations, one class, one table.
```

## The cost

The customer class now knows the table name, the column names and the
database. It cannot be created without a database, so a rule about email
addresses needs a database to test. A change to the schema changes the
domain object.

```
TWO. The cost — the domain object cannot exist without the database.
  a plain Customer changed its email with no database anywhere.
```

And there is a shape it cannot say at all: one customer spread across
two tables, and one table feeding two different objects.

## What this project must deliver

A mapper class that moves data between a customer and its rows, so the
customer has no persistence code at all. It must also admit the bill: a
second class per entity, a mapping written by hand that can lose a field
without any error, and an indirection to understand before debugging.
