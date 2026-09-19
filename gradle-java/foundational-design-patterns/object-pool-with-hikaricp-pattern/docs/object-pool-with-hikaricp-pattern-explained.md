# Object Pool with HikariCP, Explained

## The pattern in one sentence

Keep a few expensive connections, lend them out, and take them back.

## What HikariCP does that the hand-built pool did not

**It opens what demand needs.** Ten sequential payments through a pool that may hold two opened one connection.

**`close()` returns the connection.** Try-with-resources gives it back rather than closing it.

**It resets the JDBC state it knows about.** `autoCommit`, `readOnly`, isolation level and catalog return to their
defaults, which is the reset the partner project had to write.

**A timeout is a setting.** The partner project needed a hand-written timeout to rescue an exhausted pool.

```
THREE. Exhaustion, with a timeout already built in.
  a third caller waited 316ms and got: SQLTransientConnectionException
  Connection is not available, request timed out after 306ms (total=2, active=2, idle=0, waiting=0)
```

Its default is thirty seconds, so it should be set. `leakDetectionThreshold` can also log who never returned a
connection, with a stack trace.

## What it cannot fix

**State it cannot see.** A session variable set on the database side is invisible to the pool.

```
  a session variable Ada set is read by Grace: Ada Lovelace
```

The security bug the partner project found is still possible. The pool cannot reset what it cannot see.

**Sizing is still a guess.**

```
FOUR. Sizing is still a guess, and still costs in both directions.
  four payments at once, each needing 50ms on a connection, pool of 1: 223ms
  four payments at once, each needing 50ms on a connection, pool of 4: 53ms
  a pool of 50 opens 50 connections and keeps them idle, for four payments.
```

HikariCP's own documentation argues for small pools. More is not faster.

## What pooling buys, honestly

```
FIVE. What pooling buys, on real JDBC.
  opening a new connection each time: about 37.8 microseconds.
  borrowing from the pool:            about 1.6 microseconds.
```

This is in-memory H2, whose connections are cheap. A real database over a network costs far more, which is why the
pattern is right here. Timings vary by machine. No test asserts one.

## The verdict

Pool connections, threads and native handles, and use a library that has already fixed the hard parts. Never pool
ordinary objects, and never write your own connection pool.

## How to recognise this in code you did not write

- A `DataSource` bean, or a `spring.datasource.hikari.*` property.
- `HikariConfig`, `maximumPoolSize`, `connectionTimeout`, `leakDetectionThreshold`.
- Spring Boot applications with a database: HikariCP is the default pool.

## Where you have already met this

Every Spring Boot application with a database uses it.

## When this is too much

For anything cheap to create, which is nearly everything else.
