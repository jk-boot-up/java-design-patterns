# Session Guide — Cache-Aside with Redis Pattern

A 60-minute session built around one question: once the cache is a real server that every shop process shares, what does it keep, for how long, and who decides?

## Learning Objectives

1. Say, in plain words, what Redis, a key, a value, an expiry and its name TTL, and SET with NX are.
2. Show a second process finding the cache already warm, where a cache in its own memory would not.
3. Show an entry removed by Redis on its own clock, and explain why a plain SET makes an entry live for ever.
4. Explain why sharing a read inside one process fixes a stampede for one instance but not for two, and what a lock in Redis adds.
5. Name the bill: the cold start, the missing size limit, the text format, and one more system to run.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The kitchen whiteboard analogy, and the twin project recapped in two minutes |
| 0:08–0:18 | Acts one and two: no cache, then Redis on the side |
| 0:18–0:28 | Act three: a second process and redis-cli |
| 0:28–0:40 | Act four: real expiry, and the plain SET |
| 0:40–0:50 | Act five: the stampede and the lock |
| 0:50–0:55 | Act six: the bill, and the verdict |
| 0:55–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd micro-services-design-patterns/cache-aside-with-redis-pattern
./gradlew -q run
```

Act one: how many different rows did the thousand reads touch? Act two: why exactly ten misses? Act three: why did the second shop's own-memory cache cost ten reads when the first shop had just read the same ten products? Act four: who removed the key, and what did the demo do while it waited? What did minus one mean? Act five: why two reads with sharing inside each instance, and why one with the lock? Act six: what would happen to a Redis with no maxmemory on a busy week?

Then open `src/main/java/com/jk/explore/cacheasideredis/RedisCache.java` and read `put` and `putWithoutExpiry` aloud. The only difference is one argument to `set`.

## Discussion

Ask the room who writes to the cache in a real shop. The page that reads the price, certainly. But also the price-sync job, the admin screen, the warm-up script after a deploy. Every one of them has to carry the expiry. Redis cannot tell a forgotten expiry from a deliberate one.

Then ask what should happen when the lock's holder dies. The lock expires after five seconds; the waiting requests try again. Is five seconds right for a database read that normally takes half a second? What if it takes six?

## Exercises

1. Change `putWithoutExpiry` to pass `SetParams.setParams().keepTtl()`, run the fourth act, and predict what Redis reports as the time to live.
2. Set `answerSlowly` to 5 milliseconds in the stampede, run it a few times, and describe how the count changes.
3. Start the demo's Redis with `--maxmemory 1mb --maxmemory-policy allkeys-lru`, write a thousand products, and count how many remain.
4. Make the lock's release check that the lock still holds this request's own token before deleting it, and say what goes wrong without the check when a holder is slower than the lock's expiry.
5. Add a third shop instance to the stampede and predict the three counts before you run it.

Close with the verdict: an expiry on every write, a delete after every change, a shared lock on a popular refill, and a size limit before real traffic.
