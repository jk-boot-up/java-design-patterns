# Two-Phase Termination, Explained

## The pattern in one sentence

Two-phase termination stops a thread in two steps: first it is asked to stop, and it finishes what it is doing and tidies up, then the caller waits for it to end, for a limited time.

## The six acts

### Pull The Plug

The shop closes the ledger while order one is half written. Only line one was written. The order is left half written.

```
  the shop shuts down and closes the ledger while ORD-1 is half written. lines written: [ORD-1 line 1].
  left with an order half written: true. the order has a line 1 and no line 2 or 3.
```

### Ask It To Stop, And Let It Finish

Stop is requested while order one is half written and order two is waiting. The worker finishes order one, all three lines, starts nothing else, and ends. Nothing is half written.

```
  stop requested while ORD-1 is half written, and ORD-2 is waiting.
  the worker ended: true. orders finished: 1. lines: 3, all of ORD-1's, none of ORD-2's.
  left with an order half written: false.
```

### A Worker That Is Asleep

A stop request that only sets a flag does nothing to a worker waiting for an order: it is still waiting. With an interrupt to wake it, the worker ends.

```
  a stop request that only sets a flag, to a worker waiting for an order: false, still WAITING.
  the same request, with an interrupt to wake it: true.
```

### Tidy Up On The Way Out

The worker is interrupted while waiting, and its cleanup still runs, because it is in a finally block.

```
  the worker was interrupted while waiting. did its cleanup run: true.
  the cleanup is in a finally block, so it runs however the worker ends.
```

### A Worker That Will Not Stop

The worker is stuck in something that ignores the request. After two hundred milliseconds it has not ended, and is still alive. Phase two has a time limit, and what comes next is a decision, because Java gives no safe way to force a thread to stop.

```
  the worker is stuck in something that ignores the request. after waiting 200 ms: ended false, alive true.
  phase two has a time limit. what happens next is a decision: report it, wait longer, or restart the process. Java gives no safe way to force a thread to stop.
```

### The Bill

Stopped with five orders still waiting: one finished, five pending. Those five were accepted from customers and not done. A stop needs a policy, and shutting down took as long as the order in progress.

```
  stopped with 5 orders still waiting: finished 1, pending 5.
  those 5 orders were accepted from customers and have not been done. a stop needs a policy: finish them first, hand them to another worker, or save them.
  and shutting down took as long as the order in progress. stopping is never instant.
```

## The verdict

Stop threads in two phases: ask, then wait with a limit. Let a worker finish the unit of work it is in, and check for the request between units. Wake it if it may be waiting. Put cleanup in a finally block. Decide what happens to the queued work, and to a worker that does not end. Never force-stop a thread.

## How to recognise this in code you did not write

- A `volatile boolean stopRequested` checked at the top of a loop.
- `ExecutorService.shutdown()` followed by `awaitTermination(timeout, unit)`.
- `Thread.interrupt()` followed by `Thread.join(timeout)`.
- Shutdown hooks and graceful-shutdown settings in servers and frameworks.

## Where you have already met this

`ExecutorService`'s shutdown and awaitTermination, Spring's graceful shutdown, and Kubernetes sending a stop signal and then a kill after a grace period.

## When this is too much

For a thread that holds no state and whose work can be repeated, stopping at once is fine, and a daemon thread can simply be left. The pattern matters where a stop can damage something.
