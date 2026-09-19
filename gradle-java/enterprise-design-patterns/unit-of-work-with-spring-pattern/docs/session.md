# Session Guide — Unit of Work with Spring Pattern

A 60-minute session built around one question: what does @Transactional actually do, and where does it surprise?

## Learning Objectives

1. Explain what `@Transactional` replaces from the hand-built version.
2. Explain why a checked exception commits.
3. Explain why a query can cause a write.
4. Explain why a call on `this` ignores the annotation.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and the dependency |
| 0:10–0:22 | The annotation |
| 0:22–0:36 | The checked exception |
| 0:36–0:50 | The flush and the proxy |
| 0:50–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/unit-of-work-with-spring-pattern
./gradlew -q run
```

Act one: what is committed, and why? Act two: read the counts inside the method. Act three: why is half an order committed? Act four: what does `rollbackFor` say? Act five: which line caused the write? Act six: why does the annotation not apply?

## Exercises

1. Change `StockFailure` to extend `Exception`. What happens in act two?
2. Move `placeLines` into another bean and call it from `placeViaThis`. What changes?
3. Add `em.flush()` inside `TransactionalPlacement.place`. When are writes issued now?

Close with: an annotation hides the mechanism, and the mechanism still has rules.
