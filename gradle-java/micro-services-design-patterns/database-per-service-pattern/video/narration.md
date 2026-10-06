# Database per Service Pattern — Video Narration Script

## 1. Database per Service

Hello, and welcome. This video explains the Database per Service pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Each service keeps its own data. Nobody else may read that data directly. If you want another service's data, you ask that service for it. Think of two departments in an office, each with its own filing cabinet. If you need something from the other department, you ask them. You do not go through their drawers. There is no clever algorithm in this pattern. The interesting part is not how you do it, but what it costs. In our online store, there are two teams. One looks after products: names, prices, and photographs. The other looks after what people have bought. They share one database, and one Tuesday afternoon, somebody renames a column. By the end, you will know why a perfectly correct change breaks a page in another team's code. Why every test can pass while the system is broken. What splitting the database really buys. And what it takes away.

## 2. Two Teams, One Database

Here is the shop. There are two teams. The catalog team looks after products: names, descriptions, prices, and photographs. The orders team looks after what people have bought. They share one database. The products table and the orders table sit side by side. And either team can read both. We follow one page: the order history page. Each line shows an order number, a product code, the product's name, and how many were bought. Here is the key point. The product code lives in the orders table. The product name lives in the products table. So building the page means reading both. Two teams, one shared database, and nobody really in charge of it.

## 3. The Page Is One Query

In this project, there is no real database. Each table is a simple map, and each column is a key in that map. But the shape is exactly a database join. A join reads two tables together, and matches their rows up. For every order, find the matching product. Read the product's name. And build a line from the two halves. Now notice one detail, because it is the whole video. The code asks for a column by name: product name. That name is written in the orders team's code. But the column belongs to the catalog team. Nobody thinks about that when they write it. In one shared database, that is simply how you read a table.

## 4. Act One — One Database, One Query

First demo: one database, one query. And it works. Two orders come back for this customer. One stainless steel kettle. And four blue stoneware mugs. Each line has the order number, the product code, the name, and the quantity. The page is complete. It took one trip to one database. Remember that number, one. Later, we will compare against it.

## 5. Be Fair To This — It Is Very Good

Before we break it, let's be fair to this design. It is very good. One trip to one database, and the page is done. The join is done by a database engine that has been perfected for decades. And you did not have to write any of it. A join cannot forget a name. Either every line comes back complete, or the query fails. There is no half-built page. And a foreign key guarantees that the product an order refers to really exists. A foreign key is a rule inside the database that links two tables. The database will refuse an order that points at a product that is not there. Nothing here is ever out of date. What you read is what is true, right now. So here is a sentence many talks leave out. If a shop can live like this, it should.

## 6. Act Two — Tuesday Afternoon

Second demo: Tuesday afternoon. The catalog team decides that the column called product name should be called title. They have good reasons. It is their column, in their table. So they write a change to the database, called a migration. They run it. Their tests pass. Their service works. They go home. And the order history page is dead. It asked for a column called product name. And there is no longer a column with that name. The catalog team saw a successful release. The orders team saw an outage. Both are true at the same moment. And neither team can see the other.

## 7. Nobody Did Anything Wrong

Here is the uncomfortable part. Nobody did anything wrong. The migration was correct. A test proves that every product name is still there, under its new name. Nothing was lost. And the catalog team could not have known. The code that broke is in a different team's project. It is not in their code, their tests, or their build. No reviewer could have seen both sides. Here is the sharpest way to say it. This project has a test named: a rename breaks the order history page. And that test passes. Every test passes, including the one that says a page is broken. A test suite checks one codebase. This problem lives between two codebases. And nobody owns the space in between.

## 8. The Shared Filing Cabinet

Let's leave the code for a moment. There is an everyday version of this. Two departments in an office share one filing cabinet. While they share it, life is easy. Any question is one trip to one drawer. Nothing is ever out of date. Then one department reorganises its half. They have every right to. They do it carefully, and check their own work. On Monday, the other department cannot find anything. Nobody was careless. The filing system was a shared decision that neither department owned. The only safe way to change it was a meeting that nobody thought to call. So they buy a second cabinet. Remember that, because soon we will count what the second cabinet costs.

## 9. Three Tempting Fixes

