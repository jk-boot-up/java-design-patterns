# Problem Statement

## The scenario

Many threads place orders, and every order reserves stock. The stock must never go wrong, however many orders arrive together.

## The naive version

A map of stock that any thread may change, with a read and then a write.

```
  10 in stock. two orders, for 3 and for 4, read the stock at the same moment. it should be 3 left. it is 3 left: false. one of the two reservations was lost.
  every method looked correct. the state was open to anyone.
```

## What this project must deliver

A stock held in a shared map that loses an update when two threads read together; an actor base class with a mailbox, tell and ask, and a restart on failure; an inventory actor that owns the stock; four thousand reservations from four threads with no lost update; replies that are messages including refusals; no way to read the stock but by asking; a restart after a bad message; two actors waiting for each other; and a plain verdict.
