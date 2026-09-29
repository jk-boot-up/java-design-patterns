# Session Guide — Private Class Data Pattern

## Learning Objectives

By the end of the session you can:

- Explain how a class can damage its own data.
- Move protected fields into a private, final data object.
- Keep working state that must change beside it.
- Tell this pattern apart from a fully immutable object.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: A method changes its own figures | 7 min |
| 0:17 | Act 2: Private class data | 7 min |
| 0:24 | Act 3: Nothing can write | 7 min |
| 0:31 | Act 4: Working state beside the data | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: the same invoice printed twice gives two
different totals. Open `LooseInvoice.printWithStaffDiscount` and find the line
that does it. Then open `Invoice`: one private record, one counter.

## Exercises

1. Add a `VAT rate` to InvoiceData and a method that prints the total with VAT.
2. Try writing `data.netPence = 0` inside Invoice and read the compiler's message.
3. Add a credit note: a new Invoice with a negative total, rather than changing the old one.
