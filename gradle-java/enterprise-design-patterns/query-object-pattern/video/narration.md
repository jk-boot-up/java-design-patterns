# Query Object Pattern — Video Narration Script

## 1. Query Object

Hello, and welcome. This video explains the Query Object pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A query object holds a search as an object, made of small criteria. It can write itself as safe SQL for the database. And it can run over a plain list in memory, for testing. Think of a library request form. You fill in boxes: subject, author, year. Whatever you write in the author box is treated as a name, never as an instruction. And last week's form can be copied, with one more box ticked. In this video, the domain is an online shop. Its search page lets customers filter products by category, price, and name. By the end, you will hear how gluing SQL together from strings goes wrong. How a query object fixes it. How to test a query without a database. And what it costs.

## 2. The Scenario

Here is the scenario. Customers can filter products by category, by maximum price, and by part of the name. Any of those may be left empty. The search page built its database query by gluing text together. A bit of SQL for each filter that was filled in.

## 3. Act One — SQL glued from strings

First demo: the search page glues SQL together from strings. SQL is the language used to ask a database for data. Kitchen products under thirty pounds: that works. Any category, under thirty pounds. Now the SQL says where, and, with nothing in between. The database rejects it. Then a customer searches for O'Brien's mug. The apostrophe goes straight into the SQL, and ends the text early. That is exactly how SQL injection attacks begin.

## 4. Act Two — A query object

Second demo: a query object, built from criteria. Category is kitchen. Price at most thirty pounds. In stock. The query writes its own SQL. Every value is a question mark, a placeholder. The values travel separately: kitchen, and three thousand pence. Leave out the category, and that criterion is simply not there. The SQL is still correct.

## 5. Act Three — The same query in memory

Third demo: the same query runs in memory, for tests. Each criterion can also check a product directly, in Java. Run over a small list, the query finds three products. The steel kettle, the tea towel, and O'Brien's mug. The glass teapot is out of stock. The desk lamp is not kitchen. Both are left out. The query's meaning can be tested without any database.

## 6. Act Four — Safe and reusable

Fourth demo: safe with any text, and reusable. The saved cheap kitchen search gets one more criterion: name contains O'Brien. The apostrophe travels as a value, never as part of the SQL. One product is found. And adding a criterion makes a new query. The saved one is unchanged, ready to be reused.

## 7. Act Five — The bill

Fifth demo: the bill. A query object is a small query language of your own. It has only the criteria you wrote. No or, no joins, no sorting, until someone adds them. And each criterion says the same thing twice. Once in SQL, and once in Java. The two must always agree.

## 8. The Pattern

Let's name the pattern. Hold the search as an object, made of criteria. Category is kitchen. Price at most thirty pounds. The object writes its own SQL, with a placeholder for every value. The values travel separately, so customer text never becomes SQL. And the same object can run over a list in memory, so tests do not need a database.

## 9. Who Does What

Here is who does what. A criterion knows three things. Its bit of SQL, its values, and how to test a product in Java. Product query holds a list of criteria. It joins their SQL, collects their values, or runs them over a list. And string SQL is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. J P A has a Criteria A P I. Spring Data has specifications. QueryDSL and jOOQ build SQL from Java objects. And every shop that lets you save a search is keeping a query object for you.

## 11. When To Use It

So, when should you use it? When searches are built from optional filters, saved, combined, or run in more than one place. Always use placeholders for values. Test criteria in memory. And when your queries grow large, use a library such as JPA Criteria, or jOOQ, instead of growing your own language.

## 12. Thanks for Watching

That's the Query Object pattern. If you remember one sentence, make it this one. Hold a search as criteria, never as glued-together text. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a minimum price criterion, and search for a price range. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
