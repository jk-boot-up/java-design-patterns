# Data Mapper Pattern — Video Narration Script

## 1. Data Mapper

Hello, and welcome. This video explains the Data Mapper pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A data mapper is a separate class that moves data between an object and its database rows. So the object itself never knows it is being stored. Think of a removal company. Your furniture does not know how to pack itself. The movers know how to wrap each piece, and where it goes in the van. In our online store, the object is a customer. And the question is: who should know how a customer is saved? By the end, you will know when it is fine for an object to save itself, and what that costs. What a mapper does instead. And how a hand-written mapping can lose a field, without any error.

## 2. The Scenario

Here is the scenario. The online store has customers. Each one has a name, an email address, a postal address, and loyalty points. Customers must be stored in a database, and loaded again later. So here is the question. Who should know how that is done? The customer, or something else?

## 3. Active Record Works

The simplest answer: the object saves itself. This is called Active Record. The customer has a save method, a find method, and knows its own table. Listen to the database operations. An insert. A select. An update. Three operations, one class, one table. This works, and works well. For a simple application, it is the right answer.

## 4. The Cost

Now the cost. The Active Record customer holds a database connection, and names its own table and columns. So even a tiny rule, like, an email must contain an at sign, cannot be tested without a database. And a change to the table is a change to the customer class itself. Compare that with a plain customer, which has no storage code at all. It changes its email with no database anywhere in sight.

## 5. A Shape It Cannot Say

And there are shapes that one class per table simply cannot express. First, one customer stored across two tables. Loading it needs one query on the customers table, and one on the addresses table. Second, one table that feeds two different objects. The customers table also produces a small summary, with just an I D and a name, for a list page. An object that is its own table has no way to describe either shape.

## 6. The Pattern

Now, the pattern: a mapper class. It sits between the object and the database rows. And it is the only class that knows both. To store a customer, the mapper writes a row in the customers table, and a row in the addresses table. To load one, it reads both, and builds the customer. The customer itself knows about neither.

## 7. What The Customer Looks Like

The demo proves it, by listing the customer class's fields. Address, email, I D, loyalty points, and name. And its methods: change email, move to a new address, earn points. No table. No column. No database code. The customer loaded back as Ada Lovelace, in Leeds, with ten points. It is only a customer, and it can be tested and understood as one.

## 8. The Bill: A Class Per Entity

Now the costs of the pattern. First, a second class for every entity. Each domain object gets a mapper beside it. Second, loading a whole group of related objects means deciding how far to go. That decision is the subject of the Lazy Load video. Third, an extra step to follow. You must know the mapper exists, before you can track down a wrong value.

## 9. The Bill: A Silent Field

And the worst cost. The mapping is written by hand, and it is easy to get quietly wrong. This careless mapper forgets the postcode when it saves the address. The demo saves the postcode L S one, four A B. It loads back nothing. Every call succeeded. Nothing threw an error. The field is simply gone. The only defence is a test that saves an object, loads it back, and compares every field.

## 10. The Toy Database

A word about the database in these demos. It is a toy, built for teaching. It stores rows, not objects. Every operation is counted, and printed. A write can be told to fail, on demand. And nothing needs installing. Every count in this video came from its counter, not from guessing.

## 11. Where You Have Met This

You have almost certainly met this pattern already. In Java's persistence standard, J P A, an entity is the domain object. And the entity manager is the mapper. Hibernate writes the mapping code for you, so you usually only see annotations. If you have ever fixed a mapping because a field did not come back, you have met the silent field problem.

## 12. What Is Real Here

A quick, honest note about this demo. The toy database is not a real one. It has no transactions, no indexes, and no query planner. The operations it prints look like database commands, but they are not real ones. The pattern is real. The database is a stand-in that makes the counts easy to hear.

## 13. When This Is Too Much

So, when is a mapper too much? For a simple application, with one class per table, and tables that rarely change, Active Record is simpler, and it is the right answer. Reach for a mapper when your objects and your tables stop matching one to one. Or when you want to test your business logic with no database at all.

## 14. Thanks for Watching

That's the Data Mapper pattern. If you remember one sentence, make it this one. A mapper lets your business objects live without a database, and the price is an extra class you must test. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Write a test that saves a customer, loads it back, and compares every field. It would have caught the missing postcode. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
