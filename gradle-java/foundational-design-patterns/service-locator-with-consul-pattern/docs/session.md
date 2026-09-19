# Session Guide — Service Locator with Consul Pattern

A 60-minute session built around one question: what does a locator over a network add, and what does it leave?

## Learning Objectives

1. Explain what Consul answers when asked for a service by name.
2. Say what changes when an instance fails, and what does not.
3. Explain how a cached answer goes stale.
4. Say what "being given an address" removes.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependencies |
| 0:10–0:22 | The locator asks Consul |
| 0:22–0:36 | Instances change |
| 0:36–0:50 | The old costs, and the stale cache |
| 0:50–1:00 | Be given, and the verdict |

## Walkthrough

```bash
cd foundational-design-patterns/service-locator-with-consul-pattern
./gradlew -q run
```

Act one: how does the checkout know an address? Act two: what changed and what did not? Act three: in what order did the charge and the failure happen? Act four: what would you change to make the cache safe? Act five: who keeps nginx's list correct? Act six: where does your system ask?

## Exercises

1. Give the caching locator a time-to-live. What new decision did you make?
2. Have nginx's configuration regenerated when Consul's list changes.
3. Register a third notifier instance and watch the rotation.

Close with the verdict: discovery is a legitimate locator, and being given an address is better still.
