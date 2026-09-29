# Single Table Inheritance with JPA Pattern — Video Narration Script

## 1. Single Table Inheritance with JPA

Hello, and welcome. This video explains Single Table Inheritance, with JPA and Hibernate, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Single table inheritance stores several related classes in one database table. A type column says which class each row is. JPA is the Java standard for storing objects in tables, and Hibernate is the open-source library that does the work. Think of a single stock book, with a column for each kind of detail, and a word at the start of each line saying what kind of item it is. In this video, the domain is an online shop's products: books, electronics, and food. By the end, you will hear the SQL Hibernate writes for two strategies. How each row comes back as its own class. And a rule the database can no longer keep.

## 2. The Scenario

Here is the scenario. The shop sells books, electronics, and food, each with its own details. With a table for each kind, a question about all products had to search every table. And every new kind made those questions bigger.

## 3. Act One — A table per class

First demo: a table for every class. Books, electronics and food each have their own table. The shop asks for everything under ten pounds. Breakfast tea, and the desk lamp. Hibernate's query joins three tables together, one after another. A fourth kind of product makes it bigger again.

## 4. Act Two — One table

Second demo: one table. The products now share a single table, with a type column. The same question. The same answer. And Hibernate's query is one plain select, from one table.

## 5. Act Three — Each row as its own class

Third demo: each row comes back as its own class. The cook book comes back as a book, with its ISBN. The kettle, as electronics, with its warranty card. The tea, as food, with its best-before date. Hibernate chose each class from the type column.

## 6. Act Four — A new type

Fourth demo: a new kind of product. A gift card. One new class, and one new column in the same table. It loads back as a gift card, to be activated for fifty pounds on dispatch.

## 7. Act Five — The bill

Fifth demo: the bill. Fifteen of the twenty type-specific cells are empty. Every book should have an ISBN. But the database refuses to require it. The kettle, lamp, tea and gift card have none. So a book with no ISBN is saved. The rule has to live in Java instead.

## 8. The Pattern, in JPA

Let's name the pattern, in JPA's words. The inheritance annotation, set to single table. A discriminator column holds the type. Each class has its own discriminator value. And Hibernate writes all the SQL.

## 9. Who Does What

Here is who does what. Product is mapped to the one table. Book, electronics, food and gift card are its subclasses. Catalog item is the comparison, with a table for each class. And the SQL log sees every statement Hibernate sends.

## 10. Where You Have Seen It

You have probably met this already. The inheritance annotation, in JPA entities. Ruby on Rails, which does the same with a type column. And database tables with a column called D type, and many empty cells.

## 11. When To Use It

So, when should you use it? When the types share most columns, and questions span all of them. Read the SQL Hibernate writes. Keep subclass rules in Java. And move to the joined strategy when empty cells start to dominate.

## 12. Thanks for Watching

That's Single Table Inheritance, with JPA. If you remember one sentence, make it this one. One table and a type column, and always look at the SQL. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Switch to the joined strategy, and read the SQL it writes. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
