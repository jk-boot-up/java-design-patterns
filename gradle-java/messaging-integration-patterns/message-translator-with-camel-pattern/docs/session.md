# Session Guide — Message Translator with Apache Camel Pattern

## Learning Objectives

By the end of the session you can:

- Write a translator as a Camel route.
- Use Camel data formats to read CSV and JSON.
- Build a normalizer with a header and `toD`.
- Add a route to a running Camel context.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Straight to the warehouse | 7 min |
| 0:17 | Act 2: A translator route per format | 7 min |
| 0:24 | Act 3: The normalizer | 7 min |
| 0:31 | Act 4: A new format, a new route | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Open `ShopRoutes.configure`: the normalizer is three
lines, each translator three or four. Compare act four's two lines: the
error before the XML route exists, and the pick after.

## Exercises

1. Use camel-jacksonxml instead of XPath for the XML translator.
2. Send orders with no recognisable format to a dead-letter route.
3. Carry the gift note by adding a field to OrderMessage and every translator.
