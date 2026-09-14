# Client-Side Load Balancing, Explained

## In One Sentence

When several identical copies of a service are running, the caller decides which
copy to talk to — and it decides again for every single request.

## Everyday Analogy: The Supermarket Tills

You have finished your shopping and there are six tills open. Nobody is directing
anybody. You look along the row, see which queue is shortest, and join that one.

Three things about that are worth saying out loud, because all three come back as
soon as we talk about code.

The first is that **you did the choosing**. There was no member of staff at the head
of the queues assigning shoppers to tills. The decision was made by the person with
the trolley, from where they were standing.

The second is that **you chose with what you could see**. You did not know which
cashier is quickest, or that till four is about to need a price check. You looked
down the row and used the one piece of information available to you: queue length.

The third is the one people forget. **You will choose again next week.** Picking a
till is not a setting. It is a decision you make fresh every time, and the right
answer is different on a Tuesday morning than it is on a Saturday afternoon.

Now the other way round. Some shops do put a member of staff at the head of all six
queues, calling shoppers forward one at a time. That works too, and it works
*better* in one specific respect: that person can see all six queues and every
shopper. No individual shopper can. Keep that in your pocket — it is the honest
ending to this pattern, and we come back to it.

## The Problem, In The Shop

The Catalog service — the one that knows a product's name — runs as three copies.
Two of them answer in 10 milliseconds; the third takes 60, because it is on older
hardware.

Service discovery, the previous pattern, has already answered *what exists*: the
checkout asks a registry and is handed three names. This pattern is the very next
question. Now that you know about three, which one do you ask?

The answer that costs no thought is to take the first name on the list:

```java
ServiceInstance chosen = candidates.get(0);
```

Twelve requests later:

```
    catalog-1   12 requests (100%)   10ms each
    catalog-2    0 requests ( 0%)   10ms each
    catalog-3    0 requests ( 0%)   60ms each
  12 requests took 120ms in total
```

One hundred and twenty milliseconds — and that is the fastest total in this whole
project. Faster than taking turns, faster than the clever version. Taking the first
instance is not slow, it is not wrong, and it does not throw anything. It is simply
running the shop on one machine out of three that the shop is paying for, and
arranging that when that machine dies, everything dies with it.

This matters more than it looks, because it sets the tone for everything below: the
bad strategy here does not fail. It passes. Every test in
`FirstInstanceBalancerTest` passes, deliberately.

## The Pattern

Pull the choice out of the caller and give it a name.

```java
public interface LoadBalancer {
    ServiceInstance choose(List<ServiceInstance> candidates);
    default void observed(ServiceInstance instance, long tookMillis) { }
    String name();
}
```

One method that matters: given every instance currently believed to be running,
return the one to call. And the caller becomes almost empty:

```java
List<ServiceInstance> candidates = cluster.instances();
ServiceInstance chosen = balancer.choose(candidates);
log.note(clientName, "CHOSE", chosen.instanceId() + " by " + balancer.name());

long startedAt = clock.millis();
String name = cluster.call(chosen, sku);
balancer.observed(chosen, clock.millis() - startedAt);
return name;
```

Five lines, and no policy in any of them. `CatalogClient` never asks which balancer
it is holding. Swapping *take turns* for *prefer the fast ones* changes nothing in
this file.

Say it plainly: **this is Strategy.** Not "like" Strategy, not "an application of"
it — the same structure, with one method, several interchangeable implementations,
and a caller that holds one without knowing which. If you have done
`behavioural/strategy-pattern`, you have already written this interface under a
different name.

What is new is the context. The decision is about machines rather than business
rules; it is remade on every single request rather than once per order; and the
chooser has information — how slow each instance has been *for it* — that nothing
in the middle of the network can see.

## Take Turns: The Right Default

```java
ServiceInstance chosen = candidates.get(Math.floorMod(next, candidates.size()));
next++;
```

That is the whole of `RoundRobinBalancer`. A counter and a modulus. No
measurements, no configuration, no knowledge of anything.

```
    catalog-1    4 requests (33%)   10ms each
    catalog-2    4 requests (33%)   10ms each
    catalog-3    4 requests (33%)   60ms each
  12 requests took 320ms in total
```

A perfectly even split — and three hundred and twenty milliseconds, nearly three
times the naive version's total. Round-robin sent a third of the shop's traffic to
the slowest machine the shop owns, cheerfully, because round-robin does not know
what "slow" means and was never told.

This is the sentence to take away from this section: **fair is not the same as
fast.** An even split is only the best split when the instances are equally
capable, and in a real cluster they are not.

Round-robin is still the default, and should be. It has no state worth losing, it
cannot be misconfigured, and it is impossible to get subtly wrong.

## Prefer The Fast Ones: The Argument For Doing This In The Client

`LeastLatencyBalancer` keeps a running mean of how long each instance has taken and
prefers the lowest — but only after it has tried each one once:

