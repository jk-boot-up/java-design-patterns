# Problem Statement

## Read the partner first

This project assumes [Unit of Work](../unit-of-work-pattern), which builds the
mechanism by hand. Nothing here is lost by skipping the framework, and
[`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: an order with three lines, and the write that decrements the
third product's stock is rejected.

## What is new

The mechanism is now one annotation. Every change made inside a
`@Transactional` method is written when it returns, or none of them are.

```
TWO. @Transactional — the unit of work is one annotation.
  inside the method, after changing three objects: inserts written 0, updates written 0.
  after the method returned: inserts written 2, updates written 1.
  committed: orders 0, lines 0, stock keyboard 10, mouse 10, monitor 10
```

## The failures of its own

An annotation hides the mechanism, so the failures are ones you cannot see:

```
THREE. The exception nobody expected to matter.
  committed: orders 1, lines 2, stock keyboard 8, mouse 9, monitor 10
  under @Transactional, and half an order committed anyway.
```

And a flush nobody wrote, and an annotation that does nothing.
