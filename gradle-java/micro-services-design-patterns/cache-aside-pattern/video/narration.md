# Cache-Aside Pattern — Video Narration Script

## 1. Cache-Aside

Hello, and welcome. This video explains the Cache-Aside pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: cache-aside means the application looks in a cache first. If the answer is not there, the application reads the real source itself, and puts the answer in the cache for next time. This is another project in the microservices category, whose subject is how many small services stay reliable when they talk to each other. In our online store, the thing that gets asked for over and over is a product page. By the end you will see a thousand page views cost a thousand database reads, then ten, see what happens on a write, see an expiry bound how stale the cache can be, watch fifty requests stampede a cold key and one read serve them all, and see the bill.

## 2. The Scenario

Here is the scenario. Ten popular products get almost every page view. Each view reads the product from the database. The question: a thousand views is how many database reads? And should it be?

## 3. No Cache

First, no cache. A thousand product page views, over ten popular products. That is a thousand database reads, on the same ten rows, over and over.

## 4. The Pattern

The pattern. Ask the cache first. On a miss, the application reads the source itself. Then it puts the answer in the cache, for next time. The cache never talks to the database. The application does, and that is why it is called aside.

## 5. Look Aside

Second, look aside. The same thousand views now make ten database reads. Nine hundred and ninety are served by the cache, and ten were misses, one for each product. The database is asked once for each product, not once for each view.

## 6. Writes

Third, writes. The price changes to fifteen hundred, but the change forgot the cache. Customers still see a thousand. Change it to sixteen hundred and throw the cached copy away, and the next read goes to the database and sees sixteen hundred. Every write must remember to invalidate.

## 7. A Time Limit On Staleness

Fourth, a time limit on staleness. Another system changes the price behind the cache's back. After fifty nine seconds, customers still see a thousand. After sixty one, they see two thousand. An expiry does not make the cache right. It makes it wrong for a bounded time, and you choose how long.

## 8. A Stampede

Fifth, a stampede. Fifty requests arrive together for one popular product whose entry has just expired. Every one misses, so every one reads the database: fifty reads, for one row. Let the requests share a single read, and there is one. The others wait for it, and use its answer.

## 9. The Bill

Last, the bill. If the cache restarts empty, the first views all go to the database, and it takes the whole load again until the cache warms up. And the cache is a copy, not the truth. There is now a second thing to keep right, to size, and to explain to the next person.

## 10. How To Recognise It

How do you recognise this in code you did not write? Code that calls cache.get, then the database, then cache.put. @Cacheable and @CacheEvict in Spring. A Redis or Memcached client beside a database client. A comment saying 'clear the cache when you change this'.

## 11. The Verdict

Here is my verdict, plainly. Use cache-aside for data that is read far more than it is written, where a little staleness is acceptable. Invalidate on every write you control, give every entry an expiry, and share the read when many callers miss together. Do not use it for data that must always be exact, and never treat the cache as the only copy.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For data that changes on every read, or that is read once, a cache is overhead. For data that must be exact, staleness is a bug, not a trade.

## 14. Thanks for Watching

That's Cache-Aside. If you take one sentence away, take this one: cache-aside trades exactness for speed, and you pay in stale reads, stampedes and a second thing to keep right. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, change the expiry to ten seconds, and see what it does to the database reads and the staleness. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
