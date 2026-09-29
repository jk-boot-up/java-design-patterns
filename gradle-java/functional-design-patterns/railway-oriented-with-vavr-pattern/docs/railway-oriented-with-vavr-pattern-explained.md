# Railway-Oriented Programming with Vavr, Explained

## The pattern in one sentence

With Vavr, the railway is Either: steps chained with flatMap, exceptions
brought on with Try, and every problem collected with Validation when needed.

## The 5 acts

### 1. A throwing library

The payment company's client library reports a declined card by throwing an
exception. Nothing in Java makes the caller handle it, and a controller that
forgot to catch it answers 500, an internal server error.

### 2. Either

Each step returns Vavr's `Either<Failure, Cart>`, and the checkout is one
chain of `flatMap` calls. Two mugs with a good card stay on the success track
through all four steps, and the order is confirmed.

### 3. Skipping, and Try

An empty cart fails at validate, on the Left, and the other three steps are
skipped. A declined card fails at charge: the step wraps the library call in
`Try.of`, and `toEither()` turns its exception into a Left, so the failure
travels the railway like any other.

### 4. map and orElse

A step that cannot fail, adding 20% tax, rides along with `map`: two mugs come
to 23.98. And `orElse` offers a way back: when the lamp is out of stock, the
checkout's failure is replaced by a back-order.

### 5. Validation

A cart that is empty and has no card. The Either chain stops at the first
failure and reports only the empty cart. Vavr's `Validation` checks each
field on its own and `combine` collects the results: "the cart is empty and
no card given", both at once, so the customer can fix everything together.

## The verdict

Use Either for chains of steps that can fail, Try at the edge where code
throws, and Validation for forms where every problem should be reported.

## How to recognise this in code you did not write

- Methods returning `Either<Failure, T>`.
- `Try.of(...).toEither()` around library calls.
- `Validation.combine(...).ap(...)` for form checks.

## Where you have already met this

- Vavr's `Either`, `Try` and `Validation` in Java codebases.
- Kotlin's `Result` and Arrow's `Either`.
- Scala's `Either` and `Try`, which Vavr is modelled on.
