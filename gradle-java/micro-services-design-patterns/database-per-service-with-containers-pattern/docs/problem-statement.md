# Problem Statement

## The scenario

The shop has two teams. The Orders team owns what customers bought. The Catalog team owns what the shop sells: each product's name, price, stock and whatever else describes it. The order history page, which belongs to Orders, shows a customer each thing they ordered with the product's name beside it. Customer cust-7 has two orders: ord-101, one Stainless Steel Kettle, and ord-102, four Blue Stoneware Mugs.

## The naive version

Both teams keep their tables in one shared PostgreSQL database, and the order history page is one SQL query that joins them.

```
TWO. The Catalog team renames product_name to title.
  ALTER TABLE products RENAME COLUMN product_name TO title: done. Catalog's own queries updated, its tests green.
  the order history page, which belongs to Orders:
    ERROR 42703: column p.product_name does not exist
  nobody did anything wrong. the column was Catalog's; the query naming it was Orders'.
```

## What the twin project already did

The plain-Java Database per Service project in this course told this whole story in Java: a shared schema, a join, a rename that breaks somebody else's page, a split into two databases, the same page assembled from two calls, and the bill — no join, no foreign key. It is a complete teaching of the idea and nothing here replaces it.

What it could not do was use real databases. Its tables were maps, its "database refused" was an exception class written for the purpose, and both of its databases were the same kind of thing. It could not show two services choosing two different engines, what a real engine does when it is asked for a join it cannot do, or what happens to a transaction that one engine can undo and the other cannot.

## What this project must deliver

The same shop, the same customer and the same two orders, first in one real PostgreSQL database and then split: Orders on its own PostgreSQL database, Catalog on its own MongoDB database, both in containers the demo starts and stops. The shared database's join, its foreign key refusing a delete, and a rename breaking the other team's query, each with Postgres's real error. Two product documents of different shapes. The page assembled from two questions to two engines, surviving the rename. The old join tried from both sides, with Postgres refusing and MongoDB quietly answering nothing. A delete that nothing can refuse. A rollback that reaches one engine and not the other. And a page that is half there when one engine is down.

Every error message printed is the engine's own, and two runs back to back print the same thing.
