# Problem Statement

## The scenario

An online store adds up prices, shares bills, and stores customers' email addresses. Prices are pence, and the store sells in pounds and dollars.

## The naive version

Prices are doubles, the currency is a string kept beside the number, and email addresses are plain strings. It works for every demo, and fails in quiet ways.

```
  three stamps at 1.10: 3.3000000000000003.
  0.1 + 0.2 == 0.3: false.
  ten pounds added to ten dollars: 20.0.
  the number has no idea what it is a number of.
```

## What this project must deliver

A `Money` and an `EmailAddress` that are equal by value, never changed, and impossible to build wrong; four bugs of the plain version shown for real; the splitting of a bill; and a plain verdict.
