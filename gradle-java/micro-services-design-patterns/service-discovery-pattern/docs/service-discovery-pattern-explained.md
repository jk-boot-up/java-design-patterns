# The Service Discovery Pattern, Explained

## In One Sentence

Instead of writing a service's address into the caller, keep a shared list of who
is running right now, and have the caller ask that list every time.

That is the whole pattern. Everything below is about why a list beats a constant,
what the list gets wrong, and what a caller has to do about it.

## Everyday Analogy: The Taxi Rank

Imagine you need a taxi. One way is to keep the mobile number of a driver called
Dave. It works beautifully while Dave is working. It fails completely the evening
Dave is off, and it goes on failing even though there are eleven other drivers in
town who would happily take you, because your phone knows about Dave and nobody
else.

The other way is a taxi rank. You do not know any driver's name. You go to the
rank and take whoever is at the front. Drivers join the rank when they start a
shift and leave it when they finish, and none of that requires you to change
anything you know or do.

The rank is a service registry. The drivers are instances. And the crucial detail
— the one that makes this more than a nice picture — is what happens when you get
into a car whose driver has just been called away. You do not stand there
insisting. You take the next one.

Analogies are allowed to come from anywhere; the worked example below is the
online shop, as it is throughout this repository.

## The Problem, In The Shop

The shop's Pricing service runs as three instances: `pricing-1`, `pricing-2` and
`pricing-3`. They are the same program started three times, so any one of them can
answer any question and all three give the same answer.

The checkout needs a price, and so it needs an address.

Writing one down is the first thing everybody does, and for a long time it is
right. `HardcodedPricingClient` in this project holds the string `pricing-1` and
calls it. There is no bug in that class. It is four lines and every one of them is
correct.

Then somebody deploys Pricing. A rolling deployment stops `pricing-1`, and:

```
      0ms ->    10ms  pricing-1        OK        £449.99
     10ms ->    10ms  Registry         DEREGISTER pricing-1 left cleanly
  after the deploy:  pricing-1 did not answer
```

The checkout is down. Not degraded — down. And two perfectly healthy instances are
sitting idle three metres away in the same rack, because the only thing the client
was ever told was the name of a machine that no longer exists.

The same thing happens, in reverse, when the shop scales up. Start `pricing-4` for
a busy Friday and nothing will ever call it. The capacity is real, paid for, and
unreachable.

The underlying mistake is easy to state: **the set of running instances changes
several times a day, and the source code of the callers changes once a fortnight.**
A fast-moving fact has been written into a slow-moving artefact. A properties file
improves the ratio a little and does not change the shape of the problem, because
a human still has to edit it, and that human still has to notice.

## The Pattern

Add a registry — a shared list of who is running right now — and three rules
about how it is kept.

**An instance announces itself when it starts.** `PricingCluster.start` calls
`registry.register(instance)`. From that moment the instance is discoverable.
Nobody edits anything.

**An instance says "still here" periodically.** That is the heartbeat. A
registration is not permanent; it is a **lease**, good for three seconds from the
last heartbeat in this project. Renewing is cheap and forgetting is fatal, which
is exactly the property you want.

**An instance deregisters when it shuts down politely.** A rolling deployment
takes an instance off the list before it stops answering, so callers never see the
gap at all.

And on the other side, the caller asks. `DiscoveringPricingClient.price` starts
with `registry.instances("Pricing")` on **every single call**, not once at
startup. That is deliberate and it is the difference between discovery and a
slightly more elaborate configuration file. A client that looks up once and caches
the answer for the life of the process has reinvented the hardcoded address with
extra steps.

## The Half That Is Usually Skipped

A registry cannot be right. Not "is sometimes wrong" — cannot be right, in
principle. An instance that crashes cannot send a message saying it has crashed.
For some window of time, the list will confidently offer you an address that
nothing is listening on.

Act three of the demo does exactly that. `pricing-1` is killed with no
deregistration, and then a price is asked for:

