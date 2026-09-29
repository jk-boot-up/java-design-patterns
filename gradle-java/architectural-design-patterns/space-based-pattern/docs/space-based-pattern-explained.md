# Space-Based Architecture, Explained

## The pattern in one sentence

Space-based architecture gives each processing unit an in-memory copy of the
data, keeps copies in step through a data grid, and updates the database in
the background, so requests never wait for it.

## The 5 acts

### 1. One database for everyone

Three app servers each call `CentralDatabase.takeOne`, which takes 5
milliseconds and serves one query at a time. Three hundred orders take over
1.4 seconds. With six app servers it still takes over 1.4 seconds: the
database is the limit, not the servers.

### 2. Processing units

Each `ProcessingUnit` holds its own copy of the stock in memory. Orders are
spread across three units and answered from memory: 300 orders in under 0.3
seconds, with no order touching the database.

### 3. The data grid

Each unit has only seen its own 100 sales, so each shows 900 kettles. The
`DataGrid` copies every sale to the other units: after replication, all three
show 700.

### 4. The database catches up

The `DataWriter` receives the changes from the grid and writes them to the
database in batches of 100: three writes instead of three hundred. The
database now shows 700, and no customer waited for any of it.

### 5. The bill

One kettle is left. Two customers buy it at the same moment on two different
units, before the grid has copied either sale. Both units say yes, and after
replication the stock is -1. And a unit that crashes before the grid copies
its sales loses them.

## The verdict

Use it for extreme, spiky load where brief disagreement between copies is
acceptable, usually with a data grid product. For most systems, a single
database with good indexes and caching is simpler and always consistent.

## How to recognise this in code you did not write

- In-memory data grids in the request path.
- Write-behind to a database from a grid.
- Many identical processing units with no shared database in front of them.

## Where you have already met this

- In-memory data grids such as Hazelcast, Apache Ignite and Oracle Coherence.
- Ticketing and flash-sale systems.
- The "tuple space" idea from JavaSpaces, where the name comes from.
