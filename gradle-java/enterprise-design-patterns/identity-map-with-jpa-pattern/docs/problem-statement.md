# Problem Statement

## Read the partner first

This project assumes [Identity Map](../identity-map-pattern), which builds an
identity map by hand and shows why one row should be one object. If you have
not seen that, start there. Nothing here is lost by skipping the framework, and
[`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The same as the partner's: customer 7, Ada Lovelace, and order 100 which
belongs to her. It is one row in the database.

## What is new

In the partner, you built the map. In JPA, the `EntityManager` has one built
in, and it is called the persistence context. The best "oh, that is what that
is" moment in the course is this:

```
ONE. Load the same customer twice in one persistence context.
  first == second: true
  SQL statements issued: 1
```

## The failure this project exists to show

The map belongs to one context. A second context has its own map, and the same
row becomes two objects again. And a change made to an object whose context has
closed is not saved, with no error at all.

```
FOUR. Two persistence contexts — two objects again.
  customer 7 from context one == from context two: false
  a detached customer was changed. stored address is still: 12 Mill Lane, Leeds
```
