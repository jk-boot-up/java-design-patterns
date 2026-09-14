# Problem Statement

## The Scenario

The shop's Catalog service — the one that knows a product's name — is busy enough
that it runs as three copies of itself. Three machines, the same program started
three times, all answering identically. Ask any of them for `SKU-ESPRESSO` and all
three say "Espresso Machine".

They are not, however, equally quick. Two of them answer in 10 milliseconds. The
third takes 60, because it is older hardware that nobody has got round to
replacing. Real clusters look like this far more often than the diagrams admit: a
mix of generations, a machine that was cheap, a container sharing a host with
something noisy.

The previous pattern, service discovery, has already solved the question of *what
exists*. The checkout asks a registry and is handed a list of three names. So the
hard part is apparently over.

It is not. Being handed a list of three raises a question that a list of one never
does: **which one do I ask?**

## Attempt One: Take The First One

The list arrives in some order. Take the first thing in it.

```java
ServiceInstance chosen = candidates.get(0);
```

Nobody writes this as a decision. It is what you get by reaching for the list,
taking what is nearest, and moving on to the interesting part of the feature. It is
`FirstInstanceBalancer` in this project, and it is three lines long.

Now run the shop through it. Twelve requests:

```
    catalog-1   12 requests (100%)   10ms each
    catalog-2    0 requests ( 0%)   10ms each
    catalog-3    0 requests ( 0%)   60ms each
  12 requests took 120ms in total
```

## Why That Hurts

Read the timing line again before anything else: **120 milliseconds**. That is the
fastest number this project produces. Faster than round-robin. Faster than the
clever learning balancer. Taking the first instance every time is not slow.

That is precisely why it survives. There is no error, no timeout, no exception, no
red line in a log. Every request gets the right product name promptly. Every test
you would think to write against it passes — and in this project, every test in
`FirstInstanceBalancerTest` genuinely does pass, which is the point of the file
existing.

The costs are all somewhere a test does not look:

- **The shop is paying for three instances and using one.** Two machines are billed
  monthly, monitored, patched, and idle.
- **There is no headroom.** The capacity the shop believes it bought is not
  available. `catalog-1` is carrying all of it.
- **When `catalog-1` falls over it takes every request with it.** Not a third of
  them. All of them, while two healthy machines sit three metres away doing
  nothing — which should feel familiar from the previous pattern.
- **It is invisible in testing.** In a test environment there is one instance, and
  the first one is the only one. Take-the-first and take-turns behave identically
  there, so nothing in development can distinguish a bug from a policy.

The failure mode is not an outage. It is a bill, and a machine that falls over
under a load the other two could comfortably have absorbed.

## The Question This Project Answers

Once you accept that the choice has to be made deliberately, the question is not
*whether* to spread the requests out. It is what "spread out" ought to mean, and
there is more than one honest answer:

- Take turns, so every instance gets the same number of requests. Perfectly fair.
- Prefer the instances that have been fastest, so the shop's customers wait less.
  Not fair at all, and quicker.
- Pick at random, keeping nothing, so ten thousand clients starting at once do not
  all begin with the same machine.

These are not refinements of each other. Fair and fast pull in opposite directions
here, because one of the three machines is genuinely slower, and the fair strategy
has no way of knowing that.

## The Goal

Build a caller that makes the choice explicitly, on every request, with the choice
itself pulled out into something interchangeable — so that swapping *take turns*
for *prefer the fast ones* changes no line of the caller. Then measure all of them
against the same twelve requests and the same three instances, and say out loud
what each one costs.

And then be honest about the limit of the whole idea: a balancer living inside one
caller can only balance the traffic that caller can see. Two well-behaved clients,
each taking perfect turns, can between them leave a machine completely idle. When
that matters, the answer is not a cleverer client — it is one balancer in front of
the cluster that sees every request.
