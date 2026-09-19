# Session Guide — API Gateway with Spring Cloud Gateway Pattern

A 60-minute session built around one question: what does Spring Cloud Gateway give you, and what does it leave to you?

## Learning Objectives

1. Read a route.
2. Explain why a global filter runs for every route.
3. Say what a gateway does not do.

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
cd micro-services-design-patterns/api-gateway-with-spring-cloud-gateway-pattern
./gradlew -q run
```

Act one: which addresses did the client use? Act two: what path did pricing see? Act three: how many requests reached a service without a token? Act four: which status did a dead service give? Act five: how many calls did a page take? Act six: who answered for the slow service?

## Exercises

1. Add a route for orders, and test it.
2. Add a filter that logs the path.
3. Map the 500 for a refused connection to a 503.

Close with the verdict: routing and filters at the edge, timeouts everywhere, compose elsewhere.
