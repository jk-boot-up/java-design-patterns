# Session Guide — Sidecar on Kubernetes Pattern

A 60-minute session built around one question: what does Kubernetes add to a sidecar that Compose does not, and is it worth it?

## Learning Objectives

1. Explain shared by definition against shared by configuration.
2. Say what is shared in a Pod and what is not.
3. Explain injection, and what a service mesh does with it.
4. Answer whether a small shop needs Kubernetes yet.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and Compose |
| 0:10–0:22 | The shared network |
| 0:22–0:36 | Lifecycle and restarts |
| 0:36–0:48 | Injection and READY |
| 0:48–1:00 | The bill |

## Walkthrough

```bash
cd platform-design-patterns/sidecar-on-kubernetes-pattern
./gradlew -q run
```

Act one: what would you have to remember in Compose? Act two: who is deleted with whom? Act three: which container restarted, and which did not? Act four: who wrote the sidecar? Act five: what does 1/2 mean for traffic? Act six: how many services do you run?

## Exercises

1. Add a second sidecar, a log shipper, to the Pod. What does it share?
2. Make the proxy crash three times. What would a real kubelet do that the model does not?
3. Inject into an already-injected spec. Why is that safe?

Close with the honest answer: for four services, probably not yet.
