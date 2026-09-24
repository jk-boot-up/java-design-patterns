# Leader Election with Kubernetes, Explained

## The pattern in one sentence

Leader election lets several copies of a service agree that exactly one of them does a job, by letting one copy hold a lease that it must keep renewing, and letting another take the lease when the renewals stop.

## The analogy, before any of Kubernetes' words

Think of a staff room with a notice board. On it is one note: "Tonight's cash-up is done by Anna, until ten past nine." Anna rewrites the time every few minutes while she is working. If the note goes stale — the time has passed and nobody has rewritten it — anyone else may cross Anna out and write their own name.

Three things about that board matter, and the plain-Java project never had to face them. First, the board does not check the time. It is just a board. Each person who reads the note compares the time on it with their own watch. Second, the board has one rule: every note has a number in the corner that goes up with each rewrite, and if you rewrite it saying "I read number seven" when it is already number eight, the rewrite is refused. Third, Anna could fall asleep at her desk after reading the note and deciding she is in charge. Someone else takes over. Anna wakes up and carries on with the cash-up, sure it is still hers, because the last time she looked, it was.

## What Kubernetes calls these things

A **cluster** is a group of machines Kubernetes runs programs on; each machine is a **node**. This project's cluster has one node, made by kind inside the container runtime.

The **API server** is the notice board: a program that stores records and lets others read and write them.

A **Lease** is the note. Its **holder identity** is the name on it. Its **lease duration** is how long the hold lasts without renewal: 5 seconds here. Its **renew time** is when the holder last rewrote it. Its **lease transitions** is how many times the holder has changed. This project says "holder changes".

The **resource version** is the number in the corner. A write that names an old one is refused with **409 Conflict**.

The **elector** is the part of each copy that does the reading and rewriting. Here it is Fabric8's `LeaderElector`. The holder renews every 1 second. If it cannot renew for 4 seconds — the **renew deadline** — it gives up leading. The others ask every 1 to 2 seconds whether the lease has run out.

A **fencing token** is a number that goes with a lease and only ever goes up. The leader attaches it to everything it writes, and the thing being written to refuses anything carrying a lower number than one it has already seen. Here the token is the lease's own count of holder changes.

## The six acts

### Three Copies, Nobody In Charge

Three copies of the reporting service start as three separate Java processes. None of them asks anyone anything. Each is told to send the nightly sales report, and each does.

```
  three copies of the reporting service run as 3 separate processes. none of them asks who is in charge.
  the nightly sales report is sent by every copy: [A, B, C].
  the manager receives it 3 times.
```

### One Holds The Lease

A starts first, finds no lease, and creates one with its own name in it. B and C start next, read the lease, see it is fresh, and are each told by their elector that the leader is A. All three are asked to send the report; only A does.

Then two writes are made to the lease, both based on the same version of it. The first is accepted. The second is refused with 409 Conflict, because the version it was based on is gone. That is the only rule the API server enforces about a lease. It never takes a lease away by itself.

```
  A asks the API server first and is written into the lease. it says: holder A, lasts 5 seconds, holder changes 0.
  A renews it every 1 second. B and C ask as often, and each is told the leader is A.
  all three are asked to send the report. the report was sent by: [A].
  two writes to the lease, both based on the same version of it: the first is accepted, the second refused with 409 Conflict.
  that refusal is the only rule the API server enforces. it never takes a lease away by itself.
```

### The Leader Stops

A is shut down cleanly. Its elector is set to hand the lease back on the way out, so it clears the holder's name. One of B and C sees an empty lease at its next check and takes it, within a couple of seconds.

Then the new leader is killed outright, with no chance to run any code at all. The lease goes on naming the dead copy. The last copy waits until the last renewal time plus 5 seconds has passed on its own clock, and only then takes over: about one whole lease. For that time nobody leads. The others cannot tell a dead leader from a slow one.

Which of B and C wins, and exactly how long each handover takes, depend on timing the elector and the cluster choose. So the demo names neither, and prints a description chosen from the measured time.

```
  A is shut down cleanly. on its way out, its elector hands the lease back by clearing the holder.
  one of B and C took over within a couple of seconds, well inside one 5-second lease.
  now the new leader is killed outright. it gets no chance to hand anything back.
  the lease went on naming the dead copy until it ran out. the last copy took over after about one whole 5-second lease.
  for that time nobody was leading. the others cannot tell a dead leader from a slow one, so they wait.
```

### Two Who Think They Lead

This is the headline act. A leads, and B waits. A is told to send the report. It checks that it leads — yes — and starts building the report. At that moment the demo freezes A's whole process, using the operating system's stop signal. Every thread in A stops, including the one that renews the lease; this is what a long garbage-collection pause does to a real program.

