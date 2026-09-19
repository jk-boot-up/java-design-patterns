# Fork-Join, Explained

## The pattern in one sentence

Fork-join splits a big job into smaller pieces of the same kind, runs the pieces at the same time on several workers, and joins their answers back into one.

## The six acts

### One Loop

Adding up a hundred thousand order totals in a loop gives four hundred and ninety nine million eight hundred and thirty eight thousand pence, on one thread.

```
  adding up 100000 order totals in a loop: 499838000 pence, on one thread.
```

### Split It Until It Is Small

The job is split in halves until a piece is ten thousand or fewer. That gives sixteen pieces added directly and thirty one tasks in all, and the same total as the loop.

```
  split in halves until a piece is 10000 or fewer: 16 pieces added directly, 31 tasks in all.
  the total: 499838000, which is the same as the loop: true.
```

### The Pieces Really Run Together

A pool of four workers, sixteen pieces, each held until four are running at once. The most running at the same moment is four.

```
  a pool of 4 workers, 16 pieces, each held until 4 are running at once. most running at the same moment: 4.
```

### How Small Is Small Enough

With a threshold of a hundred thousand there is one piece, which is just the loop. Ten thousand gives sixteen, a hundred gives a thousand and twenty four, and one gives a hundred thousand pieces and nearly two hundred thousand tasks, which is mostly the cost of making tasks.

```
  a piece of 100000 or fewer is added directly: 1 pieces, 1 tasks.
  a piece of 10000 or fewer is added directly: 16 pieces, 31 tasks.
  a piece of 100 or fewer is added directly: 1024 pieces, 2047 tasks.
  a piece of 1 or fewer is added directly: 100000 pieces, 199999 tasks.
  one piece is just the loop. one task for every item is mostly the cost of making tasks.
```

### Pieces That Are Not The Same Size

Four equal pieces could give four times the speed. If one piece costs eighty five and the others five each, the best possible speedup is one point one eight, because the job waits for the big piece.

```
  four pieces of work, costs [25, 25, 25, 25]: the best possible speedup on 4 workers is 4.0 times.
  costs [85, 5, 5, 5]: 1.18 times. the job waits for the big piece, and three workers wait for it too.
```

### The Bill

A pool of two workers and eight pieces that each wait on something slow run only two at once, so six pieces wait. Fork-join is for work that uses the processor. And splitting twenty items to single items makes thirty nine tasks to add up twenty numbers.

```
  a pool of 2 workers and 8 pieces that each wait on something slow, such as a database: most running at once: 2 of 8.
  fork-join is for work that uses the processor. a worker that waits is a worker that cannot help.
  and for 20 items, split to single items: 39 tasks to add up 20 numbers. small jobs are faster in a loop.
```

## The verdict

Use fork-join for large, processor-bound jobs that split into independent pieces of about the same cost, such as sums, sorts, searches and image work. Choose the threshold from measurement, keep the pieces free of shared mutable state, and prefer a parallel stream when the job fits one. Do not use it for work that waits, or for small jobs.

## How to recognise this in code you did not write

- A class that extends `RecursiveTask` or `RecursiveAction`, with `fork()` and `join()`.
- `ForkJoinPool.commonPool()`, `parallelStream()`, and `Arrays.parallelSort`.
- A `compute()` method that starts with an `if (size <= THRESHOLD)`.
- `CompletableFuture` chains that run on the common pool.

## Where you have already met this

Java's parallel streams and `Arrays.parallelSort`, and merge sort taught in every algorithms class.

## When this is too much

For small jobs, or work that waits on I/O, fork-join is overhead or starvation. A plain loop, or a thread pool sized for waiting, is better.
