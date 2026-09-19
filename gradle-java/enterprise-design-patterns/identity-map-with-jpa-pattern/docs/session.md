# Session Guide — Identity Map with JPA Pattern

A 60-minute session built around one question: what is the persistence context, and what happens when there are two?

## Learning Objectives

1. Explain why `first == second` is true in one context.
2. Explain why it is false across two.
3. Say what a detached entity is, and why a change to one is not saved.
4. Name two costs of the context.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:22 | One context |
| 0:22–0:36 | Two contexts, and detached |
| 0:36–0:50 | Stale, and growing |
| 0:50–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/identity-map-with-jpa-pattern
./gradlew -q run
```

Act one: what does `==` say? Act two: how many SQL statements, and why one? Act three: how many UPDATEs, and why? Act four: why is the detached change not saved? Act five: what does refresh do? Act six: what scope would you give the context in a web application?

## Exercises

1. Use `em.merge` to save the detached change. What does it return?
2. Turn on `hibernate.show_sql` and read the statements.
3. Add `em.detach(customer)` inside a context and observe the effect.

Close with: the persistence context is an identity map, and it belongs to one EntityManager.
