# Problem Statement

## The scenario

A label printer prints five labels per tick and holds ten jobs; orders arrive
in bursts.

## The naive version

Orders are pushed at the printer as they arrive; in a burst of fifty, forty
are refused.

## What this project must deliver

- Refusals counted when orders are pushed.
- A polling consumer printing all fifty at its own pace.
- Pausing by not polling, with nothing lost.
- Empty polls counted, and long polling compared.
- The waiting cost of polling named.
- Every printed result asserted by a test.
