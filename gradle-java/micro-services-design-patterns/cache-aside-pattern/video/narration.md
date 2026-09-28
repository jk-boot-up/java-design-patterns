# Cache-Aside Pattern — Video Narration Script

## 1. Cache-Aside

Hello, and welcome. This video explains the Cache-Aside pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A cache is a fast copy of data, kept close at hand. With cache-aside, the application looks in the cache first. If the answer is not there, the application reads the real source itself. Then it puts the answer in the cache, for next time. Think of a shop assistant who keeps the most asked-about leaflets on the counter. If a leaflet is on the counter, they hand it over. If not, they walk to the back room, fetch one, and leave a copy on the counter. In our online store, the thing asked for again and again is a product page. By the end, you will hear a thousand page views cost a thousand database reads, and then only ten. What happens when a price changes. How an expiry limits how out of date the cache can be. Fifty requests rushing at one missing entry. And the bill.

## 2. The Scenario

Here is the scenario. Ten popular products get almost every page view. Each view reads the product from the database. So here is the question. A thousand views means how many database reads? And should it?

## 3. No Cache

First, with no cache. A thousand product page views, over ten popular products. That is a thousand database reads. The same ten rows, read over and over again.

## 4. The Pattern

Now, the pattern. Ask the cache first. If it is missing, that is called a miss. On a miss, the application reads the database itself. Then it puts the answer in the cache, for next time. The cache never talks to the database. The application does. The cache sits to one side, and that is why it is called cache-aside.

## 5. Look Aside

Second demo: with the cache. The same thousand views now make only ten database reads. Nine hundred and ninety views are served from the cache. Those are called hits. And there are ten misses, one for each product. The database is asked once per product, not once per view.

## 6. Writes

Third demo: changing a price. The price changes from ten pounds to fifteen pounds. But the code that changed it forgot about the cache. So customers still see ten pounds. Now the price changes to sixteen pounds, and this time the cached copy is thrown away. The next read misses, goes to the database, and sees sixteen pounds. Throwing away a cached copy is called invalidating it. And every write must remember to do it.

## 7. A Time Limit On Staleness

Fourth demo: a time limit on how out of date the cache can be. Another system changes the price to twenty pounds, without telling the cache. Fifty-nine seconds later, customers still see ten pounds. Sixty-one seconds later, they see twenty. Because every entry expires after sixty seconds. An expiry does not make the cache right. It makes sure it is only wrong for a limited time. And you choose how long.

## 8. A Stampede

Fifth demo: a stampede. Fifty requests arrive at the same moment, for one popular product. And its cache entry has just expired. Every request misses. So every request reads the database. Fifty reads, for one row. Now let the requests share a single read. The first one goes to the database. The other forty-nine wait for it, and use its answer. One read, instead of fifty.

## 9. The Bill

Finally, the bill. If the cache restarts, it starts empty. So the first views all go to the database. And the database takes the whole load again, until the cache fills up. And remember, the cache is a copy, not the truth. It is one more thing to keep correct, to size, and to explain to the next person.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for code that asks the cache, then the database, then puts the answer in the cache. In Spring, look for the Cacheable and Cache Evict annotations. Look for a Redis or Memcached client, next to a database client. Or a comment saying: clear the cache when you change this.

## 11. The Verdict

So, here is the verdict. Use cache-aside for data that is read far more often than it is written. And where being slightly out of date is acceptable. Invalidate on every write you control. Give every entry an expiry. And share the read when many callers miss together. Do not use it for data that must always be exact. And never treat the cache as the only copy.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Nothing depends on a real clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? If the data changes on every read, or is only read once, a cache is just extra work. And if the data must always be exact, being out of date is a bug, not a trade-off.

## 14. Thanks for Watching

That's the Cache-Aside pattern. If you remember one sentence, make it this one. Cache-aside trades exactness for speed, and you pay in out of date reads, stampedes, and a second thing to keep correct. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Change the expiry to ten seconds. Then see what it does to the number of database reads, and to how out of date the prices get. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