```
      0ms ->     0ms  Pricing          CRASHED   pricing-1 died without deregistering
      0ms ->     0ms  Client           LOOKUP    2 Pricing instance(s) offered
      5ms ->     5ms  Client           STALE     pricing-1 was on the list but is not answering
      5ms ->    15ms  pricing-2        OK        £449.99
```

Read the third line again. The registry offered two instances and the first one
was a lie. The shopper still got a price, because the client did the one thing
that makes discovery usable rather than merely correct: it tried the next name on
the list.

This is why the pattern is a *pair*. A registry without a client that copes with
stale entries fails every time an instance dies — which is precisely the situation
it was introduced to fix. In this project that coping is a loop and a caught
exception, and that is genuinely all it is:

```java
for (ServiceInstance instance : candidates) {
    try {
        return cluster.endpoint(instance).invoke(sku);
    } catch (ServiceUnavailableException e) {
        log.note("Client", "STALE", instance.instanceId()
                + " was on the list but is not answering");
        lastFailure = e;
    }
}
throw lastFailure;
```

Note the last line. When every offered instance is dead, the caller fails rather
than hanging or inventing a price. "Everything is down" is a real answer and the
client is allowed to give it.

## The Lease, And Why The Window Cannot Be Removed

Act four advances the clock a second at a time and asks the registry how many
instances it lists:

```
  immediately after the crash: 2 listed
  1s later: 2 listed
  2s later: 2 listed
  3s later: 2 listed
  4s later: 1 listed
```

For three seconds the registry names a dead process. On the fourth second its
lease expires unrenewed, it is dropped, and the list becomes true again.

That window is the price of the pattern, and it is worth being honest about it
because every real registry — Eureka, Consul, etcd, the endpoints controller in
Kubernetes — has one. You can make it shorter by heartbeating more often, and then
every instance spends more of its life telling a registry it is alive. You cannot
make it zero, because the only message that would close it is the one a crashed
process cannot send.

So the correct response is not to tune the lease until the problem disappears. It
is to build clients that expect to be handed a bad address occasionally, which is
the loop above.

## Client-Side And Server-Side Discovery

This project shows **client-side** discovery: the caller asks the registry and
chooses an instance itself. That makes the mechanism visible, which is why it is
the version to learn first.

The alternative is **server-side** discovery: the caller sends its request to one
fixed address — a load balancer, a Kubernetes service, an ingress — and that thing
does the looking up. The caller is simpler, because it is back to knowing one
address, but the registry has not gone away. It has moved behind something else,
and that something else is now on the critical path of every call.

Neither is more correct. The trade is fewer moving parts in the client against one
more piece of infrastructure that has to be running.

## What It Costs

**The registry is a new thing that has to be up.** If it goes down and callers
cannot look anything up, nothing can call anything. Real registries are therefore
run as a cluster, and real clients usually keep the last good answer as a fallback
— which reintroduces staleness on purpose, as the lesser of two evils.

**One more call per request.** In this project the lookup is free because the
registry is in-process. In a real system it is a network call, usually served from
a short-lived local cache for exactly that reason.

**Nothing is where you left it.** The address a request went to is no longer
something you can read out of a config file; it is a decision taken at runtime.
That is the whole point, and it means logs have to say which instance answered or
debugging becomes guesswork. `CallLog` in this project records the instance name
on every line for the same reason.

## When Not To Use It

If the service has exactly one instance, and it is started by hand, and it never
moves, a constant is the right answer and a registry is theatre. The pattern earns
its keep the moment the number of instances stops being one — or the moment
instances start being replaced rather than restarted, which in practice happens
the first time anybody deploys with zero downtime.

## What To Remember

A registry is a list of who is running, kept by the instances themselves rather
than by a person. Callers ask it every time. It is occasionally wrong, always for
a bounded period, and a client that tries the next name on the list turns that
from an outage into a line in a log.
