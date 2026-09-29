# Problem Statement

## The scenario

A hundred shop tills stay connected to the warehouse stock server all day and
ask short questions now and then.

## The naive version

`ThreadPerConnection` gives each connection its own thread: a hundred threads,
almost all waiting.

## What this project must deliver

- Thread count for a thread per connection: 100.
- A NIO reactor serving the same 100 tills with 1 thread.
- Accept and read handlers dispatched by event.
- 100 simultaneous questions answered by one thread.
- A slow handler shown delaying another client.
- Every printed result asserted by a test, over real sockets.
