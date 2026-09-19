# Problem Statement

## The scenario

Three copies of the reporting service run for reliability. Every night one sales report must go to the manager, not three.

## The naive version

Every copy sends the report, because each one runs the same schedule and knows nothing about the others.

```
  the nightly sales report is sent by every copy: [A, B, C].
  the manager receives it three times.
```

## What this project must deliver

A lease store with a token that only goes up; nodes that ask for the lease and act on what they last heard; the three-copies duplicate; the takeover after a death; the split leader after a long pause; a sink that checks the fencing token; the lease that is too short for the renewal interval; and a plain verdict.
