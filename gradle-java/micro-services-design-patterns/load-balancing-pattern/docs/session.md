# Session Guide — Client-Side Load Balancing

A one-hour session. Its shape is unusual for a patterns session in a specific way:
the naive version is the *fastest* thing in the project and every test written
against it passes. Getting a room to feel uncomfortable about working code is the
whole job of the first twenty minutes.

**Audience:** developers who know Java. No infrastructure experience assumed or
required.

**Format:** laptops open. Everything runs offline with a JDK.

## Learning Objectives

By the end, a participant can:

1. Say in one sentence what client-side load balancing is, without using the word
   "balancing".
2. Explain why `instances.get(0)` is not slow, does not fail, and still has to go.
3. Explain why an even split is not automatically a good split.
4. Say what least-latency balancing knows that a balancer in the middle of the
   network cannot know.
5. Describe the two ways client-side balancing goes wrong — herding, and clients not
   being able to see each other — and say why neither is a bug.
6. Say when to stop doing this in the client and put one balancer in front of the
   cluster instead.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check, and what this category is not |
| 0:05–0:15 | The problem: three instances, and a choice nobody noticed making |
| 0:15–0:24 | The pattern, from a row of supermarket tills |
| 0:24–0:34 | Code walkthrough: one interface, four implementations, an empty client |
| 0:34–0:44 | The half that is usually skipped: herding, and clients that cannot see each other |
| 0:44–0:56 | Exercises |
| 0:56–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check, And An Honest Warning

```bash
cd micro-services-design-patterns/load-balancing-pattern
./gradlew test
```

21 tests, green, in about a second.

Then say the honest thing up front, because it changes how people listen:

> There is no network in this project. No Docker, no Kubernetes, no service mesh, no
> cloud account. A service instance is an object with a latency attached, a remote
> call is a method call that charges simulated time, and the clock only moves when we
> move it. What you will learn is the shape of the pattern — what objects exist, who
> decides what, and the two places the idea breaks. What you will not learn is how to
> operate a real cluster. Both are real, and they are different.

## 0:05–0:15 — The Problem

Set the scene in words before showing any code, because the situation is the whole
difficulty:

> The Catalog service is busy, so it runs as three copies. Two of them answer in ten
> milliseconds. The third takes sixty, because it is older hardware nobody has got
> round to replacing. Ask any of the three for a product name and all three give the
> same answer. The checkout needs a product name. Which one does it ask?

Now run act one:

```bash
./gradlew run
```

```
1. Always the first on the list
    catalog-1   12 requests (100%)   10ms each
    catalog-2    0 requests ( 0%)   10ms each
    catalog-3    0 requests ( 0%)   60ms each
  12 requests took 120ms in total
```

**Do not explain this yet. Ask the room what is wrong with it.** Somebody will say
"it is slow". Point at the timing line: 120 milliseconds, and it will turn out to be
the fastest number in the entire session. Let that sit.

Then draw out the real costs, which are all outside the program:

- two machines are billed, monitored, patched, and idle
- the headroom the shop thinks it bought does not exist
- when `catalog-1` dies, *everything* dies, with two healthy machines metres away
- in a test environment there is one instance, so take-the-first and take-turns are
  indistinguishable

Land the sentence: **this is not a mistake somebody made. It is three lines nobody
thought of as a decision.**

## 0:15–0:24 — The Pattern, From A Row Of Tills

Six tills open, nobody directing anybody. You look along the row, see the shortest
queue, and join it. Three things:

- *You* chose — no member of staff assigned you.
- You chose with what you could see — queue length, not who the fastest cashier is.
- You will choose again next week. It is a decision, not a setting.

Then the other shop, the one with a member of staff at the head of all six queues.
Ask the room which is better. Steer towards: **that person can see all six queues and
every shopper, and no individual shopper can.** Say you are coming back to it, and
come back to it at 0:34.

Now the interface, on screen:

```java
public interface LoadBalancer {
    ServiceInstance choose(List<ServiceInstance> candidates);
    default void observed(ServiceInstance instance, long tookMillis) { }
    String name();
}
```

If the room has done `behavioural/strategy-pattern`, ask what this reminds them of
before telling them. It is Strategy — same structure, one method, interchangeable
implementations, a caller that does not ask which. What is new is the context: the
decision is about machines, it is remade on every request, and the chooser knows
something the network does not.

## 0:24–0:34 — Code Walkthrough

Go in this order, and keep it brisk — none of these classes is long.

**`CatalogClient.productName`** first, because it is the punchline.

```java
List<ServiceInstance> candidates = cluster.instances();
ServiceInstance chosen = balancer.choose(candidates);
long startedAt = clock.millis();
String name = cluster.call(chosen, sku);
balancer.observed(chosen, clock.millis() - startedAt);
```

Ask: where is the policy? There is none. That is the property Strategy buys.

**`RoundRobinBalancer`** — a counter and a modulus. Run act two:

```
    catalog-1    4 requests (33%)   catalog-2    4 requests (33%)   catalog-3    4 requests (33%)
  12 requests took 320ms in total
```

Even, and nearly three times act one. Say it plainly: **fair is not the same as
fast.** Round-robin sent a third of the traffic to the slowest machine the shop owns,
because it does not know what "slow" means.

