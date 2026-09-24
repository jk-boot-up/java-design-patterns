# Cache-Aside with Redis Pattern — Video Narration Script

## 1. Cache-Aside with Redis

Hello, and welcome. This video explains the Cache-Aside pattern in Java, using a real cache server called Redis. It is written and presented by Jayasekhar Konduru. Here is the plain definition, in general words. Cache-aside means you ask a fast copy first. When the copy has nothing, you fetch the real answer yourself, and you leave a copy behind for the next person. Now the same thing in our online store. Every product page needs a price, and the prices live in the database. So the shop asks the cache for the price first. If the cache has nothing, the shop reads the database, and writes the price into the cache on its way back. By the end you will have seen a second shop find the cache already warm, a price removed by the cache on its own clock, one ordinary write that makes a stale price last for ever, and fifty requests stampede the database with nothing arranging it.

## 2. The Scenario

Here is the scenario. Every product page needs a price, and the prices live in the database, which is the source of truth. Ten products get most of the views, and their prices rarely change. On a busy day the shop runs as more than one process, and every one of them reads the same database. The hand-built twin of this project already put a cache on the side, but that cache was a map inside the shop's own program, with a clock the demo moved by hand. This time the cache is a program of its own, shared by every shop, with a clock nobody in the shop controls. That changes three things.

## 3. No Cache

First, the version without a cache. Every product page reads the database. A thousand page views over ten popular products cost a thousand database reads. Only ten different rows were ever read. The database answered the same ten questions a hundred times each.

## 4. Redis's Words

Redis brings a few words with it, and each one is simpler than it sounds. Think of a whiteboard by the door of a busy restaurant kitchen. The recipes live in a thick book in the office, and walking there is slow. So a cook writes the answer on the board, and the next cook reads the board instead of walking. Redis is the whiteboard: a separate program that keeps small pieces of data in memory and answers over the network. Each note has a name, which Redis calls a key, and what the note says, which Redis calls its value. Here the key is product, colon, S K U dash zero, and the value is one thousand, a price in pence, written as text. And every cook in the kitchen reads the same board.

## 5. Look Aside, In Redis

Second, the pattern. The demo starts a Redis server in a container, a small sealed box the demo switches on and off itself. The shop asks Redis for the price first. When Redis has nothing, that is a miss, and the shop reads the database and writes the price into Redis, to be thrown away after sixty seconds. The same thousand views now cost ten database reads. Ten misses, one for each product, and then nine hundred and ninety hits. Redis holds ten keys.

## 6. Another Process Can See It

Third, something the twin could never show. The first shop has viewed all ten products. Then a second shop starts, as a separate Java program with its own memory. Given a cache in its own memory, the way the twin had it, its first ten views cost ten database reads. The first shop's work is no use to it. Given the same Redis, its first ten views cost no database reads at all: ten hits. Then Redis's own command-line program, a third program, asks for the key for S K U zero, and is told one thousand. Finally the first shop changes that price to sixteen hundred, and deletes the key, once. No copy is left for any process, so every shop reads the new price next time.

## 7. Where The Price Lives

Here is the whole arrangement, in words. There are two shop programs, one Redis, and one database. Each shop asks Redis first. On a miss, the shop itself reads the database, and then writes the price into Redis. Redis never reads the database. It only keeps what a shop gave it. Because Redis is its own program, every shop sees the same entry, and one delete removes it for all of them. The rule to remember is this: Redis never reads the database; each shop does.

## 8. Real Expiry

Fourth, expiry. Each entry in Redis can carry a time limit. The time an entry has left is called its time to live, and Redis shortens that to T T L. When the time is up, Redis removes the entry by itself. In the demo, the price of S K U zero is cached for two seconds. Another system changes the price in the database to two thousand, and does not tell the cache. So a customer still sees one thousand. Nobody deletes the key. The demo only asks Redis, again and again, whether the key is still there. When the two seconds are up, Redis removes it on its own clock, and the next customer sees two thousand.

## 9. A Plain Write

