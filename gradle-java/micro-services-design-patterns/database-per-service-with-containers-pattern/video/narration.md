# Database per Service with Containers Pattern — Video Narration Script

## 1. Database per Service with Containers

Hello, and welcome. This video explains the Database per Service pattern in Java, using two real databases: PostgreSQL and MongoDB. This video is presented by Jayasekhar Konduru. First, a simple definition. Each service keeps its own data, in its own database. No other service may read that database directly. If you want someone else's data, you ask them for it. In our online store, there is an Orders team and a Catalog team. Orders knows what each customer bought. Catalog knows each product's name, price, and stock. Each team gets a database of its own. And here, they are two different kinds of database. By the end, you will hear one shared database work well, and then break. The split survive the same change. And the old join tried against two real databases. One refuses it out loud. The other says nothing at all.

## 2. The Scenario

Here is the scenario. One customer has two orders. Order one oh one is one Stainless Steel Kettle. Order one oh two is four Blue Stoneware Mugs. The order history page belongs to the Orders team. It shows each order, with the product's name beside it. But the names belong to the Catalog team. So the page needs data from both teams. The plain Java version told this story with two simple maps, inside one Java program. This time, the data lives in real databases. Each runs in a container that the demo starts at the beginning, and removes at the end.

## 3. Postgres's Words

Before the first demo, some words, in plain language. PostgreSQL, usually called Postgres, keeps data in tables. Think of a spreadsheet with fixed column headings. Every row fills in the same columns. You ask it questions in a language called S Q L. Postgres can answer one question from two tables at once, by matching values between them. That is called a join. It can also keep a rule between two tables. A value in one must exist in the other. That rule is called a foreign key, and Postgres refuses any change that breaks it. A group of changes that are kept together, or undone together, is called a transaction. Undoing it is called a rollback.

## 4. One Shared Database

First demo: one shared database. Both teams keep their tables in one Postgres database. Catalog owns the products table. Orders owns the orders table. And a foreign key says every order must name a product that exists. The order history page is one S Q L join. Both orders come back with their names. And it takes one round trip, meaning one question sent to the database. Then the Catalog team tries to delete the kettle. But order one oh one still names it. So Postgres refuses, because the foreign key would be broken. This is the shared database working well. Fast, correct, and guarded by the database itself.

## 5. The Rename

Second demo: a rename. The Catalog team renames its column, from product name to title. The change is correct. They update their own queries, and their tests pass. But the order history page belongs to the Orders team. And its query still uses the old column name. Postgres answers with an error: that column does not exist. Nobody did anything wrong. The column belonged to Catalog. The query that named it belonged to Orders. The break lives between two teams, where no test suite looks.

## 6. MongoDB's Words

Now the second database, and its words. MongoDB is a document database. Think of a drawer of filled-in forms, where each form can have its own set of boxes. Each form is called a document: one record of named fields. A drawer of them is called a collection. There are no tables. And two documents in one collection do not need the same fields. Asking MongoDB for matching documents is called a find. MongoDB also has its own kind of join, called lookup. For each document, it attaches the matching documents from another collection, in the same database.

## 7. Two Services, Two Engines

Third demo: the split. Orders keeps Postgres, in a database of its own, with one table. Catalog moves to MongoDB, in a database of its own, with one collection. The kettle's document has a wattage. The mug's document has a capacity in millilitres. Nobody had to change a table to allow either. That is a common reason for a team to want its own database: a kind of store that suits its data. The page is now two questions. One S Q L query to Orders, for the customer's orders. One find to Catalog, for both names at once. Java puts the answers side by side. Two round trips, where the join took one. Then the Catalog team renames its name field to title, in every document. And the page is unchanged. Because nothing outside Catalog ever named that field.

## 8. Who Can Reach What

Here is who can reach what, in words. The order history page asks the Orders service, and then the Catalog service. The Orders service holds one connection, to its own Postgres database, and nothing else. The Catalog service holds one connection, to its own MongoDB database, and nothing else. Between the two databases, there is nothing at all. No join, no foreign key, and no shared transaction. No database holds both halves. Remember that, because the next demo tries to cross that gap anyway.

