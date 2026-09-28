# Lazy Load Pattern — Video Narration Script

## 1. Lazy Load

Hello, and welcome. This video explains the Lazy Load pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Load the object you asked for now. And load the things it refers to only when someone actually asks for them. Think of a video streaming service. It does not download the whole film before you start. It fetches each part just before you watch it. In our online store, this is the difference between loading one order, and accidentally loading the whole shop. By the end, you will know four ways to do it. Why it can make a page slower, not faster. And why one of the most searched Java errors happens.

## 2. The Scenario

Here is the scenario. A page needs to show one order. That order has a customer. The customer has other orders. Those orders have lines. The lines have products. And the products have categories. Everything is connected to everything. So how much of that should loading one order drag in?

## 3. Eager Loading

First, the naive way: eager loading. Load everything that can be reached, straight away. The demo asks for one order. Thirty-seven objects are created. And twenty-six database queries are made. There is no mistake here, and no loop in the data. Everything is simply connected. So loading anything loads nearly everything.

## 4. The Pattern

Now, the pattern, and it is simple to say. Load the order now. Load the rest only when someone asks for it. And the caller should not notice the difference. There are four common ways to build it, and you will meet all four in real code.

## 5. Four Ways To Load Later

Second demo: four ways to load later. One: lazy initialisation. A field stays empty, until its getter is first called. Two: a virtual proxy. A stand-in, with the same interface, that loads the real object on first use. Three: a value holder. The caller knows it holds a promise, and asks for the value. Four: a ghost. An object created with only its I D, which loads everything the first time anything is asked of it. The demo counts each one. Zero queries before use. One query after the first use. And still just one, after the second. They cost nothing, until needed.

## 6. Cost One: N Plus One

Now the costs, and they are heavy. The first: you have swapped one big query for many small ones. A page lists twenty orders, and shows each customer's name. With lazy loading: one query for the orders, then one query for each customer. Twenty-one queries in all. With batching: just two. In a real system, every query is a round trip to the database. So the lazy page can be slower than the eager one it replaced. This problem is called N plus one.

## 7. Cost Two: A Field Is Now I/O

The second cost: reading a field is now a database call. Asking for a customer's name looks like reading a field. But it is not. It is a trip to the database. So it can be slow, and it can fail. In this demo, the database is told to fail the next read. And asking for a name throws an error. Code that assumed a getter could never fail now has an error it never planned for.

## 8. Cost Three: The Closed Session

The third cost catches people out. An object is created while its database session is open. But nothing has been loaded yet. Then the session closes. And the object is passed on to a page. The page asks for the customer's name. The load needs the session. But the session is gone. So it fails. The failure appears where the object was used, not where it was created. That is what makes it so hard to track down.

## 9. Where You Have Met This

You have very likely met this before. In Hibernate, that failure has a name: Lazy Initialization Exception. It is one of the most searched Java errors there is. It is exactly what we just heard. A lazy object, whose session has closed. Now you know the cause, not just the workaround.

## 10. The Toy Database

A word about the database in these demos. It is a toy. It has rows, an operation counter, and now a read that can be told to fail. Every count in this video, the thirty-seven, the twenty-six, and the twenty-one, came from that counter.

## 11. What Is Real Here

A quick, honest note about this demo. The counts are real. But the time for each round trip is not measured, because the toy database has no network. N plus one is slow in a real system, because each query is a trip. Here you hear the count, and you can imagine the delay.

## 12. When This Is Too Much

So, when is this too much? If you almost always need the related data, lazy loading only adds extra queries. It earns its place when the related data is large, and rarely needed.

## 13. What To Do About It

So what do you do about the costs? Batch: fetch all the customers in one query. Join: fetch the parts you know you will need, together, up front. And keep the session open until the page is finished. Or load what you need, before the session closes. Each of those is a decision the lazy load made for you, which you are now taking back.

## 14. Thanks for Watching

That's the Lazy Load pattern. If you remember one sentence, make it this one. Lazy loading trades one big query for many small ones, and moves any failure to wherever the object is used. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Change the lazy list, so each customer is fetched only once. Then count the queries again. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
