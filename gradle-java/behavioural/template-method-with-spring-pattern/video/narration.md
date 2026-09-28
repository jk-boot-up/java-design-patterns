# Template Method with Spring Pattern — Video Narration Script

## 1. Template Method with Spring

Hello, and welcome. This video explains the Template Method pattern, in Java, using Spring Boot. This video is presented by Jayasekhar Konduru. First, a simple definition. The Template Method pattern fixes the order of a task's steps in one place, and leaves only certain steps to be filled in. In Spring, a template class owns the fixed steps of a task. You hand it a small function for the one step that differs. Think of a car wash. It always soaps, rinses, and dries, in that order. You only choose the extras, like wax. This is the framework version of the Template Method video, in the same online shop. We will hear plain database code leak a connection. Then the same query through Spring's JDBC template, which never leaks. And a transaction template that undoes a half-finished checkout.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Template Method video. That one fixes the order of an order's fulfilment steps in one final method. And three routes fill in the steps, through inheritance. If you are new to the pattern, watch that one first. Here, we ask what Spring Boot does with the same idea.

## 3. Before The First Line

One thing is new in this project: Spring Boot. We use its database support, and a small in-memory database called H2. Spring's JDBC template owns the fixed steps of a database call. Opening a connection, running the query, and closing everything. It asks you only for the part that differs. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. Plain JDBC Leaks

First demo: the problem the pattern solves. Plain database code opens a connection, runs the query, reads the rows, and then closes the connection. In that order. With a good query, no connection is left in use. But with one typo in the query, the code fails before it reaches the close. One connection is left in use, forever. The pool only has two connections. So after two typos, the pool is empty, and the whole shop stops.

## 5. The Template Closes On Every Path

Second demo: the same query, through the template. With a good query, no connection is left in use. With the same typo, three times over, still none are left in use. The template closes the connection on every path, including failures. Because closing is one of its fixed steps.

## 6. What Is Ours

Third demo: what is left for us to write. We ask for Asha's orders, and get two. The only code we wrote is one small function. It turns one database row into one order. The template did everything else. It opened the connection, prepared the query, filled in the customer, ran it, walked through the rows, and closed everything. That is the pattern. The template is the fixed sequence. Our small function fills the one gap.

## 7. Exceptions, Translated

Fourth demo: errors, translated. With plain code, a typo gives a checked error with a database-specific code. Through the template, the same typo becomes a Bad SQL Grammar exception. It is unchecked, and it is the same on every database. And a repeated order number becomes a Duplicate Key exception. So you catch errors by their meaning, not by a vendor's code.

## 8. What The Template Decides

Fifth demo: what the template decides for you. We ask for exactly one row. If none is found, that is an error. If two are found, that is also an error. Nothing in our code said so. The template decided that a missing row is an error, not an empty value. That is fine, but you should know it, because it affects every caller.

## 9. A Transaction Is A Template Too

Last demo: a transaction is a template too. The transaction template owns three fixed steps: begin, commit, and roll back. At the start, there are three orders, and three mugs in stock. A good checkout makes it four orders, and one mug. Then a checkout for four mugs begins. It saves the order first, and then fails, because there is not enough stock. Afterwards, there are still four orders, and one mug. The half-finished order was rolled back. The template did that for us.

## 10. The Verdict

So, here is the verdict. Use the template, not the raw database interface. Learn what it decides for you. Keep your small function small. And catch the translated errors, not vendor codes.

## 11. How To Recognise It

How can you spot this in code someone else wrote? Look for a JDBC template query, with a small function passed in. Look for a transaction template's execute method. Or any Spring class whose name ends in Template.

## 12. Where You Have Met This

Where have you met this before? In every Spring class whose name ends in Template. Each one owns the fixed steps of talking to something, and asks you only for the step that differs.

## 13. What Was Used

For the record, here are the versions. Spring Boot four point one point one, with its database support, and an in-memory H2 database. No web server.

## 14. What Is Real Here

A quick, honest note about this demo. Everything in it is real. A real connection pool, a real database, and real errors. Connections are counted, never timed.

## 15. When This Is Too Much

So, when is this too much? For one query in a small script, plain database code with try-with-resources is fine. The template earns its place when many callers repeat the same fixed steps.

## 16. Thanks for Watching

That's Template Method with Spring. If you remember one sentence, make it this one. A Spring template owns the fixed steps, and quietly makes some decisions for you. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add try-with-resources to the plain database method. Then run the first demo again, and count the connections left in use. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
