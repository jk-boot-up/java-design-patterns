# Space-Based Architecture Pattern — Video Narration Script

## 1. Space-Based Architecture

Hello, and welcome. This video explains Space-Based Architecture, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. In a space-based system, every copy of the application keeps its own copy of the data, in memory. The copies are kept in step through a data grid. And the database is updated in the background, so no request ever waits for it. Think of pop-up stalls at a festival, selling the same T-shirts. Each stall keeps its own tally, and serves its own queue. They radio their sales to each other, and head office updates its books overnight. In this video, the domain is an online shop's kettle flash sale. Hundreds of orders arrive at once, and every one must check the stock. By the end, you will hear why more servers did not help. How processing units with the data in memory do. How the copies catch up. And the kettle that was sold twice.

## 2. The Scenario

Here is the scenario. The shop runs a kettle flash sale. Three app servers take the orders. Every order checks and updates the stock in one central database. Five milliseconds a query, and one query at a time.

## 3. Act One — One database for everyone

First demo: three app servers, one database. Every kettle order checks and updates the stock in the database. Five milliseconds each, one at a time. Three hundred orders take over one point four seconds. Double the app servers, to six. Still over one point four seconds. The database is the limit, not the servers.

## 4. Act Two — Processing units

Second demo: processing units, each with the data in memory. Each unit is a copy of the app, holding its own copy of the stock. Orders are spread across three units, and answered straight from memory. Three hundred orders in under three tenths of a second. Not one of them touched the database.

## 5. Act Three — The data grid

Third demo: the data grid keeps the copies in step. Right after the sale, each unit has only seen its own hundred sales. Each one thinks there are nine hundred kettles left. The grid copies every sale to the other units. Now all three agree: seven hundred.

## 6. Act Four — The database catches up

Fourth demo: the database catches up, in the background. A data writer collects the changes from the grid. It writes them in batches of a hundred. Three writes, instead of three hundred. The database now says seven hundred. And no customer waited for any of those writes.

## 7. Act Five — The bill

Fifth demo: the bill. One kettle left. Two customers buy it at the same moment, on two different units. Neither unit has heard about the other's sale yet. Both say yes. After replication, the stock is minus one. And a unit that crashes before the grid copies its sales loses them.

## 8. The Pattern

Let's name the pattern. Run the app as processing units. Each unit holds the data it needs, in its own memory, and answers from it. A data grid copies every change to the other units. And a data writer brings the database up to date in the background, in batches. The database is no longer in the way of any request.

## 9. Who Does What

Here is who does what. A processing unit sells from its own copy of the stock. The data grid copies each sale to the other units. The data writer writes the changes to the database in batches. And the central database, in every request, is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. In-memory data grids such as Hazelcast, Apache Ignite, and Coherence are built for it. Ticket sales and flash sales use it to survive huge spikes. And the name comes from JavaSpaces, an early shared memory space for Java programs.

## 11. When To Use It

So, when should you use it? For extreme, spiky load, where copies disagreeing for a moment is acceptable. Use a data grid product, rather than writing your own. And for ordinary load, one database, with good indexes and caching, is simpler, and always consistent.

## 12. Thanks for Watching

That's Space-Based Architecture. If you remember one sentence, make it this one. Keep the data next to the work, and let the database catch up later. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Hold back a small safety stock on each unit, so the last kettle is never sold twice. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
