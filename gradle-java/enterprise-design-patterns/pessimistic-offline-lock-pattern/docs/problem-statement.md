# Problem Statement

## The scenario

Two clerks want to edit the same product. A change to a product takes several minutes, and a clash would throw away a lot of work.

## The naive version

The previous project let them edit freely and checked a version on save. Here the aim is the opposite: nobody starts an edit that could be thrown away.

```
  clerk A asks for MUG-BLUE: got the lock.
  clerk B asks for MUG-BLUE: refused, MUG-BLUE is locked by A.
  the clash was stopped before B could start editing.
```

## What this project must deliver

A lock manager with owners and expiry, on a clock the demo controls; a refusal that names who holds the lock; edits that overwrite nothing; the cost of waiting; a forgotten lock that expires and stops the old owner writing; a deadlock and its fix by fixed-order locking; the difference between locking a catalogue and locking a product; and a plain verdict.