Now the surprise, and the headline of this video. The command that writes a key in Redis is called SET. A SET can carry a time limit, or it can leave it out. A price-sync job writes the price of S K U zero back into Redis, with a plain SET, and no time limit. Redis treats that as a brand new value, and throws the old time limit away. Asked how long the entry has left, Redis now says minus one, which means never. The database changes the price to twenty-one hundred. Two seconds later, as long as the first entry lived, a customer still sees two thousand. And they will keep seeing it, until somebody deletes the key by hand.

## 10. One Argument

The difference between those two writes is one argument. The first write passes a time limit of two thousand milliseconds, and Redis removes the entry by itself when it runs out. The second write passes nothing, and the entry lives for ever. In the twin, every write set the expiry, because the cache did it for you. In Redis, every writer has to remember: the page that reads a price, the price-sync job, the admin screen, the warm-up script. One forgotten argument, and the promise that a price is wrong only for a short time is gone.

## 11. A Real Stampede

Fifth, a stampede. Fifty requests arrive at the same moment, split across two shop instances, for S K U zero, just after its entry has gone. A database read takes half a second. Every request asks Redis, finds nothing, and goes to the database. More than forty database reads, for one price. The exact number is up to the computer's thread scheduler, so the demo describes it rather than counting it. The twin's fix lets the requests inside one program share one read. With two instances, that gives two reads, one per instance, because neither can see the other's waiting requests. The fix that works across programs is a lock kept in Redis. A request writes a lock key, but only if nobody has written it already. Redis calls that SET with N X, and exactly one request wins. The winner reads the database. Everybody else waits for the price to appear in Redis. One database read. The lock has its own five-second time limit, so a shop that dies holding it cannot block the others for ever.

## 12. The Bill

Sixth, the bill. Redis is emptied, the way a restart with nothing saved would leave it, and the first ten views cost ten database reads again. The database takes the whole load until the cache warms up. Redis has a setting for its size limit, called max memory, and out of the box it is zero, which means no limit. Its rule for making room, called the eviction policy, is no eviction, which means it never throws anything away. A cache has to be given a size, and told what to discard. The price now crosses the network as text: Redis holds S K U zero as the string one thousand. And Redis is one more system to run, secure and watch: one container, for two shop processes.

## 13. What The Simulation Left Out

So what did the hand-built twin get right? The whole shape. Ask the cache first. On a miss, read the database and fill the cache. Delete the cached copy after a write. Expire entries. Warm up again after a restart. All of that holds on Redis, with the same figures. What it left out was three things. A second process: its cache was a map inside one program, so a second shop would have spent ten reads warming its own. A real clock: nothing expired unless the demo said so. And a real stampede: the twin had to hold every database read back to make one happen. And the headline: in the twin the expiry came with every write. In Redis, a plain write erases it, and a stale price lasts for ever.

## 14. The Verdict

The verdict. Put Redis on the side when several processes need the same cached answers. Then say four things out loud, because Redis will not assume any of them. Put an expiry on every write, or the entry lives for ever. Delete the entry after every change to the database, so every shop reads again. Guard the refill of a popular entry with a lock every shop can see, and give that lock an expiry of its own. And give Redis a size limit, and a rule for what to throw away, before it meets real traffic.

## 15. What Is Real, And When Not

What in this project is real? Redis version eight point ten point two, in a container the demo starts and stops itself. The Java client is Jedis, and the container is run by a library called Testcontainers. The second shop is a genuinely separate Java program, and every expiry runs on Redis's own clock. The database is the one thing kept simple, so that the cache stays the lesson. And when is this too much? If the shop runs as one process, a map in its own memory is faster and costs nothing to run. And if a price must always be exact, a cache that can be stale is a bug, not a trade.

## 16. Thanks for Watching

That's Cache-Aside with Redis. If you take one sentence away, take this one: the shop fills the cache, every shop sees what it filled, and an entry expires only if every write remembers to say so. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, change the plain write so it keeps the old expiry, guess what Redis will report as the time to live, and then run it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
