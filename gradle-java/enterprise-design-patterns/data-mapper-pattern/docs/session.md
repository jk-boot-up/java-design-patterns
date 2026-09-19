# Session Guide — Data Mapper Pattern

A 60-minute session built around one question: should an object know how it
is stored?

## Learning Objectives

1. Say when Active Record is the right answer.
2. Name three costs of an object that saves itself.
3. Explain what a mapper does and what the domain object no longer does.
4. Describe how a hand-written mapping can fail without an error.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:10 | Setup, and Active Record working |
| 0:10–0:22 | The cost |
| 0:22–0:36 | The pattern |
| 0:36–0:48 | The bill |
| 0:48–1:00 | Exercises |

## Walkthrough

```bash
cd enterprise-design-patterns/data-mapper-pattern
./gradlew -q run
```

Act one: count the operations. Act two: open `ActiveRecordCustomer` and
list everything it knows about storage. Act three: which of the two shapes
would you meet first in a real store? Act four: open `Customer` and find any
mention of a table. Act five: find the missing column in
`CarelessCustomerMapper`.

## Exercises

1. Add a `phone` field to `Customer` and to the mapper. Which files change?
2. Write a round-trip test that would have caught act five.
3. Rename the `email` column in the toy database. What breaks in each design?

Close with: the mapper is not free, but it lets the domain live without a database.
