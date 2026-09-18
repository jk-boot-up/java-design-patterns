# Sidecar, With the Proxy Written in Java

**One job: change the thing next door without touching the thing it stands next to.**

---

## Read the other one first

This project builds on [`sidecar-pattern`](../../sidecar-pattern). That project explains
what a sidecar is, why the retry code left the service, and what a second process costs.
This one assumes all of it and spends its time on a single question that project left
open.

If you have not read it, read it. Nothing below re-teaches it.

---

## An analogy, and then we go back to the shop

Think about the plug on a kettle.

The kettle does not know anything about the electricity supply. It does not know the
voltage, the frequency, which wire is live, or what the fuse in the plug is rated at. It
knows there is a socket in the wall, and that pushing a plug into it makes the kettle
work. Everything about the supply lives in the plug, the fuse and the wiring — not in the
kettle.

Now somebody discovers the fuse in the plug is the wrong rating. They change the fuse.
They do not open the kettle, they do not send it back to the factory, and the kettle is
not switched off for longer than it takes to pull the plug out and push it back in. The
kettle never knew a fuse existed.

That works because the contract between the kettle and the electricity is **a shape of
socket**, not a wiring diagram. Any plug that fits the socket will do.

The shop's checkout service is the kettle. The proxy next door is the plug. And the
contract between them is an address — `localhost:8081` — which is a socket with a shape.
This project changes the plug.

---

## The gap the last project shipped with

In the previous project the payment provider wrote to every merchant asking for two
things: at most three attempts per payment, **and wait properly between them.**

The shop's proxy is nginx. nginx can say the first of those. It cannot say the second.

The reason is worth understanding rather than resenting. nginx does not have a "retry"
feature in the sense you are probably imagining. What it has is an **upstream group** —
a list of servers — and a rule that says "if this one fails, try the next one in the
list". The shop's configuration lists the provider's address three times, and three
entries is how you spell "up to three attempts" when the upstream is a single address.
Moving to the next entry happens immediately, because in the case nginx was designed for
the next entry is a *different machine* and is probably fine. Waiting first would make
every request slower for nothing.

That reasoning stops working when every entry in the list is the same address, and that
address is the one having a bad minute. Three attempts at the same unwell thing, made
inside the same three milliseconds, are three attempts that will all get the same answer.

There is no directive to fix it with. The sentence does not exist in the language.

---

## What that costs, in numbers

The provider has a bad three hundred milliseconds. A customer buys a coffee maker for
£47.99. Here is what the provider recorded, at its own end:

```
  attempt at    1ms   declined
  attempt at    2ms   declined
  attempt at    3ms   declined
  3 attempts, first to last: 2ms
```

Payment failed. The whole allowance spent in two milliseconds against a provider that
recovered at three hundred.

And here is the same payment, the same wobble, the same allowance of three attempts,
through a proxy that waits:

```
  attempt at    1ms   declined
  attempt at  202ms   declined
  attempt at  603ms   charged
  3 attempts, first to last: 602ms
```

Read those two blocks side by side and notice what is **not** different. Three attempts
in both. The provider's allowance is untouched; the shop is not being greedier and the
change costs the provider nothing at all. The only thing that changed is when the third
attempt arrives — and by six hundred milliseconds the provider is well again.

**The spacing was the difference between a customer walking away and a coffee maker
being sold.**

---

## The swap

Somebody writes a proxy. It is about forty lines of Java, and the whole of it is this
shape: read the policy, try, catch, wait, double the wait, try again.

```java
long backoff = policy.firstBackoffMillis();
for (int attempt = 1; attempt <= policy.maxAttempts(); attempt++) {
    clock.waitFor(HOP_MILLIS);
    try {
        return receiptFrom(provider.charge(besideService, payment, clock.now()));
    } catch (PaymentFailed failure) {
        if (failure.reason() == PaymentFailed.Reason.RATE_LIMITED) {
            break;
        }
        if (attempt < policy.maxAttempts()) {
            clock.waitFor(backoff);
            backoff *= 2;
        }
    }
}
```

Compare that with the nginx proxy's loop in this same project. **They are the same loop
with one statement missing**, and the statement is not missing because whoever wrote the
nginx version forgot it. It is missing because there was nothing to write it with.

Now put the new one on the port:

```java
port.install(java);
```

That is the swap. Look at what that method does not take: no reference to the service,
nothing it could use to notify one, and nothing it could use to restart one. There is no
such parameter because there is no such step.

Here is the demo, before and after:

```
  before the swap, listening on localhost:8081: nginx
  checkout is on start number:       1
  checkout's configured endpoint:    http://localhost:8081/pay

  after the swap, listening:         java-proxy
  checkout is on start number:       1
  checkout's configured endpoint:    http://localhost:8081/pay
  payments services ever started:    1
```

The start number did not move, and that is not the demo being careful. There is exactly
one place in the entire program where a payments service is constructed — in `main`,
before Act 1 — and a swap is not a place where another one could go. A test reads the
source with its comments stripped and counts the constructions, so that stays true.

