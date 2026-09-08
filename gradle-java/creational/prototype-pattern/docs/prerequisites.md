# Prerequisites

What to know, and what to install, before working through this project.

## What You Should Already Know

| Topic | How much | Where it shows up |
| --- | --- | --- |
| Classes and objects | Comfortable | Everywhere |
| Constructors and `new` | Comfortable | `ProductListing`'s constructor |
| Interfaces | Basic — one method is all this project needs | `Prototype<T>` |
| Generics (`<T>`) | Basic — just enough to read `Prototype<T>` | `Prototype<ProductListing>` |
| Mutable collections (`List`, `Map`) | Comfortable — this project is about copying them safely | `images`, `attributes` |
| `record` | None needed — 60-second primer below | `ShippingProfile` |
| Reference equality vs. `equals()` | Basic — the difference between `==` and `.equals()` | Every test in `src/test` |
| JUnit 5 | Helpful, not required | `src/test` |

## 60-Second `record` Primer

```java
public record ShippingProfile(String carrier, int weightGrams, boolean freeShipping) { }
```

That one line gives you a constructor, a getter per field
(`profile.carrier()`, no `get` prefix), plus `equals`, `hashCode` and a
readable `toString` — and, crucially, no setters. `ShippingProfile` is a
`record` here specifically because it never changes, which is what lets a
`ProductListing` copy share the exact same `ShippingProfile` instance as
the listing it was copied from, with nothing to protect.

## 60-Second `==` vs. `.equals()` Primer

```java
ProductListing copy = master.copy();

copy.equals(master);              // true  — same field values
copy == master;                   // false — two different objects in memory

copy.shippingProfile() == master.shippingProfile();   // true — the very same object
```

`.equals()` asks "do these represent the same data?" `==` asks "are these
literally the same object in memory?" This project cares about both: a
copy should `.equals()` its original (same state) while never being `==`
it (independent objects) — except for `shippingProfile()`, which is `==`
on purpose, because it is shared rather than copied.

## 60-Second Shallow-vs-Deep-Copy Primer

```java
List<String> original = new ArrayList<>(List.of("a"));
List<String> shallow = original;              // same list, two names
List<String> deep = new ArrayList<>(original); // a new list, same contents

shallow.add("b");   // original now has 2 elements too
deep.add("c");       // original is unaffected
```

`ProductListing`'s constructor always does the "deep" thing for `images`
and `attributes` — it builds a brand new `ArrayList`/`LinkedHashMap` from
whatever was passed in, rather than holding onto the caller's own
collection. That single habit is what makes `copy()` safe later, without
`copy()` needing any collection-copying logic of its own.

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

All tests should pass — they cover copy independence for `images` and
`attributes`, `.equals()`-but-not-`==` for a copy, `==` for the shared
`shippingProfile`, registry-produced instances being independent of each
other, and the `NoSuchElementException` for an unregistered key.

And to watch it work:

```bash
./gradlew run
```

You should see a master listing, a white variant cloned and tweaked from
it, proof the master's images and attributes are untouched, proof the
shipping profile is the same instance on both, and a `ListingRegistry`
handing back two independent instances from the same key.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | JDK older than 21 | Install JDK 21+ |
| `./gradlew: Permission denied` | Wrapper not executable | `chmod +x gradlew` |
| Download hangs on first run | Offline or behind a proxy | Connect, or install Gradle and use `gradle` instead of `./gradlew` |
| `NoSuchElementException: no listing template registered under: ...` | Typo in a registry key | Check `registry.keys()` for the exact strings registered |

## Where to Go Next

1. [`problem-statement.md`](problem-statement.md) — why re-typing eight
   shared arguments per variant (or reaching for `Cloneable`) is not the
   answer
2. [`prototype-pattern-explained.md`](prototype-pattern-explained.md) —
   the technique, and the code
3. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
   — the two pictures
4. [`animation.html`](animation.html) — step through it in a browser
