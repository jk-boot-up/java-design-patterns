# Leader/Followers, Explained

## The pattern in one sentence

Leader/Followers lets a pool of threads take turns: the leader waits for a
message, promotes a follower, and handles the message itself, with no
dispatcher and no hand-off.

## The 5 acts

### 1. A dispatcher that hands off

`DispatcherWorkers` has one dispatcher thread that takes each message from
the source and puts it on a second queue for four workers. Twenty orders mean
twenty hand-offs between threads; none is handled by the thread that
received it, and the dispatcher handles no orders itself.

### 2. Leader and followers

`LeaderFollowers` has four pool threads and no dispatcher. Leadership is a
lock: the thread holding it is the leader and waits on the source; the
others wait for the lock. The count of threads waiting on the source at once
never goes above one.

### 3. Receive, promote, handle

Each leader takes a message, releases the lock (promoting a follower to
leader), and then handles the message itself. Leadership passes twenty times,
once per order, and all twenty are handled by the thread that received them:
zero hand-offs.

### 4. Every thread works

All twenty orders are handled by pool threads, spread across several of them.
No thread spends its life only receiving and passing on.

### 5. The bill

Two messages for the same order arrive in order: "place" (80 ms of work),
then "cancel" (5 ms). The first leader takes "place" and promotes a follower,
which takes "cancel" and finishes first. The order of arrival is not the
order of completion; messages that must stay in order need to go to the same
thread.

## The verdict

Use it in very high-throughput servers where a hand-off per message is a
measurable cost. For most applications, an ExecutorService is simpler. Either
way, keep messages that must stay in order on the same thread.

## How to recognise this in code you did not write

- A lock or semaphore guarding the wait for the next event, released before handling it.
- Several threads calling `select()` or `accept()` in turn.
- No dispatcher thread and no hand-off queue in a pool.

## Where you have already met this

- High-performance C++ servers built with ACE and TAO, where the pattern was described.
- Netty's and other event loops where several threads take turns on a shared selector.
- Several threads calling `accept()` on the same server socket.
