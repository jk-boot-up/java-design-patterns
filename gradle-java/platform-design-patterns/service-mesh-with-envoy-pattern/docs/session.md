# Session Guide — Service Mesh with Envoy Pattern

A 60-minute session built around one question: what does a real proxy do for a service, and what must you still get right?

## Learning Objectives

1. Say what the Envoy configuration sets.
2. Explain why the payment service received three calls.
3. Say what a header cannot prove.
4. Name three costs.

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
cd platform-design-patterns/service-mesh-with-envoy-pattern
./gradlew -q run
```

Act one: which callers failed? Act two: how many calls did payments receive? Act three: what changed with one setting? Act four: who was refused? Act five: what did Envoy count? Act six: how many calls did one request cause?

## Exercises

1. Allow only checkout, and see refunds refused.
2. Add a timeout to the route.
3. Set num_retries to 10 and count what payments receives.

Close with the verdict: policy in the proxy, small retries, certificates for identity, configuration reviewed.
