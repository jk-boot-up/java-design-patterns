# Session Plan — The Static Factory Method

A guided session for teaching this project to people who are new to design
patterns.

- **Audience:** anyone comfortable writing a Java class. No pattern knowledge
  assumed.
- **Duration:** ~60 minutes
- **Format:** live coding and discussion. Slides optional; the code is the
  material.
- **Group size:** works from 1 to about 20. Beyond that, the exercises need
  pairs.

> **Optional pre-work.** Ask participants to watch the ~10 minute video
> ([`../video/`](../video/)) beforehand. If they do, you can compress the
> first two blocks and spend the time on the exercises instead.

## Before You Start

Check that every machine can run:

```bash
./gradlew build
```

Someone will have JDK 17. Sort that out before the session, not during it —
see [`prerequisites.md`](prerequisites.md).

Have open in tabs: `Discount.java`, `Money.java`, `CheckoutService.java`,
`animation.html`.

## The One Thing They Should Leave With

If they remember nothing else:

> **A constructor cannot be named, and cannot refuse to allocate. A static
> factory method can do both. That is why `List.of(...)` exists and
> `new ArrayList<>(...)` is not what you reach for first.**

Everything in the session is in service of that sentence.

## Timings

| Time | Block | Goal |
| --- | --- | --- |
| 0:00–0:08 | The problem that will not compile | Make them feel the wall |
| 0:08–0:18 | The fix, live | Show the technique |
| 0:18–0:28 | The three freedoms | Why it is more than a rename |
| 0:28–0:35 | Where they already use it | Connect to the JDK |
| 0:35–0:50 | Exercises | Hands on keyboard |
| 0:50–0:58 | When *not* to use it | Honesty and boundaries |
| 0:58–1:00 | Wrap up | The one sentence |

## 0:00–0:08 — The Problem That Will Not Compile

Open a scratch file. Type this in front of them, live:

```java
public class Discount {
    public Discount(double percent) { }
    public Discount(double amountOff) { }
}
```

Let the compiler error land on screen before you say anything.

```
error: constructor Discount(double) is already defined
```

Ask: *"Why not? They mean completely different things."*

Let them work it out. The answer they should reach: a constructor's name is
the class name, so overloads can only differ by parameter type, and both of
these are `double`. The meaning lives in your head, not in the code.

Now show the workaround everyone writes:

```java
Discount tenPercent = new Discount(0.10, 0, false);
Discount fiverOff   = new Discount(0, 5.00, false);
```

Ask: *"Which of these gives £5 off?"* Wait. Someone will get it wrong, or
nobody will answer. Either way the point has made itself.

**Do not rush this block.** The rest of the session is only interesting to
people who felt this problem.

## 0:08–0:18 — The Fix, Live

Rewrite it in front of them:

```java
public interface Discount {
    static Discount percentage(int percent) { ... }
    static Discount amountOff(Money amount) { ... }
}
```

Then the call sites:

```java
Discount.percentage(10);
Discount.amountOff(Money.pounds(5));
```

Ask: *"What changed?"*

The answer to steer towards is **just the name** — and that the name is the
whole fix for this particular problem. Do not introduce the other benefits
yet; let this one land alone.

Then open `Money.java` and show `pounds` and `pence` side by side. Ask
someone to say out loud what `Money.pounds(5)` and `Money.pence(5)` are.
They will get it right instantly, which is exactly the demonstration.

## 0:18–0:28 — The Three Freedoms

Now the part that makes it more than a naming trick. Work through
`Discount.java` on screen.

**Freedom 1 — not to allocate.**

```java
static Discount none() {
    return NoDiscount.INSTANCE;
}
```

Run this in the demo, or just point at the output:

```
none() is shared: true
```

Ask: *"Could a constructor do that?"* No — `new` is defined as producing a
new object. Mention `Integer.valueOf(5)` versus `new Integer(5)`, and that
the latter is deprecated for precisely this reason.

**Freedom 2 — to choose the class.**

```java
return percent == 0 ? none() : new PercentageDiscount(percent);
```

```
percentage(0) -> No discount
```

Ask: *"Who noticed?"* Nobody, because nobody can. The caller asked for what
it wanted, not for a specific class.

**Freedom 3 — to hide the classes entirely.**

Open `PercentageDiscount.java` and put a cursor on the first line:

```java
final class PercentageDiscount implements Discount {
```

Ask: *"What is missing?"* The `public`. Then show `docs/images/boundary.png`
and let it do the rest of the explaining.

The consequence to state explicitly: **all five of these classes can be
renamed or deleted tomorrow and no caller breaks**, because no caller ever
knew their names.

