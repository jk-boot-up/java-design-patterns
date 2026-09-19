# Problem Statement

## The scenario

The product page shows the best price for a mug. Four suppliers each know their price, and each takes a different time to answer.

## The naive version

Ask the four suppliers one after another, and take the lowest.

```
  four suppliers answer in [80, 120, 200, 900] milliseconds. asked in turn, the page waits 1300.
```

## What this project must deliver

A gatherer that asks every supplier at once on a pool, waits up to a deadline, and reports what it got and who was missing; latency arithmetic for one after another, all at once and a deadline; four suppliers shown asked at the same moment by holding them at a gate; a slow supplier left out and named; a failing supplier left out; the growth of calls and of slow pages; and a plain verdict.
