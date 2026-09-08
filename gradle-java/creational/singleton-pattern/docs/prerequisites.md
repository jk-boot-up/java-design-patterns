# Prerequisites

What to know, and what to install, before working through this project.

## What You Should Already Know

| Topic | How much | Where it shows up |
| --- | --- | --- |
| Classes and objects | Comfortable | Everywhere |
| Constructors and `new` | Comfortable | `LegacyOrderSequenceGenerator`'s private constructor |
| `enum` | Basic — this project uses the simplest possible form, one constant | `OrderSequenceGenerator` |
| Static fields and methods | Comfortable | `LegacyOrderSequenceGenerator.getInstance()` |
| Reflection (`Constructor`, `setAccessible`) | None needed — 60-second primer below | Both attack tests |
| Object serialization | None needed — 60-second primer below | Both attack tests |
| Threads / concurrency basics | Basic — just enough to read a test using `ExecutorService` | `OrderSequenceGeneratorTest` |
| JUnit 5 | Helpful, not required | `src/test` |

## 60-Second `enum`-as-Singleton Primer

```java
public enum OrderSequenceGenerator {
    INSTANCE;
}
```

`INSTANCE` here is not a variable you assign — it is a constant the
compiler creates for you, once, the first time the class is loaded. Every
`OrderSequenceGenerator.INSTANCE` anywhere in the program refers to that
same object. There is no way to write `new OrderSequenceGenerator()` at
all — enum constructors exist, but only the enum's own constant
declarations may call them.

## 60-Second Reflection Primer

```java
Constructor<Foo> ctor = Foo.class.getDeclaredConstructor();
ctor.setAccessible(true);      // bypass the "private" access check
Foo instance = ctor.newInstance();
```

Reflection lets code inspect and call class members — including `private`
ones — by name at runtime, bypassing the compiler's normal access checks
via `setAccessible(true)`. It exists for legitimate reasons (frameworks,
serialization libraries, testing tools all rely on it), but it also means
"private" is a compile-time convention, not an absolute runtime guarantee
— which is exactly what lets `LegacyOrderSequenceGeneratorTest` construct a
second instance despite the private constructor.

## 60-Second Serialization Primer

```java
ByteArrayOutputStream bytes = new ByteArrayOutputStream();
new ObjectOutputStream(bytes).writeObject(someObject);
// ... later, possibly in a different process ...
Object copy = new ObjectInputStream(new ByteArrayInputStream(bytes.toByteArray())).readObject();
```

Java's built-in serialization turns an object into bytes and back,
`readObject()` rebuilding a new object from those bytes without ever
calling the original class's constructor. For an ordinary class that means
deserializing a "singleton" produces a second, independent instance. For an
`enum`, the language defines the serialized form as the constant's *name*,
and deserialization looks that name up against the enum's existing
constants rather than building anything new — which is why
`OrderSequenceGeneratorTest.serializationReturnsTheSameInstance` gets the
same `INSTANCE` back.

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

All tests should pass — they cover instance identity, order-number
formatting, the reflection attack rejected on the enum and succeeding on
the legacy class, the serialization round trip returning the same instance
on the enum and a different one on the legacy class, and concurrent calls
never producing a duplicate order number.

And to watch it work:

```bash
./gradlew run
```

You should see the enum singleton issue order numbers, reject a reflection
attack, and survive a serialization round trip — followed immediately by
the legacy class falling to both.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Unsupported class file major version` | JDK older than 21 | Install JDK 21+ |
| `./gradlew: Permission denied` | Wrapper not executable | `chmod +x gradlew` |
| Download hangs on first run | Offline or behind a proxy | Connect, or install Gradle and use `gradle` instead of `./gradlew` |
| `InaccessibleObjectException` on the reflection tests | Running on a JDK with stricter module access than this project assumes | Run with `--add-opens java.base/java.lang=ALL-UNNAMED`, or use JDK 21 as documented |

## Where to Go Next

1. [`problem-statement.md`](problem-statement.md) — why an instance per
   caller, and the classic private-constructor shape, both fall short
2. [`singleton-pattern-explained.md`](singleton-pattern-explained.md) —
   the technique, and the code
3. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
   — the two pictures
4. [`animation.html`](animation.html) — step through it in a browser
