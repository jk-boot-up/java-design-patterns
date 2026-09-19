# Problem Statement

## The scenario

The price list is expensive to build, so the shop builds it the first time anyone asks. Many threads ask, and the first several may ask together.

## The naive version

Check whether it exists, and if not, build it. Two threads can both see that it does not exist.

```
  two threads ask for the shared price list at the same moment, before it exists.
  price lists built: 2. both saw that it was missing, and both built one.
  each thread now holds a different price list, and one of them is thrown away.
```

## What this project must deliver

A price list that counts its builds; a rendezvous hook that makes the race happen every time; four ways to get it lazily, unprotected, locking every call, double-checked, and the class holder idiom; the count of price lists built and locks taken; a test that guards the volatile field; and a plain verdict.
