# Session Plan — The Singleton Pattern

A guided session for teaching this project to people who are new to design
patterns.

- **Audience:** anyone comfortable writing a Java class. No pattern
  knowledge assumed.
- **Duration:** ~45 minutes
- **Format:** live coding and discussion. Slides optional; the code is the
  material.
- **Group size:** works from 1 to about 20. Beyond that, the exercises need
  pairs.

> **Optional pre-work.** Ask participants to watch the video
> ([`../video/`](../video/)) beforehand. If they do, you can compress the
> first two blocks and spend the time on the exercises instead.

## Before You Start

Check that every machine can run:

```bash
./gradlew build
```

Have open in tabs: `OrderSequenceGenerator.java`,
`LegacyOrderSequenceGenerator.java`, `OrderSequenceGeneratorDemo.java`,
`animation.html`.

## The One Thing They Should Leave With

If they remember nothing else:

> **A private constructor is a promise the compiler checks, not one the
> JVM enforces at runtime — reflection and serialization can both break
> it. A single-element `enum` is the one Java singleton shape that closes
> both holes, for free, with no extra code.**

Everything in the session is in service of that sentence.

## Timings

| Time | Block | Goal |
| --- | --- | --- |
| 0:00–0:07 | The collision | Make them feel why "just `new` it" fails |
| 0:07–0:16 | The classic fix, and its two holes | Private constructor, then break it twice |
| 0:16–0:26 | The enum fix, live | `OrderSequenceGenerator`, and why each attack now fails |
| 0:26–0:32 | Why `AtomicLong` | Concurrency once there really is only one instance |
| 0:32–0:40 | Exercises | Hands on keyboard |
| 0:40–0:45 | Wrap up | The one sentence, and Singleton's reputation |

## 0:00–0:07 — The Collision

Open a scratch file. Write the plain class:

```java
public class OrderSequenceGenerator {
    private int counter;
    public String nextOrderNumber() {
        counter++;
        return String.format("ORD-%06d", counter);
    }
}
```

Then construct it twice, in two "different services":

```java
OrderSequenceGenerator checkout = new OrderSequenceGenerator();
OrderSequenceGenerator admin = new OrderSequenceGenerator();
checkout.nextOrderNumber();   // ORD-000001
admin.nextOrderNumber();      // ORD-000001 — same number, different customers
```

Ask: *"What actually went wrong here — is the class buggy?"* Land on: no,
the class is fine. The bug is that the language lets you construct as many
of it as you like, when the business rule is "exactly one, ever."

## 0:07–0:16 — The Classic Fix, and Its Two Holes

Write the standard private-constructor singleton on the board:

```java
public final class LegacyOrderSequenceGenerator {
    private static LegacyOrderSequenceGenerator instance;
    private LegacyOrderSequenceGenerator() { }
    public static LegacyOrderSequenceGenerator getInstance() {
        if (instance == null) instance = new LegacyOrderSequenceGenerator();
        return instance;
    }
}
```

Ask who has written this shape before. Most hands. Then run
`LegacyOrderSequenceGeneratorTest.reflectionCanCreateASecondInstance` and
let them watch it pass — meaning the "impossible" second instance was
actually created:

```java
Constructor<LegacyOrderSequenceGenerator> ctor =
        LegacyOrderSequenceGenerator.class.getDeclaredConstructor();
ctor.setAccessible(true);
LegacyOrderSequenceGenerator forged = ctor.newInstance();
```

Then run `deserializationCanCreateASecondInstance` and point out that this
one needs no `setAccessible` trick at all — plain `ObjectInputStream`
usage does it, because deserialization never calls the constructor.

## 0:16–0:26 — The Enum Fix, Live

Write `OrderSequenceGenerator` next to it:

```java
public enum OrderSequenceGenerator {
    INSTANCE;
    private final AtomicLong counter = new AtomicLong();
    public String nextOrderNumber() {
        return String.format("ORD-%06d", counter.incrementAndGet());
    }
}
```

Run `OrderSequenceGeneratorTest.reflectionCannotCreateASecondInstance` and
`serializationReturnsTheSameInstance` back to back with the legacy
versions. Ask: *"What's different about this class that makes both of
those pass instead of fail?"* Work towards the three guarantees in
[`singleton-pattern-explained.md`](singleton-pattern-explained.md): the JVM
creates enum constants exactly once, `Constructor.newInstance()` refuses
enum types outright, and enum deserialization resolves by name against the
existing constant instead of building a new object.

## 0:26–0:32 — Why `AtomicLong`

Ask: *"Now that there really is exactly one instance, reachable from
anywhere — what's new about calling a method on it?"* Land on: it can be
called from multiple threads at once, which was never a concern when every
caller had its own private instance. Point at
`counter.incrementAndGet()` and contrast with `counter++`, which is a
read-modify-write that two threads can interleave and lose an increment.
If time allows, run `concurrentCallsNeverProduceDuplicateOrderNumbers` and
point out it is asserting on a *set's size*, not on timing — a
non-flaky way to test a concurrency guarantee.

## 0:32–0:40 — Exercises

### Exercise 1 — Add `readResolve()` (about 4 minutes)

> Add `private Object readResolve() { return instance; }` to
> `LegacyOrderSequenceGenerator`. Re-run
> `deserializationCanCreateASecondInstance` and watch it start failing —
> the fix works. Ask: *"The enum needed none of this. What did you just
> have to remember to write instead?"*

### Exercise 2 — Feel the global-state cost (about 4 minutes)

> Write two `@Test` methods on `OrderSequenceGenerator`, each asserting the
> *exact* string `"ORD-000001"` is returned. Run them together. One fails,
> because the counter is shared JVM-wide state and the other test already
> advanced it. Fix both to assert on the format and on relative increase
> instead of an absolute value.

## 0:40–0:45 — Wrap Up

Back to the one sentence:

> A private constructor is a promise the compiler checks, not one the JVM
> enforces at runtime. A single-element `enum` is the one Java singleton
> shape that closes both holes, for free.

Then, the honest caveat, worth saying out loud: Singleton is the most
overused pattern in the GoF book. Send them somewhere:

- [`../README.md`](../README.md) to run it themselves
- [`animation.html`](animation.html) to step through it again slowly
- [`../video/`](../video/) if they want it narrated
- [`../../prototype-pattern`](../../prototype-pattern) for a creational
  pattern that controls *how* an object is copied rather than *how many*
  exist

## Facilitator Notes

- **The two `getDeclaredConstructor` calls are the hook.** Most people
  accept "private means private" until they watch `setAccessible(true)`
  defeat it live. Do not skip actually running the tests — reading the
  code is much less convincing than watching the assertion pass.
- **Expect "just don't call reflection on it then."** Worth taking
  seriously as a rebuttal in a closed codebase you fully control. The
  honest answer: frameworks (ORMs, DI containers, some testing tools) use
  reflection routinely and did not ask your permission first; a guarantee
  that only holds "as long as nobody uses reflection" is not really a
  guarantee.
- **If you are running short**, cut the `AtomicLong` block (0:26–0:32). The
  reflection/serialization contrast is the core of the lesson and survives
  without it.
- **Someone will ask "isn't Singleton just a global variable?"** Say yes,
  mostly, and that this is the pattern's most common criticism — it is
  worth raising unprompted if nobody does, so the session does not read as
  an unqualified endorsement.
