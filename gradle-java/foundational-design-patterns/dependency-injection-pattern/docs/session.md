# Session Guide — Dependency Injection Pattern

A 60-minute session built around one question: what happens when a class stops asking for what it needs, and is given it?

## Learning Objectives

1. Say what the constructor signature tells you that a locator hides.
2. Wire an application by hand, and count how long it takes.
3. Choose between constructor, setter and field injection, and say why.
4. State the Registry, Service Locator, Dependency Injection progression.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the signature |
| 0:10–0:22 | Wiring by hand |
| 0:22–0:36 | Three forms |
| 0:36–0:50 | A container, and its costs |
| 0:50–1:00 | The progression and verdict |

## Walkthrough

```bash
cd foundational-design-patterns/dependency-injection-pattern
./gradlew -q run
```

Act one: what does the signature say that `LocatorCheckout` could not? Act two: count the wiring lines. Act three: which form would you refuse in a code review? Act four: read `MiniContainer` from top to bottom. Act five: which failure would you rather have in production? Act six: say the progression in your own words.

## Exercises

1. Add a fourth collaborator to `CheckoutService`, and see what the compiler tells you.
2. Add a `Fraud` service that needs `Notifier`, and let the container wire it.
3. Make two beans depend on each other, and read the message.

Close with the progression, and the verdict: constructor injection, by hand until it hurts.