Before the real fix, here are three tempting fixes. The first: write a test that catches it. But in whose project does that test live? It would have to run one team's queries against the other team's database. That is a shared build with a shared owner. The same problem, in a different disguise. The second: just never rename columns. This is the one that really gets adopted, and it is the worst. Nobody writes it down. The database slowly fills with badly named columns. And everyone learns that changing anything is expensive. The third: add a database view, so the old name still works. That is a real technique, and it buys time. But it does not change who is allowed to decide. And it adds one more layer that nobody owns. So here is the real question. What if the orders team simply could not read the catalog team's data at all?

## 10. The Whole Mechanism

Here is the whole mechanism. Every database method takes the name of whoever is asking. And it refuses anybody who is not the owner. That is all. Now the most important point in this video. In a real shop, nothing in Java does this refusing. The orders service connects to the database with a login that simply cannot see the catalog tables. So any attempt to read them fails as a permissions error, inside the database. The refusal in this project's Java code only exists so you can see the rule. Think of it as: the database refused. And here is a simple test for your own system. If the rule is only a comment asking people not to, you do not have this pattern. You have a wish.

## 11. Act Three — The Same Page, For More Money

Third demo: the shop splits. Orders gets its own database. Catalog gets its own database. Now we must rebuild the page without a join. First, ask the orders service what this customer bought. It returns product codes and quantities, but no names. Because orders does not have the names. Then ask the catalog service what those codes are called. Then join the two answers together, in Java. The page that comes out is identical. A test checks that: same lines, same names, same order. But it now takes twenty milliseconds, and two service calls. It used to be one query. The cost changed. The answer did not.

## 12. Ask Once For Many, Or This Gets Much Worse

One small detail matters much more than it looks. The call to the catalog takes a whole list of product codes. And returns all the names in one answer. That is not just tidiness. Asking once per line would make a two-line page cost two network calls. A fifty-line page would cost fifty. And a big report could cause an outage. This is the most common way this pattern goes wrong. And it usually happens by accident, because asking one at a time in a loop looks natural. So one test checks that the catalog is called exactly once, however many lines the page has. And a customer with no orders never calls the catalog at all. There is nothing to name, so nobody is asked.

## 13. Who Owns What

Let's name the pieces. Each has one job. On one side is the design being replaced. One shared database holding both teams' tables. And one method that builds the whole page with a join. When a team renames a column, the failure appears in the other team's code. On the other side is the split. The orders service owns the order data, in its own database. The catalog service owns the product data, in its own database. Between them sits the order history page. It asks orders, then asks catalog once for all the names, and joins the answers. It exists because the database join no longer does. Then there is the refusal. When anyone but the owner asks, the database refuses. And the message says who asked, and whose data it was. Finally, the demo counts calls and reads a clock. Both designs produce the same page, so that is the only way to see the difference. And nothing sleeps. A simulated clock moves ten milliseconds per call, so every run gives the same result.

## 14. Act Four — The Same Rename, Now A Non-Event

Fourth demo: Tuesday again. The catalog team renames product name to title, just as before. But this time, the column is in a database only they can read. The data changes, and the code that reads it changes too. In the same place, at the same time, tested together, by the same people. And the order history page is unchanged. That is the payoff. Nothing happened, and that is the whole point. But be precise about what was bought. It bought no speed. The split page was slower. It bought no correctness. The page was already right. What it bought is freedom. The catalog team can change their mind without asking permission. And release without coordinating with a team they have never met. That is a benefit for the organisation, and it is the only one on offer. So if both teams are really the same three people, you are paying for a problem you do not have.

## 15. Act Five — The Bill

Finally, the bill. Two things were given up. And people usually forget the second. The first is the join. Every question that spans both services is now two calls, and some code. That is fine for an order history page. It is much harder for a Monday finance report that used to be one query with three joins. The second is the foreign key, and this one is worse. The catalog team deletes a product. An order still refers to it. And nothing stops the delete. Nothing can, because the two rows are in different databases. So the order survives, naming a product the catalog has never heard of. And something must decide what to show. Here, the page says: no longer in the catalogue. A rule that used to be impossible to break is now only impolite to break. It moved out of the database, and into code, tests, and agreements between teams.

## 16. Thanks for Watching

That's the Database per Service pattern. If you remember one sentence, make it this one. Each service owns its own data, which buys each team the freedom to change, and costs you the join and the foreign key. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Change the order history page to ask the catalog for one name at a time, in a loop. Watch the test fail. Then imagine a page with fifty lines. And one question to think about. Take a database you work on, and draw one line through it. Which tables end up on each side? And which query would stop working? If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
