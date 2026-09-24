# Session Guide — Database per Service with Containers Pattern

A 60-minute session built around one question: once each service has its own database on its own engine, what does each engine still promise, and what did the shop give up?

## Learning Objectives

1. Say, in plain words, what a table, a join, a foreign key, a transaction, a document, a collection and `$lookup` are.
2. Show why a correct rename in a shared database breaks another team's page, and why the same rename is harmless after the split.
3. Explain why a join across two engines cannot be written, and why MongoDB's lookup answers "nothing" rather than failing.
4. Explain why a rollback in one engine does not undo a write in the other.
5. Say what a page should show when one of its two services does not answer.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The shared filing cabinet, and the twin project recapped in two minutes |
| 0:08–0:18 | Acts one and two: one join, a foreign key, and a rename that breaks somebody else |
| 0:18–0:28 | Act three: two services, two engines, two shapes of product |
| 0:28–0:40 | Act four: the join tried from both sides |
| 0:40–0:50 | Acts five and six: no foreign key, no shared rollback, half a page |
| 0:50–0:55 | The verdict |
| 0:55–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd micro-services-design-patterns/database-per-service-with-containers-pattern
./gradlew -q run
```

Act one: what did the foreign key protect, and who wrote it? Act two: whose tests should have caught the rename, and why could they not? Act three: why is the page 2 round trips now, and why did the rename not reach it? Act four: Postgres refused twice, and MongoDB answered — which is worse, and why? Act five: who is now responsible for the kettle that ord-101 names? Act six: after the rollback, where are the 2 mugs?

Then open `src/main/java/com/jk/explore/databaseperservicecontainers/OrderService.java` and `CatalogService.java` and read the two constructors aloud. Each takes one engine and nothing else. The pattern is in what they are not given.

## Discussion

Ask the room what the shop should do about the 2 mugs the rollback missed. Put them back by hand? Put them back from code in Orders, which would then need to know about Catalog's stock? Record the intent to put them back, and have something retry until it succeeds? Each answer has a name later in the course; do not give the names yet.

Then ask which query in their own work would quietly return nothing if the data it names moved to another service.

## Exercises

1. In `CatalogService.tryToJoinOrders`, make a real `orders` collection in the catalog database with one document for SKU-MUG, run the demo, and explain the new count.
2. Remove the `ORDER BY` from `OrderService.ordersFor`, run the demo twice, and say whether anything could change.
3. Add a third product to the Catalog with a field neither of the others has, and print its fields.
4. In the sixth act, take the mugs from stock after the payment is approved instead of before, and say what can still go wrong.
5. Make `OrderHistoryPage` show the old name for a deleted product by keeping a copy of it in the Orders database when an order is placed, and say who now owns that copy.

Close with the verdict: give each service its own database and its own engine when the teams need it, and say out loud what that gives up — the join, the foreign key, the shared transaction and the guarantee that both halves are up.
