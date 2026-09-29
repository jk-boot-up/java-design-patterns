# Single Table Inheritance Pattern — Video Narration Script

## 1. Single Table Inheritance

Hello, and welcome. This video explains the Single Table Inheritance pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Single table inheritance stores several related classes in one database table. A type column says which class each row is. And each row leaves empty the columns that belong to other types. Think of one travel expenses form for every kind of trip. A section for car journeys, one for trains, one for flights. You fill in yours and leave the rest blank. And finance keeps one pile of forms. In this video, the domain is an online shop. It sells books, food, and electronics. Each has a code, a name, and a price, and one field of its own. By the end, you will hear why a table per type makes simple questions slow. How one table fixes it. How each row becomes the right class. And what it costs.

## 2. The Scenario

Here is the scenario. Books have an ISBN. Food has a best-before date. Electronics have a warranty. All of them share a code, a name, and a price. In the database, each type had its own table. In Java, they are classes that share an interface.

## 3. Act One — A table per type

First demo: a table for every product type. Books in one table, food in another, electronics in a third. A customer asks for everything under ten pounds. The shop has to ask all three tables. Three queries, to find breakfast tea and a desk lamp. Add a fourth type, and every question about all products needs a fourth query.

## 4. Act Two — One table for all

Second demo: single table inheritance. Every product now lives in one table. It has the shared columns: code, name, and price. A type column, saying book, food, or electronics. And one column for each type's own field. Everything under ten pounds is now one query, on one table.

## 5. Act Three — Each row becomes its own class

Third demo: each row comes back as its own class. When a row is loaded, its type column says which class to build. Book one becomes a book, and its packing slip shows its ISBN. The kettle becomes electronics, with a two-year warranty card. The tea becomes food, with its best-before date.

## 6. Act Four — A new type

Fourth demo: a new type. The shop starts selling gift cards. That needs one new class, and one new column, for the card's value. Existing rows are untouched. They just leave the new column empty. Gift card one loads as a gift card: activate fifty pounds on dispatch.

## 7. Act Five — The bill

Fifth demo: the bill. Five products, four type-specific columns. Fifteen of the twenty cells are empty. And the database can no longer keep type rules. The ISBN column cannot be required, because food and kettles leave it empty. So a book with no ISBN is saved, without complaint.

## 8. The Pattern

Let's name the pattern. Store every type in one table. Add a type column, saying which class each row is. And a column for every field any type has. Each row fills in its own columns, and leaves the rest empty. When loading, the type column decides which class to build.

## 9. Who Does What

Here is who does what. Product is the shared interface. Book, food, electronics, and gift card implement it. Product table saves them all into one table, and loads each row back as the right class. Table per type is the old way, kept for comparison. And H2 is a real database, running in memory.

## 10. Where You Have Seen It

You have probably met this pattern already. J P A offers single table inheritance, with a discriminator column for the type. Ruby on Rails uses a column called type for the same thing. And many shop platforms keep every product in one table, with a product type column.

## 11. When To Use It

So, when should you use it? When the types share most of their fields, and are often queried together. Keep type-specific fields few. Add check constraints for rules like: a book must have an ISBN. And when the table fills with empty columns, switch to a table per class.

## 12. Thanks for Watching

That's the Single Table Inheritance pattern. If you remember one sentence, make it this one. Many classes, one table, and a type column to tell them apart. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline once its libraries are downloaded, with nothing else installed except a Java development kit. Here is one exercise to try. Add a check constraint, so every book must have an ISBN. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
