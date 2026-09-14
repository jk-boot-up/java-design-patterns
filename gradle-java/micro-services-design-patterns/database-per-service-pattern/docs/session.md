# Session Guide — Database per Service

A one-hour session. The mechanism takes four minutes and is a single `if` statement.
Everything worth the hour is on either side of it: why a correct migration breaks
somebody else's page, and what the split costs once you have made it.

Protect the last twenty minutes. A room that leaves believing this pattern is free, or
that it is a technical improvement, has learned something worse than nothing.

**Audience:** developers who know Java and have used a relational database. No
distributed-systems experience assumed.

**Format:** laptops open. Everything runs offline with a JDK. There is no database to
install, which is worth saying at the start because people will ask.

## Learning Objectives

By the end, a participant can:

1. Explain why a correct migration by one team breaks another team's page, and why no
   test suite owns that failure.
2. State the mechanism honestly — a refusal, enforced by credentials — and say that
   there is no algorithm in it.
3. Say what the split buys (teams that can change their minds without asking
   permission) and what it does not buy (speed, correctness).
4. Price the two losses: the join, and the foreign key.
5. Explain why the cross-service call must be batched.
6. Argue for or against splitting a specific schema in a system of their own, and name
   the line they would split it on.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check, and being fair to the shared database |
| 0:05–0:16 | The Tuesday rename |
| 0:16–0:22 | Three tempting fixes |
| 0:22–0:32 | The mechanism, and the same page for more money |
| 0:32–0:40 | The payoff, and being precise about what it is |
| 0:40–0:56 | Exercises, and the bill |
| 0:56–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check, And Being Fair

```bash
cd micro-services-design-patterns/database-per-service-pattern
./gradlew test
```

16 tests, green, in about a second.

Then, before anything else, spend two minutes selling the shared database. The room
will expect you to attack it, and the session does not work if they think that is where
this is going.

> One query. One join, done by an engine that is extremely good at joins. Every row has
> a name, because a join cannot forget one. A foreign key guarantees the product row
> exists. Nothing is eventually consistent. **If a shop can live like this, it should.**

## 0:05–0:16 — The Tuesday Rename

Run it and stop at act two:

```
  catalog team: migration ran, catalog tests green, done
  order history page: no column 'product_name' in products -- somebody renamed it
```

**Ask the room whose fault this is before you say anything.** Let them argue. Somebody
will blame the catalog team, somebody will say there should have been a test.

Then land the two facts:

1. **The migration was correct.** `theRenameLosesNothing` asserts the data is all still
   there, readable under the new name.
2. **The catalog team could not have known.** The query that broke is in a repository
   they have no reason to open.

Then show the thing that usually changes the mood of the room — open
`SharedSchemaTest` and point out that **every test in it passes**, including
`aRenameBreaksTheOrderHistoryPage`.

> Your test suite is not going to tell you. A test suite tests a codebase, and this
> problem is between two codebases.

Close with the consequence that actually costs money, which is not the broken page:

> The page gets fixed in an hour. What does not get fixed is the meeting the two teams
> now agree to hold before any schema change. That is what slows a shop down for years.

## 0:16–0:22 — Three Tempting Fixes

Ask for fixes before offering any. All three of these will come up.

**"Write a test that catches it."** Whose repository does it live in? A build that runs
one team's queries against another team's schema is a shared build with a shared owner
— the same coupling wearing a hat.

**"Just don't rename columns."** The one that actually gets adopted, and the worst,
because nobody writes it down. The schema fills up with names that are wrong and
everybody learns that change is expensive.

**"Use a view so the old name still works."** A real technique that buys real time. It
does not change who is allowed to decide, and somebody now maintains a layer that
belongs to neither side.

Then the question, on the board, left there:

> What if the catalog team's data were somewhere the orders team physically could not
> read?

## 0:22–0:32 — The Mechanism, And Act Three

Show the mechanism and let it be small:

```java
if (!OWNER.equals(requester)) {
    throw new NotYourDataException(requester, OWNER);
}
```

Say the important sentence:

> In a real shop nothing throws this. Orders is given database credentials that cannot
> see the Catalog tables, and the read fails as a permissions error before it reaches
> any Java. If your rule is a comment asking people not to, you do not have this
> pattern.

Now act three:

```
      0ms ->    10ms  Orders           OK        2 order(s)
     10ms ->    20ms  Catalog          OK        2 name(s) in one call
     20ms ->    20ms  HistoryPage      ASSEMBLED 2 row(s) from 2 services
  the same page took 20ms and 2 service calls instead of 1 query
```

