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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Database per Service pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Each service keeps '
            'its own data. [[slnc 300]] Nobody else may read that data '
            "directly. [[slnc 300]] If you want another service's data, "
            'you ask that service for it. [[slnc 600]] Think of two '
            'departments in an office, each with its own filing cabinet. '
            '[[slnc 300]] If you need something from the other '
            'department, you ask them. [[slnc 300]] You do not go through '
            'their drawers. [[slnc 600]] There is no clever algorithm in '
            'this pattern. [[slnc 300]] The interesting part is not how '
            'you do it, but what it costs. [[slnc 700]] In our online '
            'store, there are two teams. [[slnc 300]] One looks after '
            'products: names, prices, and photographs. [[slnc 300]] The '
            'other looks after what people have bought. [[slnc 300]] They '
            'share one database, and one Tuesday afternoon, somebody '
            'renames a column. [[slnc 500]] By the end, you will know why '
            "a perfectly correct change breaks a page in another team's "
            'code. [[slnc 300]] Why every test can pass while the system '
            'is broken. [[slnc 300]] What splitting the database really '
            'buys. [[slnc 300]] And what it takes away.'
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
            'Here is the shop. [[slnc 400]] There are two teams. [[slnc '
            '300]] The catalog team looks after products: names, '
            'descriptions, prices, and photographs. [[slnc 300]] The '
            'orders team looks after what people have bought. [[slnc '
            '600]] They share one database. [[slnc 300]] The products '
            'table and the orders table sit side by side. [[slnc 300]] '
            'And either team can read both. [[slnc 600]] We follow one '
            'page: the order history page. [[slnc 300]] Each line shows '
            "an order number, a product code, the product's name, and how "
            'many were bought. [[slnc 500]] Here is the key point. [[slnc '
            '300]] The product code lives in the orders table. [[slnc '
            '300]] The product name lives in the products table. [[slnc '
            '300]] So building the page means reading both. [[slnc 500]] '
            'Two teams, one shared database, and nobody really in charge '
            'of it.'
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
            'In this project, there is no real database. [[slnc 300]] '
            'Each table is a simple map, and each column is a key in that '
            'map. [[slnc 300]] But the shape is exactly a database join. '
            '[[slnc 300]] A join reads two tables together, and matches '
            'their rows up. [[slnc 600]] For every order, find the '
            "matching product. [[slnc 300]] Read the product's name. "
            '[[slnc 300]] And build a line from the two halves. [[slnc '
            '600]] Now notice one detail, because it is the whole video. '
            '[[slnc 300]] The code asks for a column by name: product '
            "name. [[slnc 500]] That name is written in the orders team's "
            'code. [[slnc 300]] But the column belongs to the catalog '
            'team. [[slnc 500]] Nobody thinks about that when they write '
            'it. [[slnc 300]] In one shared database, that is simply how '
            'you read a table.'
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
            'First demo: one database, one query. [[slnc 400]] And it '
            'works. [[slnc 500]] Two orders come back for this customer. '
            '[[slnc 300]] One stainless steel kettle. [[slnc 300]] And '
            'four blue stoneware mugs. [[slnc 300]] Each line has the '
            'order number, the product code, the name, and the quantity. '
            '[[slnc 300]] The page is complete. [[slnc 600]] It took one '
            'trip to one database. [[slnc 300]] Remember that number, '
            'one. [[slnc 300]] Later, we will compare against it.'
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
            "Before we break it, let's be fair to this design. [[slnc "
            '300]] It is very good. [[slnc 600]] One trip to one '
            'database, and the page is done. [[slnc 500]] The join is '
            'done by a database engine that has been perfected for '
            'decades. [[slnc 300]] And you did not have to write any of '
            'it. [[slnc 500]] A join cannot forget a name. [[slnc 300]] '
            'Either every line comes back complete, or the query fails. '
            '[[slnc 300]] There is no half-built page. [[slnc 500]] And a '
            'foreign key guarantees that the product an order refers to '
            'really exists. [[slnc 300]] A foreign key is a rule inside '
            'the database that links two tables. [[slnc 300]] The '
            'database will refuse an order that points at a product that '
            'is not there. [[slnc 500]] Nothing here is ever out of date. '
            '[[slnc 300]] What you read is what is true, right now. '
            '[[slnc 600]] So here is a sentence many talks leave out. '
            '[[slnc 300]] If a shop can live like this, it should.'
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
            'Second demo: Tuesday afternoon. [[slnc 400]] The catalog '
            'team decides that the column called product name should be '
            'called title. [[slnc 300]] They have good reasons. [[slnc '
            '300]] It is their column, in their table. [[slnc 600]] So '
            'they write a change to the database, called a migration. '
            '[[slnc 300]] They run it. [[slnc 300]] Their tests pass. '
            '[[slnc 300]] Their service works. [[slnc 300]] They go home. '
            '[[slnc 600]] And the order history page is dead. [[slnc '
            '500]] It asked for a column called product name. [[slnc '
            '300]] And there is no longer a column with that name. [[slnc '
            '600]] The catalog team saw a successful release. [[slnc '
            '300]] The orders team saw an outage. [[slnc 300]] Both are '
            'true at the same moment. [[slnc 300]] And neither team can '
            'see the other.'
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
            'Here is the uncomfortable part. [[slnc 400]] Nobody did '
            'anything wrong. [[slnc 600]] The migration was correct. '
            '[[slnc 300]] A test proves that every product name is still '
            'there, under its new name. [[slnc 300]] Nothing was lost. '
            '[[slnc 500]] And the catalog team could not have known. '
            "[[slnc 300]] The code that broke is in a different team's "
            'project. [[slnc 300]] It is not in their code, their tests, '
            'or their build. [[slnc 300]] No reviewer could have seen '
            'both sides. [[slnc 600]] Here is the sharpest way to say it. '
            '[[slnc 300]] This project has a test named: a rename breaks '
            'the order history page. [[slnc 300]] And that test passes. '
            '[[slnc 500]] Every test passes, including the one that says '
            'a page is broken. [[slnc 300]] A test suite checks one '
            'codebase. [[slnc 300]] This problem lives between two '
            'codebases. [[slnc 300]] And nobody owns the space in '
            'between.'
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
            "Let's leave the code for a moment. [[slnc 300]] There is an "
            'everyday version of this. [[slnc 500]] Two departments in an '
            'office share one filing cabinet. [[slnc 300]] While they '
            'share it, life is easy. [[slnc 300]] Any question is one '
            'trip to one drawer. [[slnc 300]] Nothing is ever out of '
            'date. [[slnc 600]] Then one department reorganises its half. '
            '[[slnc 300]] They have every right to. [[slnc 300]] They do '
            'it carefully, and check their own work. [[slnc 500]] On '
            'Monday, the other department cannot find anything. [[slnc '
            '600]] Nobody was careless. [[slnc 300]] The filing system '
            'was a shared decision that neither department owned. [[slnc '
            '300]] The only safe way to change it was a meeting that '
            'nobody thought to call. [[slnc 600]] So they buy a second '
            'cabinet. [[slnc 300]] Remember that, because soon we will '
            'count what the second cabinet costs.'
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
            'Before the real fix, here are three tempting fixes. [[slnc '
            '600]] The first: write a test that catches it. [[slnc 300]] '
            'But in whose project does that test live? [[slnc 300]] It '
            "would have to run one team's queries against the other "
            "team's database. [[slnc 300]] That is a shared build with a "
            'shared owner. [[slnc 300]] The same problem, in a different '
            'disguise. [[slnc 600]] The second: just never rename '
            'columns. [[slnc 300]] This is the one that really gets '
            'adopted, and it is the worst. [[slnc 300]] Nobody writes it '
            'down. [[slnc 300]] The database slowly fills with badly '
            'named columns. [[slnc 300]] And everyone learns that '
            'changing anything is expensive. [[slnc 600]] The third: add '
            'a database view, so the old name still works. [[slnc 300]] '
            'That is a real technique, and it buys time. [[slnc 300]] But '
            'it does not change who is allowed to decide. [[slnc 300]] '
            'And it adds one more layer that nobody owns. [[slnc 600]] So '
            'here is the real question. [[slnc 300]] What if the orders '
            "team simply could not read the catalog team's data at all?"
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
            'Here is the whole mechanism. [[slnc 400]] Every database '
            'method takes the name of whoever is asking. [[slnc 300]] And '
            'it refuses anybody who is not the owner. [[slnc 300]] That '
            'is all. [[slnc 600]] Now the most important point in this '
            'video. [[slnc 300]] In a real shop, nothing in Java does '
            'this refusing. [[slnc 500]] The orders service connects to '
            'the database with a login that simply cannot see the catalog '
            'tables. [[slnc 300]] So any attempt to read them fails as a '
            'permissions error, inside the database. [[slnc 500]] The '
            "refusal in this project's Java code only exists so you can "
            'see the rule. [[slnc 300]] Think of it as: the database '
            'refused. [[slnc 600]] And here is a simple test for your own '
            'system. [[slnc 300]] If the rule is only a comment asking '
            'people not to, you do not have this pattern. [[slnc 300]] '
            'You have a wish.'
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
            'Third demo: the shop splits. [[slnc 400]] Orders gets its '
            'own database. [[slnc 300]] Catalog gets its own database. '
            '[[slnc 300]] Now we must rebuild the page without a join. '
            '[[slnc 600]] First, ask the orders service what this '
            'customer bought. [[slnc 300]] It returns product codes and '
            'quantities, but no names. [[slnc 300]] Because orders does '
            'not have the names. [[slnc 500]] Then ask the catalog '
            'service what those codes are called. [[slnc 500]] Then join '
            'the two answers together, in Java. [[slnc 600]] The page '
            'that comes out is identical. [[slnc 300]] A test checks '
            'that: same lines, same names, same order. [[slnc 500]] But '
            'it now takes twenty milliseconds, and two service calls. '
            '[[slnc 300]] It used to be one query. [[slnc 300]] The cost '
            'changed. [[slnc 300]] The answer did not.'
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
            'One small detail matters much more than it looks. [[slnc '
            '400]] The call to the catalog takes a whole list of product '
            'codes. [[slnc 300]] And returns all the names in one answer. '
            '[[slnc 600]] That is not just tidiness. [[slnc 300]] Asking '
            'once per line would make a two-line page cost two network '
            'calls. [[slnc 300]] A fifty-line page would cost fifty. '
            '[[slnc 300]] And a big report could cause an outage. [[slnc '
            '500]] This is the most common way this pattern goes wrong. '
            '[[slnc 300]] And it usually happens by accident, because '
            'asking one at a time in a loop looks natural. [[slnc 600]] '
            'So one test checks that the catalog is called exactly once, '
            'however many lines the page has. [[slnc 300]] And a customer '
            'with no orders never calls the catalog at all. [[slnc 300]] '
            'There is nothing to name, so nobody is asked.'
        ),
    ),
    dict(
        key="13-roles",
        kind="diagram",
        title="Who Owns What",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 300]] Each has one job. [[slnc "
            '600]] On one side is the design being replaced. [[slnc 300]] '
            "One shared database holding both teams' tables. [[slnc 300]] "
            'And one method that builds the whole page with a join. '
            '[[slnc 300]] When a team renames a column, the failure '
            "appears in the other team's code. [[slnc 600]] On the other "
            'side is the split. [[slnc 300]] The orders service owns the '
            'order data, in its own database. [[slnc 300]] The catalog '
            'service owns the product data, in its own database. [[slnc '
            '500]] Between them sits the order history page. [[slnc 300]] '
            'It asks orders, then asks catalog once for all the names, '
            'and joins the answers. [[slnc 300]] It exists because the '
            'database join no longer does. [[slnc 600]] Then there is the '
            'refusal. [[slnc 300]] When anyone but the owner asks, the '
            'database refuses. [[slnc 300]] And the message says who '
            'asked, and whose data it was. [[slnc 600]] Finally, the demo '
            'counts calls and reads a clock. [[slnc 300]] Both designs '
            'produce the same page, so that is the only way to see the '
            'difference. [[slnc 300]] And nothing sleeps. [[slnc 300]] A '
            'simulated clock moves ten milliseconds per call, so every '
            'run gives the same result.'
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
            'Fourth demo: Tuesday again. [[slnc 400]] The catalog team '
            'renames product name to title, just as before. [[slnc 300]] '
            'But this time, the column is in a database only they can '
            'read. [[slnc 600]] The data changes, and the code that reads '
            'it changes too. [[slnc 300]] In the same place, at the same '
            'time, tested together, by the same people. [[slnc 500]] And '
            'the order history page is unchanged. [[slnc 600]] That is '
            'the payoff. [[slnc 300]] Nothing happened, and that is the '
            'whole point. [[slnc 600]] But be precise about what was '
            'bought. [[slnc 300]] It bought no speed. [[slnc 300]] The '
            'split page was slower. [[slnc 300]] It bought no '
            'correctness. [[slnc 300]] The page was already right. [[slnc '
            '500]] What it bought is freedom. [[slnc 300]] The catalog '
            'team can change their mind without asking permission. [[slnc '
            '300]] And release without coordinating with a team they have '
            'never met. [[slnc 600]] That is a benefit for the '
            'organisation, and it is the only one on offer. [[slnc 300]] '
            'So if both teams are really the same three people, you are '
            'paying for a problem you do not have.'
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
            'Finally, the bill. [[slnc 400]] Two things were given up. '
            '[[slnc 300]] And people usually forget the second. [[slnc '
            '600]] The first is the join. [[slnc 300]] Every question '
            'that spans both services is now two calls, and some code. '
            '[[slnc 300]] That is fine for an order history page. [[slnc '
            '300]] It is much harder for a Monday finance report that '
            'used to be one query with three joins. [[slnc 600]] The '
            'second is the foreign key, and this one is worse. [[slnc '
            '500]] The catalog team deletes a product. [[slnc 300]] An '
            'order still refers to it. [[slnc 300]] And nothing stops the '
            'delete. [[slnc 300]] Nothing can, because the two rows are '
            'in different databases. [[slnc 500]] So the order survives, '
            'naming a product the catalog has never heard of. [[slnc '
            '300]] And something must decide what to show. [[slnc 300]] '
            'Here, the page says: no longer in the catalogue. [[slnc '
            '600]] A rule that used to be impossible to break is now only '
            'impolite to break. [[slnc 300]] It moved out of the '
            'database, and into code, tests, and agreements between '
            'teams.'
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
            "That's the Database per Service pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Each '
            'service owns its own data, which buys each team the freedom '
            'to change, and costs you the join and the foreign key. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 300]] It runs offline, with nothing installed except '
            'a Java development kit. [[slnc 500]] Here is one exercise to '
            'try. [[slnc 300]] Change the order history page to ask the '
            'catalog for one name at a time, in a loop. [[slnc 300]] '
            'Watch the test fail. [[slnc 300]] Then imagine a page with '
            'fifty lines. [[slnc 500]] And one question to think about. '
            '[[slnc 300]] Take a database you work on, and draw one line '
            'through it. [[slnc 300]] Which tables end up on each side? '
            '[[slnc 300]] And which query would stop working? [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
