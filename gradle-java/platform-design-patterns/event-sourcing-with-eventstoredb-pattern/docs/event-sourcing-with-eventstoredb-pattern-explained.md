# Event Sourcing with EventStoreDB, Explained

## The pattern in one sentence

Event sourcing means you never overwrite what you know. You write down each thing that happened, in order, never change it, and work out the current state by adding the list up.

## The analogy, before any of KurrentDB's words

Think of a village post office that keeps a paper ledger for every customer's savings. Each ledger has numbered lines. A clerk may only write on the next empty line, and nothing is ever rubbed out. To know a customer's savings, you add up their ledger.

Now there are two clerks at two windows. The same customer's husband is at one window, and the wife is at the other. Both clerks open the same ledger, see line 3 is the last, add it up to 140, and both approve a withdrawal of 100. If both then write their entry, the ledger ends at minus 60.

The post office fixes this with one rule. Before writing, a clerk says aloud "I last read line 3". The clerk who writes first fills line 4. When the second clerk says "I last read line 3", the ledger keeper says no, line 4 exists now. Go back, read again and decide again. That rule is this project.

## What KurrentDB calls these things

**KurrentDB** is the post office's ledger room: a separate program that keeps events in order and never changes them. It was called **EventStoreDB** until 2025. It is the same database under a new name, with a new Docker image name, a new Java library name and a new connection-string prefix.

A **stream** is one ledger, one named list of events. Here the stream name is `loyalty-C-4417`.

A **revision** is a line number. The first event in a stream is revision 0.

An **append** writes events on the next lines. There is no call to change an event.

The **expected revision** is "I last read line 3". The Java client calls it a `StreamState`: `streamRevision(3)` for "only if still at 3", `noStream()` for "only if the stream does not exist yet", and `any()` for "don't check". **`any()` is the default.**

**WrongExpectedVersion** is the refusal: "expected revision 3, but the stream is at revision 4".

An **event id** is a random identifier the writer puts on each event. If the same id arrives again with the same expectation, the server treats it as a retry and does not write it twice.

**`$all`** is the server's one log of every event in every stream, in the order it wrote them.

A **catch-up subscription** asks for every event from a starting point, receives the stored ones, is told "caught up", and then receives each new event as it is written. A copy built from it for one screen is a **projection**, or **read model**.

A **soft delete** hides a stream. A **tombstone** is a hard delete that forbids the name for ever. A **scavenge** is the later clean-up that actually frees the disk.

**Insecure mode** switches off TLS, which is encryption on the network, and switches off user accounts. The demo uses it; production must not.

## The six acts

### A Real Log, Read Back

The demo appends the four things that happened to customer C-4417 in March, and KurrentDB numbers them revision 0 to 3. A second connection reads the stream from the start and adds it up to 140. Nothing stores 140.

```
  4 events appended to the stream loyalty-C-4417. KurrentDB numbered them revision 0 to 3.
    revision 0  2025-03-01  earned 60 points on order ORD-8801           balance 60
    revision 1  2025-03-03  spent 25 points on order ORD-8814            balance 35
    revision 2  2025-03-08  earned 120 points on order ORD-8907          balance 155
    revision 3  2025-03-14  lost 15 points to the twelve-month expiry    balance 140
  balance: 140 points, from 4 events. nothing stores 140; it was added up just now.
```

### Two Checkouts, No Check

Customer C-5120 pays with points on the website and in the phone app at the same moment. Each checkout looks and sees 140 points at revision 3. Each decides 100 is affordable, and each appends a spend with no check. The two checkouts are two real threads, each with its own connection. They wait for each other after looking, so both always see the same thing. Both appends are accepted, and the balance is -60.

```
  C-5120 has 140 points. the website and the phone app both look: 140 points, at revision 3.
  both decide 100 is not more than 140, and both append a redemption with the check off.
  both appends accepted, at revisions 4 and 5. balance now: -60 points.
```

