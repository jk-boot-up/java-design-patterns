# Space-Based Architecture with Hazelcast, Explained

## The pattern in one sentence

With Hazelcast, a space-based design keeps data in a partitioned in-memory
grid with backups, runs changes on each key's owner, and writes the database
behind.

## The 5 acts

### 1. One database for everyone

Every order writes the stock to the database, which handles one write at a
time and takes five milliseconds for each. Three hundred kettle orders take
over 1.4 seconds, and more app servers would only queue for the same
database.

### 2. Stock in the grid

Three Hazelcast members start and form a cluster. The stock lives in a
Hazelcast map spread across them. Three hundred orders, spread over the three
units, take under a second, and not one of them waits for the database.

### 3. One grid, not three copies

Every unit reads the same stock, seven hundred. The grid does not keep three
copies to be synchronised: each key has one owner, with a backup on another
member, and every unit asks the owner.

### 4. Write-behind

Hazelcast writes the database later, in the background, with write-behind.
It keeps only the latest value of each key, so three hundred sales reach the
database as at most three writes, and the database stock is seven hundred. No
customer waited for any of those writes.

### 5. The last kettle, a crash, and the bill

One kettle is left, and two customers try for it on two different units at
once. The sale runs as an entry processor on the owning member, one at a
time: one sale succeeds, the other is refused, and stock is zero. Then unit
three crashes; its backup copies take over and the stock is still seven
hundred. The bill: data held in every unit's memory, a cluster to run, and
sales lost if the whole grid stops before write-behind runs.

## The verdict

Use a data grid for bursts of load a single database cannot absorb. Change
data with entry processors, keep at least one backup, and accept that
write-behind trades durability for speed.

## How to recognise this in code you did not write

- `IMap` and `executeOnKey(key, processor)`.
- `MapStoreConfig` with a write delay.
- Clusters of application instances sharing an in-memory map.

## Where you have already met this

- Hazelcast, Apache Ignite and Oracle Coherence data grids.
- Ticket-booking and trading systems that keep hot data in a grid.
- Caches with write-behind to a database.
