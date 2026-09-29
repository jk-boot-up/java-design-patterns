# Copy-on-Write, Explained

## The pattern in one sentence

Copy-on-write lets readers use the current version with no locks and makes
every writer copy it, change the copy and swap it in.

## The 5 acts

### 1. A plain list, changed while read

The listeners are kept in a plain `ArrayList`. The kettle's price changes and
the loop starts telling each listener. The loyalty service, when told,
subscribes the email service, which adds to the list being looped over. The
loop throws `ConcurrentModificationException` after the web page cache and
the loyalty service, and the phone app never hears the new price.

### 2. A copy-on-write list

`CowList` keeps its listeners in an array that is never changed once
published. The loop reads the current array; the loyalty service's
subscription copies the array, adds the email service, and swaps the copy in.
All three original listeners hear the first change, and all four hear the
next one.

### 3. Readers never lock

One thread runs a hundred thousand notification passes over the list while
another subscribes and unsubscribes a thousand times. Readers never take a
lock and never see a half-changed list: zero failures.

### 4. Snapshots

A reader starts going through the list when it has three listeners. A fourth
is added before it finishes. The reader completes its pass over the three it
started with; the next reader will see four.

### 5. The bill

Every write copies the whole array. Adding ten thousand listeners one at a
time copied 49,995,000 references in total. That is fine for a list read
constantly and changed rarely, and wrong for anything that changes all the
time.

## The verdict

Use copy-on-write for small collections that are read constantly and changed
rarely, above all lists of listeners. Use `CopyOnWriteArrayList` rather than
writing your own, and choose something else for data that changes often.

## How to recognise this in code you did not write

- `CopyOnWriteArrayList` or `CopyOnWriteArraySet` fields named `listeners` or `subscribers`.
- A `volatile` array or list replaced whole on every change.
- Iteration with no locks over shared data.

## Where you have already met this

- `java.util.concurrent.CopyOnWriteArrayList` and `CopyOnWriteArraySet`.
- Listener and observer lists in Swing, Spring and many libraries.
- Linux's `fork()`, which shares memory between processes until one writes to it.
- Snapshots in file systems such as ZFS and Btrfs.
