# Null Object, Explained

## The pattern in one sentence

A null object implements the same interface as the real thing and does nothing.

## How it works

`NoDiscount` implements `Discount`, and its `apply` returns the price unchanged.
`NullObjectDirectory.find` returns it whenever there is no discount, so it never
returns `null`. The eight methods lose every check.

```
THREE. The pattern — a discount that does nothing.
  every null check deleted. the same customers, the same prices:
  customer 1: 9000 pence  (same as before)
  customer 2: 10000 pence  (same as before)
  and taxBase for customer 2 now returns 10000, not an exception.
```

The behaviour is identical, and the forgotten check is no longer possible to
forget.

## The bill, which most treatments leave out

A null object **hides errors**. "No discount" and "the discount service was down"
look the same to the caller.

```
FOUR. The bill — a null object can hide an error.
  customer 1, entitled to loyalty, charged 10000 pence instead of 9000. no error, no log, no alert.
```

A failed lookup silently became a full-price order nobody noticed. That is a
worse bug than the exception it replaced, because it is quiet.

## Where the line is

A null object is right when absence is a **legitimate domain state**. No
discount is normal. It is wrong when absence means **something went wrong**.

## The two honest alternatives

**`Optional`** makes absence explicit in the type. "No discount" is
`Optional.empty()`. "The service is down" is still an exception. The two cannot
be confused, and every caller must decide what absence means to it. In Java this
is often the better answer.

```
FIVE. The two honest alternatives.
  Optional: customer 1 has one: true, customer 2 has one: false.
  and a service that is down is still a failure, not an empty Optional
```

**An explicit failure**: when absence means something went wrong, throw.

## The verdict

Use a null object when absence is a legitimate domain state. Never use one to hide
a failure. Prefer `Optional` where the caller must decide.

## How to recognise this in code you did not write

- `Collections.emptyList()` and `Collections.emptyMap()`: a list that is never
  null and does nothing.
- `InputStream.nullInputStream()` and `OutputStream.nullOutputStream()`: streams
  that read nothing and discard everything.
- A no-op logger, or a `NoOpMetrics`, handed to code that would otherwise check
  whether logging is configured.
- A class named `Default...`, `Noop...` or `Null...` implementing an interface
  with empty method bodies.

## Where you have already met this

Every time you returned an empty list instead of `null`, you used it.

## When this is too much

For a value with one call site, a null check is simpler. It earns its place when
the same check would be repeated, and when absence is normal.
