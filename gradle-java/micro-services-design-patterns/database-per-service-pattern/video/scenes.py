"""Scene definitions for the Database per Service teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches, so no sentence points at the screen, the shared
filing cabinet is described in full before any class name is spoken, and the
console slides are read out as a story about who saw what rather than as
columns. The slides illustrate the narration; they never carry it.

Every number quoted here comes from the real output of `./gradlew run`: one
round trip for the joined page, then two service calls and twenty milliseconds
for exactly the same page, then a rename that changes nothing, then a deleted
product that leaves an order naming something the catalogue has never heard of.

Scene order is the argument, and the first third of it is unusual for this
series: scene five exists to make the shared database look *good*. That is
deliberate. A viewer who thinks the shared schema is a straw man will hear
everything after it as marketing, so the pattern cannot be introduced until its
alternative has been given its best case.

Two scenes must not be cut or moved earlier. Scene ten is the honest statement
that in production nothing throws the exception -- the rule is credentials --
and without it the audience will go away thinking this pattern is a coding
convention. Scene fourteen is the bill, and a viewer who leaves believing the
split is free has learned something worse than nothing.

Layout limit: on "bullets" and "quote" slides the body starts at y=260 and
steps 60 pixels a line, and the footer sits at y~1022, so twelve body lines
is the maximum.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Database per Service",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Database per Service "
            "pattern in Java, and it is written and presented by Jayasekhar "
            "Konduru. [[slnc 300]] Let's start with the simple definition. Each "
            "service keeps its own data, nobody else is allowed to read it "
            "directly, and if you want somebody else's data, you ask them for "
            "it. [[slnc 350]] That is genuinely all it says. There is no "
            "algorithm in this pattern, and by the end of the video I want you "
            "to find the mechanism slightly disappointing, because the "
            "interesting part is not how you do it. It is what it costs. "
            "[[slnc 300]] The rest of the video builds a real working Java "
            "project: an online shop with two teams. One looks after products — "
            "names, prices, photographs. The other looks after what people have "
            "bought. [[slnc 300]] They share one database, and one Tuesday "
            "afternoon somebody renames a column. [[slnc 350]] By the end "
            "you'll know why a completely correct migration breaks a page in "
            "another team's repository; why every test can pass while the system "
            "is broken; what splitting the database actually buys, which is less "
            "than people claim; and what it takes away, which is more."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="Two Teams, One Database",
        body=[
            "THE CATALOG TEAM looks after products: names,",
            "descriptions, prices, photographs.",
            "",
            "THE ORDERS TEAM looks after what people bought.",
            "",
            "They share one database. The products table and",
            "the orders table sit in it side by side.",
            "",
            "The order history page is one query that joins",
            "them: order id, sku, product name, quantity.",
            "",
            "Two teams. One schema. Nobody in charge of it.",
        ],
        narration=(
            "Here is the shop, and it is worth picturing before any code. "
            "[[slnc 300]] There are two teams. The catalog team looks after "
            "products: the names, the descriptions, the prices, the "
            "photographs. The orders team looks after what people have actually "
            "bought. [[slnc 350]] They share one database. The products table "
            "and the orders table sit in it side by side, and either team can "
            "read both. [[slnc 300]] The page we are going to follow all the way "
            "through is the order history page — the one a shopper opens to see "
            "what they have ordered. Each line on it has an order number, a "
            "product code, the name of the product, and how many they bought. "
            "[[slnc 350]] And here is the thing to hold on to, because "
            "everything follows from it. The product code lives in the orders "
            "table. The product name lives in the products table. So building "
            "that page means reading both. [[slnc 300]] Two teams, one schema, "
            "and nobody actually in charge of the schema."
        ),
    ),
    dict(
        key="03-one-query",
        kind="code",
        title="The Page Is One Query",
        body="""// SharedSchema.orderHistory(customerId)

for (Order order : orders) {
    Map<String, String> product = products.get(order.sku());
    String name = product.get(PRODUCT_NAME_COLUMN);
    rows.add(new OrderHistoryRow(
            order.orderId(), order.sku(), name, order.quantity()));
}

