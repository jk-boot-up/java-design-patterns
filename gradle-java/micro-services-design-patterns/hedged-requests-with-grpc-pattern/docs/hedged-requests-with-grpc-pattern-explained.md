# Hedged Requests with gRPC, Explained

## The pattern in one sentence

With gRPC, hedging is a service-config policy: send another attempt after a
delay, take the first answer, and cancel the rest.

## The 5 acts

### 1. A slow tail

The product page looks up a hundred prices over a plain gRPC channel. Three
land on a paused worker and take about a second; the rest take about twenty
milliseconds. So the slowest one percent of lookups, and the pages waiting on
them, take a whole second.

### 2. A hedging policy

The channel is given a service config with a hedging policy: up to two
attempts, the second after 0.05 seconds. The shop's code does not change. Now
none of the hundred lookups takes over 0.2 seconds, and gRPC sent only three
extra calls, one for each slow one.

### 3. The loser is cancelled

When the second attempt answers first, gRPC cancels the first. The server can
see this: the three slow attempts, when their pause ends, find their call
cancelled and never send a reply.

### 4. Hedge at once

With a hedging delay of zero, gRPC sends both attempts at once, every time. A
hundred lookups send two hundred calls: twice the load on the price service,
to save a few rare slow ones.

### 5. The bill

The same policy, applied by mistake to the orders service, sends PlaceOrder
twice. The customer sees one confirmation; the server has placed two orders.
Hedge only reads, per service or per method, and cap hedges with gRPC's
retry throttling so an overloaded service is not sent more.

## The verdict

Use gRPC's hedging for cheap, repeatable reads with a rare slow outlier. Scope
it to those methods, choose a delay near the normal worst case, and add
throttling.

## How to recognise this in code you did not write

- `"hedgingPolicy"` in a service config.
- `.defaultServiceConfig(...)` and `.enableRetry()` on a channel.
- Servers checking `Context.current().isCancelled()`.

## Where you have already met this

- gRPC's `hedgingPolicy` and `retryPolicy` in a service config.
- Cassandra's speculative retry and HDFS hedged reads.
- Service meshes such as Envoy, which can hedge too.
