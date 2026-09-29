# Reactor with Netty, Explained

## The pattern in one sentence

With Netty, the reactor is an event loop: one thread waiting on many
connections, running a pipeline of handlers for each.

## The 5 acts

### 1. One event loop

A Netty server starts with one boss event loop to accept connections and one
worker event loop to serve them. A hundred tills connect. Till 1 asks for the
kettle's stock and gets four. Every handler has run on one thread.

### 2. The pipeline

Network data arrives as bytes, not questions. Till 2 sends "price MU" and then
"G-1" as two separate writes. Netty's pipeline starts with a line decoder that
waits for the end of the line, so the handler sees one whole question and
answers 800.

### 3. Everyone at once

All hundred tills ask about the mug at the same moment. All hundred get the
right answer, twenty-five, and every handler still ran on the one event-loop
thread.

### 4. Several event loops

With four worker event loops, Netty spreads the hundred connections over four
threads, one reactor each. A connection is assigned to one loop and always
stays on it, so its handlers never run on two threads at once.

### 5. The bill: never block

Till 2 asks for a report that takes 300 milliseconds, and the handler runs it
on the event loop. Till 3's quick question has to wait over 0.2 seconds, for
an answer that takes microseconds. With the handler added to the pipeline on
its own executor group, the report runs away from the event loop, and till 3
is answered in under 0.2 seconds.

## The verdict

Use Netty for servers with many mostly idle connections or custom protocols.
Keep handlers short, decode with ready-made framers, and move anything slow
to an executor group.

## How to recognise this in code you did not write

- `ServerBootstrap().group(boss, workers)`.
- `ch.pipeline().addLast(...)` with decoders and handlers.
- `SimpleChannelInboundHandler` subclasses.

## Where you have already met this

- Netty underneath gRPC, Spring WebFlux, Vert.x and many databases' drivers.
- Node.js's event loop and Nginx's worker processes.
- The JDK's NIO `Selector`, which Netty's NIO transport is built on.
