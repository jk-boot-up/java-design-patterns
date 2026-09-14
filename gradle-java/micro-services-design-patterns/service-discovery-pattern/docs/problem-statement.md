# Problem Statement

## The Scenario

The shop's Pricing service is busy enough that one copy of it is not sensible any
more, so it runs as three: `pricing-1`, `pricing-2` and `pricing-3`. They are the
same program started three times. Any of them can answer any question, and they
all give the same answer, because the price of an espresso machine does not
depend on which machine you happen to ask.

The checkout needs a price. So it calls Pricing.

Which raises a question that has no interesting answer in a single-process
program and no easy one here: **which of the three does it call, and how does it
know?**

## Attempt One: Write The Address Down

```java
private static final String PRICING_INSTANCE = "pricing-1";

public Money price(String sku) {
    return cluster.endpoint(pinned).invoke(sku);
}
```

That is `HardcodedPricingClient` in this project, and it deserves to be taken
seriously rather than mocked. When the shop had one Pricing instance, this was
the correct amount of code. It is fast, it has no dependencies, it cannot be
misconfigured, and every test written against it passes.

It works perfectly right up until the set of instances changes.

## Why That Hurts

**A routine deployment is an outage.** Run the first act of the demo. `pricing-1`
is stopped, politely, the way a rolling deployment stops things:

```
      0ms ->    10ms  pricing-1        OK        £449.99
     10ms ->    10ms  Registry         DEREGISTER pricing-1 left cleanly
  after the deploy:  pricing-1 did not answer
```

Two healthy instances, `pricing-2` and `pricing-3`, are sitting idle at that
moment. The client cannot use either of them. It was told about one machine and
it has no way of finding out about another — not because somebody wrote bad code,
but because a constant is not a question you can ask again later.

**Scaling up buys you nothing.** Start a fourth instance to cope with a busy
Friday and no existing caller will ever send it anything. The new capacity exists
and is unreachable, which is the most expensive kind of capacity there is.

**The address is in the wrong place.** The set of running instances changes
several times a day — every deploy, every autoscaling event, every crash. The
source code of the callers changes about once a fortnight. Putting a fact that
moves quickly inside an artefact that moves slowly is the whole of the problem,
and no amount of care in the client can fix it.

**Configuration files only move the problem.** Reading the address from a
properties file instead of a constant means the client can be pointed at a
different machine without recompiling — but somebody still has to edit the file
and restart the process, and that somebody has to notice in the first place. The
list is still written by a human, at a moment unrelated to the instance actually
starting or stopping.

## The Question This Project Answers

**How does a caller reach a service whose instances come and go, without anybody
editing the caller?**

And the harder half of the same question: **what should the caller do when the
answer it is given turns out to be wrong?** Because it will be. A list of who is
running cannot know that a process died a second ago.

## The Goal

Build a registry and a discovering client such that:

1. an instance is reachable **as soon as it starts**, with no configuration change
   anywhere;
2. a polite shutdown takes an instance off the list **immediately**, so a rolling
   deployment is invisible to callers;
3. a caller that is handed a **stale** address — one that belonged to a process
   that has since crashed — still answers, by trying the next instance on the
   list;
4. a crashed instance is removed automatically once its **lease** expires, without
   anyone intervening;
5. the caller asks the registry **on every call**, so its picture of the world is
   never older than one request;
6. and the demo shows the **window** during which the registry is confidently
   wrong, rather than pretending there isn't one.

Point six matters more than it looks. The few seconds between a crash and a lease
expiring are the honest cost of this pattern. A shorter lease does not remove that
window; it just trades it for more heartbeat traffic.
