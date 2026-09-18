# The Problem

**A sentence the configuration language has no words for.**

This is a follow-on project. The pattern it is built on — Sidecar — belongs to
[`sidecar-pattern`](../../sidecar-pattern), and that is the one to read first. What
happens here only makes sense if you already know why the retry code was taken out of
the service and put in a proxy next door.

Assume you know that, and the problem starts one step later.

---

## Where the last project left off

Checkout takes payments. The code that knows how to talk to the payment provider is not
in it any more; it moved next door into a proxy, and everything the shop had decided
about that provider — how many times to try, when to give up, what certificate to
present, what to call the counters — is written down once, in one configuration file,
which every proxy in the shop reads.

The service's entire configuration for reaching the provider is one line:

```
http://localhost:8081/pay
```

An address on its own machine. Not a provider hostname, not a certificate, not a retry
count. Whatever is listening there answers, and checkout has no way to find out what it
is.

Today it is nginx. Twenty-two lines of configuration in a container somebody else wrote,
tested, hardened and has been patching for twenty years. That was a good decision and
this project does not undo it.

---

## The letter from the provider

In March the provider wrote to every merchant asking for two things:

> At most three attempts per payment, **and wait properly between them.**

The shop agreed to both. The configuration says three attempts. Everybody went home.

Read the second half of that sentence again, because it is the whole problem.

---

## What happens the next time the provider wobbles

The provider has a bad three hundred milliseconds. Nothing is broken and nobody needs
paging — it declines everything, and then it is fine again.

A customer buys a coffee maker for £47.99. The proxy makes its three allowed attempts.
Here is what the provider itself recorded, with the times taken at its end rather than
the shop's:

```
  attempt at    1ms   declined
  attempt at    2ms   declined
  attempt at    3ms   declined
  3 attempts, first to last: 2ms
```

Three attempts, spanning two milliseconds, against a provider that did not recover until
three hundred. Every one of them landed inside the bad window, because they were all made
inside the bad window. The shop spent its entire allowance for that payment before the
provider had time to get better, and the customer got nothing.

**The half of the agreement that limits the shop was kept. The half that would have
helped was not.**

---

## Nobody wrote a bug

This is the part that makes it a design problem rather than a defect.

nginx retries by moving to the **next server in its upstream group**. That is why §41's
configuration lists the provider's address three times — three entries is how "up to
three attempts" is spelled when the upstream is a single address. Moving to the next
server happens immediately.

That was a good decision for the case nginx was built for. In a pool of machines, the
next machine is a *different* machine and is probably fine, so waiting first would only
make every request slower for no reason. It stops being a good decision the moment every
entry in the pool is the one address that is currently unwell, which is exactly the
shape of a sidecar in front of a single supplier.

So there is nothing to fix. There is no directive anywhere in nginx's http proxy module
that says "wait two hundred milliseconds before the next attempt". The sentence the
provider asked for does not exist in the language the shop's policy is written in.

---

## The three ways out, and why two of them are bad

**Put the waiting back in the service.** This undoes the entire previous project. Four
services, four copies of the waiting, and the next policy change lands in three of them.
That was the problem §41 existed to solve.

**Script the proxy.** nginx will run Lua, and njs will run JavaScript, and either one can
express a delay. But then you are writing code inside a proxy you chose *because* it was
configured rather than programmed, in a language most of your team does not use, with
worse tooling and nowhere obvious to put a test.

**Put a different proxy on the port.** Which is this project.

---

## Why the third option exists at all

Only because of a decision made in the last project, and it is worth saying plainly
because it is easy to walk past.

The contract between the service and its proxy is **an address**. Not a library, not a
language, not a shared build, not a version of anything. The service sends an HTTP
request to `localhost:8081` and something answers. Nothing about that is Java, and
nothing about it is nginx.

That is a far weaker promise than a library dependency, and it is exactly as sufficient.
Replace what is bound to the port and the service is already talking to the new thing —
without being told, rebuilt, restarted, or paused.

§41 made that claim, in one sentence, and moved on. **A claim is not a demonstration.**

---

## What this project has to deliver

1. **The same three attempts, spread out.** Not more attempts — the provider's allowance
   is not the thing to renegotiate. The same three, arriving far enough apart that the
   last one lands after the wobble has passed.

2. **The service untouched.** Not rebuilt, not restarted, not told, and not modified.
   Proved by identity rather than by behaviour, because a service that merely *behaves*
   the same afterwards is a service somebody carefully rebuilt.

3. **The claim demonstrated.** Two proxies, two languages, one port, and a service whose
   source file is byte-for-byte the same in both runs.

4. **The bill, in full.** Twenty-two lines of somebody else's configuration becoming
   forty lines of your own code is a trade, and most of the time it is a bad one. A
   project that showed only the win would be an advertisement for writing your own
   proxy, which is very rarely the right thing to do.

The rule this lands on is narrow, and it is the thing to remember when the demo has
faded: **swap the proxy when the thing you need cannot be said in the configuration
language at all.** Not when it is awkward. Not when you would rather write Java. Here the
missing sentence was the difference between a payment going through and a payment
failing, and that clears the bar. Very little else does.
