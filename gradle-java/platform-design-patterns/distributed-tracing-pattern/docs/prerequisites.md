# Prerequisites

This project is written for beginners. If you can read a Java method and follow a
`for` loop, you have enough. Everything else is explained as it arrives.

There is no network, no Docker, no cloud account and no tracing backend. The whole
of Tier 1 runs offline with a JDK and nothing else.

---

## Knowledge Prerequisites

### Required

- **Java basics** — classes, methods, `final`, and reading a stack trace.
- **Collections** — `List` and `Map`, and being comfortable with a `for` loop over
  a list.
- **The idea that a program can call another program.** Not the mechanics. Just
  the idea that when you open a web page, the thing that answers you may ask three
  other things before it answers.

### Helpful, but explained as we go

- **Records** — Java's short syntax for "a value with named fields". Primer below.
- **try-with-resources** — the `try (Something x = ...)` form. Primer below.
- **Streams** — a few methods use `.stream().filter(...).toList()`. Every one of
  them could be a `for` loop and means exactly what it looks like it means.
- **Thread-locals** — a variable whose value is private to each thread. Explained
  where it appears, because its behaviour is the lesson rather than the mechanism.

### Explicitly NOT required

- Any experience with Jaeger, Zipkin, OpenTelemetry, Datadog or any other tool.
- Any experience with microservices, Kubernetes, or service meshes.
- Any concurrency knowledge. There is exactly one background thread in the whole
  project, and the demo waits for it.
- HTTP headers, or knowing what `traceparent` is. It is mentioned once, as the
  thing the Tier 2 directory uses.

---

## A 60-Second "Record" Primer

A `record` is Java's short way of saying "a value made of these named fields".

```java
public record Span(String traceId,
                   String spanId,
                   String parentSpanId,
                   String name,
                   long startMillis,
                   long durationMillis) { }
```

That one line gives you a constructor taking all six values, a getter for each one
named after the field — `span.name()`, not `span.getName()` — and sensible
equality, so two spans with the same six values are equal.

Records are immutable. There is no `setSpan(...)`. Once a span is recorded it
cannot be edited, which is the right property for a measurement of something that
has already happened.

You will also see a **compact constructor**, which is where a record checks itself:

```java
public Span {
    if (durationMillis < 0) {
        throw new IllegalArgumentException("a span cannot last negative time");
    }
}
```

No parameter list and no assignments — Java fills those in. The body runs before
the fields are set, so the object either exists and is valid, or does not exist.

---

## A 60-Second "try-with-resources" Primer

You have probably seen this form with files:

```java
try (BufferedReader reader = new BufferedReader(...)) {
    // read
}   // reader.close() happens here, even if something is thrown
```

Anything implementing `AutoCloseable` can go in those brackets, and Java
guarantees `close()` is called on the way out — normally or by exception.

This project uses it for spans:

```java
try (Tracer.Scope pricing = tracer.start(request, "pricing")) {
    clock.advance(180);
}
```

The closing brace is where the span is **recorded**, because that is the moment its
duration is known. That makes the brace load-bearing in a way it is not with a
file: a span that is started and never closed does not appear in the trace at all.

---

## A 60-Second "Span" Primer

This is the one piece of vocabulary the project cannot do without, so it is worth
thirty seconds even if the word is already familiar.

- A **trace** is everything that happened because of one customer request.
- A **span** is one unit of work inside it — one service call, one database query,
  one piece of computation.
- A span carries four things: a **name**, a **start**, a **duration**, and the id
  of the span that **caused** it.
- The one span with no parent is the **root**, and it is the front door.

The fourth of those is the one that matters. Without it you have timings. With it
you have a tree, and a tree can be added up.

A useful sentence to keep: *a log line says when something happened; a span says
when it happened and because of what.*

---

## A 60-Second "Self Time" Primer

The single piece of arithmetic in the project.

A span's **duration** is how long it lasted. Its **self time** is its duration
minus however long its children lasted — in other words, the time it was actually
working rather than waiting.

The product page span lasts nine hundred milliseconds, which is the whole request.
Its self time is **zero**, because it did nothing except wait for five other
things. That is why "which span lasted longest" never names a culprit and "which
span has the most self time" always does.

If the idea feels slippery, think of a manager whose day is eight hours long and
who spent all eight of them in meetings run by other people. Their day is the
longest on the team. Their own work is zero.

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
cd gradle-java/platform-design-patterns/distributed-tracing-pattern
./gradlew test
./gradlew run
```

`test` should report 82 tests passing. `run` should print seven acts, ending with
`kept       10,000` and a request that was not.

If `run` prints the same thing twice in a row, that is not luck — the clock is
scripted precisely so that it does, which is what lets the documents and the video
quote exact figures.

---

## Troubleshooting

**`./gradlew` says permission denied.** `chmod +x gradlew`.

**Gradle downloads things on the first run.** Expected, once, for the wrapper and
JUnit. After that the project is offline.

**The waterfall bars look ragged in my terminal.** The drawing assumes a
fixed-width font and about eighty columns. Widen the window or reduce the font
size; the arithmetic is unaffected.

**The em dashes and `£` signs show as question marks.** Your terminal is not on
UTF-8. `export LANG=en_GB.UTF-8` usually fixes it.

---

## Recommended Reading Order

1. `docs/problem-statement.md` — the nine hundred milliseconds, and why four
   healthy logs cannot explain them.
2. `./gradlew run` — watch all seven acts before reading any source.
3. `docs/distributed-tracing-pattern-explained.md` — the pattern, then the bill.
4. `docs/animation.html` — the waterfall assembling itself, span by span.
5. `docs/class-diagram.md` and `docs/uml-diagram.md` — the structure and the
   sequences, including both sides of the thread boundary.
6. The source, in this order: `TraceContext`, `Span`, `Tracer`, `Trace`,
   `Waterfall`, then the three bill classes.
7. `docs/session.md` if you are running this for a group.
