# Proactor, Explained

## The pattern in one sentence

A proactor starts slow operations without waiting and lets the system call a
completion handler, or a failure handler, when each finishes.

## The 5 acts

### 1. One after another

`BlockingQuotes` opens a connection to each supplier, sends "price KETTLE-1",
and waits for the answer before moving on. Each supplier takes 0.2 seconds, so
five prices take over 0.9 seconds, and the asking thread does nothing else
the whole time.

### 2. Start everything at once

`ProactorQuotes.start` opens an asynchronous channel to each supplier and
calls `connect` with a completion handler. It does not wait: all five are
started, and `start` returns, in under a tenth of a second. The system does the
waiting, the five 0.2 second waits overlap, and all answers arrive in under
0.6 seconds.

### 3. Completion handlers

Each request is a chain of three handlers: `Connected` sends the question,
`Written` starts reading the answer, `Read` records the price. The five read
handlers record £21.00, £19.50, £22.40, £18.90 and £20.10, and the warehouse
picks the cheapest, £18.90.

### 4. A failure is a completion

A sixth supplier is down. Its connect cannot complete, so the system calls
that request's `failed` handler instead of `completed`. It is recorded as a
failure, and the other two requests in the batch answer as normal. No
try-catch surrounds the call that started them.

### 5. The bill

One request is now three handlers: `Connected.completed` writes,
`Written.completed` reads, `Read.completed` records. The steps no longer read
top to bottom in one method, and a stack trace from a handler starts in the
system's thread, not in the code that asked.

## The verdict

Use a proactor, or the futures and reactive libraries built on the idea, when
many slow operations can overlap. Keep handlers short, collect results safely,
and consider virtual threads when readable, top-to-bottom code matters more.

## How to recognise this in code you did not write

- `CompletionHandler` with `completed` and `failed` methods.
- `sendAsync`, `thenAccept`, `whenComplete`.
- Callbacks passed to I/O calls.

## Where you have already met this

- `AsynchronousSocketChannel` and `CompletionHandler` in Java NIO.2.
- `HttpClient.sendAsync` and `CompletableFuture.thenAccept`.
- Windows I/O completion ports and Linux io_uring, which the pattern is named after.
- Callbacks in JavaScript's Node.js file and network APIs.
