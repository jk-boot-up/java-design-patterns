# Railway-Oriented Programming, Explained

## The pattern in one sentence

Railway-Oriented Programming chains steps that each return success or
failure, so the first failure skips the rest and must be handled at the end.

## The 5 acts

### 1. Exceptions nobody caught

Each checkout step throws its own exception. The controller catches the
out-of-stock exception and returns 409. But the declined-card exception was
added later by another team, and nothing forced anyone to handle it. It falls
through to the catch-all, and a customer with a declined card sees "500
internal server error".

### 2. The success track

Now each step returns a `Result` instead of throwing. The checkout is one
straight chain: `validate`, `flatMap` `reserve`, `flatMap` `charge`,
`flatMap` `email`. Two mugs with a good card travel the success track through
all four steps, and the order is confirmed.

### 3. Switching tracks

An empty cart fails at the first step. The result switches to the failure
track, and reserve, charge and email never run. A declined card gets through
validate and reserve, fails at charge, and the email is skipped. Each failure
says which step failed and why, and the controller must handle it, because
the only way off the railway is to say what to do with both tracks.

### 4. Plain functions, and a way back

A step that cannot fail, such as adding 20% tax, rides along with `map`: two
mugs come to 23.98. And `recover` offers a way back to the success track: when
the lamp is out of stock, the failure at reserve is turned into a back-order,
and the customer is told they will get an email when it arrives.

### 5. The bill

The first failure stops everything. A cart that is empty and has no card
reports only the empty cart; the customer fixes that, submits again, and only
then hears about the card. Showing every form error at once needs a different
tool. And the style is unfamiliar in Java, so keep exceptions for the truly
unexpected.

## The verdict

Use it for chains of steps that can fail for business reasons. Return
`Result`s, chain with `flatMap`, lift plain steps with `map`, recover
deliberately, and keep exceptions for the unexpected.

## How to recognise this in code you did not write

- Methods returning `Result`, `Either` or `Try`.
- Chains of `.flatMap(...)` calls.
- A final `fold` or `match` that handles both outcomes.

## Where you have already met this

- `Optional.map` and `flatMap`, a railway whose failure track has no reason.
- `CompletableFuture.thenCompose` and `exceptionally`.
- Vavr's `Try` and `Either`, Kotlin's `Result`, Rust's `Result` and its `?` operator.
