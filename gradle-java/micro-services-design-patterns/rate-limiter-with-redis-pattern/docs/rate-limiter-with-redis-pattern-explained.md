# Rate Limiter with Redis, Explained

## The pattern in one sentence

A rate limiter gives each caller a bucket of tokens, spends one on every request, refuses when the bucket is empty and refills it on a timer — and when a service runs as many copies, the bucket has to live somewhere every copy can reach, or each copy grants the full limit on its own.

## The analogy, before any of the tools' words

Think of a nightclub with three doors and a rule of 100 people inside. If each door has its own bouncer with his own clicker, each lets in 100, and the club holds 300. The fix is one tally everyone can see: a whiteboard in the middle, where every bouncer crosses off a place before letting someone in.

Three new questions come with the whiteboard. What if two bouncers both read "one place left" and both walk off to let someone in, before either has crossed it off? What if one bouncer's watch is an hour fast, and he decides it is a new night and wipes the board clean? And what if the whiteboard falls off the wall? Those three questions are this project.

## What Redis and Bucket4j call these things

**Redis** is the whiteboard: a separate program that keeps small values in memory and lets many programs read and change them over the network. It runs in a container the demo starts and stops.

A **key** is a heading on the whiteboard: the name a value is kept under. Each client's bucket is one key, such as `search-limit:client-42`.

**Time to live** is a countdown on a key, after which Redis deletes it by itself.

A **script** is a short list of commands that Redis runs in one go, with nothing from any other connection in between.

**Bucket4j** is the Java library that does the token bucket. Its **bucket configuration** is the rule: 10 tokens, filled back up to 10 once an hour. Its **proxy manager** is the part that fetches a client's bucket from Redis and writes it back.

**Compare-and-swap** is Bucket4j's way of writing: write the new bucket only if the one in Redis is still the one that was read, and if not, read again and try again.

The **client clock** is the clock Bucket4j uses to work out how many tokens have come back. It is the clock of the server Bucket4j runs on, not Redis's.

One note on timing. The bucket in this project refills once an hour, not once a second, so that no token comes back while the demo runs and every count is exact on every machine.

## The six acts

### A Bucket In Each Server

Three copies of the search service sit behind a load balancer, which deals searches to them in turn. Each keeps its own bucket for each client in its own memory, with Bucket4j's ordinary in-memory bucket. client-42 sends 90 searches, and each server lets 10 through: 30 in all. Scaled out to six servers, the same 90 searches get 60 through. Every server added loosens the limit by another 10.

```
  the rule: 10 searches per client, refilled once an hour. client-42 sends 90 searches, dealt in turn across the servers.
  3 servers, each with its own bucket: 30 allowed, not 10.
  scaled out to 6 servers, the same 90: 60 allowed. every server added loosens the limit by another 10.
```

### One Bucket In Redis

Now each server keeps no bucket at all. Each has its own connection to one Redis, and on every search it asks Redis for the client's bucket. 90 searches through three servers: 10 allowed, 80 refused. Six servers, and a different client, client-77: still 10. Redis holds two keys, one per client, however many servers there are. Then server one is restarted with empty memory. client-42's next search is refused, with the advice to come back in 60 minutes. The bucket was never in the server, so restarting the server does not refill it.

```
  3 servers, each with its own connection to one Redis. client-42 sends 90: 10 allowed, 80 refused.
  scaled out to 6 servers, client-77 sends 90: 10 allowed. Redis holds 2 keys: one bucket per client, not per server.
  server-1 is restarted with empty memory. client-42's next search: refused. retry after 60 minutes.
```

### All At The Same Moment

Ninety searches, thirty on each of three servers, each on its own thread, all held at a gate and released at the same instant. Exactly 10 are allowed. Nobody holds a lock. Each server writes its answer back only if the bucket has not changed since it read it, and reads again if it has. The order the threads reach Redis differs from run to run; the count does not.

```
  3 servers, 30 searches each, all 90 released at the same instant on 90 threads: 10 allowed, 80 refused.
  no server holds a lock. each writes its answer back only if the bucket has not changed since it read it, and reads again if it has.
```

### Why Not Just A Number In Redis?

