# Rate Limiter Pattern — Video Narration Script

## 1. Rate Limiter

Hello, and welcome. This video explains the Rate Limiter pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A rate limiter refuses requests beyond an agreed rate. So one caller cannot use up a service that everyone shares. It says no early, so the service does not fail later. Think of a nightclub with a door attendant. Only so many people are let in each minute. The rest are told to wait, before the room gets dangerously full. In our online store, the thing that can be overwhelmed is the product search. By the end, you will hear a thousand requests reach a search that can serve a hundred. A bucket of tokens allow a burst, and then a steady rate. A separate bucket for each caller protect a polite caller from a greedy one. A refusal that says exactly when to come back. And the bill.

## 2. The Scenario

Here is the scenario. The product search can serve a hundred requests a second. One client, perhaps a script, sends a thousand in a single second. And every other customer waits behind it. So here is the question. What should the search do about the other nine hundred?

## 3. No Limit

First demo: no limit. The search can serve a hundred requests a second. One client sends a thousand. All thousand are accepted. Nine hundred of them are more than the search can serve. And every other customer waits behind them.

## 4. The Pattern

Now, the pattern. Picture a bucket that holds tokens. Each request takes one token. The bucket refills at a steady rate, up to its size, and no further. If there is no token left, the request is refused, straight away. And it is told when to come back.

## 5. A Bucket Of Tokens

Second demo: a bucket of tokens. The bucket holds ten tokens, and refills at five per second. A burst of twenty requests arrives at once. Ten are allowed, and ten are refused. One second later, another twenty arrive. Five are allowed: the five tokens that refilled. After ten quiet seconds, the bucket is full again. But no fuller than ten.

## 6. A Steady Rate Always Gets Through

Third demo: a steady rate always gets through. Five requests a second, evenly spaced, for a whole minute. All three hundred are allowed. A well-behaved client never notices the limiter. A short burst is allowed, up to the size of the bucket. But a rate that stays above the refill rate is not.

## 7. One Bucket For Everyone, Or One Each

Fourth demo: one bucket for everyone, or one each. With a single shared bucket, a greedy client takes all ten tokens. And a polite client is refused. That is not protection. It is just a different outage. With a bucket for each caller, the greedy client is held to ten. And the polite client is allowed through.

## 8. Say When To Come Back

Fifth demo: say when to come back. The bucket is empty. The refusal says: try again in one second. One millisecond too early, and the request is refused. At exactly the time it said, it is allowed. The client does not have to guess. And it does not keep hammering the service.

## 9. The Bill

Finally, the bill. Three servers, each with its own bucket, allow thirty requests, not ten. So the limit is three times looser than it says. Ten thousand callers means ten thousand buckets in memory. And a real web page that loads twelve things at once only gets ten. The limit cannot tell a person from a script.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for an H T T P response with status four two nine, meaning too many requests. Often with a header saying when to retry. Look for a class named bucket, limiter, or throttle. Look for rate limiter classes from libraries like Resilience four J or Guava. Or a limit in the A P I documentation, such as a hundred requests a minute.

## 11. The Verdict

So, here is the verdict. Use a rate limiter on any service that shared callers can overwhelm. And on any A P I you offer to others. Use a token bucket, so short bursts are allowed. Give each caller its own bucket. Tell refused callers exactly when to retry. Share the count across servers, if the limit must be exact. And set the bucket size from real page loads, not from a guess.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Nothing depends on a real clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For an internal service with one known caller, a limit is only another way to fail. It earns its place when there are many callers, or callers you do not know.

## 14. Thanks for Watching

That's the Rate Limiter pattern. If you remember one sentence, make it this one. A rate limiter says no early, and says when to come back, and the price is extra state, and a limit that cannot tell a person from a script. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Make each caller's bucket larger. Then see which polite requests stop being refused. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
