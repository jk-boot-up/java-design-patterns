# Session Guide — Service Discovery Pattern

A one-hour session. It has an unusual shape for a patterns session, because half
the time goes on the pattern working and half goes on the pattern being wrong — and
the second half is the half people remember.

**Audience:** developers who know Java. No infrastructure experience assumed or
required.

**Format:** laptops open. Everything runs offline with a JDK.

## Learning Objectives

By the end, a participant can:

1. Say in one sentence what service discovery is, without using the word
   "discovery".
2. Explain why a hardcoded address is not a coding mistake, and still has to go.
3. Explain what a lease is and why registration expires.
4. Say why a registry is *always* wrong for a few seconds, and why no setting fixes
   that.
5. Point at the `catch` in `DiscoveringPricingClient` and say why the pattern does
   not work without it.
6. Say honestly what this project does not teach.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check, and what this category is not |
| 0:05–0:16 | The problem: a deployment takes checkout down |
| 0:16–0:26 | The pattern, from a taxi rank |
| 0:26–0:38 | Code walkthrough: register, heartbeat, look up |
| 0:38–0:46 | The half that is usually skipped: stale entries |
| 0:46–0:56 | Exercises |
| 0:56–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check, And An Honest Warning

```bash
cd micro-services-design-patterns/service-discovery-pattern
./gradlew test
```

19 tests, green, in about a second.

Then say the honest thing up front, because it changes how people listen:

> There is no network in this project. No Docker, no Consul, no Eureka, no
> Kubernetes. A service instance is a name in a set, a remote call is a method call
> that costs simulated time, and the clock only moves when we move it. What you
> will learn is the shape of the pattern — what objects exist, who tells whom what,
> and where it goes wrong. What you will not learn is how to operate a registry.
> Both of those are real, and they are different.

Getting this out of the way early stops the question that otherwise derails minute
thirty.

## 0:05–0:16 — The Problem

Don't show the registry. Show the obvious code, and show it sympathetically:

```java
private static final String PRICING_INSTANCE = "pricing-1";

public Money price(String sku) {
    return cluster.endpoint(pinned).invoke(sku);
}
```

Ask the room what is wrong with it. Some will say "hardcoded values are bad",
which is a slogan rather than an answer. Push back: **when the shop had one
Pricing instance, this was exactly the right amount of code.** It is fast, it has
no dependencies, it cannot be misconfigured, and every test written against it
passes.

Then run act one:

```
      0ms ->    10ms  pricing-1        OK        £449.99
     10ms ->    10ms  Registry         DEREGISTER pricing-1 left cleanly
  after the deploy:  pricing-1 did not answer
```

Say the next sentence slowly, because it is the whole motivation:

> Checkout is down. Not slow — down. And `pricing-2` and `pricing-3` are up,
> healthy, idle, in the same rack. The client cannot reach either of them, because
> a constant is not a question you can ask again later.

Then name the real diagnosis, which is not "hardcoding is bad":

> The set of running instances changes several times a day. The source code of the
> callers changes once a fortnight. A fast-moving fact has been stored inside a
> slow-moving artefact.

That framing also kills the first suggestion you will get — "put it in a properties
file" — before anyone has to argue about it. A file moves the fact one step, and a
human still has to edit it, and that human still has to notice.

## 0:16–0:26 — The Pattern

Do the taxi rank out loud, before any code:

> One way to get a taxi is to keep Dave's mobile number. Works beautifully until
> the evening Dave is off, and then keeps not working, while eleven other drivers
> in town would happily take you. The other way is a taxi rank. You know no
> driver's name. Drivers join when they start a shift and leave when they finish,
> and none of that requires you to learn anything.

Then the three rules, one sentence each: an instance **registers** when it starts, it
**heartbeats** while it lives, and it **deregisters** when it shuts down politely.
And on the other side, the caller **asks, every time**.

Now run act two and read the timeline out loud — the lookup count is the story:

```
  LOOKUP    3 Pricing instance(s) offered
  DEREGISTER pricing-1 left cleanly
  LOOKUP    2 Pricing instance(s) offered
  REGISTER  pricing-4 (10.0.1.148:8084)
  LOOKUP    3 Pricing instance(s) offered
```

Three, then two, then three. A deployment and a scale-up happened, and the last
line of the act is the point: *no code changed, no restart, no configuration edit.*

## 0:26–0:38 — Code Walkthrough

Read `ServiceRegistry` and say plainly that most of it is boring. `register` is a
map put. `deregister` is a map remove. `heartbeat` is a map put with a new
timestamp. If the class stopped there it would be a phone book.

Then stop on the one line that makes it a registry:

```java
if (clock.millis() - lease.lastHeartbeatAt() > LEASE_MILLIS) {
```

Ask the room why a registration expires at all. Work towards the answer rather than
giving it: **a process that crashes cannot send a message saying it has crashed.**
The registry cannot detect death. It can only notice silence, and silence is the
one thing a dead process is reliably good at.

