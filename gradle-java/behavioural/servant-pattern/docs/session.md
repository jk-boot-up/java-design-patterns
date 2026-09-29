# Session Guide — Servant Pattern

## Learning Objectives

By the end of the session you can:

- Explain why copies of the same behaviour drift apart.
- Say why a shared parent class is not always possible or wanted.
- Write a servant that depends only on a small interface.
- Name the cost: behaviour you cannot find on the object.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Copied postage | 7 min |
| 0:17 | Act 2: One servant | 7 min |
| 0:24 | Act 3: A new kind of item | 7 min |
| 0:31 | Act 4: Tested alone | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: three copies, two of them wrong. Then
open `Shippable` (three methods) and `ShippingServant` (two). Point out that
`Items` contains no shipping code at all, and that `GiftCard` is also a
`Voucher`, which is why a shared parent class would not fit.

## Exercises

1. Add international postage: double the rate when the city is outside the UK. Where does the change go?
2. Add a `CustomsServant` that uses the gift card's value. What interface does it need?
3. Make the servant refuse items over 200 kg.
4. Write a test with a made-up item that proves 0 grams is charged as one started kilo.
