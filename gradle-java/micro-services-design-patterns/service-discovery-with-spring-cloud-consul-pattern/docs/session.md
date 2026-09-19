# Session Guide — Service Discovery with Spring Cloud Consul Pattern

A 60-minute session built around one question: what does a real registry give you, and where can its list be wrong?

## Learning Objectives

1. Say who registers a service.
2. Explain the difference between a graceful stop and a crash.
3. Say what the client needs when the registry is gone.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:25 | The first acts |
| 0:25–0:40 | The failures of its own |
| 0:40–0:52 | The cost |
| 0:52–1:00 | Exercises and the verdict |

## Walkthrough

```bash
cd micro-services-design-patterns/service-discovery-with-spring-cloud-consul-pattern
./gradlew -q run
```

Act one: who told Consul? Act two: how were six requests spread? Act three: what happened to the hardcoded address? Act four: how quickly did a stop show? Act five: how many requests failed while the entry was stale? Act six: what did the client remember?

## Exercises

1. Change the health check interval to five seconds and rerun act five.
2. Add a client-side cache of the last list.
3. Register a fourth copy and watch act two.

Close with the verdict: register at startup, expect stale entries, retry, and remember the last list.
