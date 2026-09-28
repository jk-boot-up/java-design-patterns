# Lazy Load with Hibernate Pattern — Video Narration Script

## 1. Lazy Load with Hibernate

Hello, and welcome. This video explains the Lazy Load pattern, in Java, using Hibernate. This video is presented by Jayasekhar Konduru. First, a simple definition. A lazy field does not hold its data straight away. It holds a stand-in, which loads the data the first time someone asks. Think of a gift voucher. It is not the gift itself. It only turns into the gift if you redeem it while the shop is still open. This is the framework version of the Lazy Load video. And it is about one of the most searched Java errors there is: the Lazy Initialization Exception. By the end, you will know exactly what is in a lazy field. Why asking after the session has closed fails. And what each of the three usual fixes costs.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Lazy Load video. That one builds four ways of loading later, by hand, and shows a failure once the session has closed. Here, we use the very same store. Five customers, twenty orders, and four lines in each order. We will not teach the pattern again. Instead, we hear the real error, from Hibernate itself.

## 3. Before The First Annotation

Two things are new in this project. First, Hibernate, the most widely used implementation of J P A, Java's standard for storing objects. You mark your classes, and it turns work on those objects into database commands. Second, H2, a database that runs in memory, inside the test, so nothing needs installing. And one promise. If you skip this video, you lose none of the pattern. This one explains an error.

## 4. One Word Makes It Lazy

Here is the one word that matters. On the order class, the customer, and the order's lines, are both marked with fetch type lazy. That one word is what this whole video is about.

## 5. The Exception

First demo: the error, on purpose. Load an order. Close the session. Then ask the order for its customer's name. The order loaded fine. But asking for the name threw a Lazy Initialization Exception. The message says: could not initialise proxy, customer number one, no session. Notice where it failed. Not where the order was loaded, but where the customer was used. That is why this error is so hard to track down.

## 6. What Is In The Field

So what is actually in that field? Not a customer. Hibernate generated a subclass of the customer class. It holds just two things: the customer's I D, and a link to the session. It has not loaded anything yet. Ask it for the name while the session is open, and it loads the customer. Close the session first, and it has nothing to load with. That is the error. Not a bug, but a promise that needed something that is now gone.

## 7. Fix One: Keep The Session Open

The first usual fix: keep the session open while the page is built. It works. Twenty orders, each showing its customer's name: six database queries, not twenty-one. One for the orders, and one for each of the five different customers. Because the session loads each customer only once. But twenty orders, each showing how many lines it has: twenty-one queries. One for the orders, then one for each order's lines. That is the N plus one problem. The cost: the session, and its database connection, stay open while the page is built. And the extra queries hide inside the page code, where nobody looks.

## 8. Fix Two: Fetch It In The Same Query

The second fix: fetch the related data in the same query, with a join fetch. One query for the customers. And one query for the lines. But there is a hidden cost. Fetching the lines makes the database send eighty rows for twenty orders. Each order is repeated, once for each of its four lines. Hibernate folds them back together for you. And every caller of that query now gets the lines, whether it wanted them or not.

## 9. Fix Three: Ask For What You Need

The third fix: ask for exactly what the page needs. This is called a projection. One query, twenty rows, each with just an order number and a customer name. No entity, no stand-in, and nothing lazy left to fail. The cost: a small class for every query. And a row is not an object with behaviour. This is the idea from the D T O video, arriving from the other direction.

## 10. The Fix Not On The List

There is a fourth fix, which is not on the list, because it needs care. Make the relationship eager, instead of lazy. That removes the error. But it brings back the first problem from the Lazy Load video. Load one order, and you load the whole shop.

## 11. Where You Have Met This

You have very likely met this in a Spring application. It is almost always a controller, or a page template, using a lazy field after the transaction has ended. Exactly the first demo. Now you know the cause, not just the workaround.

## 12. What Was Used

For the record, here are the versions. Hibernate seven point four point five. And H2 two point four point two forty. These versions come from Spring Boot four point one point one's list of tested libraries. But Spring Boot itself is not used here.

## 13. What Is Real Here

A quick, honest note about this demo. Everything here is real. The error is Hibernate's. The stand-in is Hibernate's. And the query counts come from Hibernate's own statistics. The only stand-in is the database, which is H2, in memory.

## 14. When This Is Too Much

So, when is lazy loading too much? If you almost always need the related data, it only adds extra queries. It earns its place when the related data is large, and rarely needed.

## 15. Thanks for Watching

That's Lazy Load with Hibernate. If you remember one sentence, make it this one. A lazy field is a promise, and it needs an open session to keep it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a batch size setting to the order lines. Then count the queries again. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