Two details worth naming while you are there:

- Expiry is **lazy** — it happens inside `instances(...)`, when somebody asks.
  There is no background thread. Several real registries behave this way too, and
  it means a dead entry costs nothing until it is looked at.
- `heartbeat` on an unknown id does **nothing**, quietly. There is a test for it.
  A resurrection-by-heartbeat would let a deregistered instance walk back onto the
  list.

Then `DiscoveringPricingClient.price`, and ask the room to spot the two separate
behaviours in one short method. The first is discovery: ask, then call. The second
is the loop.

## 0:38–0:46 — The Half That Is Usually Skipped

Run act three:

```
      0ms ->     0ms  Pricing          CRASHED   pricing-1 died without deregistering
      0ms ->     0ms  Client           LOOKUP    2 Pricing instance(s) offered
      5ms ->     5ms  Client           STALE     pricing-1 was on the list but is not answering
      5ms ->    15ms  pricing-2        OK        £449.99
```

Read line two out loud twice. **The registry offered two instances and the first
one was a lie.** Then ask the room what it cost: five milliseconds, and a line in a
log. Without the loop it would have cost an outage — the same outage act one
showed, from the pattern that was supposed to have fixed it.

This is the sentence to leave on the screen:

> A registry without a client that copes with stale entries fails every time an
> instance dies, which is precisely the situation it was introduced to fix.

Then run act four, which has no client in it at all:

```
  immediately after the crash: 2 listed
  1s later: 2 listed
  2s later: 2 listed
  3s later: 2 listed
  4s later: 1 listed
```

Three seconds of a registry confidently naming a dead process. Ask: how do we make
that window shorter? (Heartbeat more often.) How do we make it zero? Let the room
try. The answer is that you cannot, because the only message that would close it is
the one a crashed process cannot send. Every real registry — Eureka, Consul, etcd,
the endpoints controller in Kubernetes — has this window.

## 0:46–0:56 — Exercises

### Exercise 1 — Delete the loop (everyone)

In `DiscoveringPricingClient.price`, replace the loop with a call to the first
candidate only. Run the tests. Note *which* tests fail and which still pass — the
deployment tests are all fine. Only the crash tests break. That is exactly the trap
a real system falls into, because deployments are common in testing and crashes are
not.

### Exercise 2 — Make the lease shorter (everyone)

Set `LEASE_MILLIS` to `500`. One test fails —
`aLeaseIsStillGoodOnItsLastMillisecond` — which is the test telling you the
boundary moved, correctly. Then ask what the change would cost in production:
heartbeats from every instance six times more often, forever, in exchange for a
shorter lie.

### Exercise 3 — Cache the lookup (discussion, then code)

Make the client look up once in the constructor and reuse the list.
`theRegistryIsConsultedOnEveryCallRatherThanOnce` fails. Ask whether the test is
being pedantic.

Expected discussion: a client that caches for the life of the process has
reinvented the hardcoded address with extra steps. Real clients *do* cache — for a
second or two, with the loop as the safety net. The design question is not
"cache or not" but "for how long, and what happens when the cache is wrong".

### Exercise 4 — Stretch

Add round-robin: keep an index in the client and start the loop at a different
instance each call. Then look at `callsTo(...)` in `PricingCluster` and assert the
spread. You have just written client-side load balancing, which is the next project
in this category.

## 0:56–1:00 — Wrap-Up

One sentence: **instances put themselves on a list, the list forgets anyone who
goes quiet, callers ask it every time — and callers try the next name, because the
list is sometimes wrong.**

Then the honest closer, again: you now know what discovery is and could write a
registry. You have not operated one. Point at
[`service-discovery-pattern-explained.md`](service-discovery-pattern-explained.md)
for the long form, including the client-side versus server-side distinction, which
this session deliberately skipped.

## Facilitator Notes

- **Defend the hardcoded client.** If the room writes it off as bad code in minute
  six, the rest of the session has no tension. It is good code that a changing
  world made wrong.
- **Act three is the emotional core, not act one.** Act one motivates the pattern;
  act three motivates doing the pattern *properly*. Budget time accordingly.
- **Somebody will suggest health checks — the registry polling the instances.**
  Good sign. Ask where the registry gets the list of who to poll. That is the
  original problem, one level up.
- **Somebody will say "DNS already does this".** Also nearly right. DNS is a
  registry with caching and a TTL, which is a lease with a different name; the
  difference is that DNS gives you one answer and does not help you try the next.
- **Do not let Exercise 3 become a lecture on caching.** The point is the trade,
  not the implementation.

## Materials Checklist

- [ ] JDK 21 on every laptop, verified before the session
- [ ] `./gradlew test` and `./gradlew run` both run once on the presenting machine
- [ ] Act one and act three output ready to show side by side
- [ ] `docs/animation.html` open in a browser tab
- [ ] The `LEASE_MILLIS` comparison line on a slide of its own
