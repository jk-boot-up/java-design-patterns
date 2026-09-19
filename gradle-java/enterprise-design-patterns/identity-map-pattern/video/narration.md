# Identity Map Pattern — Video Narration Script

## 1. Identity Map

Hello, and welcome. This video explains the Identity Map pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: keep a map, for one session, from an id to the one object loaded for it, so asking for the same thing twice gives you the same object. This is the second project in the enterprise category. It solves a problem the Data Mapper creates: once objects and rows are separate, one row can become two objects. In our online store, the row is a customer. By the end you will know how two copies of one customer lose a change silently, why overriding equals does not fix it, how the map does, and what the map costs.

## 2. The Scenario

Here is the scenario. An order page loads an order, and the customer who placed it. Somewhere else, the same code loads that same customer directly, by id. It is one row in the database. The question this video answers is: how many objects should that be?

## 3. Two Loads, Two Objects

The naive mapper builds a fresh object on every load. Load the order, and its customer comes with it. Load customer seven by id, and you get another. Are they the same object? False. Three selects went to the database, for what is one customer. Two objects now both say they are customer seven.

## 4. The Lost Change

Now the bug. One of the two objects moves her to York. The other changes her email. Each does its job. Both are saved, and each save writes the whole row. The second save writes the old address back over the first. The stored address is Leeds again. The stored email is the new one. The move to York silently disappeared. Nothing failed. The last writer simply won.

## 5. equals() Is Not Enough

A common first fix is to override equals, so two customers with the same id are equal. The demo does that. The two objects are now equal. But they are still two objects. One says York. The other still says Leeds. Equal is not the same as the same. Each object is still free to be changed on its own.

## 6. The Pattern

The pattern is a map. It lives for one session, and maps an id to the one object loaded for it. Ask for customer seven. Look in the map first. Only if it is missing, go to the database, build the object, and put it in the map. Every route to customer seven, the order's customer included, goes through the same map.

## 7. One Map, One Object

Same demo, with the map. The order's customer, and customer seven loaded by id, are the same object. True. Two selects in all: the order's own row, and the customer, once. Ask for customer seven twice more, and it costs zero operations. Both come from the map. And with only one object, one change can no longer overwrite another.

## 8. Cost One: The Map Is A Cache

Now the bill. First cost: the map is a cache. Another process changes the customer's email in the database. This session asks again, and the map answers with the old email. It has no reason to look. A brand new session, with an empty map, sees the new one. Speed and freshness are being traded, and the map decides which wins.

## 9. Cost Two: It Holds Everything

Second cost. The map holds a reference to every object it has loaded. A bulk load of one thousand customers leaves one thousand objects held, until the session ends. A long-running session with a lot of loads is a memory problem waiting to happen.

## 10. Cost Three: Scope Is A Decision

Third cost: scope is a decision, and every choice is wrong in some way. Per request is safe from staleness, but too small if two requests need to agree. Per session goes stale for as long as the session lives. Per application is stale, and only ever grows. There is no scope that is free.

## 11. The Toy Database

A word about the database in these demos. It is a toy. It stores rows, not objects, it counts every operation, and it needs nothing installed. Every count in this video, the three selects, the two, the zero, came from that counter, not from guessing.

## 12. Where You Have Met This

You have almost certainly met this. The persistence context in JPA is an identity map. Load the same entity twice inside one transaction, and you get the same object. That is why double equals is true there. If a second find ever surprised you by not touching the database, this was why.

## 13. What Is Real Here

The same honest admission as everywhere in this course. The pattern is real. The database is a stand-in. There are no real transactions here, and no second process. Staleness in act five is simulated by writing to the table directly, which is exactly what another process would do.

## 14. When This Is Too Much

So when is it too much? A request that loads a customer once, and never again, gains nothing from a map. It earns its place when the same row can be reached by two different routes, as it was here, and when two objects for one row would be a bug.

## 15. Thanks for Watching

That's the Identity Map. If you take one sentence away, take this one: one row should be one object, per session, and the session decides how long that stays true. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add an evict method to the session, and decide when you would call it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
