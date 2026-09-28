# Cache-Aside with Redis Pattern — Video Narration Script

## 1. Cache-Aside with Redis

Hello, and welcome. This video explains the Cache-Aside pattern in Java, using a real cache server called Redis. This video is presented by Jayasekhar Konduru. First, a simple definition. Cache-aside means you ask a fast copy first. If the copy has nothing, you fetch the real answer yourself. And you leave a copy behind, for the next person. In our online store, every product page needs a price, and prices live in the database. So the shop asks the cache for the price first. If the cache has nothing, the shop reads the database, and writes the price into the cache on the way back. By the end, you will hear a second shop find the cache already filled. A price removed by the cache on its own clock. One ordinary write that makes an old price last forever. And fifty requests rushing at the database, with nobody arranging it.

## 2. The Scenario

Here is the scenario. Every product page needs a price. The prices live in the database, which holds the truth. Ten products get most of the views, and their prices rarely change. On a busy day, the shop runs as more than one program, and all of them read the same database. The plain Java version of this project also used a cache. But that cache lived inside the shop's own program, with a clock the demo moved by hand. This time, the cache is a program of its own, shared by every shop. With a clock that nobody in the shop controls. And that changes three things.

## 3. No Cache

First, with no cache. Every product page reads the database. A thousand page views, over ten popular products, cost a thousand database reads. Only ten different rows were ever read. The database answered the same ten questions, a hundred times each.

## 4. Redis's Words

Redis brings a few words with it, and each is simpler than it sounds. Think of a whiteboard by the door of a busy restaurant kitchen. The recipes live in a thick book in the office, and walking there is slow. So one cook writes the answer on the board. And the next cook reads the board, instead of walking. Redis is the whiteboard. It is a separate program that keeps small pieces of data in memory, and answers over the network. Each note has a name, which Redis calls a key. And what the note says is called its value. Here, the key is the product's code, and the value is its price: ten pounds. And every cook in the kitchen reads the same board.

## 5. Look Aside, In Redis

Second demo: the pattern, with Redis. The demo starts Redis in a container, a small sealed box that the demo switches on and off by itself. The shop asks Redis for the price first. If Redis has nothing, that is a miss. So the shop reads the database, and writes the price into Redis, to be thrown away after sixty seconds. The same thousand views now cost only ten database reads. Ten misses, one for each product. And nine hundred and ninety hits. Redis now holds ten keys.

## 6. Another Process Can See It

Third demo, and this is something the plain Java version could never show. The first shop has viewed all ten products. Then a second shop starts, as a separate Java program, with its own memory. With a cache inside its own memory, its first ten views cost ten database reads. The first shop's work is no use to it. With the same Redis, its first ten views cost no database reads at all. Ten hits. Then a third program, Redis's own command-line tool, asks for the same key. And it is told: ten pounds. Finally, the first shop changes that price to sixteen pounds, and deletes the key, once. No copy is left anywhere, so every shop reads the new price next time.

## 7. Where The Price Lives

Here is the whole setup, in words. There are two shop programs, one Redis, and one database. Each shop asks Redis first. On a miss, the shop itself reads the database. Then it writes the price into Redis. Redis never reads the database. It only keeps what a shop gives it. Because Redis is its own program, every shop sees the same entry. And one delete removes it for all of them.

## 8. Real Expiry

Fourth demo: expiry. Each entry in Redis can carry a time limit. The time an entry has left is called its time to live, or T T L. When the time is up, Redis removes the entry by itself. In the demo, one price is cached for two seconds. Another system changes that price in the database to twenty pounds, and does not tell the cache. So a customer still sees ten pounds. Nobody deletes the key. The demo only keeps asking Redis whether the key is still there. When the two seconds are up, Redis removes it on its own. And the next customer sees twenty pounds.

## 9. A Plain Write

Now the surprise, and the headline of this video. The command that writes a key in Redis is called SET. A SET can carry a time limit, or leave it out. A price-sync job writes the same price back into Redis, with a plain SET, and no time limit. Redis treats that as a brand new value. And it throws the old time limit away. Asked how long the entry has left, Redis now says minus one. That means never. Then the price in the database changes to twenty-one pounds. Two seconds later, customers still see twenty pounds. And they will keep seeing it, until somebody deletes the key by hand.

## 10. One Argument

The difference between those two writes is one argument. The first write passes a time limit of two seconds. So Redis removes the entry by itself, when the time runs out. The second write passes nothing. So the entry lives forever. In the plain Java version, every write set the expiry automatically. In Redis, every writer has to remember it. The product page, the price-sync job, the admin screen, and the warm-up script. Forget one argument, and the promise that a price is only wrong for a short time is gone.

## 11. A Real Stampede

Fifth demo: a stampede. Fifty requests arrive at the same moment, split across two shop programs. All for the same product, just after its entry has gone. And a database read takes half a second. Every request asks Redis, finds nothing, and goes to the database. More than forty database reads, for one price. The exact number depends on the computer's scheduling, so the demo does not count it exactly. The plain Java fix lets requests inside one program share a single read. With two programs, that gives two reads, one each. Because neither program can see the other's waiting requests. The fix that works across programs is a lock, kept in Redis. A request writes a lock key, but only if nobody has written it already. So exactly one request wins. The winner reads the database. Everybody else waits for the price to appear in Redis. One database read. The lock has its own five-second time limit. So a shop that crashes while holding it cannot block the others forever.

## 12. The Bill

Sixth demo: the bill. Redis is emptied, just as a restart with nothing saved would leave it. The first ten views cost ten database reads again. The database takes the whole load, until the cache fills up. Next, size. Out of the box, Redis has no memory limit. And its rule for making room is to never throw anything away. So a cache has to be given a size, and told what to throw away when it is full. Also, the price now crosses the network as text. And Redis is one more system to run, secure, and watch.

## 13. What The Simulation Left Out

So what did the plain Java version get right? The whole shape. Ask the cache first. On a miss, read the database, and fill the cache. Delete the cached copy after a write. Expire entries. And warm up again after a restart. All of that holds on Redis, with the same numbers. But it left out three things. A second program. Its cache lived inside one program, so a second shop would have warmed up its own. A real clock. Nothing expired unless the demo said so. And a real stampede. It had to hold every read back, to make one happen. And the headline. In Redis, a plain write erases the expiry, and an old price lasts forever.

## 14. The Verdict

So, here is the verdict. Put Redis to the side when several programs need the same cached answers. Then settle four things, because Redis will not assume any of them. One. Put an expiry on every write, or the entry lives forever. Two. Delete the entry after every change to the database. Three. Guard the refill of a popular entry with a lock that every shop can see. And give that lock an expiry of its own. Four. Give Redis a size limit, and a rule for what to throw away, before real traffic arrives.

## 15. What Is Real, And When Not

A quick, honest note about this demo. Redis is version eight point ten point two, in a container the demo starts and stops by itself. The Java client is called Jedis. The container is run by a library called Testcontainers. The second shop really is a separate Java program. And every expiry runs on Redis's own clock. Only the database is kept simple, so the cache stays the lesson. So, when is this too much? If the shop runs as one program, a cache in its own memory is faster, and costs nothing to run. And if a price must always be exact, a cache that can be out of date is a bug, not a trade-off.

## 16. Thanks for Watching

That's Cache-Aside, with Redis. If you remember one sentence, make it this one. The shop fills the cache, every shop sees what it filled, and an entry only expires if every write remembers to say so. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Change the plain write so it keeps the old expiry. Guess what Redis will report as the time to live, and then run it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
