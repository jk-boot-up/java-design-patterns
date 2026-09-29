# Write-Through Cache Pattern — Video Narration Script

## 1. Write-Through Cache

Hello, and welcome. This video explains the Write-Through Cache pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. With a write-through cache, every write goes through the cache. It writes the database, then updates its own copy, before saying the write is done. So reads from the cache always match the database. Think of a supermarket, where the till price and the shelf label must match. Whoever changes a price in the till also changes the shelf label, straight away, before moving on. A customer never sees one price and pays another. In this video, the domain is an online shop. Its product page reads prices from a cache, and a nightly job changes prices. By the end, you will hear how a write round the cache causes trouble. How write-through fixes it. What happens when a write fails. And what it costs.

## 2. The Scenario

Here is the scenario. The product page reads prices from a fast cache. Checkout reads them from the database. A nightly job changes prices. It wrote them straight into the database.

## 3. Act One — A write round the cache

First demo: a price change goes round the cache. The product page reads prices from a fast cache. Checkout reads them from the database. The nightly job cuts the kettle to twenty-seven pounds. It writes straight to the database, and forgets the cache. The page still shows thirty pounds. Checkout charges twenty-seven. The customer sees one price, and pays another.

## 4. Act Two — Write-through

Second demo: write-through. Every write now goes through the cache. The job asks the store to set the kettle to twenty-seven pounds. The store writes the database. Then it updates its own copy. Only then does it return. The page says twenty-seven. Checkout says twenty-seven.

## 5. Act Three — Fast reads

Third demo: reads come from the cache. A hundred people view the kettle. Database reads: zero. Every view was answered from the cache. And every answer was up to date.

## 6. Act Four — A refused write

Fourth demo: a refused write changes nothing. The database is read-only, for maintenance. The price job tries twenty-five pounds. The database refuses. Because the store writes the database first, it never touches its cache. Both still say twenty-seven. They never disagree.

## 7. Act Five — The bill

Fifth demo: the bill. Every write waits for the database. A thousand price updates spend twenty seconds waiting. And all thousand prices now sit in the cache. Though most of those products will never be viewed.

## 8. The Pattern

Let's name the pattern. Every write goes through the cache. Nothing writes around it. The cache writes the database first. Then it updates itself. Only then does it tell the caller the write is done. And reads come from the cache, which is always up to date.

## 9. Who Does What

Here is who does what. The write-through store has two methods. Get reads from the cache. Put writes the database, then the cache. The database is the source of truth. And cache aside, with the forgetful price job, is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Caches such as Hazelcast and Ehcache can be configured to write through. Spring's cache put annotation updates the cache whenever a method writes. And computer processors have write-through caches, between the processor and main memory.

## 11. When To Use It

So, when should you use it? For data that is read often, and must never be out of date. Prices, and stock levels. Make it the only way to write that data. And when writes are many, and speed matters more, consider write-behind instead.

## 12. Thanks for Watching

That's the Write-Through Cache pattern. If you remember one sentence, make it this one. Change the database and the cache together, every time, through one door. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Swap the two lines in put, and write a test that shows what breaks. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
