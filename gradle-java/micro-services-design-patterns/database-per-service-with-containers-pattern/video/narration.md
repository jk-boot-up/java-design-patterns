# Database per Service with Containers Pattern — Video Narration Script

## 1. Database per Service with Containers

Hello, and welcome. This video explains the Database per Service pattern in Java, using two real databases: PostgreSQL and MongoDB. It is written and presented by Jayasekhar Konduru. Here is the plain definition, in general words. Each service keeps its own data, in its own database. No other service may read that database directly. If you want somebody else's data, you ask them for it. Now the same thing in our online store. The shop has an Orders team and a Catalog team. Orders knows what each customer bought. Catalog knows what each product is called, what it costs, and how many are on the shelf. Each team gets a database of its own, and in this video they are two different kinds of database. By the end you will have seen one shared database work well and then break, the split survive the same change, and the old join tried against two real engines. One of them refuses it out loud. The other one says nothing at all.

## 2. The Scenario

Here is the scenario. Customer cust-7 has two orders. Order one oh one is one Stainless Steel Kettle. Order one oh two is four Blue Stoneware Mugs. The order history page belongs to the Orders team. It shows each order with the product's name beside it. But the names belong to the Catalog team. So the page needs data from both teams. The hand-built twin of this project told this story with two maps inside one Java program. This time the data lives in real databases, each in a container that the demo starts at the beginning and removes at the end.

## 3. Postgres's Words

Before the first act, some words, each in plain language first. PostgreSQL, usually called Postgres, keeps data in tables. Think of a spreadsheet with fixed column headings, where every row fills in the same columns. It is asked questions in a language called SQL. Postgres can answer one question from two tables at once, by matching a value in one with a value in the other. That is called a join. It can also keep a rule between two tables: a value in one must exist in the other. It refuses any change that would break the rule. That rule is called a foreign key. And a group of changes that are kept together or undone together is a transaction. Undoing it is a rollback. Every error Postgres gives has a five-character code, and the video will say those codes out loud.

## 4. One Shared Database

Act one. Both teams keep their tables in one Postgres database, called shop. Catalog owns the products table. Orders owns the orders table. And a foreign key says every order must name a product that exists. The order history page is one SQL join. Both rows come back with their names, and it takes one round trip: one question sent to the database. Then the Catalog team tries to delete the kettle, which order one oh one still names. Postgres refuses, with error two three five zero three: the foreign key would be broken. This is the arrangement working well. Fast, correct, and guarded by the database itself.

## 5. The Rename

Act two. The Catalog team renames its column, from product name to title. The change is correct. They update their own queries, and their tests pass. But the order history page belongs to the Orders team, and its query still names the old column. Postgres answers with error four two seven zero three: the column does not exist. Nobody did anything wrong. The column was Catalog's. The query naming it was Orders'. The break lives between two teams, where no test suite looks.

## 6. MongoDB's Words

Now the second engine, and its words. MongoDB is a document database. Think of a drawer of filled-in forms, where each form can have its own set of boxes. Each form is what MongoDB calls a document: one record of named fields. A drawer of them is a collection. There are no tables, and two documents in one collection need not have the same fields. Asking MongoDB for the documents that match is called a find. And MongoDB has its own kind of join. For each document, it attaches the matching documents from another collection in the same database. That step is called lookup, written with a dollar sign in front.

## 7. Two Services, Two Engines

Act three is the split. Orders keeps Postgres, in a database of its own, holding one table. Catalog moves to MongoDB, in a database of its own, holding one collection of documents. The kettle's document has a wattage. The mug's has a capacity in millilitres. Nobody changed a table to allow either. That is the usual reason a team wants its own database: a different kind of store that suits its data. The page is now two questions. One SQL query to Orders for the customer's orders. One find to Catalog for both names at once. Java puts the answers side by side. Two round trips, where the join took one. Then the Catalog team renames its name field to title, in every document. MongoDB changed two documents. The page is unchanged, because nothing outside Catalog ever named that field.

## 8. Who Can Reach What

Here is who can reach what, in words. The order history page asks the Orders service, and then asks the Catalog service. The Orders service holds one connection, to its own Postgres database, and nothing else. The Catalog service holds one client, for its own MongoDB database, and nothing else. Between the two databases there is no line at all. No join, no foreign key, and no shared transaction. No engine holds both halves. Hold on to that, because the next act tries to cross that gap anyway.

