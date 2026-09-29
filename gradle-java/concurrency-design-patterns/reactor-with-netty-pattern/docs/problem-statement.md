# Problem Statement

## The scenario

A hundred tills keep connections open to a stock server and ask short
questions.

## The naive version

A thread per till means a hundred threads, almost all idle.

## What this project must deliver

- One event loop serving a hundred tills.
- A line decoder reassembling a split question.
- A hundred simultaneous questions on one thread.
- Four worker loops sharing the connections.
- A blocking handler, and its fix with an executor group.
- Every printed result asserted by a test.
