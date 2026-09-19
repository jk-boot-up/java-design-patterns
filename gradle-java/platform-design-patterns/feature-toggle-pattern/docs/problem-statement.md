# Problem Statement

## The scenario

Gift wrap adds three pounds to an order. It has been coded, but it has a bug that nobody has found yet, and we would like to try it on a few customers first.

## The naive version

Release gift wrap by deploying it, and remove it by deploying again.

```
  gift wrap goes live by deploying it: 1 deploy. it has a bug, so taking it away is another: 2 deploys.
  each deploy ships every other change waiting in the branch too, so the wish to switch one thing carries everything else with it.
```

## What this project must deliver

A table of switches with four rules: off, on, a percentage of customers and named customers; a checkout that ships with gift wrap already in it; a bugged gift wrap failing orders; a switch that turns it off with no deploy; the safe default when the table cannot be read; and a count of combinations and of stale toggles.
