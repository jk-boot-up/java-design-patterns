# Problem Statement

## The scenario

Thirty customers use one shared back end; releases go to everyone at once.

## The naive version

One shared stack: a release with a checkout bug stops all 30 customers from
checking out.

## What this project must deliver

- A buggy release failing every customer on one shared stack.
- Three cells with a router placing customers evenly.
- The same bug limited to one cell's customers, then rolled back.
- A new cell for new customers without moving anyone.
- The costs shown: cross-cell questions and copies to run.
- Every printed result asserted by a test.
