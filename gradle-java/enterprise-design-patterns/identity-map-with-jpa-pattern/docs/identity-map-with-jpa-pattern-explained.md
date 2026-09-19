# Identity Map with JPA, Explained

## The pattern in one sentence

The persistence context is an identity map, scoped to an `EntityManager`.

## What is new here

Everything about why one row should be one object is in
[Identity Map](../identity-map-pattern). This page is only what JPA adds.

**The map is built in.** `em.find(Customer.class, 7)` twice gives the same
object and one SQL statement. The order's customer and customer 7 by id are the
same object too.

```
TWO. The order's customer and customer 7 by id.
  the order's customer == customer 7 by id: true
  SQL statements issued: 1 (the order and its customer, once)
```

**The lost change cannot happen inside one context**, because there is only one
object. Both changes are kept, and are written as one `UPDATE` at commit.

```
THREE. Two changes to one customer are both kept.
  SQL statements at commit: 1 (one UPDATE)
  stored address: 1 High Street, York
  stored email:   ada@newmail.example
```

## The failure of its own: detached entities

The map belongs to one persistence context. Two contexts give two objects.

```
FOUR. Two persistence contexts — two objects again.
  customer 7 from context one == from context two: false
  equals: true. same customer, two objects, and each is free to disagree.
```

And once a context is closed, its objects are detached. A change to one is
tracked by nothing, and is silently not saved.

```
  a detached customer was changed. stored address is still: 12 Mill Lane, Leeds
```

## The costs, as in the partner

**The context is a cache, so it can be stale.** `em.refresh` is the cure.

```
FIVE. The context is a cache, so it can be stale.
  this context still sees: ada@example.com
  after refresh it sees:   ada@other.example
```

**It holds references.** After loading a thousand customers it holds a thousand
entities, until `clear()`.

**Its scope is a decision.** In a Spring application the context normally lives
for one transaction or one request.

## Where you have already met this

This is where you have already met it. Every JPA developer has used an identity
map without knowing. If you have ever been surprised that a second `find` did
not hit the database, or that an entity did not pick up another transaction's
change, this was the reason.

## When this is too much

If you use JPA you already have it and cannot turn it off. The lesson is knowing
it is there.