### The Expected Revision

This is the same race for customer C-5121, but each append now says "only if the stream is still at revision 3". One append is written at revision 4. The other is refused with WrongExpectedVersion. The refused checkout looks again, sees 40 points, and says no. Which checkout wins depends on the machine, so the demo does not name it. That exactly one wins is certain, because the server makes the comparison.

```
  appends accepted: 1, at revision 4. appends refused: 1.
  the refusal is WrongExpectedVersion: expected revision 3, but the stream is at revision 4.
  the refused checkout looks again: 40 points, at revision 4. 100 is more than 40, so it tells the customer no.
  balance now: 40 points. nothing was locked; the server compared one number.
```

### A Retry It Recognises

The shop awards C-5122 45 points, the reply is lost, and the shop sends the award again with a new event id. Now there are two awards and a balance of 90. This is the twin's double-award bug, caused here by the network rather than by a release.

For C-5123 the retry reuses the event id and the expectation of "no stream yet". The server answers revision 0 again and writes nothing, so there is one award and a balance of 45.

```
  sent again with a new event id: 2 awards for ORD-9001 in the stream. balance 90.
  sent again with the same event id and the same expectation: the server answers revision 0 again, and writes nothing.
  1 award in the stream. balance 45.
```

### A Screen That Catches Up

The support dashboard starts after everything else. It subscribes to every stream whose name starts with `loyalty-`, from the start. It receives 18 stored events and is told it has caught up. Then an award of 20 for C-4417 arrives on its own, and C-4417 shows 160.

```
  it receives 18 events that were already stored, and the server tells it it has caught up.
  it shows C-4417 = 140, C-5120 = -60, C-5121 = 40, C-5122 = 90.
  a new order awards C-4417 20 points. moments later the dashboard shows C-4417 = 160, with 19 events received in all.
```

### The Bill: Deleting A Stream

C-5122 asks to be forgotten, and the shop deletes the stream. Reading it by name now fails. Reading `$all` still finds its 2 events, and they stay until a scavenge runs. The dashboard still shows 90. A later write to the same name is accepted at revision 2, not 0. The server also ran with security off.

```
  reading the stream now: stream not found.
  reading the store's whole log, every stream at once: 2 events of loyalty-C-5122 are still there, until a clean-up called a scavenge runs.
  the support dashboard still shows C-5122 = 90. the delete reached the stream, not the copies built from it.
  a later order writes to the same stream name. it is accepted at revision 2, not 0, and reading the stream shows 1 event.
  and this server ran with security off: no TLS, no passwords, in 1 container. production must never run like that.
```

## The verdict

- Give each thing that must stay consistent its own stream: here, one customer's points.
- Look, decide, then append with the revision you looked at.
- On a refusal, look again and decide again; never resend blindly.
- Choose an event id once per decision and reuse it on every retry.
- Treat erasure as a job for every projection as well as the stream, and schedule the scavenge that really removes the bytes.
- Run the server with TLS and user accounts.

## How to recognise this in code you did not write

- `appendToStream(name, events)` with no options, or with `StreamState.any()`. That writer races.
- `StreamState.streamRevision(n)`, where `n` came from the read that the decision was based on. That writer is safe.
- A `catch (WrongExpectedVersionException e)` that simply calls append again. That is a blind retry, and the check it was meant to enforce is gone.
- `EventDataBuilder.json(UUID.randomUUID(), ...)` inside a retry loop. Each retry gets a new id, so the server cannot recognise it.
- `subscribeToAll(...fromStart())` feeding a map or a table. That is a projection, and it has to be told about deletes.

## Where you have already met this

Bank ledgers, wallets, loyalty and gift-card balances, and order histories. Any SQL event table with a unique key on stream and revision is doing the same check.

## When this is too much

If one program writes each customer's points, the race cannot happen. If nobody will ask how a number came to be, store the number.