No renewals arrive. After 5 seconds by B's clock, B takes the lease: holder B, holder changes 1. B sends the report. Then A is woken. It finishes the report it had started, and sends it, because when it checked, it was the leader. The report was sent twice: B, then A.

The lease's own record proves A was wrong. When A sent, the lease named B, and its renewal time was later than A's last renewal. A's elector did notice — on waking, by its own stopwatch, it saw it had missed its renewal deadline and said it had stopped leading — but the check had already been made, and the report was already on its way.

```
  A checks that it leads, and starts building the report. then A freezes, as in a long garbage-collection pause.
  every thread in A stops, the one that renews the lease too. the lease runs out, and B takes it.
  the lease says: holder B, holder changes 1.
  B sends the report. A wakes up, still believing it leads, and sends too. the report was sent by: [B, A].
  when A sent, the lease named B, renewed after A's last renewal: yes.
  A's elector did tell it the lease was lost, but only once A woke up. A had checked before it froze.
```

### Fencing

The same again, with one change. When a copy starts leading, it reads the lease's count of holder changes and keeps it as its token: A's is 0, B's is 1. Every report carries its token, and the manager's inbox remembers the highest token it has seen. B sends first, with 1. A wakes and sends with 0, and the inbox refuses it. Only B's report arrives.

The lease cannot stop A. The inbox, the thing being written to, can.

```
  the same again, but each report now carries a token: the lease's count of holder changes when that copy took it.
  A's token is 0, B's is 1. B sends first. A wakes up and tries to send: refused, token 0 is older than 1.
  the report was sent by: [B]. the count only goes up, and the inbox, the thing being written to, checks it.
```

### The Bill

B is killed. A is still running, but Fabric8's elector cannot be restarted: when A lost the lease, its elector said so and stopped for good. Two whole leases later the lease still names the dead B, and nobody leads. A leads again only when it starts a brand-new elector, with token 2. The usual answer in Kubernetes is simpler: a copy that loses the lease exits, and Kubernetes starts it again.

Then three costs that do not go away. The lease length is a trade: 5 seconds means a dead leader goes unnoticed for up to 5 seconds, and a shorter lease means one slow moment costs a healthy leader its lease. The lease runs out by each copy's own clock, compared with a time the holder wrote with its clock, so machines whose clocks disagree can take over too early. And all of it needs a Kubernetes API server: one cluster, with one node, for one nightly report.

```
  B is killed. A is still running, but its elector gave up when it lost the lease, and it never asks again.
  two whole leases later the lease still names B, and nobody leads. the loser does not rejoin by itself.
  A starts a new elector, and leads again with token 2. the usual answer is simpler: a copy that loses the lease exits, and Kubernetes restarts it.
  a lease of 5 seconds, renewed every 1: a dead leader goes unnoticed for up to 5 seconds. make it shorter, and one slow moment costs a healthy leader its lease.
  the lease runs out by each copy's own clock, measured from a time the holder wrote. clocks that disagree break it.
  and all of it needs a Kubernetes API server: this demo ran 1 cluster, with 1 node, for 1 nightly report.
```

## The verdict

Use a Lease to pick one copy, and let the elector do the renewing. Then say three things out loud, because Kubernetes will not. A leader's belief that it leads can be stale at any moment, so anything it writes must carry a fencing token that the receiver checks. A copy that loses the lease should exit and be restarted, rather than sit alive and leaderless. And the lease length is a choice between noticing a dead leader quickly and not losing a healthy one to a slow moment.

## How to recognise this in code you did not write

- `leaderElector()` with a `LeaseLock`, and a `withLeaseDuration`, `withRenewDeadline` and `withRetryPeriod`. The lease must be longer than the deadline, and the deadline more than twice the retry.
- An `onStopLeading` callback that only logs. The copy is now alive and will never lead again; it usually should call `System.exit`.
- `withReleaseOnCancel(true)`, which hands the lease back on a clean shutdown, so a rolling upgrade does not leave a whole lease with no leader.
- A leader that checks `isLeader` once and then does slow work. That check can be stale by the time the work is written.
- A write from a leader with no token on it, into a store that cannot refuse it.
- In Kubernetes itself, `kubectl get lease -n kube-system`, which shows the scheduler's and the controller manager's own leases.

## Where you have already met this

The Kubernetes scheduler and controller manager, both of which run several copies with one holding a Lease. Every operator built with the Java Operator SDK, which uses this same Fabric8 elector. Outside Kubernetes, locks in ZooKeeper, etcd and Consul, with the same stale-leader problem and the same fencing answer.

## When this is too much

If the job is safe to run twice, run it everywhere and make the result idempotent. If one copy is enough, run one and let Kubernetes restart it. A Lease earns its keep only when several copies must be running and exactly one may act — and even then the receiver has to check a token, because the lease alone cannot stop a leader that froze.
