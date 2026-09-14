# Database per Service, Explained

## In One Sentence

Each service keeps its own data, nobody else is allowed to read it directly, and if you
want somebody else's data you ask them for it.

## Everyday Analogy: The Shared Filing Cabinet

Two departments in an office share one filing cabinet.

While they share it, life is easy. A question that spans both departments is one trip
to one drawer. Nothing is ever out of date, and the folders are all in the same order,
because there is only one order.

And then one department decides to reorganise. They have every right to — it is their
half of the cabinet, and the new arrangement suits their work much better. They do it
carefully, they check their own work, and everything they need is exactly where they
now expect it.

The other department comes in on Monday and cannot find anything.

Nobody was careless. The trouble is that the filing system was a shared decision that
neither department was in charge of, and the only way to change it safely was a meeting
that nobody thought to call.

So they buy a second cabinet. Each department keeps its own, arranges it however it
likes, and reorganises on a Tuesday afternoon without telling anybody.

**And now notice the price, because it is not small.** A question that spans both
departments is no longer one trip to a drawer. It is a phone call, and then another
one, and then somebody writing the two answers down on one sheet of paper. And a rule
that used to be physically enforced — you could not file a receipt without the matching
invoice, because they lived in the same folder — is now just something both departments
have agreed to be careful about.

That is this pattern, exactly. The rest of this document is the same story told with
tables.

## Act One: The Shared Database, Working

```
  ord-101   SKU-KETTLE   Stainless Steel Kettle       x1
  ord-102   SKU-MUG      Blue Stoneware Mug           x4
  database round trips: 1
  every row has a product name, because a join cannot forget one
```

`SharedSchema` holds both teams' tables, and `orderHistory` is one query with a join.
One trip. No assembly. No missing names. `queriesForOnePage()` returns the constant `1`,
which is not a joke — it is there so that act three's number has something to be
compared against.

Read `SharedSchema` generously. It is the thing being given up, and if you have not
appreciated it you will not understand what the rest of the category is paying for.

## Act Two: The Same Database, Breaking

```
  catalog team: migration ran, catalog tests green, done
  order history page: no column 'product_name' in products -- somebody renamed it
  nobody did anything wrong. The column was theirs.
```

The rename is a real rename. In this project a column is a map key, so
`renameProductNameColumnTo("title")` genuinely moves every value from one key to
another, and the order history query — which names `product_name` in its own source —
finds nothing.

Three things are worth saying out loud.

**The migration was correct.** The data is all still there. `theRenameLosesNothing`
asserts exactly that: after the rename, every product name is still readable, under its
new name, by anybody who knows the new name.

**The catalog team could not have known.** The query that broke is in a different
repository, written by people they may never have met.

**Every test passes.** `aRenameBreaksTheOrderHistoryPage` is a passing test that
asserts a page is broken. That is what makes this so hard to see: your test suite is
not going to tell you, because a test suite tests a codebase, and the problem is
between two codebases.

## The Mechanism, Which Is Almost Nothing

```java
public List<Order> ordersFor(String requester, String customerId) {
    if (!OWNER.equals(requester)) {
        throw new NotYourDataException(requester, OWNER);
    }
    ...
}
```

Every database method takes the name of whoever is asking, and refuses anybody but the
owner. That is the pattern. There is no algorithm, nothing adaptive, nothing clever.

**In a real shop nothing throws that exception**, and this is the most important
sentence in the document. The rule is not enforced in Java and it is not a convention
in a wiki. The Orders service is given database credentials that simply *cannot see*
the Catalog tables; an attempt to read them fails as a permissions error long before it
reaches any application code. `NotYourDataException` exists here only so the rule is
visible in a project small enough to read. When you see it thrown, read it as "the
database refused".

If the rule is a comment asking people not to, it is not this pattern. It is a wish.

## Act Three: Two Databases, Doing The Same Job For More Money

```
      0ms ->    10ms  Orders           OK        2 order(s)
     10ms ->    10ms  OrderDb          QUERY     2 order(s) for cust-7
     10ms ->    20ms  Catalog          OK        2 name(s) in one call
     20ms ->    20ms  HistoryPage      ASSEMBLED 2 row(s) from 2 services
  the same page took 20ms and 2 service calls instead of 1 query
```

Ask Orders what the customer bought. Collect the skus. Ask Catalog what they are
called. Stitch the two answers together in Java. `OrderHistoryPage` is those four
sentences and nothing else.

Two details in there earn their place.

**`catalog.namesFor(skus)` takes a list.** That is not a convenience method. Asking
once per sku would turn this two-row page into two calls, a fifty-row page into fifty,
and a report into an outage. `itAsksCatalogOnce` asserts that Catalog receives exactly
one call no matter how many rows the page has. The batch call is the difference between
an assembly step and a disaster.

