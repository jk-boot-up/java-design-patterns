# Problem Statement

## The scenario

The legacy checkout is one large class that does pricing, stock, payment and email. It works. It is also
where every change is slow and every incident starts. The business wants it replaced.

## The naive version: the big-bang rewrite

Months of parallel work, a cutover weekend, and a Monday.

```
ONE. The big-bang rewrite.
  26 weeks of work in parallel with production. orders the new code served in that time: 0.
  no feedback from real traffic for half a year, and then a cutover weekend.
  Monday: 1 of 4 capabilities is faulty: payment declines large orders.
  the only rollback is all-or-nothing, so 4 of 4 go back, including the three that were fine.
```

The problem is the single switch. A fault in one capability can only be answered by taking all four back.

## What this project must deliver

A way to replace the checkout with no cutover weekend, evidence that moves are safe before they are made, and
an honest account of what running two systems costs, including the way it most often ends.