public static final String PRODUCT_NAME_COLUMN = "product_name";""",
        narration=(
            "In this project there is no real database — the tables are maps, "
            "and a column is a key in a map, which turns out to matter in a "
            "minute. But the shape is exactly the shape of a join. [[slnc 300]] "
            "For every order the customer placed, find the matching product, "
            "read the product's name out of it, and put a row together from the "
            "two halves. [[slnc 350]] Now notice the last line, because it is "
            "the whole video in one constant. The query names the column it "
            "wants. It asks for a column called, in so many words, product "
            "underscore name. [[slnc 300]] That string is written down in the "
            "orders team's code. And the column it refers to belongs to the "
            "catalog team. [[slnc 350]] Nobody thinks about that on the day they "
            "write it, because in one database it is simply how you read a "
            "table."
        ),
    ),
    dict(
        key="04-act-one",
        kind="console",
        title="Act One — One Database, One Query",
        body="""$ ./gradlew run

Act 1 - one database, one query
  ord-101   SKU-KETTLE   Stainless Steel Kettle       x1
  ord-102   SKU-MUG      Blue Stoneware Mug           x4
  database round trips: 1
  every row has a product name, because a join cannot
  forget one""",
        narration=(
            "And it works. [[slnc 250]] Two orders come back for this customer. "
            "A stainless steel kettle, one of them. A blue stoneware mug, four "
            "of them. Each line has the order number, the product code, the "
            "product's name and the quantity, and the page is complete. "
            "[[slnc 350]] One round trip to one database. [[slnc 300]] That "
            "number — one — is printed on purpose, because in a few minutes we "
            "are going to have something to compare it against, and the "
            "comparison is the argument of the entire video."
        ),
    ),
    dict(
        key="05-be-fair",
        kind="bullets",
        title="Be Fair To This — It Is Very Good",
        body=[
            "✓ One round trip. One conversation, one database.",
            "",
            "✓ The join is done by an engine that is extremely",
            "  good at joins, by people who have thought about",
            "  it for thirty years.",
            "",
            "✓ A join cannot forget a name. There is no such",
            "  thing as a half-built page.",
            "",
            "✓ A foreign key guarantees the product row exists.",
            "",
            "If a shop can live like this, it should.",
        ],
        narration=(
            "Before we break it, I want to spend half a minute being fair to "
            "this arrangement, because the rest of the video is the story of "
            "giving it up, and if you have not appreciated it you will not "
            "understand what is being paid. [[slnc 350]] One round trip. One "
            "conversation with one database, and the page is done. [[slnc 250]] "
            "The join itself is performed by a query engine that is "
            "extraordinarily good at joins, written by people who have been "
            "refining it for thirty years, and you did not have to write any of "
            "it. [[slnc 300]] A join cannot forget a name. Either every row "
            "comes back complete, or the query fails — there is no such thing "
            "as a half-built page. [[slnc 350]] And a foreign key guarantees "
            "that the product an order refers to actually exists. Not "
            "probably. Not usually. The database will refuse to let you create "
            "an order pointing at a product that is not there. [[slnc 300]] "
            "Nothing here is eventually consistent. What you read is what is "
            "true, right now. [[slnc 350]] So let me say the sentence that most "
            "talks about microservices leave out. If a shop can live like this, "
            "it should."
        ),
    ),
    dict(
        key="06-act-two",
        kind="console",
        title="Act Two — Tuesday Afternoon",
        body="""Act 2 - the catalog team renames product_name to title
  catalog team: migration ran, catalog tests green, done
  order history page: no column 'product_name' in products
                      -- somebody renamed it
  nobody did anything wrong. The column was theirs.""",
        narration=(
            "Now it is Tuesday afternoon, and the catalog team decides that the "
            "column called product name should be called title instead. "
            "[[slnc 300]] They have good reasons. Perhaps it is what the rest of "
            "their schema looks like. Perhaps title is the word the business "
            "actually uses. It is their column, in their table, and renaming it "
            "is entirely their business. [[slnc 350]] So they write a migration. "
            "They run it. Their tests pass. Their service works. They go home. "
            "[[slnc 400]] And the order history page is dead. [[slnc 350]] It "
            "asked for a column called product name, and there is no longer a "
            "column called product name. [[slnc 300]] Look at what each side "
            "saw. The catalog team saw a green build and a clean deployment. The "
            "orders team saw an incident. Both of those are true at the same "
            "moment, and neither team can see the other one."
        ),
    ),
    dict(
        key="07-nobody-wrong",
        kind="quote",
        title="Nobody Did Anything Wrong",
        body=[
            "The migration was correct. Every product name is",
            "still there, readable under its new name.",
            "",
            "The catalog team could not have known. The query",
            "that broke is not in their code, not in their",
            "tests, and not in their build.",
            "",
            "And this project has a test called",
            "aRenameBreaksTheOrderHistoryPage —",
            "which PASSES.",
            "",
            "A test suite tests a codebase. This lives between two.",
        ],
        narration=(
            "Here is the uncomfortable part, and it is the reason this problem "
            "survives in real companies for years. [[slnc 350]] Nobody did "
            "anything wrong. [[slnc 300]] The migration was correct. There is a "
            "test in this project that proves it: after the rename, every "
            "product name is still there, still readable, under its new name. "
            "Nothing was lost. [[slnc 350]] And the catalog team could not have "
            "known. The query that broke is in a different repository, written "
            "by people they may never have met. It is not in their code, not in "
            "their tests, not in their build. There is no review that would have "
            "caught this, because there is no reviewer who can see both sides. "
            "[[slnc 400]] And now the sharpest way I can put it. This project "
            "has a test named: a rename breaks the order history page. "
            "[[slnc 250]] That test passes. [[slnc 350]] Every test in the file "
            "passes, including the one asserting that a page is broken. Your "
            "test suite is never going to warn you about this, and it is not "
            "being careless. A test suite tests a codebase, and this problem "
            "lives in between two codebases. [[slnc 300]] Nobody owns the "
            "in-between."
        ),
    ),
    dict(
        key="08-filing-cabinet",
        kind="quote",
        title="The Shared Filing Cabinet",
        body=[
            "Two departments share one filing cabinet.",
            "",
            "It is easy. A question spanning both is one trip",
            "to one drawer. Nothing is out of date. There is",
            "only one order, so everything is in it.",
            "",
            "Then one department reorganises their half —",
            "carefully, correctly, and entirely within their",
            "rights. The other comes in on Monday and cannot",
            "find anything.",
            "",
            "So they buy a second cabinet.",
        ],
        narration=(
            "Let me leave the code for a moment, because there is an ordinary "
            "version of this that everybody has lived through. [[slnc 350]] Two "
            "departments in an office share one filing cabinet. [[slnc 300]] "
            "While they share it, life is easy. A question that spans both "
            "departments is one trip to one drawer. Nothing is ever out of date. "
            "The folders are all in the same order, because there is only one "
            "order. [[slnc 350]] And then one department decides to reorganise. "
            "They have every right to — it is their half of the cabinet, and the "
            "new arrangement suits their work far better. They do it carefully. "
            "They check their own work. Everything they need is exactly where "
            "they now expect it. [[slnc 300]] The other department comes in on "
            "Monday and cannot find anything. [[slnc 350]] Nobody was careless. "
            "The trouble is that the filing system was a shared decision that "
            "neither department was in charge of, and the only safe way to change "
            "it was a meeting that nobody thought to call. [[slnc 300]] So they "
            "buy a second cabinet. [[slnc 250]] Hold on to that image, because in "
            "a minute we are going to count what the second cabinet costs, and it "
            "is not nothing."
        ),
    ),
    dict(
        key="09-tempting-fixes",
        kind="bullets",
        title="Three Tempting Fixes",
        body=[
            "✗ \"Write a test that catches it.\" In whose",
            "  repository? A build that runs one team's queries",
            "  against another team's schema is a shared build",
            "  with a shared owner — the same coupling, in a hat.",
            "",
            "✗ \"Just don't rename columns.\" The one that really",
            "  gets adopted, and the worst, because nobody",
            "  writes it down.",
            "",
            "✗ \"Add a view so the old name still works.\" Real,",
            "  and it buys time. It does not change who decides.",
        ],
        narration=(
            "Before the fix, the three answers that come up in every room I have "
            "asked this in. [[slnc 350]] The first: write a test that catches it. "
            "Good instinct — but in whose repository does it live? For it to "
            "help, the catalog team's build would have to run the orders team's "
            "queries against the catalog team's schema. That is possible, and "
            "what you have then is a shared build with a shared owner, which is "
            "the coupling you were trying to remove wearing a different hat. "
            "[[slnc 400]] The second: just don't rename columns. [[slnc 250]] "
            "This is the one that actually gets adopted, and it is the worst of "
            "the three, because it is invisible. Nobody writes it down. The "
            "schema slowly fills up with columns whose names are wrong, and every "
            "person on both teams quietly learns that changing anything is "
            "expensive. [[slnc 400]] The third: add a database view so the old "
            "name still works. That is a real technique and it buys real time. "
            "But it does not change who is allowed to decide, and now there is "
            "one more layer maintained by somebody who owns neither side of it. "
            "[[slnc 350]] So here is the actual question. What if the catalog "
            "team's data were somewhere the orders team physically could not "
            "read?"
        ),
    ),
    dict(
        key="10-the-mechanism",
        kind="code",
        title="The Whole Mechanism",
        body="""public List<Order> ordersFor(String requester, String customerId) {
    if (!OWNER.equals(requester)) {
        throw new NotYourDataException(requester, OWNER);
    }
    ...
}

