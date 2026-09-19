# Rate Limiter Pattern — Video Narration Script

## 1. Rate Limiter

Hello, and welcome. This video explains the Rate Limiter pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a rate limiter refuses requests beyond an agreed rate, so that one caller cannot use up a service that everyone shares. It says no early, so the service does not fail late. This is another project in the microservices category, whose subject is how many small services stay reliable when they talk to each other. In our online store, the thing that can be overwhelmed is the product search. By the end you will see a thousand requests reach a search that can serve a hundred, see a token bucket allow a burst and then a steady rate, see a bucket each protect a polite caller from a greedy one, hear a refusal say exactly when to come back, and see the bill.

## 2. The Scenario

Here is the scenario. The product search can serve a hundred requests a second. One client, perhaps a script, sends a thousand in a single second, and every other customer waits behind them. The question: what should the search do about the other nine hundred?

## 3. No Limit

First, no limit. The search can serve a hundred requests a second. One client sends a thousand. All are accepted. Nine hundred of them are beyond what the search can serve, and every other customer waits behind them.

## 4. The Pattern

The pattern. A bucket holds tokens. Each request takes one. The bucket refills at a steady rate, up to its size, and no further. If there is no token, the request is refused at once, and told when to come back.

## 5. A Bucket Of Tokens

Second, a bucket of tokens. Ten tokens, refilled at five a second. A burst of twenty at once: ten are allowed, ten are refused. One second later, another twenty: five are allowed, the five that refilled. After ten quiet seconds the bucket is full again, and no fuller. Ten.

## 6. A Steady Rate Always Gets Through

Third, a steady rate always gets through. Five requests a second, evenly spaced, for a whole minute: three hundred of three hundred are allowed. A well behaved client never notices the limiter. A burst is tolerated, up to the size of the bucket. A sustained rate above the refill is not.

## 7. One Bucket For Everyone, Or One Each

Fourth, one bucket for everyone, or one each. With a single shared bucket, a greedy client takes all ten tokens, and a polite client is refused. That is not protection, it is a different outage. With a bucket each, the greedy client is held to ten, and the polite client is allowed.

## 8. Say When To Come Back

Fifth, say when to come back. The bucket is empty, and the refusal says: retry after a thousand milliseconds. One millisecond early, and the request is refused. At the moment it said, it is allowed. The client does not have to guess, and does not hammer.

## 9. The Bill

Last, the bill. Three servers, each with its own bucket, allow thirty, not ten. The limit is three times looser than it says. Ten thousand callers mean ten thousand buckets in memory. And a real page that loads twelve things at once gets only ten. The limit cannot tell a person from a script.

## 10. How To Recognise It

How do you recognise this in code you did not write? A 429 Too Many Requests response, with a Retry-After header. A class named Bucket, Limiter or Throttle. Resilience4j's RateLimiter, Guava's RateLimiter, or a gateway plugin. A limit written in the API documentation, such as 100 requests a minute.

## 11. The Verdict

Here is my verdict, plainly. Use a rate limiter on any service that shared callers can overwhelm, and on any API you expose. Use a token bucket to allow short bursts, key it by caller, and tell refused callers exactly when to retry. Share the count across servers if the limit must be exact. Set the burst size from real page loads, not from a guess.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For an internal service with one known caller, a limit is only a way to fail. It earns its place with many or unknown callers.

## 14. Thanks for Watching

That's Rate Limiter. If you take one sentence away, take this one: a rate limiter says no early and says when to come back, and the price is state, and a limit that cannot tell a person from a script. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, make the bucket for a caller larger, and see which polite requests stop being refused. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
