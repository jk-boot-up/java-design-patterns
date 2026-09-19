# Unit of Work with Spring, Explained

## The pattern in one sentence

`@Transactional` is a unit of work: changes are held, and written at commit, or
not at all.

## What is new here

The pattern is [Unit of Work](../unit-of-work-pattern). This page is what Spring
adds, and where it surprises.

**One annotation replaces the hand-built class.** The persistence context tracks
what changed. The transaction commits it. Nothing is written where the code is.

```
ONE. No transaction around the order — every step commits alone.
  committed: orders 1, lines 2, stock keyboard 8, mouse 9, monitor 10
```

Without the annotation each step commits alone, and the partner's first act
returns.

## The failure of its own: the checked exception that commits

Spring's default is to roll back on unchecked exceptions and errors, and to
commit on checked ones. The same failure, declared as a checked exception:

```
THREE. The exception nobody expected to matter.
  committed: orders 1, lines 2, stock keyboard 8, mouse 9, monitor 10
```

The fix is one attribute, and someone has to know to write it:

```
FOUR. The one-line fix: rollbackFor.
  @Transactional(rollbackFor = StockFailureChecked.class), same failure:
  committed: orders 0, lines 0, stock keyboard 10, mouse 10, monitor 10
```

## The failure of its own: a flush nobody wrote

Changes are held until commit, except that running a query first makes Hibernate
write pending changes so the query sees them.

```
FIVE. A flush nobody wrote.
  updates written before changing anything: 0
  after changing a product's stock:         0 (held back until commit)
  after running an unrelated query:         1 (Hibernate wrote it first)
```

## The annotation that does nothing

`@Transactional` works through a proxy. A call from one method of a bean to
another goes to `this`, not through the proxy, so the annotation on the second
method is never seen.

```
SIX. The annotation that does nothing.
  TransactionRequiredException: No EntityManager with actual transaction available for ...
  committed: orders 1, lines 0, stock keyboard 10, mouse 10, monitor 10
```

## Costs, as in the partner

Order of writes, knowing what is dirty, and memory that disagrees with the
database until commit are all still true. Spring and Hibernate solve them for
you, and add the surprises above.

## Where you have already met this

Every `@Transactional` method in a Spring application. The `TransactionRequiredException`
message in act six is one of the most common Spring errors there is.

## When this is too much

For a single write, the annotation is not needed at all. It earns its place when
one business action writes several rows together.
