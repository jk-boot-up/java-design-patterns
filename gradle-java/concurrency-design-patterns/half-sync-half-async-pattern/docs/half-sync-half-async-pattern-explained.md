# Half-Sync/Half-Async, Explained

## The pattern in one sentence

Half-Sync/Half-Async splits a system into a non-blocking half that accepts and
queues events and a blocking half of plain workers that process them, joined
by a bounded queue.

## The 5 acts

### 1. Blocking work on the event thread

`EventThreadOnly` receives orders on a single event thread and processes each
one there: save, charge, email, 100 milliseconds. Twenty orders arrive in a
burst. Each must wait for every order before it to be fully processed, so the
last is not even accepted until over 1.5 seconds later.

### 2. The async half

`HalfSyncHalfAsync.burst` keeps the event thread's job tiny: offer the order
to a queue. Every one of the twenty orders is accepted within a tenth of a
second, and the event thread is free again at once.

### 3. The sync half

Four ordinary worker threads loop: take an order from the queue, then save,
charge and email it, one step after another, in plain blocking code. All
twenty orders are done in under a second.

### 4. The queue absorbs the burst

During the burst the queue held ten or more orders waiting for a free worker.
That is its job: the event thread never waited for a card payment, only the
workers did.

### 5. The bill

If the card provider is down, the workers stall and the queue fills. With a
queue of ten, ten of twenty orders are turned away. Every queue needs a
limit, and a plan for what happens beyond it: reject, retry later, or save to
disk.

## The verdict

Use it whenever events arrive on a thread that must stay responsive and the
work behind them blocks. Keep the async half tiny, bound the queue, decide
what happens when it is full, and keep the worker code plain.

## How to recognise this in code you did not write

- An event loop or listener that only submits work to an executor.
- `BlockingQueue` between a receiver and worker threads.
- "Background workers" consuming from a job queue.

## Where you have already met this

- Web servers whose event loop hands requests to a worker thread pool.
- `ExecutorService` with a `BlockingQueue`: a direct implementation.
- Message queues between a front-end API and background workers.
- Operating systems: interrupt handlers (async) queue work for kernel threads (sync).
