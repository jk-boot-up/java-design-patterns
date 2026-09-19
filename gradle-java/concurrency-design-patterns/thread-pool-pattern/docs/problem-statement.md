# Problem Statement

## The scenario, continued from Producer–Consumer

Orders arrive at checkout and need packing. §46 fixed the handoff between
the two with a bounded queue and exactly one packer thread. That packer
thread is now the bottleneck: one thread, one order at a time, no matter
how many are queued behind it. This project is about the packing *team* —
more than one packer — and the two ways to get there, one of which is the
naive version this whole category keeps meeting in a new costume.

## The naive version, in two parts

### Part one: a thread per order, again

`ThreadPerOrderPacking` is §46's naive version, unchanged in shape: every
order gets a brand new thread. It is the same failure, seen from the
packing team's side this time — nothing anywhere caps how many packers
exist at once.

```
ONE. A thread per order — the same cost §46 measured, from the team's side.
  created 2,000 real threads in 98.1ms (49.1 microseconds each)
  every thread is live and holding a stack until its order is packed —
  nothing here caps how many pile up if orders outpace packing.
```

### Part two: a fixed number of workers, with a queue nobody chose

The fix most people reach for next looks right: `Executors.newFixedThreadPool(2)`
really does cap the number of worker threads at two. What it hands those
two workers to pull from is an unbounded `LinkedBlockingQueue`, built in
behind the factory method with no argument anywhere to change it.
Submitting never blocks and never rejects — the backlog just grows,
silently, until it is a heap dump instead of a decision.

```
TWO. A fixed pool with the queue nobody chose — the default trap.
  2 workers, both provably busy; 500 more orders submitted
  Executors.newFixedThreadPool never blocked and never rejected once
  backlog waiting behind the 2 busy workers: 500
  nothing anywhere would have told you that number until you asked.
```

## What the pattern must deliver

A **fixed, small number of worker threads, created once and reused,
pulling from a queue whose capacity is also chosen on purpose.** Two
bounds, both explicit: how many orders can be packed at once, and how many
more can be waiting before a submission is refused outright. This project
also has to show the deadlock a fixed pool can reach at *any* size — a
task that submits a second task to its own pool and waits for it, with no
worker left free to run the second one — and has to say plainly what Java
21's virtual threads do and do not change about any of this.
