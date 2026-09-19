# Problem Statement

## Read the partner first

This project assumes [Repository](../repository-pattern), which hides the
database behind an interface that looks like a collection of customers, with two
implementations you wrote. Nothing here is lost by skipping the framework, and
[`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: six customers, and the question "London customers who ordered in
the last month".

## What is new

The interface has no implementation.

```
ONE. An interface with no implementation.
  CustomerRepository is an interface, and this project has no class that implements it.
  the object Spring injected is a generated proxy
```

And the partner's query, which was written by hand in two places, is generated
from a method's own name:

```
TWO. A query generated from the method's own name.
  findDistinctByCityAndOrdersDayGreaterThan("London", 70): [Ada, Grace]
  statements issued: 1. no query was written by hand.
  the partner's MarketingService, unchanged, gives: [Ada, Grace]
```

## The failure this project exists to show

The leak. An entity a repository hands out is a managed object. Change it inside
a transaction and it is written, with no `save` anywhere. Change it outside one and
the change is lost, with no error.
