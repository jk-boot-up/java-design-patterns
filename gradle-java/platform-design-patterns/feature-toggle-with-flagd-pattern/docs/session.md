# Session Guide — Feature Toggle with flagd Pattern

A 60-minute session built around one question: what does a real flag daemon give you, and what does it cost?

## Learning Objectives

1. Say where the flag is stored.
2. Explain why a change needs no restart.
3. Say what happens when the daemon is down.
4. Name the costs.

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
cd platform-design-patterns/feature-toggle-with-flagd-pattern
./gradlew -q run
```

Act one: how many deploys? Act two: what did the order cost after the edit? Act three: how many named testers got it? Act four: how many orders failed after the switch was off? Act five: what did the order cost with flagd stopped? Act six: how many combinations?

## Exercises

1. Add a flag for express shipping.
2. Make the rollout 50 percent and count.
3. Make a stopped flagd mean on, and think about what breaks.

Close with the verdict: flags outside the code, repeatable rollouts, down means off, and remove settled flags.
