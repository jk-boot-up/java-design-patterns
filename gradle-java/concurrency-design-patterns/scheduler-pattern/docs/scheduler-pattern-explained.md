# Scheduler, Explained

## The pattern in one sentence

A scheduler makes threads ask for their turn at a shared resource and lets a
replaceable policy decide whose turn comes next.

## The 5 acts

### 1. A fair lock

A bulk job is printing. Three standard jobs arrive, then three express ones.
The printer is guarded by a fair `ReentrantLock`, which serves strictly in
arrival order: STD-1, STD-2, STD-3, EXP-1, EXP-2, EXP-3. The express labels
wait behind every standard one.

### 2. Express first

Each station now calls `scheduler.enter(job)`, which waits until the printer
is free and the policy picks that job. With `EXPRESS_FIRST`, the order is
EXP-1, EXP-2, EXP-3, then STD-1, STD-2, STD-3.

### 3. A replaceable policy

The policy is a comparator. Swapping `EXPRESS_FIRST` for `SMALLEST_FIRST`
prints the jobs with the fewest labels first: STD-2, EXP-2, STD-3, EXP-3,
EXP-1, STD-1. The stations and the printer did not change.

### 4. Nobody waits for ever

One standard job arrives, then five express ones. With express-first alone,
the standard job is printed last, and in a longer rush it would never be
printed. With ageing, a job overtaken three times is promoted: STD-1 prints
fourth, after EXP-3.

### 5. The bill

Deciding costs something every time: each job takes the scheduler's lock,
joins its list, and is woken to check whether it is next. And every priority
rule needs a guard against starving the jobs it does not favour.

## The verdict

Use a scheduler when the order of access to a shared resource matters and may
change. Keep the policy in one comparator, add ageing so nobody starves, and
prefer a priority queue and worker when callers need not wait.

## How to recognise this in code you did not write

- `enter`/`leave` or `acquire`/`release` methods around a condition and a list of waiters.
- Comparators named for a policy: `EXPRESS_FIRST`, `SHORTEST_JOB_FIRST`.
- Ageing or promotion counters on waiting jobs.

## Where you have already met this

- Operating system CPU schedulers and I/O schedulers.
- `PriorityBlockingQueue` feeding a worker thread.
- Print queues, and job schedulers in build servers.
- Kubernetes pod priority and preemption.
