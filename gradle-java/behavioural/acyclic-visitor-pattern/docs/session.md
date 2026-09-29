# Session Guide — Acyclic Visitor Pattern

## Learning Objectives

By the end of the session you can:

- Explain the dependency cycle in the classic Visitor.
- Build an acyclic visitor from an empty root and one interface per type.
- Add a type without changing existing visitors.
- Weigh compile-time checks against open-ended type lists.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: The classic visitor | 7 min |
| 0:17 | Act 2: The acyclic visitor | 7 min |
| 0:24 | Act 3: A new product type | 7 min |
| 0:31 | Act 4: A visitor for one type | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. In act one, open `ClassicVisitor` and `ClassicCustoms`
and count the empty methods. Then open `ProductVisitor`: an empty interface
with four tiny nested ones. Finish on act five and ask when the classic
version's compiler checks are worth more than the freedom to add types.

## Exercises

1. Add a `Clothing` type and a size-label visitor that handles only clothing.
2. Make the VAT visitor handle gift cards (they are outside the scope of VAT). What changes?
3. Rewrite VAT with a sealed interface and a `switch`. What does the compiler now check?
4. Make `accept` log every skipped product, so act five's silent skip is at least visible.
