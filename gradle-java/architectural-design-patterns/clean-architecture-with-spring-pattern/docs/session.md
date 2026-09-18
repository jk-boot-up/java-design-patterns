# Session Guide — Clean Architecture with Spring

A 40-minute session — shorter than the rest of the category on purpose,
because this project owns one comparison rather than a whole architecture.
Run it immediately after a session on `clean-architecture-pattern`, not on
its own.

## Learning Objectives

By the end of the session a participant can:

1. Point at the line in `AppConfig` that corresponds to a specific line in
   §66's hand-wired `PlaceAnOrderDemo.shop()`.
2. State the one contrast this project owns, precisely: hand-wiring fails
   at compile time, container wiring fails at startup.
3. Explain why deleting a `@Bean` method compiles cleanly and where the
   resulting failure actually surfaces.
4. Say what this project would lose nothing by skipping.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup, and side-by-side recall of §66's composition root |
| 0:05–0:15 | `AppConfig`, read next to `shop()` |
| 0:15–0:28 | The one contrast: delete a bean, watch it fail |
| 0:28–0:35 | Exercises |
| 0:35–0:40 | What was not re-taught, and wrap-up |

## 0:00–0:05 — Setup

```bash
cd architectural-design-patterns/clean-architecture-with-spring-pattern
./gradlew run
```

Have `clean-architecture-pattern/src/main/java/.../PlaceAnOrderDemo.java`
open in a second window.

## 0:05–0:15 — `AppConfig`, Read Next To `shop()`

Go method by method. For every `@Bean` method, find the corresponding line
in `shop()`. Land the point: the correspondence is exact, and that is the
entire content of this section.

## 0:15–0:28 — The One Contrast

Ask the room to predict what happens if a constructor argument is deleted
from the hand-wired call. Then ask what happens if the corresponding
`@Bean` method is deleted instead. Run:

```bash
./gradlew test --tests WiringContrastTest
```

Read `BrokenAppConfig.java`. Confirm it compiles on its own
(`./gradlew compileJava` after temporarily copying it in place of
`AppConfig` — or simply trust the test). Discuss: which failure would you
rather have, and why might the answer depend on whether you already have
good tests?

## 0:28–0:35 — Exercises

1. **Break it yourself.** Comment out `paymentGateway()` in `AppConfig`
   temporarily, run `./gradlew run`, read the failure, then restore it.
2. **Add a bean.** Wire a fifth, imaginary gateway with its own `@Bean`
   method and give it to nothing, then ask whether an unused bean is a
   cost the way an unused hand-written class would be.

## 0:35–0:40 — What Was Not Re-Taught, And Wrap-Up

Ask directly: which parts of Clean Architecture did this session skip?
(Entities, use cases, the dependency-inversion moment, the forced change,
the bill — all of it, because §66 already covered it completely.)

Close with the sentence worth remembering: `@Component` is not magic. It is
the twenty lines you have already seen written by hand.
