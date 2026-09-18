# Database per Service — Sequence Diagrams

Five acts, as sequences. The interesting differences between them are in the words on the
arrows rather than in the shapes, so read the notes rather than the outlines.

## Act One — One Database, One Query

![Database per Service sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Page as Order history page
    participant Db as SharedSchema<br/>(orders + products)

    Page->>Db: orderHistory("cust-7")
    Note over Db: one query, joining<br/>orders to products
    Db-->>Page: 2 complete rows, names attached

    Note over Page,Db: 1 round trip. A join cannot forget a name,<br/>and a foreign key guarantees the product row exists.
```

</details>

## Act Two — The Catalog Team Renames A Column

![Act Two — The Catalog Team Renames A Column](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Cat as Catalog team
    participant Db as SharedSchema
    participant Page as Order history page

    Cat->>Db: rename product_name -> title
    Db-->>Cat: migration ran, catalog tests green
    Note over Cat: goes home

    Page->>Db: orderHistory("cust-7")
    Db--xPage: ColumnNotFoundException:<br/>no column 'product_name' in products

    Note over Cat,Page: Nobody did anything wrong. The column was theirs,<br/>and the query that names it is in another repository.
```

</details>

## Act Three — Two Databases, Two Calls, One Assembly

![Act Three — Two Databases, Two Calls, One Assembly](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Page as OrderHistoryPage
    participant Ord as OrderService
    participant OrdDb as OrderDatabase
    participant Cat as CatalogService
    participant CatDb as CatalogDatabase

    Page->>Ord: ordersFor("cust-7")
    Ord->>OrdDb: ordersFor("Orders", "cust-7")
    OrdDb-->>Ord: 2 orders — skus, no names
    Ord-->>Page: 2 orders (10ms)

    Note over Page: collect the distinct skus:<br/>[SKU-KETTLE, SKU-MUG]

    Page->>Cat: namesFor([SKU-KETTLE, SKU-MUG])
    Cat->>CatDb: nameOf("Catalog", ...) for each
    CatDb-->>Cat: 2 names
    Cat-->>Page: 2 names in ONE call (10ms)

    Note over Page: stitch orders to names in Java
    Note over Page,CatDb: Same page. 20ms and 2 service calls,<br/>instead of 1 query.
```

</details>

## Act Four — The Same Rename, Against A Database Catalog Owns

![Act Four — The Same Rename, Against A Database Catalog Owns](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Cat as Catalog team
    participant CatDb as CatalogDatabase
    participant Page as OrderHistoryPage

    Cat->>CatDb: rename product_name -> title
    Note over CatDb: the rows AND the query that reads them<br/>change in the same class, same commit

    Page->>CatDb: (via CatalogService) namesFor([...])
    CatDb-->>Page: 2 names, exactly as before

    Note over Cat,Page: The page is unchanged. Nothing outside Catalog<br/>ever named that column.
```

</details>

## Act Five — The Bill

![Act Five — The Bill](images/uml-diagram-5.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Ord as OrderService
    participant CatDb as CatalogDatabase
    participant Page as OrderHistoryPage

    Ord->>CatDb: nameOf("Orders", "SKU-KETTLE")
    CatDb--xOrd: NotYourDataException:<br/>ask Catalog for it
    Note over Ord,CatDb: the join is gone

    CatDb->>CatDb: delete("SKU-KETTLE")
    Note over CatDb: nothing refuses the delete —<br/>the order row is in another database

    Page->>CatDb: (via CatalogService) namesFor([SKU-KETTLE, SKU-MUG])
    CatDb-->>Page: SKU-KETTLE -> (no longer in the catalogue)
    Note over Page,CatDb: the foreign key is gone. A rule that was impossible<br/>to break is now merely impolite to break.
```

</details>

## Notes On Reading These

**The two round-trip counts are the argument.** Act one is one query. Act three is two
service calls plus an assembly step, for exactly the same page —
`itProducesTheSamePage` asserts that the two pages are identical, which is what makes
the comparison fair. Everything else in this project is about whether that extra cost
is worth paying.

**The batch call in act three is deliberate.** `namesFor` takes a list, and Catalog is
called once regardless of how many rows the page has. If it were `nameOf` in a loop,
act three would have one arrow per row and a fifty-row page would be fifty network
calls. `itAsksCatalogOnce` holds the line.

**The requester name on every database arrow is the pattern.** `ordersFor("Orders",
…)` succeeds and `nameOf("Orders", …)` throws, and that difference is all there is to
it. In production the check is not in Java at all — it is database credentials that
cannot see the other service's tables.

**Nothing here sleeps.** `SimulatedClock` advances by ten milliseconds per service
call, so the timings in act three are exact and free, and the whole suite runs in about
a second.

**Act five is two separate losses, and they are usually taught as one.** The first is
the join: cross-service questions now cost two calls and some Java. The second is the
foreign key: an order can outlive the product it names, and something in application
code has to decide what to show. The second is the expensive one, and it is why Saga,
Transactional Outbox and Idempotent Consumer are separate projects.