## 9. The Whole Pattern, In Two Constructors

In the code, the whole pattern is two constructors. The Orders service is handed Postgres, and opens a connection to one database, called orders. The Catalog service is handed MongoDB, and opens a client for one database, called catalog, and one collection, called products. What matters is what they are not handed. The Orders service has no MongoDB address and no MongoDB password. The Catalog service has no Postgres connection. The hand-built twin needed an exception class to say you may not. Here nothing says it. The rule is the wiring.

## 10. The Join, Tried Anyway

Act four is the headline of this project. The old join is tried from both sides. From the Orders side, the old SQL. Postgres answers with error four two P zero one: there is no table called products here. Then a reach across to the shop database, which sits on the very same Postgres server. Error zero A zero zero zero: cross-database references are not implemented. Postgres will not even join two of its own databases. From the Catalog side, MongoDB's own join, pointed at a collection called orders. MongoDB has no such collection. The orders are in Postgres. And it does not complain. It treats the missing collection as empty, and hands back both products, each with zero orders. That quiet answer is the dangerous one. A report built on it would say nobody ever bought a kettle, and no log anywhere would say why. The join is not forbidden. It cannot be written.

## 11. No Foreign Key Between Engines

Act five. The Catalog team deletes the kettle. MongoDB deleted one document, and nothing refused. Postgres still holds one order naming the kettle, and it has no way of knowing the kettle has gone. The page has to decide what to show, and it shows: no longer in the catalogue. In act one, Postgres refused this exact delete. Across two engines, nothing can. The rule that used to live in the database now lives in code, and in agreements between teams.

## 12. The Bill

Act six is the bill. Customer cust-7 checks out two more mugs. Orders writes order one oh three inside a Postgres transaction. Catalog takes two mugs off the shelf in MongoDB. Then the payment is declined, and Orders rolls back. Postgres forgets the order: the customer has two orders again. MongoDB keeps its change: thirty eight mugs, where there were forty. The rollback reached one engine, not both. In the shared database, the stock and the order would have been one transaction. Then MongoDB is stopped. The page asks Orders, which answers. It asks Catalog, which does not. Every name reads: catalog unreachable. The page is half there. And the shop now runs two containers, two drivers and two query languages, where it had one of each.

## 13. What The Simulation Left Out

So what did the hand-built simulation get right? The whole argument. One shared database answers the page in one join, and a foreign key protects it. A correct rename breaks somebody else's page. The split does the same page in two calls, and the rename becomes harmless. What it left out was everything that needs real engines. Its two databases were the same kind of thing, so it could not show a team choosing a different store for different data. Its refusal was an exception it wrote itself, so it could not show a real engine answering a join with a quiet nothing. It had no transactions, so no rollback could stop halfway. And a map in memory is never down.

## 14. The Verdict

The verdict. When two teams keep breaking each other, give each service its own database, and let each pick the engine that suits its data. Then say out loud what that gives up. One. The join becomes two questions and some code. Two. The foreign key becomes an agreement between teams. Three. One transaction becomes two, and they can disagree. Four. One engine can be down while the other is up. And never trust an answer of nothing from a join, until you know where the other half lives.

## 15. What Is Real, And When Not

What is real here? Two real databases. Postgres, version eighteen point six, and MongoDB, version eight point three point eleven, the newest releases, each in its own container. The demo starts both at the beginning and removes both at the end, each on a random free port. Java talks to them through the newest Postgres driver and the newest MongoDB driver. The one thing you need is a container runtime, such as Docker Desktop, switched on before you start. Every number and every error code in this video comes from the program's own output, and two runs one after the other print the same thing. So when is this too much? If one small team owns both halves, one database keeps the join, the foreign key and the single transaction. And if the two teams' data has the same shape, two databases on one engine is often enough. A second engine is one more thing to back up, upgrade, watch and learn.

## 16. Thanks for Watching

That's Database per Service with Containers. If you take one sentence away, take this one: once each service has its own engine, the join is not forbidden, it is impossible, and one engine will not even tell you. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, create a real orders collection in the catalog database with one document in it, guess what the lookup will say, and then run it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
