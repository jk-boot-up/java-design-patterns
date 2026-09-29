# Session Guide — Content Enricher Pattern

## Learning Objectives

By the end of the session you can:

- Say what a thin message is and why receivers struggle with it.
- Place an enricher between a sender and its receivers.
- Decide what to do with a message that cannot be enriched.
- Name the two costs: stale copies and bigger messages.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: The thin message | 7 min |
| 0:17 | Act 2: Every receiver looks it up | 7 min |
| 0:24 | Act 3: The enricher | 7 min |
| 0:31 | Act 4: A customer who cannot be found | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act two first: six calls for three orders, and a
warehouse that stops when the customer service stops. Then open
`ContentEnricher.java`: one method, `enrich`, that finds the customer, copies
three fields, and either returns the fuller message or records a problem. End on
act five and ask when a stale address is right and when it is wrong.

## Exercises

1. Add a third receiver, a loyalty service that needs the tier. How many lookups does it add with and without the enricher?
2. Make the enricher add only the fields a receiver asks for. What does that cost?
3. Give the cache an expiry time, and write a test that a moved customer is seen after it expires.
4. When the customer service is down, should the enricher wait and retry, or send the order to the problem list? Try both.
