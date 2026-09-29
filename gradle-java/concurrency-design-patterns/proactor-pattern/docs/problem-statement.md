# Problem Statement

## The scenario

The warehouse asks five suppliers for a price before each order; each takes
0.2 seconds to answer.

## The naive version

`BlockingQuotes` asks one supplier at a time and waits for each answer: over
0.9 seconds, with the thread doing nothing else.

## What this project must deliver

- Sequential blocking asks shown taking over 0.9 s.
- Asynchronous channels started at once, returning in under 0.1 s.
- Completion handlers recording each price; the cheapest chosen.
- A down supplier reported through failed().
- Every printed result asserted by a test, over real sockets.
