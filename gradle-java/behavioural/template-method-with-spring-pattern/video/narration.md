# Template Method with Spring Pattern — Video Narration Script

## 1. Template Method with Spring

Hello, and welcome. This video explains the Template Method pattern with Spring Boot, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Template Method video. That one fixed the order of an order's fulfilment steps in one final method, and let three routes fill in the holes. This one shows the same idea inside Spring Boot. The plain definition, in short: in Spring, a template owns the fixed steps of a task, and you hand it a small function for the one step that differs. By the end you will see plain database code leak a connection, see the same query through JdbcTemplate never leak, and see a transaction template roll back a half-finished checkout.

## 2. The Partner Project

This video assumes the Template Method video. If you have not seen it, start there. It fixes the order of the fulfilment steps in one final method, and lets three routes fill in the holes, by inheritance. This one uses the same example. It does not teach the pattern again. It shows what Spring Boot does with it.

## 3. Before The First Line

Before the first line of code, what Spring Boot is. Spring is a framework whose core is a container that creates your objects. Its JDBC support has a template that owns opening, running and closing a database call, and asks you only for the part that differs. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it.

## 4. Plain JDBC Leaks

First, the problem the pattern solves. Plain database code opens a connection, runs the query, walks the rows, and closes, in that order. On a good query, no connection is left in use. With one typo in the SQL, the code throws before it reaches the close. One connection stays in use. The pool has two. Two typos, and the pool is empty.

## 5. The Template Closes On Every Path

Second, the same query through the template. A good query leaves none in use. The same typo, three times over, still leaves none in use. The template closes on every path, because closing is one of its fixed steps.

## 6. What Is Ours

Third, what is ours. Ask for Asha's orders and you get two. The only code we wrote is one lambda, which turns a row into an order. The template opened the connection, prepared the statement, bound the customer, ran it, walked the rows, and closed everything. That is the pattern. The template is the skeleton. The lambda is the hole.

## 7. Exceptions, Translated

Fourth, exceptions. By hand, a typo gives a checked exception, with a vendor's state code. Through the template, it becomes a bad SQL grammar exception, unchecked, and the same on every database. A repeated order number becomes a duplicate key exception. You catch by meaning, not by vendor code.

## 8. What The Template Decides

Fifth, what the template decides for you. Ask for exactly one row. None found is an exception. Two found is an exception. Nothing in your code says so. The template decided that a missing row is an error, not a null. That is fine, but you should know it, because it shapes every caller.

## 9. A Transaction Is A Template Too

Last, a transaction is a template too. The transaction template owns begin, commit and roll back. A good checkout takes the orders from three to four and the mugs from three to one. A checkout for four mugs inserts an order first, then fails on the stock. Afterwards there are still four orders, and one mug. The order row was rolled back. The template did that.

## 10. The Verdict

My verdict, plainly. Use the template, not the raw API. Learn what it decides for you. Keep the lambda small. And catch the translated exceptions, not vendor codes.

## 11. How To Recognise It

How do you recognise this in code you did not write? A call to the JDBC template with a lambda. A transaction template execute. Or any Spring class whose name ends in template.

## 12. Where You Have Met This

You have met this in every Spring class whose name ends in template. Each owns the fixed steps of talking to something, and asks for the step that differs.

## 13. What Was Used

For the record. Spring Boot four point one point one, with JDBC and an in memory H2 database. No web server.

## 14. What Is Real Here

The same honest admission as everywhere in this course. Everything is real: a real pool, a real database, real exceptions. Connections are counted, never timed.

## 15. When This Is Too Much

So when is it too much? For one query in a script, plain JDBC with try with resources is fine. The template earns its place when many callers repeat the fixed steps.

## 16. Thanks for Watching

That's Template Method with Spring. If you take one sentence away, take this one: a Spring template owns the fixed steps, and quietly makes some decisions for you. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, add try with resources to the by hand method, and rerun act one. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
