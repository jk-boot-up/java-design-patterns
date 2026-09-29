# Session Guide — Domain Service Pattern

## Learning Objectives

By the end of the session you can:

- Decide whether a rule belongs to an object or to a service.
- Write a stateless domain service named in business words.
- Explain the difference between a domain service and an application service.
- Recognise an anemic domain model.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: The rule, copied twice | 7 min |
| 0:17 | Act 2: A domain service | 7 min |
| 0:24 | Act 3: In the shop's words | 7 min |
| 0:31 | Act 4: One service, every case | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: two prices for the same order. Open
`Copies` and find the one line that differs. Then open `PricingService` and
`Model.Basket` side by side: which rule belongs where, and why?

## Exercises

1. Add a free-delivery rule for gold customers over £50. Service or entity?
2. Add a second coupon type, 10% off. Where does the percentage live?
3. Write an application service `Checkout` that loads a basket, calls PricingService and saves an order. What must it not contain?
