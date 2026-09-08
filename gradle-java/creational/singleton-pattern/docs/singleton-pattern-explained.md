# The Singleton Pattern, Explained

## First, an Honest Note

This is the Gang of Four's smallest pattern, and the one Java developers
reach for the most casually — and the one *Effective Java* Item 3 spends
the most effort steering people away from misimplementing. The GoF book
states the intent; Item 3 supplies the part the GoF book does not: which of
the several ways to write "exactly one instance" in Java actually holds up
under reflection and serialization, and which only look like they do. This
project builds the one Item 3 recommends, and deliberately also builds the
one it warns against, so the difference is something you can run, not just
read about.

## The Definition

> Ensure a class only has one instance, and provide a global point of
> access to it.
>
> — *Design Patterns* (Gamma, Helm, Johnson, Vlissides)

In plainer words:

> **Make it impossible to construct more than one of this class, and give
> every caller in the program the same one well-known way to reach the
> instance that does exist.**

## The Participants

| Role | In this project | What it does |
| --- | --- | --- |
| Singleton | `OrderSequenceGenerator` | A single-element `enum`; `INSTANCE` is the one and only instance |
| The trap | `LegacyOrderSequenceGenerator` | The classic private-constructor shape, kept here to demonstrate what it fails to prevent |
| Client | `OrderSequenceGeneratorDemo` | Uses the singleton, then tries to break both implementations |

## The Code, Walked Through

### `OrderSequenceGenerator` — a single-element enum

```java
public enum OrderSequenceGenerator {
    INSTANCE;

    private final AtomicLong counter = new AtomicLong();

    public String nextOrderNumber() {
        return String.format("ORD-%06d", counter.incrementAndGet());
    }
}
```

That is the entire singleton. No private constructor to remember to write,
no `getInstance()` method, no null check, no lock. `INSTANCE` is a `public
static final` field the compiler generates for you, and three separate
guarantees come along with it for free, each one answering a specific way
the classic shape fails:

**The JVM creates each enum constant exactly once**, during class
initialization, and class initialization is itself thread-safe by the Java
Language Specification — no double-checked locking, no explicit
`synchronized`, needed to get a single instance safely under concurrent
first use.

**Reflection cannot call an enum's constructor.**
`Constructor.newInstance()` explicitly checks whether the declaring class
is an enum and throws `IllegalArgumentException: Cannot reflectively create
enum objects` if it is — a check written directly into the reflection API,
not something this project's code has to add.

**Enum serialization is defined by name, not by field.** The default
serialized form of an enum constant is its name; deserializing looks the
name up via `Enum.valueOf` against the already-existing constant rather
than reconstructing a new object from scratch. A round trip through
`ObjectOutputStream`/`ObjectInputStream` hands back the exact same
`INSTANCE`, not a copy.

`counter` is an `AtomicLong` rather than a plain `int` for a reason that
matters once "exactly one instance" is guaranteed: that one instance is now
reachable from every thread in the program at once, so the method that
mutates its state has to be safe to call concurrently. `incrementAndGet()`
is a single atomic operation — no two callers can ever read-then-write the
same intermediate value the way two threads incrementing a plain `int`
could.

### `LegacyOrderSequenceGenerator` — the shape this project deliberately avoids shipping

```java
public final class LegacyOrderSequenceGenerator implements Serializable {
    private static LegacyOrderSequenceGenerator instance;
    private int counter;

    private LegacyOrderSequenceGenerator() { }

    public static LegacyOrderSequenceGenerator getInstance() {
        if (instance == null) {
            instance = new LegacyOrderSequenceGenerator();
        }
        return instance;
    }
    ...
}
```

Under ordinary use — every caller writing `getInstance()` and nothing
more exotic — this behaves identically to the enum. The three guarantees
above are exactly the three things it is missing:

- its lazy `if (instance == null)` check is not atomic, so two threads
  racing through it for the first time can each construct their own
  instance;
- its private constructor is reachable via
  `getDeclaredConstructor().setAccessible(true)`, because reflection has no
  special knowledge that this particular private constructor is meant to
  be singular;
- implementing `Serializable` without also writing a `readResolve()`
  method means deserializing it builds a brand-new object with its fields
  restored from the byte stream — `counter` included, reset to whatever it
  was at serialization time, not carried forward from the live instance.

