# Repository with Spring Data, Explained

## The pattern in one sentence

An interface that looks like a collection of domain objects, with the
implementation generated.

## What is new here

The pattern is [Repository](../repository-pattern). This page is what Spring Data
adds.

**No implementation.** `CustomerRepository extends JpaRepository<Customer, Integer>`
and nothing else. `save`, `findById`, `findAll` and `delete` all work. Spring
injects a generated proxy.

**A query from a name.** `findDistinctByCityAndOrdersDayGreaterThan` is parsed by
Spring Data, which builds the query. One statement, and the partner's
`MarketingService` gives the same answer with its body unchanged.

## The costs, as in the partner

**A method per question, and now a name that can be wrong.** The partner's
interface grew a method for every question. Here the name is also the query.

```
THREE. The bill — a method per question, and a name that can be wrong.
    findAllWithOrders
    findByCityAndOrderedAfter
    findDistinctByCityAndOrdersDayGreaterThan
    findDistinctByCityAndOrdersDayGreaterThanAndOrdersStatusIn
  a typo in a method name, findByCiity, is caught only when Spring reads it:
  PropertyReferenceException: No property 'ciity' found for type 'Customer'
```

The compiler cannot check a name.

**The abstraction leaks when performance matters.** Counting every customer's
orders costs seven statements, the same seven as the partner's. `@EntityGraph` makes
it one, and the interface now carries a persistence hint.

```
FOUR. The abstraction leaks when performance matters.
  counting every customer's orders, lazily: 7 orders, 7 statements.
  with @EntityGraph on the repository method: 7 orders, 1 statement.
```

## The failure of its own: the managed entity that leaks

An entity returned by a repository is managed by the persistence context.

```
FIVE. The managed entity that leaks.
  a caller inside a transaction changed a customer from findAll(), and never called save.
  Ada's city in the database now: Manchester
  the same change with no transaction around it. Ada's city in the database: London
```

Inside a transaction the change is written at commit, with no `save`. Outside one
it is lost with no error. The interface looks like a collection, and it is not one.

## Where you have already met this

This is Repository, with the framework supplying the implementation. Every
`JpaRepository` is one. "You can swap the database" is still claimed far more
often than it is used.

## When this is too much

For a handful of queries in one place, Spring Data still saves you two classes. The
cost is the leak, which needs to be known about.
