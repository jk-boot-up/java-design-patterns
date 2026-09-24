# Database per Service with Containers, Explained

## The pattern in one sentence

Each service keeps its own data in its own database, which no other service may read directly — and once those databases are on different engines, "may not" becomes "cannot": there is no query left that joins them.

## The analogy, before any of the tools' words

Think of two departments that used to share one filing cabinet. Anyone could pull a folder from either drawer and lay two folders side by side. That was quick. It also meant that when one department relabelled its folders, the other department's routine broke.

So they split. Accounts keeps its ledgers in a locked cabinet of fixed-format ledger books. Design keeps its samples in a drawer of index cards, each card with whatever notes that sample needs. Now nobody can lay a ledger page beside a card, because they are different kinds of thing in different rooms. A question about both needs two conversations. And if the Design department throws a card away, nothing in Accounts' cabinet stops it.

## What Postgres and MongoDB call these things

**PostgreSQL**, or **Postgres**, is the cabinet of ledger books: a relational database, holding **tables** with fixed **columns**, asked questions in **SQL**.

A **join** is one question answered from two tables at once, by matching a value in one with a value in the other.

A **foreign key** is a rule the database keeps: a value in one table must exist in another. Postgres refuses any change that would break it.

A **transaction** is a group of changes kept together or undone together. Undoing them is a **rollback**.

A **SQLSTATE** is the five-character code Postgres puts on every error. 23503 means a foreign key would be broken; 42703, no such column; 42P01, no such table; 0A000, not supported.

**MongoDB** is the drawer of index cards: a document database. A **document** is one record of named fields, like one filled-in form. A **collection** is a drawer of them. Two documents in one collection need not have the same fields.

A **find** asks MongoDB for the documents that match. **`$lookup`** is MongoDB's join: for each document, attach the matching documents from another collection in the same database.

**Testcontainers** is the Java library that starts both databases in containers when the demo begins and removes them when it ends.

## The six acts

### One Shared Database

Both teams' tables live in one Postgres database called shop, with a foreign key from orders to products. The order history page for cust-7 is one SQL join, and it takes 1 round trip — one question to a database. Then the Catalog team tries to delete the kettle, which order ord-101 still names. Postgres refuses, with code 23503.

```
  the order history page for cust-7 is one SQL join:
    ord-101   SKU-KETTLE   Stainless Steel Kettle       x1
    ord-102   SKU-MUG      Blue Stoneware Mug           x4
  round trips to a database: 1
  Catalog tries to delete SKU-KETTLE, which ord-101 still names. Postgres refuses:
    ERROR 23503: update or delete on table "products" violates foreign key constraint "orders_sku_fkey" on table "orders"
```

This is the arrangement working well: fast, correct, and guarded by the database itself.

### The Rename

The Catalog team renames its column product_name to title. The change is correct, their queries are updated, their tests pass. The order history page belongs to the Orders team, and its query still names product_name. Postgres answers with 42703: no such column.

```
  ALTER TABLE products RENAME COLUMN product_name TO title: done. Catalog's own queries updated, its tests green.
  the order history page, which belongs to Orders:
    ERROR 42703: column p.product_name does not exist
  nobody did anything wrong. the column was Catalog's; the query naming it was Orders'.
```

### Two Services, Two Engines

Now the split. Orders keeps Postgres, in a database of its own called orders, holding 1 table. Catalog moves to MongoDB, in a database called catalog, holding 1 collection of documents. The kettle's document has a wattage; the mug's has a capacity in millilitres; nobody changed a table to allow either.

The page is now two questions: one SQL query to Orders for the customer's orders, and one find to Catalog for both products' names at once. Java puts the two answers side by side. 2 round trips, where the join took 1. Then the Catalog team renames the name field to title in every document — MongoDB changed 2 documents — and changes its own code in the same release. The page is unchanged, because nothing outside Catalog ever named that field.

```
  Orders owns the orders database on Postgres 18.6: 1 table.
  Catalog owns the catalog database on MongoDB 8.3.11: 1 collection of documents.
  two products, two shapes, and no table to change first:
    SKU-KETTLE: _id, name, priceInPence, stock, wattage
    SKU-MUG: _id, name, priceInPence, stock, capacityMl
  round trips to a database: 2
  Catalog renames name to title in every document: MongoDB changed 2 documents. Catalog's own code reads title from now on.
  the page is unchanged. nothing outside Catalog ever named that field.
```

### The Join, Tried Anyway

