# Problem Statement

## The scenario

Inventory updates arrive from several places at once. Checkout reserves
stock. Returns add it back. A back-office import corrects the count, and
that import is slow.

## The naive version: a monitor

The monitor from [§50](../../monitor-object-pattern) is correct. Every
call takes the lock, so no update is lost. But a caller waits while
another holds the lock.

```
ONE. A monitor — the checkout thread waits on a slow import.
  the import holds the lock. the checkout thread state: WAITING
  a customer is waiting behind a back-office import.
```

A customer stands behind a back-office job.

## What this project must deliver

An inventory whose callers never wait for its work. A call should return at
once with a promise of the answer. And the object should need no lock at
all. It then has to say what that costs: a mailbox that can back up,
errors that arrive later and from another thread, and a single worker that
caps throughput.

## This project is an assembly

Nothing here is new. The parts came from four earlier projects, and this
one links to them rather than teaching them again.

| Part | Where it was taught |
| --- | --- |
| A queue of messages | [§46 Producer–Consumer](../../producer-consumer-pattern) |
| A thread that works through it | [§47 Thread Pool](../../thread-pool-pattern) |
| A future for the answer | [§48 Future/Promise](../../future-promise-pattern) |
| State owned by exactly one party | [§50 Monitor Object](../../monitor-object-pattern) |
