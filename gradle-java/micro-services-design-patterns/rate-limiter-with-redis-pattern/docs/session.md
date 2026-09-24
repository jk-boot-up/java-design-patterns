# Session Guide — Rate Limiter with Redis Pattern

A 60-minute session built around one question: once the bucket lives in Redis and every copy of the service shares it, what does Redis do for you, and what is still up to the servers?

## Learning Objectives

1. Say, in plain words, what Redis, a key, a time to live, a script, a proxy manager and compare-and-swap are.
2. Show that a bucket per server multiplies the limit by the number of servers, and that a bucket in Redis does not.
3. Explain why a count read and written in two steps lets two servers spend the same last token, and how a conditional write stops it.
4. Explain why a server with a wrong clock can refill a shared bucket for everyone.
5. Say what the limiter should answer when Redis cannot be reached, and why that is the shop's decision.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The nightclub with three doors, and the twin project recapped in two minutes |
| 0:08–0:18 | Acts one and two: a bucket in each server, then one bucket in Redis |
| 0:18–0:30 | Acts three and four: all at once, and the plain number |
| 0:30–0:42 | Act five: whose clock? |
| 0:42–0:50 | Act six: the bill |
| 0:50–0:55 | The verdict |
| 0:55–1:00 | Exercises |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd micro-services-design-patterns/rate-limiter-with-redis-pattern
./gradlew -q run
```

Act one: why 30, and why 60 on six servers? Act two: why did the restarted server refuse, when its memory was empty? Act three: 90 threads at once, and still 10 — what stopped the eleventh? Act four: after two searches were served from one token, what did Redis say, and why is that the dangerous part? Act five: which program did the refill sum, and which clock did it use? Act six: when Redis was stopped, should those 5 searches have been served?

Then open `src/main/java/com/jk/explore/ratelimiterredis/ServerSharingRedis.java` and read the constructor aloud. Everything the pattern needs from Bucket4j is in that one builder chain.

## Discussion

Ask the room which is worse for a shop: a search limit that fails open for five minutes while Redis restarts, or a checkout page that shows errors for five minutes. There is no single answer; a limit that protects a costly partner API may need to fail closed, while one that only guards against scrapers can fail open.

Then ask how the clocks on a real fleet are kept in step, and what an hour's drift would mean for every other thing the servers do.

## Exercises

1. Change `SearchLimit` to refill 10 every second, run the demo a few times, and find the counts that stop being exact.
2. In the fifth act, make the fast server's clock run an hour slow instead, predict the count, and run it.
3. Change `PlainCounter` to use Redis's own `DECR` command, and say whether two servers can still spend the same last token.
4. Remove `expirationAfterWrite` from `ServerSharingRedis`, run the sixth act, and ask Redis how long the keys will live.
5. Wrap `search` so that an error from Redis falls back to a bucket in the server's own memory, and say what limit a client really gets while Redis is down.

Close with the verdict: keep the bucket outside the servers, make the check and the write one step, keep the clocks in step, and decide what an error means.
