# Lazy Load with Hibernate Pattern — Video Narration Script

## 1. Lazy Load with Hibernate

Hello, and welcome. This video explains Lazy Load with Hibernate, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Lazy Load video. That one built the pattern by hand. This one is about the most searched Java error there is: lazy initialization exception. The plain definition: a lazy field does not hold its data. It holds a stand-in, that loads the data the first time somebody asks. By the end you will know exactly what is in that field, why asking after the session has closed fails, and what each of the three usual fixes costs.

## 2. The Partner Project

This video assumes the Lazy Load video. If you have not seen it, start there. It builds four ways of loading later, by hand, and a failure when the session has closed. This one uses the very same store: five customers, twenty orders, four lines in each. It does not teach the pattern again. It shows the real exception, from Hibernate itself.

## 3. Before The First Annotation

Before the first annotation, two new things. Hibernate is the most widely used implementation of J P A. You mark your classes, and it turns operations on them into S Q L. H two is a database that runs inside the test, in memory, so nothing needs installing. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it. This one explains an exception.

## 4. One Word Makes It Lazy

Here is the one word. On the order class, the customer, and the lines, are both declared with fetch type lazy. That one word is what this whole video is about.

## 5. The Exception

Now the failure, on purpose. Load an order. Close the session. Then ask the order for its customer's name. The order loaded fine. Asking for the name threw a lazy initialization exception. Could not initialize proxy, customer number one, no session. Look where it failed. Not where the order was loaded. Where the customer was used. That is why it is so hard to find.

## 6. What Is In The Field

So what is actually in that field? Not a customer. Hibernate generated a subclass of the customer class. It holds only two things: the customer's id, and a reference to the session. It has not loaded anything. Initialised: false. Ask it for the name while the session is open, and it selects the customer, and becomes initialised. Close the session first, and it has nothing to load with. That is the exception. Not a bug. A promise that needed something that has gone.

## 7. Fix One: Keep The Session Open

The first usual fix: keep the session open while the page renders. It works. Twenty orders, each with its customer's name: six statements. Not twenty-one. One for the orders, and one for each of the five different customers, because the session loads each customer only once. That is the identity map from the earlier video, at work. But twenty orders, each with its line count: twenty-one statements. One for the orders, then one for every order's lines. That is N plus one. The cost: the session, and its database connection, stay open while the page renders. And the extra queries are hidden inside the view, where nobody looks.

## 8. Fix Two: Fetch It In The Same Query

The second fix: fetch it in the same query, with a join fetch. One statement, for the customers. One statement, for the lines. The cost is hidden in the middle. Fetching the lines makes the database send eighty rows for twenty orders, each order repeated once for each of its four lines. Hibernate folds them back together for you. And every caller of that query now gets the lines, whether it wanted them or not.

## 9. Fix Three: Ask For What You Need

The third fix: ask for exactly what the page needs. A projection. One statement, twenty rows, each with just an order number and a customer name. No entity. No proxy. Nothing lazy left to fail. The cost: a class for every query, and a row is not an object with behaviour. This is the idea from the D T O video, arriving from the other direction.

## 10. The Fix Not On The List

There is a fourth fix, that is not on the list, because it is the one to be careful of. Make the mapping eager. That removes the exception. And it brings back the first act of the Lazy Load video: load one order, and you load the shop.

## 11. Where You Have Met This

You have very likely met this in a Spring application. It is almost always a controller, or a view, using a lazy field after the transaction has ended. Exactly act one. Now you know the mechanism, not just the workaround.

## 12. What Was Used

For the record. Hibernate O R M seven point four point five, and H two two point four point two forty. The versions come from Spring Boot four point one point one's bill of materials. Spring Boot itself is not used in this video.

## 13. What Is Real Here

The same honest admission as everywhere in this course, and again a short one. Everything is real. The exception is Hibernate's. The proxy is Hibernate's. The statement counts come from Hibernate's own statistics. The only stand-in is the database, which is H two in memory.

## 14. When This Is Too Much

So when is lazy loading too much? If you almost always need the related data, it only adds queries. It earns its place when the related data is large, and rarely needed.

## 15. Thanks for Watching

That's Lazy Load with Hibernate. If you take one sentence away, take this one: a lazy field is a promise that needs a session to keep. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, add a batch size to the lines, and count the statements. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