**`LeastLatencyBalancer`** — the loop that tries every instance once before it starts
preferring. Ask why that loop is there. Answer: a balancer that trusts a measurement
it has not taken is round-robin with extra confidence.

Act three: 170ms, and the line that matters most in the whole demo —

```
  the client now believes: catalog-1 10ms, catalog-2 10ms, catalog-3 60ms
  it learned that on its own, from its own requests. Nothing told it.
```

Nobody configured those numbers, and a client in a different rack would have
measured different ones. **That is the entire argument for doing this in the
caller.**

**`observed` is a default method.** Ask why. Because round-robin does not care, and
should not be forced to write an empty method to say so.

## 0:34–0:44 — The Half That Is Usually Skipped

Two problems, neither of which is a bug. Spend real time here; this is the part
people remember.

### One: the favourite

Back to act three's numbers. `catalog-2` is *exactly as fast* as `catalog-1` — both
10ms — and it got one request out of twelve.

Ask what happened. Ties broke towards whoever was measured first, so the client found
a favourite and kept it. Harmless with one client.

Now ask the room to imagine a thousand clients in front of the same cluster. Let them
get there themselves: they all measure the same thing, all reach the same conclusion,
all crowd the same instance, make it slow, then all leave it together. The cluster
oscillates and no client did anything wrong.

**A learning balancer needs a random tie-break or it will herd.** This is the honest
price of the clever strategy, and a large part of why round-robin is still the
default.

### Two: a client cannot see the other clients

Act four. Two clients, each with its own round-robin balancer, two requests each:

```
    catalog-1    2 requests (50%)
    catalog-2    2 requests (50%)
    catalog-3    0 requests ( 0%)
```

Ask which client made the mistake. Let the silence do the work. **Neither.** Each
took perfect turns. The counter lives inside one client, so it counts one client's
requests, and two counters that each start at zero produce a pattern that is correct
twice and wrong collectively.

Then come back to the member of staff at the head of the six queues:

> A client-side balancer can only balance the traffic it can see, and it can only see
> its own. When that is not good enough, the answer is not a cleverer client. It is
> one balancer in front of the cluster that sees every request.

Say the unpopular part out loud: server-side balancing is simpler, easier to operate,
and the right answer more often than this pattern's fans admit. The price is one more
hop and one more thing to fail.

## 0:44–0:56 — Exercises

### Exercise 1 — Break least-latency's fairness (everyone)

Delete the "try each once" loop from `LeastLatencyBalancer.choose`, so it goes
straight to `min`. Run the tests.

`leastLatencyMeasuresBeforeItJudges` fails. Ask what the balancer now believes about
an instance it has never called, and why that is worse than knowing nothing.

### Exercise 2 — Give it a tie-break (everyone)

In `LeastLatencyBalancer`, when two instances are within a few milliseconds of each
other, pick between them at random. Re-run act three.

The total time should stay near 170ms, and `catalog-2` should now get a real share.
Discuss: what did you have to give up to get that? (Reproducibility — unless you seed
the random, which is exactly what `RandomBalancer` does and why.)

### Exercise 3 — Make the cluster even (discussion, then code)

Change `catalog-3`'s latency from 60 to 10 in `LoadBalancingDemo.clusterOf`, so all
three instances are identical. Run all four acts.

Least-latency's advantage evaporates. Ask the room what that tells them about when to
reach for the clever strategy at all.

### Exercise 4 — Stretch

Write a balancer that prefers the instance with the fewest requests *currently in
flight* rather than the best average. Discuss what it would need that the current
interface does not give it — a signal when a call *finishes*, not just how long it
took. That is a real design conversation, and it is where the interface's limits
show.

## 0:56–1:00 — Wrap-Up

Six sentences, spoken, no slides:

1. Several identical instances means a choice, remade on every request.
2. Taking the first one is fast, correct, and runs the shop on one machine out of
   three.
3. The choice goes behind a one-method interface, and the caller then holds no policy
   at all. That interface is Strategy.
4. Round-robin is fair. Fair is not fast.
5. Least-latency is fast because the *caller* measured the latency — the one thing
   only the caller can do.
6. A client can only balance what it can see. When that is not enough, put one
   balancer in front of the cluster.

## Facilitator Notes

**Do not rescue act one.** The temptation is to explain what is wrong with it
immediately. Let the room look at 120 milliseconds and be puzzled. The discomfort is
the teaching.

**Someone will say "just use a load balancer".** They are right, and it is the ending
of the session, not an interruption. Thank them, say you will get there at 0:34, and
hold the line — the pattern still has to be understood before its limits mean
anything.

**Someone will ask about health checks and retries.** Both are real and both are
other patterns in this category. Note them on the board and move on; a chosen
instance that does not answer is the retry pattern's problem.

**If the room is senior**, spend the saved time on Exercise 4. The question of what
signal an interface *fails* to provide is the most valuable half-hour in this project.

## Materials Checklist

- [ ] JDK 21 on every laptop, verified with `./gradlew test` before the session
- [ ] `./gradlew run` output on screen, all four acts, large enough to read
- [ ] `docs/animation.html` open in a browser tab for 0:15–0:24
- [ ] `docs/images/class-diagram.png` to hand for the walkthrough
- [ ] A whiteboard for the thousand-clients-herding sketch — it lands far better drawn
      than described
