# Problem Statement

## The scenario

A product page asks the supplier's stock API how many mugs are left. Usually it answers in fifty milliseconds. Sometimes it never answers at all.

## The naive version

No limit. The page waits for the supplier, however long that takes.

```
  the supplier never answers. the product page's thread is: WAITING, with no limit on for how long.
  nothing in the code says it will ever come back, and the customer is looking at a spinner.
```

## What this project must deliver

A supplier held at a gate so that silence is exact; a call that waits and one that gives up; the work that continues after giving up; the effect of the limit on a typical hundred calls; one budget shared across three calls; a payment that times out and still happens; and a plain verdict.
