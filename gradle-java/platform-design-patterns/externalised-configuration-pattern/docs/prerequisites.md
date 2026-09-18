# Prerequisites

This is the first project in the platform category as most people will meet it, and
it is deliberately the gentlest one. If you have written a Java class with a
constant in it and then been asked to change the constant, you already understand
the problem.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, interfaces, `final` fields, and what a `static final`
  constant is.
- **Records** — Java 16's `record`. If you have not met them, the 60-second primer
  below covers everything this project uses.
- **`Optional`** — `isEmpty`, `orElseThrow`, `map`. Used to say "this key has no
  value" without inventing one.
- **Unchecked exceptions** — what it means for an exception to travel up through
  callers that did not ask about it.

### Helpful, but explained as we go

- **`java.time`** — `LocalDateTime`, `Duration`, `DayOfWeek`. The release pipeline
  walks a working-hours calendar, but the arithmetic is all in one class and you can
  read the demo output without it.
- **Having deployed something** — if you have ever waited for a pipeline to go
  green so a one-line change could reach production, act 2 will land harder.
- **Spring's `@Value` or a `.properties` file** — you will recognise the shape
  immediately, and the interesting question becomes what those tools do *not* do for
  you.

### Explicitly NOT required

- **No Spring, no Docker, no Kubernetes, no config server.** Tier 1 of this project
  — which is all of the code, all of the tests and all of the video — runs offline
  with nothing but a JDK. `ConfigServer` is a map in the same JVM with a clock
  bolted on.
- **No network, no HTTP, no YAML, no JSON.** A configuration source stores text
  against keys. The file format it happens to use teaches you nothing about the
  pattern.
- **No prior platform patterns.** This project does not depend on any of the other
  seven. The listed order in the category is a dependency order for the material,
  not a difficulty order.

## A 60-Second "Record" Primer

A record is a class whose whole job is to hold a few values:

```java
public record ConfigChange(int sequence, LocalDateTime at, String key,
                           String was, String now, String who) { }
```

That one line gives you a constructor taking all six values, a getter for each one
named after the field (`change.who()`, not `change.getWho()`), plus `equals`,
`hashCode` and `toString`. Records are shallowly immutable: there are no setters and
the fields cannot be reassigned.

You can add methods, and this project does — `ConfigChange.asLine()` formats a line
for the audit report, and `MoneySetting.read(String)` turns text into money or
throws. A record is a normal class with the boilerplate written for you.

## A 60-Second "Configuration" Primer

**Configuration** is any value your program needs that is not part of its logic: a
free-delivery threshold, a page size, a timeout, the address of another service.

The question this project is about is *where the value lives*.

**Internal configuration** lives in the compiled program, as a constant. Changing it
means producing a new program: edit, review, build, test, approve, deploy.

**Externalised configuration** lives outside the program — a file, an environment
variable, a config server — and is read while the program runs. Changing it means
changing a value.

Two things follow from that, and the second is the one to hold onto.

First, the change becomes fast. This project measures it: four seconds against two
hours fifteen of pipeline work spread over a weekend.

Second, the value loses its guards. A constant in the source is protected by the
compiler (it cannot be the word "fifty"), by the type system (it cannot be a
postcode), and by whoever reviews the change (they would query minus one pound).
None of that follows the value out of the source file. You have to rebuild those
guards deliberately, and most of this project is about doing so.

## A 60-Second "Release Window" Primer

Most organisations do not deploy whenever they feel like it. Releases happen inside
a **window** — commonly weekday working hours — because that is when the people who
review, approve, and watch a release for problems are at their desks. Outside the
window there is a **change freeze**.

This is a sensible policy and not a failure of nerve. It is also why act 2 of the
demo matters: a fifteen-minute edit requested at half past four on a Friday does not
go live two hours later. It goes live on Monday, after the weekend the promotion was
for.

`ReleasePipeline` in this project models exactly that: five steps totalling 135
minutes of work, and a window from 09:00 to 17:00, Monday to Friday.

## Software Prerequisites

| Need | Version | Why |
| --- | --- | --- |
| JDK | 21 or later | Records, sealed types, the Gradle toolchain |
| Gradle | none to install | The wrapper (`./gradlew`) fetches what it needs |

Nothing else. No Spring, no container runtime, no config server.

### Verify Your Setup

```bash
java -version          # expect 21 or later
cd platform-design-patterns/externalised-configuration-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 54 tests
./gradlew -q run       # expect nine acts of output
```

If `java -version` reports something older than 21, the Gradle toolchain will try to
download a suitable JDK on the first build, which needs a network connection once.

## Troubleshooting

**`./gradlew: Permission denied`** — `chmod +x gradlew`.

**The demo prints different times than the documents quote** — it should not. Every
date in the demo is fixed and there is no clock or randomness anywhere;
`DemoRunsTest.theDemoIsDeterministic` runs it twice and requires identical output.
If you see drift, something has been edited.

**`£` characters appear as mojibake** — your terminal is not reading UTF-8. Try
`JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF-8 ./gradlew -q run`.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the constant, and what changing
   it actually costs
2. Run `./gradlew -q run` and read all nine acts of output
3. [`externalised-configuration-pattern-explained.md`](externalised-configuration-pattern-explained.md)
   — the pattern, the three moves, and the bill
4. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
5. [`animation.html`](animation.html) — step through the nine acts in a browser
6. The source, starting with `HardCodedCheckout` and then `ConfiguredCheckout`
7. `TheBillTest` — the two tests that pass and should worry you
