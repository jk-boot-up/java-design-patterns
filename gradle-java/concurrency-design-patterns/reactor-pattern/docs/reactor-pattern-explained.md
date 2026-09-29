# Reactor, Explained

## The pattern in one sentence

A reactor uses one thread to wait for events on many connections at once and
dispatches each event to a short handler.

## The 5 acts

### 1. A thread per connection

`ThreadPerConnection` starts a new thread for every client. A hundred tills
connect and wait for their next question: a hundred threads, nearly all of
them idle, each holding its own stack. Till 1 asks "stock KETTLE-1" and gets
4.

### 2. One reactor thread

`Reactor` uses one thread and a `Selector`. The selector waits on all hundred
connections at once and wakes the thread only when one is ready. Till 1's
question is answered, and the number of threads that ever ran a handler is
one.

### 3. A handler per event

The reactor's loop dispatches by event. A new connection goes to the accept
handler, which registers it for reading. Arriving bytes go to the read
handler, which answers the line. Till 2 asks "price MUG-1" and gets 800.

### 4. Every till, one thread

All hundred tills send "stock MUG-1" at once. The selector reports whichever
are ready, and the one thread answers them in turn: 100 correct answers, and
still only one thread ever ran a handler.

### 5. The bill

Till 2 asks for a report whose handler takes 300 milliseconds. Till 3 then
asks a question that takes microseconds, and waits over 200 milliseconds,
because the only thread is busy. Handlers must never block; slow work must be
handed to another thread.

## The verdict

Use a reactor, usually through Netty or a framework built on it, for servers
with many mostly idle connections. Keep handlers short and non-blocking, and
hand slow work to a thread pool. For modest numbers of connections, virtual
threads are simpler.

## How to recognise this in code you did not write

- `Selector.select()` in a loop.
- "Event loop" in a framework's documentation.
- Warnings not to block the event loop.

## Where you have already met this

- Java NIO's `Selector`, `ServerSocketChannel` and `SocketChannel`.
- Netty's event loops, used by gRPC, Cassandra and many Java servers.
- Node.js's event loop, Nginx, and Redis.
- Spring WebFlux and Vert.x, built on reactors.
