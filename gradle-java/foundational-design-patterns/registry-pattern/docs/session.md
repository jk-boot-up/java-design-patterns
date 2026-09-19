# Session Guide — Registry Pattern

A 60-minute session built around one question: how does an object get hold of what it needs, and what does each answer hide?

## Learning Objectives

1. Say why passing dependencies down is friction.
2. Explain what a registry removes and what it hides.
3. Explain why a test can fail because of the order tests ran in.
4. Say the one place a registry is the best answer.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the six constructors |
| 0:10–0:20 | The registry |
| 0:20–0:36 | Invisible dependencies |
| 0:36–0:50 | Order dependence and the contents |
| 0:50–1:00 | The verdict |

## Walkthrough

```bash
cd foundational-design-patterns/registry-pattern
./gradlew -q run
```

Act one: count the classes that forward the gateway. Act two: read the checkout's constructor. Act three: what should the class have told you? Act four: run the two tests in both orders. Act five: where would you look to see what is registered? Act six: which of your application's objects are truly application-wide?

## Exercises

1. Add `@BeforeEach Registry.clear()` to a test class and explain what it fixes and hides.
2. Make `Registry.register` refuse to overwrite. What breaks?
3. Pass the three collaborators to `RegistryCheckout`'s constructor. What did you get back?

Close with the verdict: narrowly, for a very few application-wide things, and never for what tests must replace.
