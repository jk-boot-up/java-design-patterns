# Identity Map, Explained

## The pattern in one sentence

A map, scoped to a session, from id to the one loaded object, so asking for
the same row twice gives the same object.

## Why the naive version fails

`PlainCustomerMapper.find` builds a new `Customer` on every call. Nothing
connects two objects that came from the same row. They can disagree, and
whichever is saved last wins.

## The pattern

`CustomerSession` owns an `IdentityMap`. `find(7)` looks in the map first.
Only on a miss does it go to the database, and it then puts the new object
in the map. The order's customer comes through the same `find`, so it is the
same object as customer 7 loaded by id, and `==` is true.

```
FOUR. The pattern — one map, one object.
  the order's customer and customer 7 by id, same object (==): true
  2 selects: the order's row, and the customer once.
  two more finds of customer 7 cost 0 operations.
```

## The bill

**The map is a cache, so it can be stale.** Another process changes the row.
This session still sees the old value.

```
FIVE. The map is a cache, so it can be stale.
  this session still sees: ada@example.com
  a new session sees:      ada@other.example
```

**It holds references, so a long session leaks memory.** A bulk load of a
thousand customers leaves a thousand objects held.

**Its scope is a decision.** Per request, per session, or per application,
each is wrong in a different way. Too small and the same customer is two
objects again. Too large and it is stale and grows without limit.

## Where you have already met this

The JPA persistence context is an identity map. Load the same entity twice
inside one transaction and you get the same object, which is why `==` is
true. Anyone who has been surprised that a second `find` did not hit the
database has met this pattern.

## When this is too much

For a request that loads a customer once and never again, the map does
nothing. It earns its place when the same row can be reached by two routes.
