# Session Guide — Service Layer Pattern

A 60-minute session built around one question: where should "place an order" live?

## Learning Objectives

1. Explain how a copied entry point drifts.
2. Say why putting everything in the domain object fails.
3. Say what the service owns and what the domain owns.
4. Describe the anemic domain model.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and one door |
| 0:10–0:22 | The second door |
| 0:22–0:36 | The pattern |
| 0:36–0:50 | The bill and the line |
| 0:50–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/service-layer-pattern
./gradlew -q run
```

Act one: read `ControllerLogic`. Act two: diff `ControllerLogic` and `CopiedInTheCli` and find the difference. Act three: count the constructor arguments. Act four: what does `WebController` decide? Act five: which class holds the rule that stock cannot go negative? Act six: where would your team put free delivery?

## Exercises

1. Add a third door, a batch import. How many files change?
2. Move `deliveryIsFree` into a ShippingService. What do you gain and lose?
3. Add a rule that an order over £1,000 needs approval. Where does it go?

Close with: rules in the domain, orchestration in the service, and every door calls the service.
