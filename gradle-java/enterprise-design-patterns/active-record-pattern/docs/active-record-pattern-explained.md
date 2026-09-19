# Active Record, Explained

## The pattern in one sentence

An active record is an object that wraps one row of a database table, carries the rules about that row, and knows how to find, save and change itself.

## The six acts

### A Record That Saves Itself

An order is created, saved and found again in three lines, with nothing else needed.

```
  saved order 1 for customer 1, 1600 pence, DRAFT.
  three lines: new, save, find. no repository, no mapper.
```

### Finders On The Class

A finder on the class returns all three of a customer's orders, with their totals.

```
  Order.forCustomer(2): 3 orders, totals [500, 1000, 1500].
```

### The Rules Are On The Record

A placed order refuses a new line, and an empty order refuses to be placed. The rules are on the record.

```
  a PLACED order cannot change.
  an empty order cannot be placed.
  what an order may do sits beside what an order is.
```

### The Bill: A Rule That Needs The Table

A delivery rule written on the record loads the customer to answer, so it touches the table. The same rule on two numbers touches nothing.

```
  is a 60.00 order eligible for free delivery? true. table operations to find out: 1.
  the same rule on two numbers: true. table operations: 0.
  to test the rule on the record, the customers table has to exist and hold a customer.
```

### The Bill: The Class Is The Table

When a column is renamed, loading an order fails, because the class's fields are the table's columns.

```
  a column was renamed. loading an order: the orders table has no column total_pence.
  the fields of the class are the columns of the table. one cannot change without the other.
```

### The Bill: Queries You Cannot See

Checking five orders for free delivery makes five table operations, because each call loads the customer again. Nothing in the loop shows it.

```
  checking 5 orders for free delivery, 5 eligible: 5 table operations.
  each call looked innocent. each one loaded the customer again.
```

## The verdict

Use an active record when the objects are close to the tables, the rules are few, and speed of writing matters: admin tools, small services, the first version. Move the rules that need no table into plain functions or objects. Move to a data mapper when the model and the schema start to differ, or when the logic grows.

## How to recognise this in code you did not write

- A class with `save()`, `find()` and `delete()` on it.
- Ruby on Rails' `ActiveRecord`, and Laravel's Eloquent.
- JPA entities with methods that reach for the database themselves.
- Fields named exactly like columns.

## Where you have already met this

Rails, Laravel, Django models, and any framework where the model class is also the way to load and save it.

## When this is too much

Active Record is rarely too much. It is often too little once the rules grow. Watch for rules that need a table to test, and loops that hide queries.
