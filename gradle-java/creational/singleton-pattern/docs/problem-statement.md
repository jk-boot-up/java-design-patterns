# The Problem

Every checkout on our marketplace needs an order number: `ORD-000001`,
`ORD-000002`, and so on, handed out in strict sequence with no gaps and no
repeats. Two different customers must never end up with the same order
number, no matter which part of the codebase happened to issue it —
checkout, the admin console that lets support staff raise a manual order, or
a background job replaying a failed payment.

## Attempt one: an instance per caller

```java
public class OrderSequenceGenerator {
    private int counter;

    public String nextOrderNumber() {
        counter++;
        return String.format("ORD-%06d", counter);
    }
}
```

Reasonable-looking class. The problem shows up the moment two different
parts of the system each do this:

```java
// in CheckoutService
OrderSequenceGenerator checkoutSequence = new OrderSequenceGenerator();
checkoutSequence.nextOrderNumber();   // ORD-000001

// in AdminConsoleService, constructed independently
OrderSequenceGenerator adminSequence = new OrderSequenceGenerator();
adminSequence.nextOrderNumber();      // ORD-000001 — collision
```

Each `new OrderSequenceGenerator()` starts its own counter at zero. There is
nothing wrong with the class itself — the bug is that the language lets
anyone construct as many of them as they like, when the domain rule is that
there must be exactly one.

## Attempt two: a classic private-constructor singleton

The textbook fix is to take `new` away from callers and hand back one
shared instance instead:

```java
public final class LegacyOrderSequenceGenerator {
    private static LegacyOrderSequenceGenerator instance;
    private int counter;

    private LegacyOrderSequenceGenerator() { }

    public static LegacyOrderSequenceGenerator getInstance() {
        if (instance == null) {
            instance = new LegacyOrderSequenceGenerator();
        }
        return instance;
    }

    public String nextOrderNumber() {
        counter++;
        return String.format("ORD-%06d", counter);
    }
}
```

Every caller now goes through `getInstance()`, and under normal use it
really does return the same object every time. But "private constructor"
is a promise the JVM only half-keeps:

```java
Constructor<LegacyOrderSequenceGenerator> ctor =
        LegacyOrderSequenceGenerator.class.getDeclaredConstructor();
ctor.setAccessible(true);
LegacyOrderSequenceGenerator forged = ctor.newInstance();   // succeeds

forged != LegacyOrderSequenceGenerator.getInstance();       // true — a second instance exists
```

Reflection can call a private constructor directly, `setAccessible(true)`
and all. And Java's default serialization does not go through a
constructor at all — it rebuilds an object's fields straight from bytes —
so passing this class through an `ObjectOutputStream`/`ObjectInputStream`
round trip mints a second instance too, silently, with `counter` reset back
to zero. Either route reopens exactly the collision this class was written
to prevent.

## The Question This Project Answers

> How do we guarantee, not just by convention but in a way the language
> itself enforces, that a class has exactly one instance — one that
> reflection cannot forge a second copy of, and that serialization cannot
> duplicate?

The answer is the Gang of Four's **Singleton** pattern, and specifically
the implementation *Effective Java* Item 3 recommends over the classic
private-constructor shape above: a single-element `enum`.

Read on in
[`singleton-pattern-explained.md`](singleton-pattern-explained.md).
