# Prerequisites

What to know, and what to install, before working through this project.

## What You Should Already Know

| Topic | How much | Where it shows up |
| --- | --- | --- |
| Classes and objects | Comfortable | Everywhere |
| Constructors and `new` | Comfortable — this project is about their limits | `docs/problem-statement.md` |
| Interfaces | Comfortable | `Discount` |
| `static` members | Basic — a method on the class, not on an instance | Every factory method |
| Access modifiers | Basic — the difference between `public` and no modifier | The whole point of the hidden classes |
| `record` | None needed — 60-second primer below | `Order`, `Receipt` |
| `switch` expressions | None needed — read `->` as "gives back" | `Discount.forCoupon` |
| JUnit 5 | Helpful, not required | `src/test` |

If you can read a Java class and know what `new` does, you have enough.

## 60-Second `static` Primer

An instance method belongs to an object, so you need one before you can call
it:

```java
String name = "hello";
name.toUpperCase();        // needs the object "hello"
```

A **static** method belongs to the class itself, so you call it on the class
and you need no object at all:

```java
Integer.parseInt("42");    // no Integer exists yet — that is the point
Money.pounds(5.00);        // no Money exists yet either
```

That is why a static method can be the thing that *creates* the first
instance. An instance method could not: you would already need the object you
were trying to make.

## 60-Second Access Modifier Primer

Java has four levels of visibility. This project only cares about two:

```java
public class PercentageDiscount { ... }   // anyone, anywhere, can use this
class PercentageDiscount { ... }          // only this package can see it
```

The second one — no keyword at all — is called **package-private**. Miss the
`public` and you get it by accident; use it deliberately and it becomes a
wall. Five classes in this project are package-private, so code in any other
package genuinely cannot name them. Not "should not". *Cannot* — it is a
compile error.

Check it for yourself: `NoDiscount.java` and `PercentageDiscount.java` start
with `final class`, not `public final class`.

## 60-Second `record` Primer

A `record` is a short way of writing a class that only carries data:

```java
public record Order(String orderId, String customerId, Money subtotal, Money shipping) { }
```

That one line gives you a constructor, a getter per field (called
`order.subtotal()`, with no `get` prefix), plus `equals`, `hashCode` and a
readable `toString`.

Records are used here for `Order` and `Receipt` — things with nothing to
decide. `Discount` and `Money`, which *do* have something to decide, are not
records, and that contrast is deliberate.

## 60-Second Private Constructor Primer

```java
public final class Money {

    private Money(long pence) { ... }         // nobody outside can call this

    public static Money pounds(double p) {    // ...so this is the only way in
        return new Money(Math.round(p * 100));
    }
}
```

`private` on a constructor means only code inside `Money` may run it. From
outside, `new Money(500)` is a compile error, and `Money.pounds(5)` is the
door. Once every caller has to come through that door, the class controls
everything about what comes out — including whether anything new is created
at all.

## What You Need Installed

| Tool | Version | Check with |
| --- | --- | --- |
| JDK | 21 or newer | `java -version` |
| Gradle | Not needed — use the wrapper | — |

The Gradle wrapper (`./gradlew`) downloads the right Gradle for you on first
run, so a JDK is genuinely the only requirement.

If `java -version` prints something older than 21, install a current JDK
(Temurin, Zulu and Oracle builds are all fine) and try again.

### A note on `£`

Every amount in this project prints with a pound sign. On macOS and Linux
that just works. On Windows, if you see `?` or mojibake instead, run:

```
chcp 65001
```

before `gradlew.bat run`, which switches the console to UTF-8.

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

**Thirty-four tests should pass.** They are the fastest way to check that
your JDK is happy before you start reading code.

And to watch it work:

```bash
./gradlew run
```

You should see the same order priced five different ways, then a short
section proving the two things constructors cannot do — shared instances, and
a substituted class — and finally a rejected coupon code.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | JDK older than 21 | Install JDK 21+ |
| `./gradlew: Permission denied` | Wrapper not executable | `chmod +x gradlew` |
| Download hangs on first run | Offline or behind a proxy | Connect, or install Gradle and use `gradle` instead of `./gradlew` |
| `?` instead of `£` | Console is not UTF-8 | `chcp 65001` on Windows |
| `error: PercentageDiscount is not public` | You tried to use a hidden class from outside the package | That is the pattern working. Use `Discount.percentage(...)` |

## Where to Go Next

1. [`problem-statement.md`](problem-statement.md) — why constructors run out
   of road
2. [`static-factory-pattern-explained.md`](static-factory-pattern-explained.md)
   — the technique, and the code
3. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
   — the two pictures
4. [`animation.html`](animation.html) — step through it in a browser
