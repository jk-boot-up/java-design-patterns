# Session Guide — MVC Pattern

A 60-minute guided session built around one moment: two views of the same
order printing two different totals.

## Learning Objectives

By the end of the session a participant can:

1. Name the three MVC roles and what each is not allowed to know.
2. Explain the difference between classic (observing) MVC and web MVC.
3. Reproduce the naive email's £383.00 bug and explain exactly why it
   happens.
4. Read the ArchUnit rule and say what it forbids in plain English.
5. State one situation where MVC is not worth the separation.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup, and the screen that already works |
| 0:05–0:18 | The bug: two totals for one order |
| 0:18–0:30 | The pattern, and the narrow view interface |
| 0:30–0:40 | Classic MVC vs web MVC vs MVP/MVVM |
| 0:40–0:50 | The rule, as a test |
| 0:50–0:57 | Exercises |
| 0:57–1:00 | When this is too much, and wrap-up |

## 0:00–0:05 — Setup

```bash
cd architectural-design-patterns/mvc-pattern
./gradlew -q run
```

Read act two together: one model, one controller, one view, and a correct
£382.50.

## 0:05–0:18 — The Bug

Read act three. Put `RoundedEmailView.render` on the screen. Ask the room:
does this class do anything wrong in isolation? Most will say no — it
compiles, it is short, and its own arithmetic is internally consistent.

Then ask what it imports. `ProductTable` — the catalogue, not the model.
Trace through the grinder line by hand: 8950 pence, divided by 100 is 89.5,
`Math.round` gives 90, times 100 pence is 9000 — ninety pounds, not
eighty-nine fifty. Total the three rounded lines and compare with the
model's real £382.50.

## 0:18–0:30 — The Pattern, And The Narrow Interface

Open `OrderSummaryView`. One method, one parameter type. Ask: what would
have to change about this interface for `RoundedEmailView`'s bug to have
been possible through it? (Answer: it would need to accept something other
than the finished model — a product, a price, a quantity.) The interface
being narrow is not incidental; it is the entire enforcement mechanism, more
than the ArchUnit rule is.

## 0:30–0:40 — Classic vs Web vs MVP/MVVM

Ask the room to define MVC before you say anything. Let the definitions
disagree — they will. Then lay out the three: classic MVC's view observes
the model; web MVC's controller assembles a model once and hands it to a
template, no ongoing observation; MVP makes the view fully passive, pushed
to by a presenter; MVVM binds a view to a ViewModel's properties. Ask which
one matches whatever web framework the room uses day to day.

## 0:40–0:50 — The Rule, As A Test

Run:

```bash
./gradlew test --tests ArchitectureRuleCatchesTheShortcutTest
```

Read the printed failure together and find `RoundedEmailView` and
`ProductTable` in it by name.

## 0:50–0:57 — Exercises

1. **Widen the model on purpose.** Add a method to `OrderSummaryModel` that
   exposes rounded-to-the-pound unit prices, and rewrite a corrected email
   view to use it instead of reaching into `ProductTable`. Confirm both
   views now agree.
2. **Add a third view.** Write a one-line `PlainTextReceiptView` and add it
   to a `CompositeOrderView` alongside the other two. Note how little of the
   existing code had to change.
3. **Break the model-does-not-know-views rule on purpose.** Add an import of
   `ScreenSummaryView` to `OrderSummaryModel`, run the tests, and read the
   failure.

## 0:57–1:00 — When This Is Too Much, And Wrap-Up

Ask directly: when is building a separate model, view and controller not
worth it? Push for "a program with exactly one output that will never grow a
second" as the concrete answer.

Close with the sentence worth remembering: two views cannot disagree about a
number neither of them is allowed to calculate.