---

## Why this is the demonstration and not just a nicer number

The previous project claimed that a sidecar is language-independent: the proxy may be
written in a language nobody on your team knows, and the service will not care.

That claim was true and it was unsupported. Every line of evidence in that project was
Java talking to Java.

Here there are two proxies. One is configured in nginx's configuration language; the
other is written in Java. They go on the same port, beside the same service, and they are
handed **the same policy object**. The service's source file is byte-for-byte identical
in both runs. That is not a claim about language independence. It is language
independence, happening.

---

## The bill, which is longer than the benefit

A pattern taught without its costs is an advertisement, and the honest accounting here
mostly argues against doing it.

**Twenty-two lines of somebody else's configuration became forty lines of your own
code.** That code is now yours to test, to review, to keep working on the next JDK, and
to fix at three in the morning. Nobody is patching it for you while you sleep.

**Everything nginx brought for free is gone until you write it.** TLS termination. A
structured access log with a format every service in the shop shares. Connection pooling.
Header handling nobody has to think about. And twenty years of somebody answering
security advisories before you have heard of them. The forty-line version has none of
that, and a forty-line version that grows all of it back is not forty lines any more.

**A JVM sits beside every service where a few megabytes of nginx used to sit.** Multiply
by the number of services, then look at what that costs on the machines you actually rent.

**And nothing now stops the next person putting the shop's refund rules in the proxy.**
A configuration language is a fence: there is no way to express "refunds are not allowed
after ninety days" in an nginx `location` block, so nobody ever tries. Java will happily
let them, and a business rule hidden in a proxy is a business rule no developer will
think to look for.

---

## The window in the middle

There is one more cost, and it is the one that will actually page somebody.

A swap is not instant. The old proxy stops and the new one starts, and in between there
is a moment when **nothing is listening on the port at all**. A payment that arrives in
that moment does not fail slowly, it fails immediately — and the service has nothing to
fall back on, because its retry code was deleted in the last project, on purpose.

The demo shows it rather than skipping over it:

```
  The provider is healthy. The network is healthy. Checkout is
  healthy. A customer pays for a £31.50 kettle:
    ORD-4419     £31.50    NOT PAID
      connection refused to localhost:8081 — nothing is listening

  attempts that reached the provider: 0
```

A healthy provider, a healthy network, a healthy service, and zero attempts reached
anybody. The request never left the machine.

So a real swap is not one line; it is a rollout. Start the new proxy before stopping the
old one. Move one service at a time. And keep the old proxy installable — because the
honest reason to be able to swap forwards is to be able to swap back.

---

## The rule to take away

**Swap the proxy when the thing you need cannot be said in the configuration language at
all.**

Not when it is awkward. Not when the config file has grown ugly. Not when you would
rather write Java, which you would, because everybody would.

Here the missing sentence was the difference between a payment going through and a
payment failing, and that clears the bar. Very little else does. Most of the time the
right answer is to keep nginx, accept the gap, and spend the afternoon on something that
matters more.

What is worth keeping either way is that **the choice was available**. Because the
service talks to an address rather than to a library, swapping the proxy was a decision
somebody could make on a Tuesday afternoon — and swapping it back is the same decision in
the other order. That optionality is what the previous project actually bought, and this
project is what it looks like when somebody finally spends it.

---

## Where you have already met this

- **A service mesh changing its data plane.** Istio moved from a mesh built on Envoy to
  offering an alternative lighter proxy per node. Every service in the mesh kept talking
  to the same local address throughout.
- **Swapping a logging or metrics agent.** The agent beside your service is replaced with
  a different vendor's agent and no application is rebuilt, because the application writes
  to a local socket and does not know who is reading it.
- **Changing a reverse proxy in front of a website.** Apache to nginx, nginx to Caddy or
  HAProxy. The application behind it is not recompiled; something else starts answering
  the port.

Every one of those is this project at a different scale: the contract was an address, so
the thing on the other end of it turned out to be replaceable.

---

## What this simulation does not show

**Tier 1 has no network.** The port is an object with something bound to it, and both
proxies are objects. There is no socket, no TLS handshake, no serialisation and no
process boundary. For the real second process, see [`../real/`](../real) — and read
§41's Tier 2 first, because this one reuses its service image unchanged.

**Tier 1 cannot show the swap's timing.** `LocalPort.vacate()` makes the window visible
but not realistic. A real swap's window depends on how fast the new proxy accepts
connections, whether the old one drains in-flight requests, and what your orchestrator
does in between. Compose and Kubernetes each answer that differently, and §43 is where
the Kubernetes answer lives.

**And Tier 2 still does not show a fleet.** Two containers on one laptop are not a
network that partitions, a control plane, or a rollout across two hundred services where
half of them are on the new proxy for an hour. Every honest thing this pattern is hard at
is hard at a scale neither tier reaches.