## 9. The Whole Pattern, In Two Constructors

In the code, the whole pattern is two constructors. The Orders service is given Postgres, and connects to one database, called orders. The Catalog service is given MongoDB, and connects to one database, called catalog. What matters is what they are not given. The Orders service has no MongoDB address, and no MongoDB password. The Catalog service has no Postgres connection. The plain Java version needed special code to say: you may not. Here, nothing needs to say it. The rule is in how things are connected.

## 10. The Join, Tried Anyway

Fourth demo, and this is the headline of the project. The old join is tried from both sides. From the Orders side, the old S Q L query. Postgres answers with an error: there is no products table here. Then the query reaches across to the old shared database, on the very same Postgres server. Another error: Postgres cannot join across two of its own databases. From the Catalog side, MongoDB's own join, pointed at a collection called orders. MongoDB has no such collection. The orders are in Postgres. And MongoDB does not complain. It treats the missing collection as empty. And it returns both products, each with zero orders. That quiet answer is the dangerous one. A report built on it would say nobody ever bought a kettle. And no log anywhere would say why. The join is not forbidden. It simply cannot be written.

## 11. No Foreign Key Between Engines

Fifth demo: no foreign key between two databases. The Catalog team deletes the kettle. MongoDB deletes one document. And nothing refuses. Postgres still holds one order that names the kettle. And it has no way of knowing the kettle has gone. The page has to decide what to show. It shows: no longer in the catalogue. In the first demo, Postgres refused this exact delete. Across two databases, nothing can. That rule now lives in code, and in agreements between teams.

## 12. The Bill

Sixth demo: the bill. The customer checks out two more mugs. Orders writes order one oh three, inside a Postgres transaction. Catalog takes two mugs off the shelf, in MongoDB. Then the payment is declined, and Orders rolls back. Postgres forgets the order. The customer has two orders again. But MongoDB keeps its change. Thirty-eight mugs, where there were forty. The rollback reached one database, not both. In the shared database, the stock and the order would have been one transaction. Then MongoDB is stopped. The page asks Orders, which answers. It asks Catalog, which does not. So every name reads: catalog unreachable. The page is only half there. And the shop now runs two containers, two drivers, and two query languages, where it had one of each.

## 13. What The Simulation Left Out

So what did the plain Java version get right? The whole argument. One shared database answers the page in one join, protected by a foreign key. A correct rename breaks somebody else's page. The split builds the same page in two calls, and the rename becomes harmless. What it left out was everything that needs real databases. Its two databases were the same kind of thing. So it could not show a team choosing a different store for different data. Its refusal was code it wrote itself. So it could not show a real database answering a join with a quiet nothing. It had no transactions, so no rollback could stop halfway. And a map in memory is never down.

## 14. The Verdict

So, here is the verdict. When two teams keep breaking each other, give each service its own database. And let each team pick the kind of database that suits its data. Then be honest about what that gives up. One. The join becomes two questions, and some code. Two. The foreign key becomes an agreement between teams. Three. One transaction becomes two, and they can disagree. Four. One database can be down while the other is up. And never trust an empty answer from a join, until you know where the other half lives.

## 15. What Is Real, And When Not

A quick, honest note about this demo. There are two real databases. Postgres, version eighteen point six. And MongoDB, version eight point three point eleven. Each runs in its own container, which the demo starts and removes by itself. You just need Docker switched on first. Every number you heard comes from the program's own output. So, when is this too much? If one small team owns both halves, one database keeps the join, the foreign key, and the single transaction. If both teams' data has the same shape, two databases on the same kind of engine is often enough. A second kind of database is one more thing to back up, update, watch, and learn.

## 16. Thanks for Watching

That's Database per Service, with Containers. If you remember one sentence, make it this one. Once each service has its own database, the join is not forbidden, it is impossible, and one database will not even tell you. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Create a real orders collection in the catalog database, with one document in it. Guess what the lookup will return, and then run it. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
