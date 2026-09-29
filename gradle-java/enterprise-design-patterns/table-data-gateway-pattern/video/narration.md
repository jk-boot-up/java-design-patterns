# Table Data Gateway Pattern — Video Narration Script

## 1. Table Data Gateway

Hello, and welcome. This video explains the Table Data Gateway pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A table data gateway is one class for each database table. It holds every piece of SQL for that table. The rest of the program asks it plain questions, and never writes SQL itself. Think of a bank. Customers do not walk into the vault. They ask at the counter. When the vault is reorganised, only the counter staff learn the new layout. In this video, the domain is an online shop. It keeps its products in a database table: a code, a name, a price, and how many are in stock. By the end, you will hear how SQL spread across a program breaks. How a gateway fixes it. How a change is made in one place. And what the pattern costs.

## 2. The Scenario

Here is the scenario. The shop's products live in a database table. Each row has a code, a name, a price, and a stock count. Three parts of the shop use it. The product page shows stock. The stock report counts what has run out. Checkout takes items out of stock. Each one wrote its own SQL.

## 3. Act One — SQL in every caller

First demo: every caller writes its own SQL. The product page, the stock report, and checkout each talk to the product table directly. They work. The kettle has four in stock. One product is out of stock. Checkout takes a kettle. Then the database team renames the stock column to quantity. The product page fails. The stock report fails. Checkout fails. All three say: column stock not found.

## 4. Act Two — A table data gateway

Second demo: a table data gateway. One class now holds every piece of SQL for the product table. The page asks it: find the product with this code. The report asks: how many are out of stock? Checkout says: take one of these. They get plain records back. Everything works as before. And a new question, products cheaper than ten pounds, returns the tea towel and the mug.

## 5. Act Three — A rename, fixed once

Third demo: the same rename, fixed in one place. Stock is renamed to quantity again. This time, the column's name lives in exactly one place: the gateway. It is told the new name, once. The page, the report, and checkout do not change at all. And they all work.

## 6. Act Four — Where the SQL lives

Fourth demo: where the SQL lives now. In the old code, three classes talked to the product table. In the new code, none of the callers do. Only the gateway. The callers get plain records. No database connections, and no SQL.

## 7. Act Five — The bill

Fifth demo: the bill. The gateway returns rows, which are just data. A rule like low on stock has nowhere to live, except in each caller. And the gateway grows a new method for every question anyone asks the table.

## 8. The Pattern

Let's name the pattern. Give each table one class: the gateway. The gateway holds every piece of SQL for that table. Finding, counting, inserting, updating. Everyone else asks it plain questions, and gets plain records back. Nobody else writes SQL for that table.

## 9. Who Does What

Here is who does what. Product gateway holds all of the product table's SQL. Row is a record: one product, as plain data. Pages holds the three callers: the product page, the stock report, and checkout. H2 is a real database that runs inside the program, in memory. And the scattered package is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Classes called D A O, data access objects, such as product D A O, are table data gateways. So is Spring's J D B C template, wrapped in one class per table. And MyBatis mapper interfaces.

## 11. When To Use It

So, when should you use it? As soon as more than one part of a program touches a table. Keep SQL, connections, and result sets inside the gateway. Return plain records. And when rows start needing behaviour, such as rules about stock, move on to a repository or a data mapper.

## 12. Thanks for Watching

That's the Table Data Gateway pattern. If you remember one sentence, make it this one. One class speaks SQL for each table, and everyone else just asks it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline once its libraries are downloaded, with nothing else installed except a Java development kit. Here is one exercise to try. Add insert and delete to the gateway, with tests. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
