# Problem Statement

## The scenario

A phone app shows and changes an order over a mobile network, where every
round trip costs about 80 milliseconds.

## The naive version

`FineGrainedApi` exposes each small method of `Order` over HTTP. One screen
takes five round trips, and a two-call change can fail half way.

## What this project must deliver

- Five round trips (400 ms) for one screen, shown over real HTTP.
- A summary call answering the whole screen in one trip.
- A delivery change that is all or nothing.
- The rules kept on the domain object.
- The cost shown: 73 bytes where 8 would do.
- Every printed result asserted by a test.