```java
for (ServiceInstance candidate : candidates) {
    if (!averageMillis.containsKey(candidate.instanceId())) {
        return candidate;   // never tried; measure it before judging it
    }
}
return candidates.stream()
        .min((a, b) -> Long.compare(averageMillis.get(a.instanceId()),
                averageMillis.get(b.instanceId())))
        .orElseThrow();
```

That first loop is not politeness. A balancer that trusts a measurement it has not
taken is round-robin with extra confidence.

```
    catalog-1   10 requests (83%)   10ms each
    catalog-2    1 requests ( 8%)   10ms each
    catalog-3    1 requests ( 8%)   60ms each
  12 requests took 170ms in total
  the client now believes: catalog-1 10ms, catalog-2 10ms, catalog-3 60ms
```

One hundred and seventy milliseconds instead of three hundred and twenty, and the
slow box was asked exactly once — the once it took to find out it was slow.

Now read the last line again, because it is the argument for this entire pattern.
Nothing configured those three numbers. No file, no environment variable, no
operator. The client measured them, from its own requests, and it would have
measured different numbers if it were running in a different rack.

"How slow has this instance been **for me**" is a question only the caller can
answer. A balancer in the middle of the network measures its own view of the
cluster, and its view is not the caller's view: different path, different switches,
different distance. That is the one thing client-side balancing can do that
server-side balancing structurally cannot.

## The Half That Is Usually Skipped, Part One: Herding

Look at act three once more. `catalog-2` is exactly as fast as `catalog-1` — both
10 milliseconds — and it received one request out of twelve.

Ties broke towards whoever happened to be measured first. The client found a
favourite and stayed with it, which is harmless with one client.

Now put a thousand clients in front of the same cluster. They all measure the same
thing, they all reach the same conclusion, and they all pile onto the same instance.
They make it slow. They then all notice it is slow, and they all leave together, for
the same replacement. The cluster oscillates, and no individual client did anything
wrong.

A learning balancer needs a tie-break — a random choice among the near-equals, or a
small random jitter on the measurements — or it will herd. That is the honest cost
of the cleverer strategy, and a large part of why round-robin stays the default.

## The Half That Is Usually Skipped, Part Two: A Client Cannot See The Others

Act four runs two clients, each with its own round-robin balancer, four requests
each:

```
    catalog-1    2 requests (50%)   10ms each
    catalog-2    2 requests (50%)   10ms each
    catalog-3    0 requests ( 0%)   60ms each
```

Both clients behaved impeccably. Each took perfect turns. Between them they left an
instance with nothing at all to do.

There is no bug to find here, and this is what makes it worth a section of its own.
The counter lives inside one client, so it counts one client's requests. Two
counters that each start at zero and each advance by one produce a pattern that is
correct twice over and wrong collectively.

So the limit of this pattern, stated plainly: **a client-side balancer can only
balance the traffic it can see, and it can only see its own.** The more clients
there are, and the more they come and go, the further the collective pattern drifts
from the one each client thinks it is producing.

And here is the ending the textbooks tend to hurry past. If the callers are not
yours to change, or there are too many of them to reason about, do not build a
cleverer client — **put one balancer in front of the cluster and let it see every
request.** That is server-side balancing. It is the member of staff at the head of
all six queues. It is simpler, it is easier to operate, and it is the right answer
more often than this pattern's fans admit. The price is one more hop and one more
thing that can fail; the prize is a single component with the complete picture.

## What It Costs

- **One more decision on every request.** Cheap here, but it is code on the hot path
  of every call the caller makes.
- **State in the caller.** Round-robin's counter and least-latency's table both live
  in the client, so they are lost on restart and are per-instance-of-the-client, not
  per-service.
- **A learning balancer can herd**, as above, unless it deliberately breaks ties
  randomly.
- **No client has the whole picture**, so the collective result is never as good as
  each client's local result looks.
- **It has to be in every caller.** A balancing policy implemented in the client is
  implemented once per client language and once per client team. Server-side
  balancing is implemented once.

## When Not To Use It

- **When you do not own the callers.** A mobile app in the app store cannot be
  updated to fix a balancing policy. Put the balancer in front of the cluster.
- **When the instances really are identical.** If every box is the same speed,
  least-latency has nothing to learn and round-robin is already optimal.
- **When there are very many short-lived callers.** Per-client state is worthless if
  the client exits after three requests, and the herd problem is at its worst.
- **When a platform already does it.** A service mesh or a Kubernetes Service is
  already balancing. A second balancer inside your caller does not compose with it
  so much as argue with it.

## What To Remember

1. Several identical instances means a choice, and the choice is remade on every
   request.
2. Taking the first one is not slow and does not fail — it just runs the shop on one
   machine out of three and falls over completely when that machine does.
3. Pull the choice behind an interface. That interface is Strategy, and the caller
   ends up holding no policy at all.
4. Round-robin is fair. Fair is not fast, because the instances are not equally
   capable.
5. Least-latency is fast because the *caller* measured the latency, which is
   something only the caller can do.
6. A clever balancer with many copies will herd unless it breaks ties at random.
7. A client can only balance what it can see. When that is not enough, one balancer
   in front of the cluster is the better answer, not a cleverer client.
