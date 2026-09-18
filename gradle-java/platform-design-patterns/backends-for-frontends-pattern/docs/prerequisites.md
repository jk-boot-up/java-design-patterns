# Prerequisites

This project is written for beginners. If you can read a Java method and follow a
`for` loop, you have enough. Everything else is explained as it arrives.

There is no network, no Docker, no cloud account, no HTTP server and no web
framework. The whole project runs offline with a JDK and nothing else.

---

## Knowledge Prerequisites

### Required

- **Java basics** — classes, methods, `final`, and reading a stack trace.
- **Collections** — `List` and `Map`, and being comfortable with a `for` loop over
  a list.
- **The idea that a program can call another program.** Not the mechanics. Just
  the idea that when you open a product page, the thing that answers you may ask
  five other things before it answers.

### Helpful, but explained as we go

- **Interfaces with more than one implementation** — the heart of this pattern is
  that two classes implement one interface and answer differently. Primer below.
- **Records** — Java's short syntax for "a value with named fields". Primer below.
- **Lambdas** — `SavingRules` is a one-method interface, so its implementations are
  written as `(a, b, c) -> ...`. Primer below.
- **Streams** — a few methods use `.stream().filter(...).count()`. Every one of
  them could be a `for` loop and means exactly what it looks like it means.

### Explicitly NOT required

- Any experience with Spring, Node, GraphQL, REST frameworks or API gateways.
- Any experience with microservices or Kubernetes.
- Any mobile development. The phone in this project is a comment and a byte count.
- Any concurrency knowledge. Everything runs on one thread, in order.
- JSON. `Doc` is an ordered map that can print itself; no library is involved.

---

## A 60-Second "Two Implementations" Primer

Most tutorials introduce an interface as a way to swap one thing for another —
today a `FileStore`, tomorrow an `S3Store`, only one of them live at a time.

This pattern uses an interface the other way. Both implementations are live, at
the same time, in production, answering the same question differently on purpose.

```java
public interface ClientBackend {
    String client();
    Doc productScreen(String sku);
}
```

`MobileBff` returns six fields. `WebBff` returns fifteen. Neither is the fallback
and neither is the real one, and nobody is ever going to "pick" between them,
because the phone always talks to the first and the desktop always talks to the
second.

If you find yourself wanting to unify them, that instinct is exactly what the
pattern is asking you to resist — and `WebBffTest` has a test asserting they stay
different.

---

## A 60-Second "Record" Primer

A `record` is Java's short way of saying "a value made of these named fields".

```java
public record Client(String name, boolean disagreesAboutTheProduct, String reason) { }
```

That one line gives you a constructor taking all three values, a getter for each one
named after the field — `client.name()`, not `client.getName()` — and sensible
equality, so two clients with the same three values are equal.

Records are immutable. There is no `setName(...)`. Once a client is described it
cannot be edited.

---

## A 60-Second "Lambda" Primer

An interface with exactly one abstract method can be implemented with an arrow
instead of a class.

```java
static SavingRules current() {
    return (listPence, nowPence, listPriceHeldLongEnough) -> {
        if (!listPriceHeldLongEnough) {
            return "";
        }
        ...
    };
}
```

Read `(a, b, c) -> { ... }` as "given these three values, do this and return
something". It is the body of `savingLabel`, written without the ceremony of a
named class, and Java works out which method it is implementing because the
interface only has one.

The reason it matters here is that the project needs **two** versions of the same
rule alive in one run — the current one and a stale copy — so that Act 5 can show
them disagreeing. Two lambdas is the shortest honest way to do that.

---

## A 60-Second "Round Trip" Primer

A **round trip** is one request going out and its answer coming back. It is the
unit this project counts, and the only thing you need to know about it is that not
all round trips cost the same.

- **From a phone to the shop**: crosses the customer's mobile network. On a good
  connection, tens of milliseconds. On a train, a tenth of a second or worse, and
  it happens before any work has been done.
- **Between two of the shop's own processes**: crosses a data-centre network.
  Under a millisecond, and nobody is waiting on a train.

`CallLog.Origin` has exactly two values, `DEVICE` and `INTERNAL`, for this reason.
When the demo says five device calls became one, and four internal calls appeared
in their place, both halves of that are true and only the first half is a saving.

---

## A 60-Second "Payload Shape" Primer

Two different things can be wrong with a response, and the project keeps them
apart because only one of them has an easy fix.

**Size** — the response contains fields this screen does not draw. Easy to fix:
add a `?fields=` parameter and the server sends less. `SharedApi.product(sku,
fields)` does exactly this, and it works.

**Shape** — the response does not contain a field this screen needs, because that
field does not exist in any service and has to be composed: three services joined,
a clock consulted, a sentence written. No parameter fixes that. Somebody has to
write it, and the question is who is allowed to.

If you remember one distinction from the whole project, make it that one. The
pattern is often sold on size and is actually about shape and ownership.

---

## Software Prerequisites

| Need | Version | Check |
| --- | --- | --- |
| JDK | 21 or newer | `java -version` |
| Gradle | none — the wrapper is included | `./gradlew --version` |

Nothing else. No Docker, no network access at build time beyond Gradle fetching
JUnit once.

### Verify Your Setup

```bash
cd gradle-java/platform-design-patterns/backends-for-frontends-pattern
./gradlew test
./gradlew run
```

`test` should report 46 tests passing. `run` should print seven acts, ending with
`one per genuine disagreement: 3 backends`.

If `run` prints exactly the same numbers twice in a row, that is not luck — the
shop's data is fixed rather than random precisely so that it does, which is what
lets the documents and the video quote exact figures.

---

## Troubleshooting

**`./gradlew` says permission denied.** `chmod +x gradlew`.

**Gradle downloads things on the first run.** Expected, once, for the wrapper and
JUnit. After that the project is offline.

**The comparison table in Act 4 looks ragged.** The demo assumes a fixed-width
font and about seventy-five columns. Widen the window or reduce the font size; the
arithmetic is unaffected.

**The em dashes and `£` signs show as question marks.** Your terminal is not on
UTF-8. `export LANG=en_GB.UTF-8` usually fixes it.

**A test fails after I added a field to a backend.** That is the test working. A
backend may only send what its screen draws, and the screens are written down in
`Screens.java`. Add it there too if the screen really does draw it.

---

## Recommended Reading Order

1. `docs/problem-statement.md` — five calls from a train, and the field the shared
   endpoint could not give anybody.
2. `./gradlew run` — watch all seven acts before reading any source.
3. `docs/backends-for-frontends-pattern-explained.md` — the pattern, then the bill.
4. `docs/animation.html` — the three designs drawn one after another.
5. `docs/class-diagram.md` and `docs/uml-diagram.md` — the structure and the
   sequences, including the two rejected designs.
6. The source, in this order: `Screens`, `CallLog`, `Shop`, `ChattyPhone`,
   `SharedApi`, `ClientBackend`, `MobileBff`, `WebBff`, then the three bill classes
   `SavingRules`, `CrossCutting` and `ClientEstate`.
7. `docs/session.md` if you are running this for a group.
