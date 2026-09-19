# Problem Statement

## Read the partner first

This project assumes [Object Pool](../object-pool-pattern), which builds a pool by hand and finds four
costs: a small object pooled is slower than allocating it, a returned object carries its old state, a
leaked object is never returned, and sizing is a guess. Nothing here is lost by skipping the library, and
[`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: payments that need a connection. Here the connection is a real JDBC connection, from a
real pool.

## What is new

The four costs, met by people who spent years on them.

```
TWO. The dirty return, which the partner project had to fix by hand.
  Grace's borrower gets the same physical connection: autoCommit true, readOnly false.
  HikariCP reset the JDBC state it knows about on return. that is the reset the partner had to write.
```

But not all of it:

```
  but state it does not know about stays: a session variable Ada set is read by Grace: Ada Lovelace
```
