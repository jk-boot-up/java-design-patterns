# Prerequisites — Chain of Responsibility

What you need before starting, and the two comparisons that cause the most
trouble.

## Tools

| Tool | Version | Check |
| --- | --- | --- |
| JDK | 21 | `java -version` |
| Gradle | wrapper, no install needed | `./gradlew --version` |

Everything else — JUnit 5, the test runner — is fetched by the wrapper on the
first build.

```bash
./gradlew run     # the walkthrough
./gradlew test    # 21 tests
```

## Java You Should Recognise

| Feature | Where it appears | Why it is there |
| --- | --- | --- |
| `abstract class` with a `final` method | `ScreeningHandler.screen` | walking the chain is written once, and a subclass cannot skip the next link |
| `protected abstract` | `ScreeningHandler.check` | the only thing a link author writes |
| `Optional<Decision>` | every `check` | "I am deciding" and "pass it on" are two states, and `null` is neither |
| `record` | `CheckoutRequest`, `BasketItem`, `Decision`, `ScreeningReport` | value objects, equality for free, no setters |
| `enum` | `Outcome` | three answers, not two — see below |
| varargs | `new ScreeningChain(name, fallback, links...)` | the wiring reads as a list |
| anonymous subclass | the `no-mondays` link in `ScreeningChainTest` | proves a new link needs no change to anything that exists |

If `Optional` is new, read it as a two-state box before reading the code: an
empty `Optional` here means *this handler has no opinion*, and that is a
different thing from a handler that decided the answer is "no".

## Why Three Outcomes, Not a Boolean

`Outcome` has `APPROVED`, `REJECTED` and `REFERRED`. The third exists because a
fraud model produces a score, not a verdict, and the band in the middle is the
whole reason anyone buys one. A method returning `boolean` cannot express it,
so the naive version guesses — and the tests in `NaiveScreeningTest` pin down
which way it guesses.

This is worth internalising before the pattern itself: **the shape of the
return type decides what a check is allowed to say.**

## Chain of Responsibility vs Decorator

These two are the pair people confuse, and it is not carelessness — both are
objects that hold a reference to the next object and pass work along it. If you
have already worked through
[`decorator-pattern`](../../../structural/decorator-pattern), the `ShippingQuote`
wrappers there and the `ScreeningHandler` links here look almost identical on a
class diagram.

**The question to ask yourself:** *does every layer have to run?*

| | Decorator | Chain of Responsibility |
| --- | --- | --- |
| Delegates onward | always | only if it has no answer |
| Purpose of a layer | add something on the way through | decide, or step aside |
| Can a layer end the run? | no | yes, and that is the point |
| What you get at the end | the accumulated result of every layer | the answer of one layer |
| Removing a layer changes | the result | possibly nothing at all |

A decorator that stopped delegating would be a bug — a gift-wrap decorator that
declined to call the thing it wraps returns no shipping quote at all. A handler
that stops delegating is doing its job. Concretely, in this project:
`AddressCheck` rejecting a Jersey postcode means `StockCheck`, `FraudScoreCheck`
and `PaymentLimitCheck` **never run**, and the report says so out loud.

That is also the practical tell in a codebase you did not write: if the class
has a field for the next object and its method always ends by calling it, it is
a decorator. If the call to the next object is inside a conditional, it is a
handler.

## Chain of Responsibility vs a `List<Check>` and a `for` Loop

The honest alternative, and worth sitting with, because it is not obviously
worse:

```java
for (Check check : checks) {
    Optional<Decision> decision = check.apply(request);
    if (decision.isPresent()) return decision.get();
}
```

Same independence, same reordering-by-configuration, same testability in
isolation, and the traversal is visible in one place instead of distributed
across the links. What the loop cannot do is let a link decide *what comes
next* — dispatch to a different branch, skip two links, or hand off to a chain
it was given. Nothing in this project needs that, and the notes say so.

Use the loop when every element gets the same request and the sequence is
linear. Reach for the linked version when a handler needs a say in where the
request goes after it.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the method, and its three bugs
2. `NaiveScreening.java` — read `validate` and `validateTradeAccount` side by side
3. `ScreeningHandler.java` — twenty lines, and the whole pattern is in `screen`
4. [`chain-of-responsibility-pattern-explained.md`](chain-of-responsibility-pattern-explained.md)
5. `./gradlew run`, with [`class-diagram.md`](class-diagram.md) open
6. [`animation.html`](animation.html) — the runtime view, step by step
