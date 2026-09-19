# Session Guide — Load Balancing with Spring Cloud LoadBalancer Pattern

A 60-minute session built around one question: what does Spring Cloud LoadBalancer choose, and what does it not know?

## Learning Objectives

1. Explain round robin.
2. Say why fair is not fast.
3. Say what a balancer does not know about health.

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
cd micro-services-design-patterns/load-balancing-with-spring-cloud-loadbalancer-pattern
./gradlew -q run
```

Act one: how were twelve spread? Act two: which copy did the most work? Act three: what changed with a different name? Act four: how many failed? Act five: what did a retry do? Act six: why did a real address fail?

## Exercises

1. Change the cost of copy-c to two.
2. Add a fourth copy.
3. Make the balancer skip a copy that just failed.

Close with the verdict: default first, health or retries, names not addresses.
