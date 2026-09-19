# Session Guide — Service Locator Pattern

A 60-minute session built around one question: what does asking a middleman fix about a registry, and what does it leave?

## Learning Objectives

1. Name two genuine advances over a registry.
2. Show, with the demo, why a missing registration is worse than it looks.
3. Say why every class depending on the locator is a cost.
4. Say where the pattern is still right.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the advances |
| 0:10–0:22 | The test swap |
| 0:22–0:38 | The compiler says nothing |
| 0:38–0:50 | ServiceLoader, and the verdict |
| 0:50–1:00 | Exercises |

## Walkthrough

```bash
cd foundational-design-patterns/service-locator-pattern
./gradlew -q run
```

Act one: which recipe is a singleton and which is a prototype? Act two: what did the swap not need? Act three: in what order did the money and the failure happen? Act four: how many classes ask the locator? Act five: why is ServiceLoader different? Act six: where would you keep a locator?

## Exercises

1. Make `LocatorCheckout` validate its collaborators in a constructor. What did you just rebuild?
2. Add a third plug-in to META-INF/services and run act five.
3. Change act three so the checkout asks for the notifier first. What changes about the bill?

Close with the verdict: the word that matters is ask.
