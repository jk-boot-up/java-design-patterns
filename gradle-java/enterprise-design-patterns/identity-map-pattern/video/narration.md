# Identity Map Pattern — Video Narration Script

## 1. Identity Map

Hello, and welcome. This video explains the Identity Map pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An identity map keeps a list, for one session, from each I D to the one object loaded for it. So asking for the same thing twice gives you the very same object. Think of a library's loan desk. If a book is already out on your card, the librarian does not print you a second copy. You get the one you already have. In our online store, the thing loaded twice is a customer. By the end, you will know how two copies of one customer silently lose a change. Why overriding equals does not fix it. How the map does. And what the map costs.

## 2. The Scenario

Here is the scenario. An order page loads an order, together with the customer who placed it. Somewhere else, the same page loads that same customer directly, by I D. It is one row in the database. So here is the question. How many objects should that be?

## 3. Two Loads, Two Objects

First demo: two loads, two objects. The naive loader builds a fresh object every time. Load the order, and its customer comes with it. Load customer seven by I D, and you get another object. Are they the same object? No. Three database queries were made, for what is really one customer. And two separate objects now both claim to be customer seven.

## 4. The Lost Change

Second demo: the lost change. One of the two objects moves the customer to York. The other changes her email address. Both are saved. And each save writes the whole row. So the second save writes the old address, Leeds, back over the new one. The stored address is Leeds again. The stored email is the new one. The move to York silently disappeared. Nothing failed. The last one to save simply won.

## 5. equals() Is Not Enough

Third demo: overriding equals is not enough. A common first fix is to override the equals method. So two customers with the same I D count as equal. Now the two objects are equal. But they are still two separate objects. One says York. The other still says Leeds. Equal is not the same as being the same object. Each can still be changed on its own.

## 6. The Pattern

Now, the pattern: a map. It lives for one session. And it maps each I D to the one object loaded for it. Ask for customer seven. First, look in the map. Only if it is missing, go to the database, build the object, and put it in the map. Every route to customer seven, including the order's customer, goes through the same map.

## 7. One Map, One Object

Fourth demo: one map, one object. Now the order's customer, and customer seven loaded by I D, are the very same object. Only two queries in total. One for the order, and one for the customer. Ask for customer seven twice more, and it costs no queries at all. Both come straight from the map. And with only one object, one change can no longer overwrite another.

## 8. Cost One: The Map Is A Cache

Now the costs. The first: the map is a cache. Another program changes the customer's email in the database. This session asks again. And the map answers with the old email, because it has no reason to look. A brand new session, with an empty map, sees the new email. Speed and freshness are being traded. And the map decides which one wins.

## 9. Cost Two: It Holds Everything

The second cost: the map holds on to everything. It keeps a reference to every object it has loaded. A bulk load of one thousand customers leaves one thousand objects held in memory, until the session ends. A long-running session with many loads is a memory problem waiting to happen.

## 10. Cost Three: Scope Is A Decision

The third cost: how long the map lives is a decision. And every choice is wrong in some way. One map per request is always fresh. But it may be too small, if two requests need to agree. One map per session goes stale for as long as the session lives. One map for the whole application goes stale, and only ever grows. There is no choice that is free.

## 11. The Toy Database

A word about the database in these demos. It is a toy. It stores rows, not objects. It counts every operation. And it needs nothing installed. Every count in this video came from that counter, not from guessing.

## 12. Where You Have Met This

You have almost certainly met this pattern already. In Java's persistence standard, J P A, the persistence context is an identity map. Load the same entity twice, inside one transaction, and you get the very same object. If a second lookup ever surprised you by not touching the database, this was why.

## 13. What Is Real Here

A quick, honest note about this demo. The pattern is real. The database is a stand-in, with no real transactions, and no second program. The out-of-date data is simulated by writing to the table directly. Which is exactly what another program would do.

## 14. When This Is Too Much

So, when is this too much? A request that loads a customer once, and never again, gains nothing from a map. It earns its place when the same row can be reached by two different routes, as it was here. And when two objects for one row would be a bug.

## 15. Thanks for Watching

That's the Identity Map pattern. If you remember one sentence, make it this one. One row should be one object, per session, and the session decides how long that stays true. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a method that removes one object from the map. And decide when you would call it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