The first thing most people write is a plain number: read it, check it, write it back one lower. This act puts two servers' steps in a fixed order by hand, so the failure happens on every run. One token is left. Server one reads 1. Server two reads 1. Both write back 0, and both serve a search: 2 searches from 1 token. Afterwards Redis says 0, so nothing looks wrong.

Then the same, but each write lands only if the number is still what was read. Server one's write lands. Server two's is turned down; it reads again, finds 0, and refuses. 1 search from 1 token. That conditional write is what Bucket4j does on every search, as a small script Redis runs in one step.

```
  one token left. server-1 reads 1. server-2 reads 1. both write back 0 and serve: 2 searches from 1 token. Redis now says 0.
  again, but each write lands only if the number is still what was read. server-2's write is turned down; it reads again, finds 0, and refuses. 1 search from 1 token, 1 refused, 1 retry.
  Bucket4j does the second, on every search: its write is a small script that Redis runs in one step.
```

### Whose Clock?

This is the headline find of the project. Two servers with correct clocks spend client-42's 10 searches, and the next is refused. A third server's clock runs one hour fast. client-42 sends 20 searches through it, and 10 are allowed. The fast server read the empty bucket, worked out by its own clock that the hour was up, refilled it, and wrote the answer to Redis. Redis stored it, because Redis never looks at a clock. It keeps the bucket; the sums are done on each server. So a limit shared by every server is only as good as the worst clock among them.

```
  server-1 and server-2 have correct clocks. client-42 spends 10 searches through them. the next: refused.
  server-3's clock runs one hour fast. client-42 sends 20 through it: 10 allowed. it thinks the hour is up, refills the bucket, and Redis stores its answer.
  Redis keeps the bucket. the sums are done on each server, with that server's clock. the servers' clocks must agree.
```

### The Bill

1000 different clients search once each, and Redis holds 1000 keys. Each is set to delete itself in 60 minutes, when its bucket would be full again, because a full bucket and no bucket mean the same thing. So the keys do not pile up for ever.

Then Redis is stopped. Five searches reach the limiter and get five errors: not a yes and not a no. Let them through, and there is no limit at all. Refuse them, and five real customers see an error. Bucket4j cannot choose; the shop has to. And every search, allowed or not, now waits for a trip across the network to Redis before it is served. One container, for six servers.

```
  1000 different clients search once each: Redis holds 1000 keys. each is set to delete itself in 60 minutes, when its bucket would be full again.
  Redis is stopped. 5 searches: 5 errors from the limiter, and no answer. let them through, and there is no limit at all; refuse them, and 5 real customers see an error. the shop must choose.
  and every search now waits for a trip across the network to Redis before it is served. this demo needed 1 container for 6 servers.
```

## The verdict

When a service runs as more than one copy, keep the bucket outside all of them, in a store they all reach. Then say three things out loud, because the store will not: the check and the write must be one step, which Bucket4j's compare-and-swap does for you and a plain number does not; the servers' clocks must agree, because they, not Redis, do the refill sums; and somebody must decide what the limiter answers when the store is down.

## How to recognise this in code you did not write

- A `Bucket.builder()` in a service that runs as several copies: a limit per copy, multiplied by however many there are.
- A `Bucket4jLettuce.casBasedBuilder`, or a Jedis or Redisson equivalent, building a proxy manager: the bucket lives in Redis.
- An `expirationAfterWrite` on that builder, which lets Redis forget full buckets. Without it, every client ever seen leaves a key behind.
- A `GET` followed by a `SET` or `DECR` checked in application code: the two-step count that spends the last token twice.
- A `try` around `tryConsume` with nothing in the `catch`, or nothing at all: nobody has decided what happens when Redis is down.

## Where you have already met this

Any public API that answers "429 Too Many Requests" while running on many servers. Spring Cloud Gateway's Redis rate limiter, Envoy's global rate limit service and NGINX Plus's shared zones all keep the count outside the servers, as this project does.

## When this is too much

On one server, the twin's in-memory bucket is exact, free and cannot go down. If a limit only needs to be roughly right, a bucket per server with the limit divided by the number of servers costs no network trip. A shared store earns its place when there are many servers, the number changes as they scale, and the limit has to be one number regardless.