## 0:28–0:35 — Where They Already Use It

This block converts the technique from "a thing in a tutorial" to "a thing I
have done a thousand times".

Put these on screen and ask what each has in common:

```java
List.of("a", "b")
Integer.valueOf(5)
Optional.empty()
LocalDate.now()
String.valueOf(42)
```

Then the killer detail: `List.of()` returns a *different class* depending on
how many arguments you pass — there are specialised implementations for zero,
one and two elements. Ask if anyone has ever noticed. Nobody has. Ask if it
has ever caused them a problem. It has not.

Finish with the naming table from
[`static-factory-pattern-explained.md`](static-factory-pattern-explained.md)
— `of`, `from`, `valueOf`, `getInstance`, `parse`, `copyOf`. Tell them to use
these names, because the whole ecosystem already has.

## 0:35–0:50 — Exercises

Two exercises, and they are the two halves of the lesson. The first shows how
cheap extension is; the second shows the wall being real. **The session does
not work with only one of them.**

### Exercise 1 — Add a discount (about 8 minutes)

> Add a `Discount.tiered()`: 5% off orders under £50, 15% off the rest.

Steps:

1. Write `final class TieredDiscount implements Discount` — package-private.
2. Add `static Discount tiered()` to the `Discount` interface.
3. Add a coupon code `"TIERED"` to `forCoupon`.
4. Run the tests.

The thing to draw out at the end: **`CheckoutService` did not change, and
could not have.** It cannot name `TieredDiscount`. Ask how many files they
edited, and how many *callers* they edited. The answers are three and zero.

### Exercise 2 — Try to break in (about 5 minutes)

> From a test in a package of your own — say `com.example.hack` — write
> `new PercentageDiscount(10)`.

It does not compile. Ask them to make it compile *without* editing
`PercentageDiscount.java`. They cannot.

Then ask the real question: *"Is that a good thing?"*

Sit with the disagreement — this is the most valuable two minutes of the
session. The honest answer is: it is good when you want to keep the freedom
to change those classes, and it is annoying when someone genuinely needed to
extend one and now has to ask you. Both are true. That is a design trade, not
a rule.

## 0:50–0:58 — When *Not* to Use It

End on the boundaries, or they will over-apply it next week.

**Do not bother when there is nothing to decide.** `Order` and `Receipt` in
this project are plain records with public constructors. They carry data,
there is one sensible way to build them, and a factory method would be
ceremony. Point at them.

**It cannot move the decision elsewhere.** A static method is resolved at
compile time. It cannot be overridden, so a subclass cannot change what gets
built, and a configuration file cannot either. When you need *that*, you have
outgrown this technique — and that is exactly where Factory Method and
Abstract Factory come in.

If the group has already done the other projects in this repository, put the
comparison table on screen and walk the four columns. If they have not, just
plant the flag: *"There are three more of these, and they exist because this
one has a ceiling."*

**And the real cost:** no public constructor means no subclassing from
outside. Say it plainly — usually a feature for value types, occasionally a
genuine problem.

## 0:58–1:00 — Wrap Up

Back to the one sentence:

> A constructor cannot be named, and cannot refuse to allocate. A static
> factory method can do both.

Then send them somewhere:

- [`../README.md`](../README.md) to run it themselves
- [`animation.html`](animation.html) to step through it again slowly
- [`../video/`](../video/) if they want it narrated
- The next pattern:
  [`../../simple-factory-pattern`](../../simple-factory-pattern), where the
  decision moves out of the type and into a class of its own

## Facilitator Notes

- **The compile error in block one is the hook.** If you paraphrase it
  instead of showing it, you lose half the room. Type it live.
- **Expect "why not just use a builder?"** Good question, and the answer is
  that builders solve a different problem — many optional parameters, not
  many *kinds* of thing. A builder still cannot return a shared instance or
  a different class. They compose fine: `Thing.builder()` is itself a static
  factory method.
- **Expect "isn't a static method untestable?"** Worth taking seriously. The
  answer is that these particular static methods only construct objects, and
  the objects they return are ordinary and fully testable. You are not
  hiding I/O or state behind a static call; you are hiding a `new`.
- **Expect someone to conflate this with Factory Method.** They share a word
  and nothing else. Have the comparison table ready, and say plainly that the
  naming collision is unfortunate and not their fault.
- **If you are running short**, cut block 0:28–0:35. It is the most enjoyable
  block and the least essential.
- **If you have longer than an hour**, add: have them write `bestOf` from
  scratch without looking. It forces them to notice that the composite class
  is invisible to callers, which is the deepest idea in the project.
