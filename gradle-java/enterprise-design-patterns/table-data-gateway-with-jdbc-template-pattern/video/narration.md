# Table Data Gateway with JdbcTemplate Pattern — Video Narration Script

## 1. Table Data Gateway with JdbcTemplate

Hello, and welcome. This video explains the Table Data Gateway pattern, with Spring's JdbcTemplate, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A table data gateway is one class that holds all the SQL for one table. Everyone else asks it, instead of writing their own. JdbcTemplate is part of the open-source Spring framework, and it takes care of the database plumbing. Think of a library's front desk. Nobody walks into the stacks. You ask the desk, and it fetches and returns books the same careful way every time. In this video, the domain is an online shop's product table. By the end, you will hear how hand-written database code leaks. How the gateway keeps SQL in one place. And what errors, and stock, look like with Spring.

## 2. The Scenario

Here is the scenario. The product page, the stock report, and checkout each wrote their own database code. One page borrowed connections, and never gave them back. And a renamed column broke them all at once.

## 3. Act One — Hand-written JDBC that leaks

First demo: every page writes its own database code. One page borrows a connection from the pool, and never gives it back. The pool holds two connections. The page works twice. The third time, there are none left. After a quarter of a second, it fails.

## 4. Act Two — A gateway on JdbcTemplate

Second demo: a table data gateway, built on JdbcTemplate. All the product table's SQL, in one class. The product page is asked four times, on the same pool of two. It works every time. JdbcTemplate always gives the connection back. One product is out of stock. And under ten pounds, the mug and the tea towel.

## 5. Act Three — Errors that mean something

Third demo: errors that mean something. A column is renamed, behind the gateway's back. The next query fails, with Spring's bad SQL error. A second mug with the same code. A duplicate key error. The same kinds of error, whatever the database. So callers can react to them.

## 6. Act Four — Stock in one statement

Fourth demo: stock taken in one statement. Four customers try for two desk lamps. The gateway takes one only if the quantity is above zero, in the same statement. Two are taken. Stock ends at zero. It can never go below.

## 7. Act Five — The bill

Fifth demo: the bill. A row is only data. Whether a product is low on stock is still decided by each caller. The gateway grows a method for every question. And its SQL is still text, only checked when it runs.

## 8. The Pattern, with JdbcTemplate

Let's name the pattern, with Spring. One gateway class for each table. JdbcTemplate borrows a connection, runs the SQL, and always returns it. A row mapper turns each row into a record. And errors come back as Spring's own exceptions.

## 9. Who Does What

Here is who does what. The product gateway holds all the SQL for the product table. A row is one product's data. Scattered JDBC is the old way, with its missing close. And the pool holds just two connections, to make the leak visible.

## 10. Where You Have Seen It

You have probably met this already. Spring repository classes, built on JdbcTemplate. Spring Data JDBC and jOOQ, which generate or check the SQL for you. And data access objects, the older name for the same idea.

## 11. When To Use It

So, when should you use it? When several parts of the code share a table. Keep plain SQL, and let Spring handle the plumbing. Map rows to records. And keep business rules out of the gateway.

## 12. Thanks for Watching

That's the Table Data Gateway, with JdbcTemplate. If you remember one sentence, make it this one. Keep a table's SQL in one class, and let the framework do the plumbing. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Point the gateway at PostgreSQL, and check the same errors come back. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
