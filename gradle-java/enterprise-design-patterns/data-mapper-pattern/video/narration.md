# Data Mapper Pattern — Video Narration Script

## 1. Data Mapper

Hello, and welcome. This video explains the Data Mapper pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a mapper class moves data between an object and its database rows, so the object itself never knows it is stored. This is the first project in the enterprise category, and the others assume it. In our online store, the object is a customer, and the question is who should know how a customer is saved. By the end you will know when it is fine for an object to save itself, what that costs, what a mapper does instead, and how a hand-written mapping can lose a field without any error.

## 2. The Scenario

Here is the scenario. The online store has customers. Each has a name, an email address, a postal address and loyalty points. They must be stored in a database, and loaded again later. The question this video answers: who should know how that happens? Should the customer, or something else?

## 3. Active Record Works

The simplest answer: the object saves itself. It is called Active Record. The customer has a save method, and a find method, and knows its own table. Watch the operations against the toy database. An insert. A select. An update. Three operations, one class, one table. This works, and it works well. For a simple application it is the right answer, and nothing in this video says otherwise.

## 4. The Cost

Now the cost. The Active Record customer holds a database and names its own table and columns. So a rule as small as, an email must contain an at sign, cannot be tested without a database. And a change to the schema is a change to the domain object itself. Compare a plain customer, with no storage in it at all. It changes its email with no database anywhere in sight.

## 5. A Shape It Cannot Say

And there are shapes one class per table cannot say at all. First, one customer stored across two tables. Loading it takes a select on customers and a select on addresses. Second, one table feeding two different objects. The customers table also produces a smaller summary, with just an id and a name, for a list page. Two summaries, from one select. An object that is its own table has no way to describe either.

## 6. The Pattern

The pattern is a mapper class. It sits between the object and the rows, and it is the only class that knows both. To store a customer, the mapper writes a row in customers and a row in addresses. To load one, it reads both, and builds the customer. The customer itself knows neither.

## 7. What The Customer Looks Like

The demo proves it by printing the customer class. Its fields: address, email, id, loyalty points, and name. Its methods: change email, move to a new address, earn points, and getters. No table. No column. No SQL. No database. It loaded back as Ada Lovelace, in Leeds, with ten points. It is only a customer, and can be tested and understood as one.

## 8. The Bill: A Class Per Entity

Now the bill. First, a second class for every entity. Each domain object gets a mapper beside it. Second, loading a whole object graph means deciding how far to go. That decision is the subject of the Lazy Load video. Third, an indirection. You must know the mapper exists before you can debug a wrong value.

## 9. The Bill: A Silent Field

The worst part of the bill. The mapping is written by hand, and it is easy to get subtly wrong. This careless mapper forgets the postcode when it writes the address. The demo saves L S one four A B. It loads back null. Every call succeeded. Nothing threw. The field is simply gone. The only defence is a test that saves an object, loads it, and compares every field.

## 10. The Toy Database

A word about the database in these demos. It is a toy, built for teaching. It stores rows, not objects. Every operation is counted and printed. A write can be told to fail, on demand. And nothing needs installing. Every count in this video came from its counter, not from guessing. The rest of this category uses the same one.

## 11. Where You Have Met This

You have almost certainly met this already. A JPA entity is the domain object. The entity manager is the mapper. Hibernate writes the mapping code, so you usually only see it as annotations. If you have ever fixed a mapping because a field did not come back, you have lived act five.

## 12. What Is Real Here

The same honest admission as everywhere in this course. The toy database is not a real one. It has no transactions, no indexes, no query planner. The operation lines it prints are shaped like SQL, they are not SQL. The pattern is real. The database is a stand-in that makes the counts easy to see.

## 13. When This Is Too Much

So when is a mapper too much? For a simple application, with one class for each table and a schema that rarely changes, Active Record is simpler, and it is the right answer. Reach for a mapper when the objects and the tables stop matching one to one, or when you want to test the domain with no database at all.

## 14. Thanks for Watching

That's the Data Mapper. If you take one sentence away, take this one: a mapper lets the domain live without a database, and the price is a class you must test. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, write a test that saves a customer, loads it, and compares every field. It would have caught act five. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