Fixing all three by hand is possible — a `volatile` field with
double-checked locking, a `readResolve()` that returns `INSTANCE`, and
still nothing stops a determined caller with reflection access. The enum
gets all three for the price of one keyword.

### Using it

```java
String orderNumber = OrderSequenceGenerator.INSTANCE.nextOrderNumber();
// ORD-000001, issued from wherever in the program this line runs
```

No constructor, no factory method, no null check — `INSTANCE` already
exists by the time any code can reference it, and every reference to it,
anywhere in the program, is the same object.

## What You Gain

**A guarantee the compiler and the JVM enforce**, not one your team has to
remember to uphold by code review. There is no private constructor for a
future maintainer to accidentally make public, no lazy-initialization race
to get subtly wrong.

**Safety under concurrency, by construction.** Because there is exactly one
instance and it is reachable from every thread, its mutable state
(`counter`) is written once, using `AtomicLong`, instead of being
duplicated per-caller and needing no synchronization at all.

**Immunity to the two classic escape hatches.** Reflection and
serialization are the two ways a "singleton" written the ordinary way can
quietly stop being one. The enum closes both without any extra code in
this project.

## What to Watch Out For

**A singleton is global mutable state**, dressed up in a pattern name. Any
code, anywhere in the program, can call
`OrderSequenceGenerator.INSTANCE.nextOrderNumber()` — there is no way to
give one part of the program its own counter for a test without either
resetting shared state between tests or restructuring the code to accept
an injected dependency instead of reaching for a global.

**It does not compose with instance-per-tenant designs.** The moment the
system needs a separate order sequence per storefront, warehouse, or test
run, "exactly one instance for the whole JVM" is precisely the wrong
guarantee, and no amount of tuning `OrderSequenceGenerator` fixes that —
the pattern itself has to be abandoned in favour of an ordinary object
handed to whoever needs one.

**It hides a dependency.** A method that calls
`OrderSequenceGenerator.INSTANCE` inside its body does not show that
dependency in its signature, unlike a method that takes an
`OrderSequenceGenerator` parameter. That makes the call site shorter and
the dependency graph less visible at the same time.

## How This Relates to the Other Creational Patterns

| | Singleton | Prototype | Builder | Abstract Factory |
| --- | --- | --- | --- | --- |
| In the GoF book? | Yes | Yes | Yes | Yes |
| The problem it solves | Guaranteeing exactly one instance exists | Cheaply producing near-duplicates of an expensive object | Many optional pieces, one object | Which whole matching set? |
| What the caller writes | `EnumName.INSTANCE.method()` | `template.copy()`, then a few setters | A chain of calls, one per piece | One call, gets a family back |
| Extra classes needed | None — the enum is the whole implementation | One interface (`Prototype<T>`) | One builder | One per family |

The honest summary: every other creational pattern in this collection
controls *how* an object gets built. Singleton is the odd one out — it
controls *how many* exist, full stop, and says nothing about assembly at
all. It is also the only one of the four that is arguably better avoided
than reached for by default: the other three solve construction problems
that recur constantly; Singleton solves a narrower one — "the domain
genuinely requires exactly one" — and is frequently misused to solve a
different problem entirely ("I don't want to pass this object around"),
which dependency injection solves without the global-state cost.

## Try It Yourself

1. **Prove the race in the classic shape.** Write a test that starts many
   threads all calling `LegacyOrderSequenceGenerator.getInstance()` for the
   first time simultaneously and collects the returned references into a
   `Set` by identity. It is timing-dependent — you may need several runs —
   but it can produce a set with more than one element, which
   `OrderSequenceGenerator.INSTANCE` never can.
2. **Add `readResolve()`.** Give `LegacyOrderSequenceGenerator` a
   `private Object readResolve() { return instance; }` method and re-run
   `LegacyOrderSequenceGeneratorTest.deserializationCanCreateASecondInstance`.
   Watch it start failing — the fix works, but notice it is one more thing
   an author has to remember to write, where the enum needs nothing.
3. **Feel the global-state cost.** Write two unit tests for
   `OrderSequenceGenerator` that each assert on the exact order number
   returned, run in the same JVM, and watch the second one fail because the
   first already advanced the shared counter. Fix it by asserting on
   relative behaviour (increases, matches the format) instead of an
   absolute value — which is what this project's own tests do, and why.
