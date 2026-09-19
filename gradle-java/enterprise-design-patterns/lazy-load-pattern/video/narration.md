# Lazy Load Pattern — Video Narration Script

## 1. Lazy Load

Hello, and welcome. This video explains the Lazy Load pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: load the object you asked for now, and load the things it refers to only when someone actually asks for them. This is the fourth project in the enterprise category. In our online store, it is the difference between loading one order, and accidentally loading the shop. By the end you will know four ways to do it, why it can make a page slower rather than faster, and why one of the most searched Java errors happens.

## 2. The Scenario

Here is the scenario. A page needs one order. That order has a customer. The customer has other orders. Those orders have lines, the lines have products, and the products have categories. Everything is connected to everything. The question is: how much of that should loading one order drag in?

## 3. Eager Loading

The naive way is eager loading: load everything reachable, straight away. The demo asks for one order. Thirty-seven objects are created. Twenty-six database operations are made. And there is no cycle in that graph and no obvious mistake. It is just that everything is connected, so loading anything loads nearly everything.

## 4. The Pattern

The pattern is simple to say. Load the order now. Load the rest only when someone asks for it. The caller is not meant to notice the difference. There are four common ways to build it, and you will meet all four in real code.

## 5. Four Ways To Load Later

Four variants. Lazy initialisation: a field is empty until a getter is called. A virtual proxy: a stand-in with the same interface, which loads the real thing on first use. A value holder: the caller knows it holds a promise, and asks for the value. And a ghost: an object created with only its id, which loads everything the first time anything is asked of it. The demo counts each one. Zero queries before use. One query after the first use. Still one after the second. They cost nothing until needed.

## 6. Cost One: N Plus One

Now the bill, and it is a heavy one. You have replaced one large query with many small ones. A page lists twenty orders, and shows each customer's name. Lazily: one query for the orders, then one for each customer. Twenty-one queries. Batched: two. In a real system every query is a round trip to the database. So the lazy page can be slower than the eager one it replaced. This is called N plus one.

## 7. Cost Two: A Field Is Now I/O

Second cost. Asking for a customer's name looks like reading a field. It is not. It is a database call. So it can be slow, and it can fail. In this demo, the database is told to fail the next read, and asking for a name throws. Code that assumed a getter cannot fail now has an exception it never planned for.

## 8. Cost Three: The Closed Session

Third cost, and the one that catches people out. The object is created while its session is open. Nothing has been loaded yet. Then the session closes, and the object is passed on to a page. The page asks for the name. The load needs the session. The session is gone. It fails. The failure is where the object was used, not where it was created. That is what makes it hard to find.

## 9. Where You Have Met This

You have very likely met this. That failure has a name in Hibernate: lazy initialization exception. It is one of the most searched Java errors there is. It is exactly act five: a lazy object, whose session has closed. Now you know the mechanism, not just the workaround.

## 10. The Toy Database

A word about the database in these demos. It is a toy: rows, an operation counter, and now a read that can be told to fail. Every count in this video, the thirty-seven, the twenty-six, the twenty-one, came from that counter.

## 11. What Is Real Here

The same honest admission as everywhere in this course. The counts are real. The cost of a round trip is not measured, because the toy database has no network. N plus one is slow in a real system because each query is a trip. Here you see the count, and you can supply the latency yourself.

## 12. When This Is Too Much

So when is it too much? If you almost always need the related data, lazy loading just adds queries. It earns its place when the related data is large, and rarely needed.

## 13. What To Do About It

So what do you do about the bill? Batch: fetch all the customers in one query. Join: fetch the parts you know you will need, together. And keep the session open until the page is finished, or load what you need before you leave. Each of those is a decision the lazy load made for you, and now you are making back.

## 14. Thanks for Watching

That's the Lazy Load. If you take one sentence away, take this one: lazy loading trades one big query for many small ones, and moves the failure to wherever the object is used. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, change the lazy list so each customer is fetched only once, and count the queries. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
