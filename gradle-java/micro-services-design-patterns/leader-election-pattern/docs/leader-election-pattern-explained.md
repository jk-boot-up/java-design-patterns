# Leader Election, Explained

## The pattern in one sentence

Leader election makes exactly one of several identical copies of a service responsible for a job, and hands the job to another copy if the leader disappears.

## The six acts

### Three Copies, Nobody In Charge

With nothing coordinating the copies, all three send the report, and the manager receives it three times.

```
  the nightly sales report is sent by every copy: [A, B, C].
  the manager receives it three times.
```

### One Holds The Lease

All three ask for the lease. A gets it, and is the leader. The report is sent by A alone.

```
  all three ask for the lease. the leader is A. the report was sent by: [A].
```

### The Leader Dies

A dies holding the lease. After ten seconds B asks and is refused, because A still holds it. After thirty seconds the lease has expired, and B takes it. For those thirty seconds nobody was actually leading.

```
  A, the leader, dies. leader now: A, and its lease has 30 seconds to run.
  after 10 seconds B asks: leader is still A.
  after 30 seconds the lease has expired. B asks first and becomes leader: B.
  for those 30 seconds nobody was leading. that is the cost of not being sure A was dead.
```

### Two Who Think They Lead

A pauses for thirty five seconds, perhaps in a long garbage collection. Its lease expires and B takes it. A wakes, still believing it leads, and sends, and so does B. The report goes twice.

```
  A paused for 35 seconds, say for a long garbage collection. its lease expired and B took it. the store says the leader is B.
  A wakes up, still believing it leads, and sends. so does B. the report was sent by: [A, B].
```

### Fencing

Each lease carries a token that only goes up. B's is two, A's was one. When A wakes and tries to send, the report sink refuses the older token. Only B's report is sent.

```
  A wakes up and tries to send: refused, token 1 is older than 2.
  the report was sent by: [B]. each lease carries a token that only goes up, and the thing being written to checks it.
```

### The Bill

A healthy leader that renews every seven seconds against a lease of five loses leadership at second five. Against a lease of thirty it never does. Too short loses a healthy leader, too long misses a dead one, and everything depends on one shared record.

```
  a leader that is perfectly healthy, renewing every 7 seconds against a lease of 5: it loses leadership at second 5.
  the same leader against a lease of 30: never loses it.
  the lease must be longer than the renewal interval, with room for a slow moment. too long, and a dead leader goes unnoticed for that long.
  and everything now depends on one shared record. if it is down, nobody can lead.
```

## The verdict

Use leader election when exactly one copy must do a job: a scheduler, a coordinator, a cache warmer. Use a lease with a time limit, renew it well inside that limit, and use a fencing token wherever a stale leader could do harm. Prefer a store built for it, such as ZooKeeper, etcd or Consul, over building your own. If the job can safely run twice, do not elect anyone.

## How to recognise this in code you did not write

- A lock or lease record with an owner and an expiry time.
- ZooKeeper's ephemeral nodes, etcd leases, Consul sessions, Kubernetes `Lease` objects.
- A `@Scheduled` job wrapped in something like ShedLock.
- A token or `epoch` number passed with every write.

## Where you have already met this

Kubernetes controllers, Kafka's controller broker, and every cluster with a single scheduler.

## When this is too much

If a job is safe to run twice, or if a single instance is acceptable, an election is machinery for nothing. The simplest leader is the only instance.
