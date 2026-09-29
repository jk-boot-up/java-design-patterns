# Problem Statement

## The scenario

`Checkout` pays through a `PaymentGateway`. The real gateway is slow, needs the
network and charges real money, and a real card cannot be made to decline on
demand.

## The naive version

Testing against the real gateway: the tests pass while online, take 800 ms per
call, cost real money, and fail on a train for reasons that have nothing to do
with checkout.

## What this project must deliver

- The cost of testing against the real provider, in simulated milliseconds and real pounds.
- All five doubles, hand-written: dummy, stub, spy, mock and fake, each used for the question it answers.
- A double-click double charge caught by a mock at the moment it happens.
- A whole pay, decline, cancel, pay journey through a fake.
- The limit of doubles: a bug a stub misses and a spy catches.
- Every printed result asserted by a test.