This is the headline of the project. The old join is tried from both sides.

From the Orders side, the old SQL: Postgres says there is no table called products here, code 42P01. Then a reach across to the shop database, which is on the very same Postgres server: code 0A000, cross-database references are not implemented. Postgres will not join two of its own databases, let alone one of MongoDB's.

From the Catalog side, MongoDB's own join, `$lookup`, pointed at a collection called orders. MongoDB has no such collection — the orders are in Postgres. It does not complain. It treats the missing collection as empty and returns both products, each with 0 orders.

```
  from Orders, the old SQL join:
    ERROR 42P01: relation "products" does not exist
  from Orders, reaching across to the shop database on the same Postgres server:
    ERROR 0A000: cross-database references are not implemented: "shop.public.products"
  from Catalog, MongoDB's own join, $lookup, into a collection called orders:
    no error. 2 products came back: SKU-KETTLE with 0 orders, SKU-MUG with 0 orders.
    MongoDB has no collection called orders, so it treated it as empty and said nothing.
  no engine holds both halves. the join is not forbidden; it cannot be written.
```

The plain-Java twin could only throw an exception it had written for the purpose. Two real engines give two different answers, and the quiet one is the dangerous one: a report built on that lookup would say nobody ever bought a kettle, and no log anywhere would say why.

### No Foreign Key Between Two Engines

The Catalog team deletes the kettle. MongoDB deleted 1 document; nothing refused. Postgres still holds 1 order naming the kettle, and has no way of knowing it has gone. The page has to decide what to show, and shows "no longer in the catalogue".

```
  Catalog deletes SKU-KETTLE: MongoDB deleted 1 document. nothing refused.
  Postgres still holds 1 order naming SKU-KETTLE.
    ord-101   SKU-KETTLE   (no longer in the catalogue) x1
  in act ONE Postgres refused this delete. across two engines nothing can.
```

### The Bill

Customer cust-7 checks out 2 more mugs. Orders writes ord-103 inside a Postgres transaction, and Catalog takes 2 mugs off the shelf in MongoDB. Then the payment is declined, and Orders rolls back. Postgres forgets ord-103: the customer has 2 orders again. MongoDB keeps its change: 38 mugs, where there were 40. The rollback reached one engine, not both. In the shared database, the stock and the order would have been one transaction.

Then MongoDB is stopped. The page asks Orders, which answers with 2 orders, and asks Catalog, which does not answer. Every name reads "catalog unreachable". The page is half there. And the shop now runs 2 containers, 2 drivers and 2 query languages where it had 1 of each.

```
  Postgres: ord-103 is gone. orders for cust-7: 2.
  MongoDB: SKU-MUG stock 38, was 40. the rollback reached one engine, not both.
  MongoDB is stopped. the order history page for cust-7:
    ord-101   SKU-KETTLE   (catalog unreachable)        x1
    ord-102   SKU-MUG      (catalog unreachable)        x4
  Orders still answered; Catalog did not. the page is half there.
  this demo runs 2 containers, 2 drivers and 2 query languages, where the shared database had 1 of each.
```

## The verdict

Give each service its own database when two teams keep breaking each other, and let each pick the engine that suits its data. Then accept, out loud, what that gives up: the join becomes two questions and some code; the foreign key becomes an agreement between teams; one transaction becomes two that can disagree; and one engine can be down while the other is up. And never trust a cross-engine answer of "nothing" without asking where the other half lives.

## How to recognise this in code you did not write

- Each service's configuration names one database address and one set of credentials, and no service names two.
- A page or report built by calling two services and matching their answers in code, often by collecting ids into one batch call.
- Code that shows a placeholder when a name, price or product is missing: the foreign key that used to make that impossible.
- A `$lookup`, or any join, whose `from` names data that lives in another service. It will not fail. It will be empty.
- A rollback in one service followed by nothing in the other: the transaction stopped at the edge of its engine.

## Where you have already met this

Any shop split into services: orders on Postgres or MySQL, the catalogue on MongoDB, Elasticsearch or DynamoDB, sessions in Redis. The arrangement is often called polyglot persistence — many kinds of storage — and it only becomes possible once each service owns its own.

## When this is too much

If one small team owns both halves, one database is faster, simpler and safer. If two teams need separating but their data is the same shape, two databases on the same engine is often enough. A second engine earns its place only when the data genuinely differs in shape, because every engine added is another thing to back up, upgrade, watch and learn.
