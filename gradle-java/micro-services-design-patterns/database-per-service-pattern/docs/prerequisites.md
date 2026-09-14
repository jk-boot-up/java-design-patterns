# Prerequisites

What you need before starting this project, what you can pick up as you go, and what
you explicitly do not need to know.

There is no database here, and that surprises people. The bar is Java and a rough sense
of what a `SELECT` with a join does.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, records, `List`, `Map`, `final` fields.
- **What a join is, roughly.** One query that reads two tables and returns rows with
  columns from both. If you can say that sentence, you have enough.
- **What a foreign key is, roughly.** A constraint that stops one table referring to a
  row that does not exist in another. You need to believe that the database enforces
  it, not that somebody remembered to.
- **What a schema migration is.** A change to the shape of a table — adding a column,
  renaming one — run as part of a deployment.
- **Reading a JUnit test** — `assertEquals`, `assertThrows`, `assertTrue`.

### Helpful, but explained as we go

- **Database credentials and grants.** The real enforcement mechanism for this pattern
  is a database user that cannot see another service's tables. The primer below is
  enough.
- **The idea of a bounded context** — that a "product" means something slightly
  different to the catalog team than to the orders team. Useful, not required.
- **API Composition** ([`../api-composition-pattern`](../api-composition-pattern)),
  which is about doing this project's assembly step properly. Read this one first;
  that one answers the question this one raises.

### Explicitly NOT required

- **SQL.** Not one line of it appears in this project. Tables are `Map`s and a column
  is a map key, which is what makes a rename a real rename rather than a story about
  one.
- **Any actual database.** No Postgres, no MySQL, no H2, no Docker, no JDBC, no
  connection string.
- **ORMs, JPA, Hibernate, Spring Data.** None of it.
- **Distributed transactions, two-phase commit, or eventual consistency theory.** The
  hole this pattern opens up is real and this project names it, but filling it is
  Saga's job, not yours today.
- **Kafka, message brokers, CDC.** Later projects in the category.

## A 60-Second "Database per Service" Primer

Each service keeps its own data. Nobody else may read it directly. If you want somebody
else's data, you ask them for it.

That is the whole thing. The mechanism in this project is that every database method
takes the name of whoever is asking and throws `NotYourDataException` at anybody but
the owner.

In production that check is not in your code at all. The Orders service connects with a
database user that has no grant on the Catalog tables, so a cross-service read fails as
a permissions error before any Java runs. **If the rule in your system is a comment
asking people not to, you do not have this pattern.**

## A 60-Second "Why A Rename Breaks Somebody Else" Primer

In a shared schema, the order history page is one query that names `product_name`.

The catalog team owns the products table. One Tuesday they rename `product_name` to
`title`. Their migration is correct, their tests pass, their service works.

The order history query, in a different repository, is now broken.

Nobody did anything wrong. The failure lives in the gap between two codebases, and a
test suite only ever tests one codebase, which is why `SharedSchemaTest` can contain a
**passing** test called `aRenameBreaksTheOrderHistoryPage`.

## A 60-Second "What You Lose" Primer

Two things, and the second is the one people forget.

**The join.** A question spanning both services is now two calls plus code that stitches
the answers together. Batch that second call or you will turn a fifty-row page into
fifty network requests — `CatalogService.namesFor` takes a list for exactly this reason.

**The foreign key.** The two rows are in different databases, so no constraint can span
them. Catalog can delete a product an order refers to, and nothing stops it. Something
in application code then has to decide what to render, and here that decision is the
string `(no longer in the catalogue)`.

A rule that used to be impossible to break is now merely impolite to break.

## Why There Is No Real Database Here

A real database would add setup, a container, a schema file, and about four minutes to
every run — and it would teach nothing this project is about.

The subject is **who is allowed to read what**, and that is a question about ownership,
not about SQL. Storing rows in `LinkedHashMap`s keeps the whole argument visible in a
file you can read in one sitting, and it makes the column rename literal: a map key
genuinely moves, and the query that names the old key genuinely finds nothing.

`SimulatedClock` does the same job for time. Each service call advances it by ten
milliseconds, so the timings in act three are exact, repeatable, and free. Nothing in
this project sleeps.

## Software Prerequisites

- **JDK 21 or newer.** Nothing else.
- **Gradle:** not needed globally. The project ships a wrapper.

### Installing JDK 21

macOS, with Homebrew:

```bash
brew install openjdk@21
sudo ln -sfn $(brew --prefix)/opt/openjdk@21/libexec/openjdk.jdk \
    /Library/Java/JavaVirtualMachines/openjdk-21.jdk
```

Linux (Debian or Ubuntu):

```bash
sudo apt install openjdk-21-jdk
```

Windows: install the Microsoft Build of OpenJDK 21 or Temurin 21 from the installer,
and let it set `JAVA_HOME`.

### Verify Your Setup

```bash
java -version          # expect 21 or newer
cd micro-services-design-patterns/database-per-service-pattern
./gradlew test         # expect BUILD SUCCESSFUL
./gradlew run          # expect five acts
```

If `./gradlew` will not execute on macOS or Linux, make it executable:

```bash
chmod +x gradlew
```

The first `./gradlew` command downloads Gradle itself and needs a network connection.
Everything after that works offline.

## Troubleshooting

**"Unsupported class file major version"** — Gradle is using an older JDK than the
toolchain asks for. Check `java -version`, and set `JAVA_HOME` to a 21 install.

**Act 2 prints an error and the build still succeeds** — correct. The broken page *is*
act two. `aRenameBreaksTheOrderHistoryPage` is a passing test that asserts a page is
broken, which is the most pointed thing this project has to say.

**Act 3 looks worse than act 1, and that seems backwards** — it is worse, and that is
the point. Two service calls and 20ms instead of one query. The split bought no speed;
it bought the catalog team the right to change their minds.

**Act 5 shows a row with no product name and the demo does not crash** — deliberate.
There is no foreign key any more, so `OrderHistoryPage` has to decide what to render
for a sku Catalog has never heard of, and it chooses a placeholder.

**The timings are always 0, 10 and 20ms** — they are meant to be. `SimulatedClock` is
not a real clock; ten milliseconds per service call is a stated assumption, not a
measurement.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the Tuesday rename, and why no test
   suite owns the failure
2. `SharedSchema.java` — read it **generously**. One query, one join, a complete page.
   It is the thing being given up, and the rest of the category is the price
3. Run `./gradlew run` and read all five acts in order, comparing act 1's round-trip
   count against act 3's timeline
4. [`database-per-service-pattern-explained.md`](database-per-service-pattern-explained.md)
   — the shared filing cabinet, and what the split does and does not buy
5. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md) — the
   structure, including the arrows that are missing on purpose, then the five acts as
   sequences
6. [`animation.html`](animation.html) — the rename spreading through a shared schema,
   and then failing to spread at all
7. The tests, which are the specification. Read `aRenameBreaksTheOrderHistoryPage`
   first, then `aRenameIsNowANonEvent`, then `anOrderCanReferToAProductThatIsGone` —
   which is the bill
