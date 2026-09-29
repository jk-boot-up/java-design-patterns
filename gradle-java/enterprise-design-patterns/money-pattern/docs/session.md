# Session Guide — Money Pattern

## Learning Objectives

By the end of the session you can:

- Explain why a `double` cannot hold 0.1 exactly, in one sentence.
- Store a price as whole minor units and a currency.
- Say where rounding should happen, and why it must be a decision.
- Split an amount by ratio without losing a penny.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Prices as doubles | 5 min |
| 0:15 | Act 2: Prices as Money | 5 min |
| 0:20 | Act 3: Currencies travel with the amount | 5 min |
| 0:25 | Act 4: Rounding is a choice, made once | 5 min |
| 0:30 | Act 5: Splitting without losing a penny | 5 min |
| 0:35 | Act 6: The bill | 5 min |
| 0:40 | Exercises | 20 min |

## Walkthrough

Run `./gradlew run` and read act one aloud before looking at any code: the
learners should see 0.30000000000000004 before they are told why. Then open
`Money.java`: two fields, a handful of methods, every one short. Spend the most
time on `allocate`, because it is the part people get wrong, and on the two
VAT totals in act four, because they start the useful argument about where
rounding belongs.

## Exercises

1. Add `negate()` and use it to represent a refund. What should `allocate` do with a negative amount?
2. Add EUR. Which lines of `Money` did you have to change?
3. Change act four to use `RoundingMode.HALF_EVEN`. Does either total change? Why might a bank prefer it?
4. Write a test that a £0.01 amount allocated to three shares gives 1p, 0p, 0p.
