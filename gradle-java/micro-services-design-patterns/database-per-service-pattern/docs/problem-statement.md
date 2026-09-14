# Problem Statement

## The Scenario

The shop has two teams. The catalog team looks after products — names, descriptions,
prices, photographs. The orders team looks after what people have bought.

They share one database. The products table and the orders table sit in it side by
side, and the order history page is a single query that joins them:

```
  ord-101   SKU-KETTLE   Stainless Steel Kettle       x1
  ord-102   SKU-MUG      Blue Stoneware Mug           x4
  database round trips: 1
```

Before anything else, be fair to this. It is very good.

- **One round trip.** The page costs one conversation with one database.
- **The join is done by an engine that is extremely good at joins**, written by people
  who have thought about it for thirty years.
- **A join cannot forget a name.** Every row comes back complete or the query fails;
  there is no half-built page.
- **A foreign key guarantees the product row is there.** An order cannot refer to a
  product that does not exist, because the database will not permit it.
- **Nothing is eventually consistent.** What you read is what is true, right now.

If a shop can live like this, it should. Most of the difficulty in the rest of this
category is the price of giving it up.

## What Goes Wrong

On a Tuesday afternoon the catalog team renames a column. `product_name` becomes
`title`, for perfectly good reasons of their own — consistency with the rest of their
schema, or a word the business actually uses.

```
  catalog team: migration ran, catalog tests green, done
  order history page: no column 'product_name' in products -- somebody renamed it
```

Look at what each team saw.

The catalog team wrote a migration. It ran. Their tests passed. Their service works.
They went home.

The order history page is broken, and it belongs to somebody else.

## Why That Hurts

The uncomfortable part is that **nobody did anything wrong**.

The column was the catalog team's column, in the catalog team's table, and they are
entitled to rename it. The order history query is the orders team's query, and it is a
perfectly ordinary query.

The failure lives in the space between the two, and that space belongs to nobody. It is
not in the catalog team's code, not in their tests, not in their repository, and not in
their build. There is no review that would have caught it, because there is no reviewer
who can see both sides.

`SharedSchemaTest` in this project pins that down in the most pointed way available:
**every test in it passes**, including `aRenameBreaksTheOrderHistoryPage`. The break is
not a bug. It is a correctly working system doing what it was told.

And the consequence is not really the broken page — that gets fixed in an hour. The
consequence is what happens next: the two teams agree that from now on, schema changes
need a meeting. That agreement is the thing that slows a shop down for years.

## The Tempting Fixes, And Why They Are Not

**"Write a test that catches it."** Whose repository does it live in? The catalog
team's build would have to run the orders team's queries against the catalog team's
schema. That is possible, and it is a shared build with a shared owner, which is the
coupling you were trying to remove wearing a different hat.

**"Just don't rename columns."** This is the one that actually gets adopted, and it is
the worst of the three, because it is invisible. Nobody writes it down. The schema
slowly fills with columns whose names are wrong, and every team learns that changing
anything is expensive.

**"Use views, so the old name still works."** A real technique, and it buys time. It
does not change who is allowed to decide, and one more layer now has to be maintained
by somebody who does not own either side of it.

## The Question This Project Answers

If the catalog team's data were somewhere the orders team physically could not read,
the Tuesday rename would be nobody else's business.

So: what happens if each service gets its own database, and nobody may read anybody
else's?

## The Second Half, Which Is Harder

The mechanism is a refusal, and it takes about ten lines. The interesting part is what
the refusal costs, and this project prices it exactly.

The same page now costs two service calls and a piece of Java that stitches the answers
together. The join is gone. And the foreign key is gone with it — `Catalog` can delete
a product that an order refers to, and nothing stops it, because the two rows are in
different databases and no constraint can span them.

A rule that used to be *impossible* to break becomes merely impolite to break. It moves
out of the database and into code, tests, and agreements between teams.

## The Goal

By the end of this project you should be able to:

1. Explain why a correct migration by one team breaks another team's page, and why no
   test suite owns that failure.
2. State the mechanism honestly: it is a refusal, enforced by database credentials, and
   there is no algorithm in it.
3. Describe exactly what a split database buys — teams that can change their minds
   without asking permission — and say plainly that it buys no speed and no
   correctness.
4. Price the two losses: the join, and the foreign key.
5. Say when *not* to do this. If the two teams are the same three people, the price is
   real and the benefit is imaginary.
