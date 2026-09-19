# Lazy Load with Hibernate, Explained

## The pattern in one sentence

A lazy field holds a proxy that loads on first use, and the proxy needs its
session to do it.

## What is new here

The pattern is [Lazy Load](../lazy-load-pattern). This page is only what
Hibernate adds.

**A lazy field is a generated proxy.** `order.customer()` is not a `Customer`. It
is a subclass Hibernate generated, holding the customer's id and a reference to
the session. It has not loaded anything.

```
TWO. What is actually in the field.
  order.customer() is a generated subclass of Customer, initialised: false
  the proxy holds only the id (1) and a reference to the session. it has not loaded the customer.
  after asking for the name, inside the session, initialised: true
```

When the session closes, the proxy has nothing to load with. That is the exception.

## The three usual fixes, and what each costs

**Fix one: keep the session open.** It works. The session, and its database
connection, stay open while the page renders, and the extra queries are hidden
inside the view where nobody looks.

```
THREE. Fix one: keep the session open.
  20 orders, each with its customer's name: 6 statements.
  20 orders, each with its line count: 21 statements. that is N+1.
```

The customers cost only 6 because the session loads each of the five distinct
customers once. That is the identity map, again. The lines cost 21 because each
order has its own.

**Fix two: fetch it in the same query.** One statement. But that statement makes
the database send 80 rows for 20 orders, each order repeated once per line, and
Hibernate folds them back together. And every caller of the query now gets the
lines, wanted or not.

```
FOUR. Fix two: fetch it in the same query.
  join fetch of the customer: 20 orders, 1 statement.
  join fetch of the lines:    20 orders, 1 statement.
  the cost: that one statement makes the database send 80 rows for 20 orders,
```

**Fix three: ask for exactly what the page needs.** A projection: one statement,
no entity, no proxy, nothing lazy to fail. The cost is a class for every query,
and a row is not an object with behaviour. That is the [DTO](../dto-pattern) idea.

```
FIVE. Fix three: ask for exactly what the page needs.
  projection: 20 rows, 1 statement, first row OrderRow[orderId=1, customerName=Customer 1]
```

## The fix not on the list

Making the mapping eager would remove the exception, and bring back the partner's
first act: loading one order loads the shop.

## Where you have already met this

`LazyInitializationException` is one of the most searched Java errors there is. If
you have met it in a Spring application, it was almost always a controller or view
using a lazy field after the transaction ended, exactly act one.

## When this is too much

If you almost always need the related data, lazy loading only adds queries.