**An empty order history never troubles Catalog at all.** `forCustomer` returns early
when there are no orders, and `itSkipsCatalogWhenThereIsNothingToName` holds it to
that. A service you do not need to call is the cheapest call there is.

And `itProducesTheSamePage` asserts the thing that makes the comparison fair: the
assembled page says exactly what the joined page said. Same rows, same names, same
order. What changed is the cost, not the answer.

## Act Four: The Same Rename, Now A Non-Event

```
  ord-101   SKU-KETTLE   Stainless Steel Kettle       x1
  ord-102   SKU-MUG      Blue Stoneware Mug           x4
  the page is unchanged. Nothing outside Catalog ever named that column.
```

This is the payoff, and it is quiet, which is the point. `CatalogDatabase` renames the
column *and updates its own queries in the same class*, because the only code that ever
names that column lives beside the column, is tested beside it, and is changed in the
same commit.

`aRenameIsNowANonEvent` asserts that the page is byte-for-byte what it was before the
migration.

Be precise about what has been bought here, because it is easy to oversell:

- It bought **no speed**. Act three is slower than act one. The query engine was
  perfectly happy.
- It bought **no correctness**. The page was already right.
- It bought **the catalog team the ability to change their minds** without asking
  permission, and to deploy that change without coordinating a release with a team
  they have never met.

That is an organisational benefit, and it is the only one on offer. Which gives you the
test for whether to do this at all: if the two teams are the same three people, you are
paying an organisational price to solve an organisational problem you do not have.

## Act Five: The Bill

### The join is gone

```
  Orders may not read Catalog's database directly. Ask Catalog for it.
```

Every question that spans both services is now two calls and some code. That is fine
for an order history page. It is considerably less fine for the report somebody in
finance runs on a Monday, which used to be a `SELECT` with three joins and now has
nowhere to live. Hold that thought — it is the whole reason CQRS exists.

### The foreign key is gone, and this one is worse

```
  b) no more foreign key. Catalog deletes a product that an order refers to:
  ord-101   SKU-KETTLE   (no longer in the catalogue) x1
  ord-102   SKU-MUG      Blue Stoneware Mug           x4
     the row survives with no name. A foreign key would have refused the delete.
```

Catalog deletes a product. An order still refers to it. Nothing stopped the delete,
because the two rows are in different databases and no constraint can span them.

So `OrderHistoryPage` has to decide what to render for a sku nobody has heard of, and
its answer is `(no longer in the catalogue)` rather than a crash.
`anOrderCanReferToAProductThatIsGone` asserts both halves: the row survives, and the
name is that placeholder.

**The page surviving is the good news and the bad news at once.** A rule that used to
be impossible to break is now merely impolite to break. It has moved out of the
database and into code, tests, and agreements between teams — which is to say, into
hope. Two later projects in this category, Transactional Outbox and Idempotent
Consumer, exist because hope is not quite enough.

## What It Buys

- Each team can change its own schema without asking anybody.
- Each team can deploy without coordinating a release.
- Each team can choose a different kind of database if its data wants one.
- A slow query in one service cannot exhaust the connections another service needed.

## What It Costs

- Every cross-service question becomes two calls and a piece of assembly code.
- No foreign keys across the boundary, so referential integrity moves into application
  code and into agreements.
- No transaction across the boundary either — which is a large enough hole that Saga is
  a separate project.
- Reporting has nowhere obvious to live.
- More moving parts to run, back up, and restore, and backups that are no longer
  consistent with each other at a single instant.

## When Not To Use It

- **One team.** The benefit is that teams stop waiting for each other. One team is
  never waiting for itself.
- **Data that is genuinely one thing.** If two tables are always read together and
  always written together, splitting them makes an assembly step out of nothing.
- **When reporting is the product.** If the main thing the business does with the data
  is ask arbitrary questions across all of it, losing the join is not a price, it is
  the end of the road.
- **Before the boundary is known.** A split down the wrong line is far more expensive
  than not splitting, because now the wrong line is in two schemas and a network
  protocol.

## What To Remember

1. The unit of ownership is the data, not the code. Two services sharing a schema are
   one service with two deployment pipelines.
2. The mechanism is a refusal, enforced by credentials — not a convention, not a
   comment, not a wiki page.
3. The migration that broke the page was correct, and the team that ran it did nothing
   wrong. That is what makes shared schemas hard.
4. Every test can pass while the system is broken, because the failure lives between
   two codebases and a test suite only ever tests one.
5. The split buys no speed and no correctness. It buys the right to change your mind
   without asking permission.
6. Batch the cross-service call, or you turn one page into fifty requests.
7. The join is gone: cross-service questions cost two calls and some Java.
8. The foreign key is gone: an order can outlive the product it names, and something
   has to decide what to show.
9. A rule that moves from the database into an agreement between teams has become
   weaker, and you should be able to say so out loud.
10. If the two teams are the same three people, do not do this.
