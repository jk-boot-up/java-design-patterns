# Hedged Requests, Explained

## The pattern in one sentence

Hedged Requests sends a second copy of a slow call to another replica after a
short delay, and uses whichever answer arrives first.

## The 5 acts

### 1. One call, and a slow tail

Each price is asked for once. The median answer takes twenty milliseconds,
but about one call in thirty-three lands on a paused replica and takes a
whole second. So the 99th percentile is a thousand milliseconds, and a product
page waiting for that price waits a whole second.

### 2. Hedge after 50 ms

Now the client waits fifty milliseconds, more than a normal call ever takes.
If there is no answer, it asks a second replica too, and takes the first
answer. The slow calls now finish in seventy milliseconds, fifty waiting plus
twenty for the backup. The 99th percentile falls from a thousand to seventy,
and only thirty-one calls in a thousand needed a second call.

### 3. Hedge at once

Why wait at all? Sending two calls every time brings the 99th percentile down
to twenty milliseconds, but it doubles the load on the price service: a
thousand extra calls. Twice the work to save fifty milliseconds on a few
calls. Waiting first is the better deal.

### 4. A real race

The same idea with real threads. Replica A is paused and would take a second;
replica B answers in twenty milliseconds. The hedger calls A, waits fifty
milliseconds, calls B, and returns B's answer in well under half a second.
Then it cancels A's call, so A does not keep working on an answer nobody needs.

### 5. The bill

Hedging sends the same request twice, so it is only for calls that are safe to
repeat, like reading a price. Hedging "place order" could charge the customer
twice. And if every replica is slow because they are all overloaded, extra
calls make it worse, so hedges are capped at a few percent of requests.

## The verdict

Hedge read-only or otherwise repeatable calls to replicated services with an
occasional slow outlier. Wait about the 95th percentile before hedging, cancel
the loser, and cap hedges so they cannot add much load.

## How to recognise this in code you did not write

- Two calls to different replicas, the first answer used.
- gRPC `hedgingPolicy`, Cassandra `speculative_retry`.
- `CompletableFuture.anyOf` with a delayed second call.

## Where you have already met this

- Google's "The Tail at Scale" and Bigtable's hedged reads.
- gRPC's hedging policy, configured per method.
- Cassandra's speculative retry and HDFS hedged reads.
- `CompletableFuture.anyOf` for racing calls in Java.