Two things to point at:

- `itProducesTheSamePage` — the assembled page is identical to the joined one. Same
  rows, same names, same order. **The cost changed; the answer did not.**
- `namesFor` takes a *list*. Ask what act three would look like with `nameOf` in a loop,
  and then what a fifty-row page would look like. `itAsksCatalogOnce` is the guard.

## 0:32–0:40 — The Payoff, Stated Precisely

Act four, which is deliberately boring:

```
  the page is unchanged. Nothing outside Catalog ever named that column.
```

Then do not let the room round this up into "microservices are better". Put the three
statements up and say them plainly:

- It bought **no speed**. Act three is slower than act one.
- It bought **no correctness**. The page was already right.
- It bought the catalog team the **right to change their minds** without asking
  permission or coordinating a release.

> That is an organisational benefit, and it is the only one on offer. Which gives you
> the test: if the two teams are the same three people, you are paying an
> organisational price for an organisational problem you do not have.

## 0:40–0:56 — Exercises, And The Bill

Start with act five, because it makes the exercises honest.

```
     Orders may not read Catalog's database directly. Ask Catalog for it.
  ord-101   SKU-KETTLE   (no longer in the catalogue) x1
     the row survives with no name. A foreign key would have refused the delete.
```

Two losses, and the second is the one people forget. Ask the room what a foreign key
actually is — a rule the database will not let you break — and then what it has become
here: a rule that lives in code, tests, and agreements between teams.

### Exercise 1 — Break it in the shared schema (everyone)

Rename a *different* column in `SharedSchema` and find every place that needs changing.
Then count how many repositories those places would be in, in a real shop.

### Exercise 2 — Un-batch the call (everyone)

Change `OrderHistoryPage` to call `catalog.nameOf(sku)` per row instead of `namesFor`.
Watch `itAsksCatalogOnce` fail, and read the timeline. Then imagine fifty rows. This is
the single most common way this pattern gets implemented badly.

### Exercise 3 — Where does the line go? (discussion)

In pairs, on a schema they actually work on: draw one line through it. Which tables go
on which side, which query that exists today would break, and where that query would
live afterwards. Expect a fight about the reporting query — that is the useful part.

### Exercise 4 — Stretch: put the integrity back

Catalog deletes a product an order refers to. Where could the rule "you may not delete
a product that has been ordered" now live? Walk through the options — Catalog asks
Orders before deleting, Catalog soft-deletes, Orders copies the name at order time —
and notice that the last one is the answer most real shops reach, and that it is a
denormalisation, not a constraint.

## 0:56–1:00 — Wrap-Up

Five sentences:

1. The unit of ownership is the data, not the code — two services sharing a schema are
   one service with two pipelines.
2. The mechanism is a refusal enforced by credentials, not a convention.
3. Every test can pass while the system is broken, because the failure is between two
   codebases.
4. The split buys the right to change your mind, and buys nothing else.
5. You lose the join and the foreign key, and the foreign key is the expensive one.

## Facilitator Notes

- **Sell the shared database first, and mean it.** If the room thinks you are building
  a straw man, nothing after act two lands. The strongest version of this session has
  someone arguing at the end that their own shop should *not* split, and being right.
- **The whose-fault-is-it question in act two is the best five minutes available.** Do
  not shorten it. People arrive believing that every production failure is somebody's
  mistake, and this one genuinely is not.
- **Expect "this is just microservices".** Narrow it: this is the one rule that makes
  the rest of microservices mean anything. Services that share a schema are not
  separate services, whatever the deployment diagram says.
- **Expect "we could use a read replica of their database".** Take it seriously and then
  ask who owns the column names in that replica. It is the shared schema again with
  extra infrastructure.
- **Expect "what about reporting?"** Say plainly that this project loses it, and that
  CQRS is where it comes back. Do not improvise an answer.
- **If the group is quiet in exercise 3**, put your own schema up and let them argue
  with your line.
- **Timings assume a group that talks.** Act four and exercise 1 compress. Act two and
  the bill do not.

## Materials Checklist

- [ ] JDK 21 installed, `./gradlew test` run once beforehand so nothing downloads live
- [ ] A terminal with a font big enough to read the act three timeline from the back
- [ ] [`animation.html`](animation.html) open in a browser tab for the rename spreading,
      and then not spreading
- [ ] [`uml-diagram.md`](uml-diagram.md) open for the five acts as sequences
- [ ] A whiteboard for the three tempting fixes, and for exercise 3
