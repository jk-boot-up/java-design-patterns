# Session Guide — Repository with Spring Data Pattern

A 60-minute session built around one question: what does Spring Data supply, and what does it leak?

## Learning Objectives

1. Explain what an interface with no implementation means.
2. Say how a query is built from a method name.
3. Explain N+1 and the entity-graph fix.
4. Explain why a change to a returned entity may or may not be saved.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:22 | No implementation |
| 0:22–0:36 | Names and queries |
| 0:36–0:50 | N+1 and the leak |
| 0:50–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/repository-with-spring-data-pattern
./gradlew -q run
```

Act one: find the class that implements the interface. Act two: read the method name aloud. Act three: what would your typo have cost in the partner project? Act four: how many statements, and why seven? Act five: which change was written, and why?

## Exercises

1. Add `findByNameStartingWith` and call it. Write no other code.
2. Make `moveFirstCustomerOutsideATransaction` save its change. What must be added?
3. Return a `CustomerDto` from a repository method instead of an entity.

Close with: the interface hides the database, and the entity it returns does not hide the persistence context.