// Orders may not read Catalog's database directly.
// Ask Catalog for it.""",
        narration=(
            "And here is the entire mechanism. [[slnc 300]] Every method on "
            "every database takes the name of whoever is asking, and refuses "
            "anybody who is not the owner. That is it. There is no algorithm, "
            "nothing adaptive, nothing to configure. [[slnc 400]] Now the most "
            "important sentence in this video, and I am going to say it slowly. "
            "[[slnc 300]] In a real shop, nothing throws that exception. "
            "[[slnc 350]] The rule is not enforced in Java. It is not a "
            "convention, it is not a comment, and it is not a page on a wiki "
            "asking people not to. The orders service connects to the database "
            "with credentials that simply cannot see the catalog tables. An "
            "attempt to read them fails as a permissions error, long before it "
            "reaches any application code. [[slnc 350]] That exception exists in "
            "this project only so that the rule is visible in something small "
            "enough to read in one sitting. When you see it, read it as: the "
            "database refused. [[slnc 400]] And take the test away with you. If "
            "the rule in your system is a comment asking people not to, you do "
            "not have this pattern. You have a wish."
        ),
    ),
    dict(
        key="11-act-three",
        kind="console",
        title="Act Three — The Same Page, For More Money",
        body="""Act 3 - two databases, two calls, one assembly
      0ms ->   10ms  Orders       OK        2 order(s)
     10ms ->   10ms  OrderDb      QUERY     2 order(s) for cust-7
     10ms ->   20ms  Catalog      OK        2 name(s) in one call
     20ms ->   20ms  HistoryPage  ASSEMBLED 2 row(s) from 2 services
  the same page took 20ms and 2 service calls
  instead of 1 query""",
        narration=(
            "So the shop splits. Orders gets its own database, catalog gets its "
            "own database, and now we have to rebuild that page without a join. "
            "[[slnc 350]] It goes like this. Ask the orders service what this "
            "customer bought. What comes back is product codes and quantities, "
            "and no names at all, because orders does not have the names. "
            "[[slnc 300]] Then collect the product codes. Ask the catalog "
            "service what those codes are called. [[slnc 250]] Then stitch the "
            "two answers together in Java. [[slnc 350]] And the page that comes "
            "out is identical. A test in this project asserts exactly that: same "
            "rows, same names, same order, the assembled page says precisely "
            "what the joined page said. [[slnc 300]] That is what makes the "
            "comparison fair — and it is what makes the next number mean "
            "something. [[slnc 350]] Twenty milliseconds and two service calls, "
            "for a page that used to be one query. The cost changed. The answer "
            "did not."
        ),
    ),
    dict(
        key="12-ask-once",
        kind="bullets",
        title="Ask Once For Many, Or This Gets Much Worse",
        body=[
            "catalog.namesFor(skus) takes a LIST.",
            "",
            "That is not a convenience method.",
            "",
            "One call per row would make this 2-row page cost",
            "2 network calls — and a 50-row page cost 50.",
            "That is how a page becomes an outage.",
            "",
            "itAsksCatalogOnce pins it: one call, whatever the",
            "row count.",
            "",
            "And a customer with no orders never calls Catalog.",
        ],
        narration=(
            "One detail in there is doing far more work than it looks. "
            "[[slnc 300]] The call to the catalog service takes a list of "
            "product codes, and returns all of the names in a single answer. "
            "[[slnc 350]] That is not a convenience method, and it is not "
            "tidiness. Asking once per row would turn this two-row page into two "
            "network calls, a fifty-row page into fifty, and a report into an "
            "outage. It is the single most common way this pattern gets "
            "implemented badly, and it usually happens by accident, because "
            "asking for one name at a time reads perfectly naturally in a loop. "
            "[[slnc 350]] So there is a test that asserts the catalog service is "
            "called exactly once, no matter how many rows the page has. "
            "[[slnc 300]] And one more, which is the cheapest call of all: a "
            "customer with no orders never troubles the catalog service at all. "
            "There is nothing to name, so nobody is asked. [[slnc 300]] The "
            "batch call is the difference between an assembly step and a "
            "disaster."
        ),
    ),
    dict(
        key="13-roles",
        kind="diagram",
        title="Who Owns What",
        body=None,
        narration=(
            "Let me name the pieces, because each one has exactly one job. "
            "[[slnc 300]] On one side is the design being replaced: a single "
            "schema holding both teams' tables, and one method that builds the "
            "whole page with a join. When a team renames a column in it, what "
            "comes out is an exception in somebody else's repository — and I want "
            "to stress again that this is not a bug in anybody's code. "
            "[[slnc 350]] On the other side is the split. The orders service, "
            "which owns the order rows and reads its own database as, quite "
            "literally, Orders. The catalog service, which owns the product rows "
            "and reads its own database as Catalog. [[slnc 300]] Between them "
            "sits the order history page, and that class is the price of this "
            "pattern made concrete. Ask orders, ask catalog once for all the "
            "names, stitch the two answers together. It exists because the join "
            "does not. [[slnc 350]] And the refusal. When anybody but the owner "
            "asks, the database throws — and the message names who asked and "
            "whose data it was, which is a far more useful thing to be woken up "
            "by than a permissions error with no story attached. [[slnc 300]] "
            "One last piece: the call log. Both designs return exactly the same "
            "page, so the only way to see the difference between them is to count "
            "the calls and read the clock. That is why the demo prints a timeline "
            "rather than printing the page. [[slnc 350]] And nothing in this "
            "project sleeps. A simulated clock moves forward ten milliseconds per "
            "service call, so the timings are exact, repeatable and free."
        ),
    ),
    dict(
        key="14-act-four",
        kind="console",
        title="Act Four — The Same Rename, Now A Non-Event",
        body="""Act 4 - the same rename, against a database Catalog owns
  ord-101   SKU-KETTLE   Stainless Steel Kettle       x1
  ord-102   SKU-MUG      Blue Stoneware Mug           x4
  the page is unchanged. Nothing outside Catalog ever
  named that column.""",
        narration=(
            "Now run Tuesday again. [[slnc 300]] The catalog team renames "
            "product name to title, exactly as before — except this time the "
            "column is in a database that only they can read. [[slnc 350]] The "
            "rows change, and the queries that read those rows change in the same "
            "class, in the same commit, tested together, by the same people. "
            "[[slnc 300]] And the order history page is unchanged. "
            "[[slnc 400]] That is the payoff, and notice how quiet it is. "
            "Nothing happened. That is the whole point. [[slnc 350]] But be "
            "precise about what has just been bought, because this is the moment "
            "people oversell it. [[slnc 300]] It bought no speed. Act three was "
            "slower than act one — twenty milliseconds and two calls instead of "
            "one query. [[slnc 250]] It bought no correctness. The page was "
            "already right. [[slnc 350]] What it bought is that the catalog team "
            "can change their mind without asking permission, and can deploy that "
            "change without coordinating a release with a team they have never "
            "met. [[slnc 300]] That is an organisational benefit, and it is the "
            "only one on offer. Which gives you the test for whether to do this "
            "at all: if the two teams are the same three people, you are paying an "
            "organisational price to solve an organisational problem you do not "
            "have."
        ),
    ),
    dict(
        key="15-act-five",
        kind="console",
        title="Act Five — The Bill",
        body="""Act 5 - what it cost
  a) Orders may not read Catalog's database directly.
  b) Catalog deletes a product an order refers to:
  ord-101   SKU-KETTLE   (no longer in the catalogue) x1
     the row survives with no name. A foreign key would
     have refused the delete.
     that rule now lives in code and in agreements
     between teams, not in the database.""",
        narration=(
            "And now the bill, because any explanation that stops before here is "
            "selling you something. [[slnc 350]] Two things were given up, and "
            "the second is the one people forget. [[slnc 300]] The first is the "
            "join. Every question that spans both services is now two calls and "
            "a piece of code. That is fine for an order history page. It is "
            "considerably less fine for the report somebody in finance runs on a "
            "Monday morning, which used to be one statement with three joins and "
            "now has nowhere to live. [[slnc 400]] The second is the foreign key, "
            "and this one is worse. [[slnc 300]] Watch what happens. The catalog "
            "team deletes a product. An order still refers to it. And nothing "
            "stops the delete — nothing can, because the two rows are in "
            "different databases and no constraint can span them. [[slnc 350]] "
            "So the order survives, naming a product that the catalogue has never "
            "heard of, and something has to decide what to put on the page. Here "
            "it prints: no longer in the catalogue. [[slnc 350]] And the page "
            "surviving is the good news and the bad news at the same time. A rule "
            "that used to be impossible to break is now merely impolite to break. "
            "It has moved out of the database and into code, into tests, and into "
            "agreements between teams — which is to say, into hope."
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the passing test that",
            "asserts a page is broken, and the one that proves an order",
            "can outlive the product it names.",
        ],
        narration=(
            "That's database per service. [[slnc 250]] The full source, the "
            "written notes, the diagrams and an animated walkthrough are all in "
            "the repository, and everything runs offline with nothing installed "
            "but a Java development kit. [[slnc 300]] There is no real database "
            "in this project, and that is deliberate: the tables are maps, and a "
            "column is a key in a map, which is what lets a rename be a real "
            "rename rather than a story about one. The subject here is who is "
            "allowed to read what, and that is a question about ownership, not "
            "about SQL. [[slnc 350]] If you try one exercise, try this one. Take "
            "the order history page and change it to ask the catalog service for "
            "one name at a time, in a loop, instead of asking once for all of "
            "them. Watch the test fail, and then read the timeline. Then imagine "
            "fifty rows. [[slnc 300]] And then the harder question, which no "
            "exercise can answer for you. Take a schema you actually work on, and "
            "draw one line through it. Which tables end up on each side? Which "
            "query that exists today would stop working? And where would that "
            "query live afterwards? [[slnc 350]] If the answer is that it would "
            "have nowhere to live, that is not a reason to give up — it is the "
            "question the next pattern in this series exists to answer. "
            "[[slnc 300]] Because the real lesson here is this. The mechanism is "
            "a refusal, and you already know how to write it. Deciding where the "
            "line goes, and admitting out loud that you are trading a guarantee "
            "for the ability to move, is the part that needs a person. "
            "[[slnc 300]] If this helped, a like genuinely does help other people "
            "find it, and subscribe if you would like the rest of the series. "
            "[[slnc 250]] Thanks for watching, and I'll see you in the next one."
        ),
    ),
]
