# Repository, Explained

## The pattern in one sentence

An interface that looks like an in-memory collection of domain objects, so the
caller asks for customers and never for rows.

## How it works

`CustomerRepository` has `add`, `findById` and a few finders. `MarketingService`
takes one in its constructor and knows nothing else. Two implementations sit
behind it: `InMemoryCustomerRepository` over a list, and
`ToyDatabaseCustomerRepository` over the toy database.

```
FOUR. Swap the store — the calling code does not change.
  in memory: [Ada, Grace]
  database:  [Ada, Grace]
    - new MarketingService(new InMemoryCustomerRepository())
    + new MarketingService(new ToyDatabaseCustomerRepository(db))
```

The whole change is one line where the service is built. `MarketingService`
itself is untouched.

## The bill

**A method per question.** Every real repository grows query methods until it
is a query language with worse ergonomics.

```
FIVE. The bill — a method per question.
    findByCity
    findByCityAndOrderDateAfterAndStatusIn
    findByCityAndOrderDateAfterAndStatusInOrderByNameAsc
    findByCityAndOrderedAfter
```

Specifications fix it, so `matching(inCity("London").and(orderedAfter(70)))`
needs no new method, and cost one more concept.

**The abstraction leaks the moment performance matters.** The caller cannot
say "join" or "fetch the orders together".

```
SIX. The abstraction leaks when performance matters.
  one question, against 6 customers: 7 database operations: one for the
  customers, then one per customer for their orders.
```

**"You can swap the database" is claimed far more often than it is used.** The
real benefit is that callers ask in the language of the domain.

## Where you have already met this

A Spring Data repository interface is this pattern. `save`, `findById` and
`findByCity` are collection-shaped methods, and the framework supplies the
implementation. A later project builds exactly that.

## When this is too much

For an application with a handful of queries, in one place, a repository is an
extra layer. It earns its place when the same questions are asked from several
places, or when the domain should not know about storage.
