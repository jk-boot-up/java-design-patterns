# Prerequisites

What to know, and what to install, before working through this project.

## What You Should Already Know

| Topic | How much | Where it shows up |
| --- | --- | --- |
| Classes and objects | Comfortable | Everywhere |
| Constructors and `new` | Comfortable — this project is about their limits | `docs/problem-statement.md` |
| Method chaining (`return this;`) | Basic — the mechanism, not the pattern | Every method on `Builder` |
| Static nested classes | Basic — a class declared inside another, with `static` | `PurchaseOrder.Builder` |
| `static` members | Basic — a method on the class, not on an instance | `PurchaseOrder.builder(...)` |
| `record` | None needed — 60-second primer below | `LineItem`, `Address` |
| `Optional<T>` | None needed — 60-second primer below | `giftMessage()`, `couponCode()`, `notes()` |
| JUnit 5 | Helpful, not required | `src/test` |

If you have ever chained calls on a `StringBuilder`, you have already used
the shape this pattern is named after.

## 60-Second Static Nested Class Primer

```java
public final class PurchaseOrder {

    public static final class Builder {
        ...
    }
}
```

`Builder` lives inside `PurchaseOrder`, and the `static` means it does not
need an existing `PurchaseOrder` to be created — sensible, since its whole
job is to make one. From outside, you write `PurchaseOrder.Builder`, though
in this project you never write that type name directly: you get one back
from `PurchaseOrder.builder(...)` and immediately start chaining.

## 60-Second Method-Chaining Primer

```java
public Builder priority() {
    this.priority = true;
    return this;
}
```

Returning `this` means the result of calling `priority()` is the very
builder you called it on, so another method can be called straight off the
end of it:

```java
builder.addItem(mug).shippingAddress(home).priority();
```

Three calls, one statement, no temporary variable. Nothing here is special
to builders — `StringBuilder.append(...)` and `Stream.filter(...).map(...)`
work the same way — but a builder is the pattern that leans on it hardest.

## 60-Second `record` Primer

```java
public record LineItem(String sku, String description, Money unitPrice, int quantity) { }
```

That one line gives you a constructor, a getter per field (`item.sku()`,
no `get` prefix), plus `equals`, `hashCode` and a readable `toString`.

`LineItem` and `Address` are records here because they have nothing to
decide — every field is required, there is one sensible way to build one,
and a builder for either would be ceremony around a non-problem. That
contrast with `PurchaseOrder`, which has real optional pieces, is
deliberate; see `docs/builder-pattern-explained.md` for why.

## 60-Second `Optional<T>` Primer

```java
public Optional<String> giftMessage() {
    return Optional.ofNullable(giftMessage);
}
```

`giftMessage` is `null` inside `PurchaseOrder` when no message was set.
Rather than handing back `null` and trusting every caller to check for it,
`giftMessage()` wraps it in an `Optional`, so the caller must explicitly
ask `.isPresent()` or provide a fallback with `.orElse(...)` before using
the value. It is a way of putting "this might not be here" into the method
signature itself, rather than into a comment.

## What You Need Installed

| Tool | Version | Check with |
| --- | --- | --- |
| JDK | 21 or newer | `java -version` |
| Gradle | Not needed — use the wrapper | — |

The Gradle wrapper (`./gradlew`) downloads the right Gradle for you on
first run, so a JDK is genuinely the only requirement.

## Verify Your Setup

From the project directory:

```bash
./gradlew build
```

The first run downloads Gradle and JUnit, so give it a minute. You should
finish with `BUILD SUCCESSFUL`.

Then:

```bash
./gradlew test
```

All tests should pass — they cover the required-field checks, the
gift-message-implies-gift-wrap rule, fee stacking, the coupon discount, and
that a reused builder never reaches back into an order it already built.

And to watch it work:

```bash
./gradlew run
```

You should see one order built by hand, three built from presets, proof
that a reused builder does not mutate earlier orders, and finally two
rejected orders — one missing an item, one missing an address.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | JDK older than 21 | Install JDK 21+ |
| `./gradlew: Permission denied` | Wrapper not executable | `chmod +x gradlew` |
| Download hangs on first run | Offline or behind a proxy | Connect, or install Gradle and use `gradle` instead of `./gradlew` |
| `error: cannot find symbol: class Builder` | Missing the outer type name | Write `PurchaseOrder.Builder`, not just `Builder`, outside the package |

## Where to Go Next

1. [`problem-statement.md`](problem-statement.md) — why a constructor with
   nine parameters is not the answer
2. [`builder-pattern-explained.md`](builder-pattern-explained.md) — the
   technique, and the code
3. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
   — the two pictures
4. [`animation.html`](animation.html) — step through it in a browser
