"""Scene definitions for the Database per Service with Containers teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count and error code out loud, says each of Postgres's
and MongoDB's words in plain language before using the tool's name for it, and
never points at a picture the listener cannot see. Every figure is the output
of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Database per Service with Containers',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Database per Service '
            'pattern in Java, using two real databases: PostgreSQL and '
            'MongoDB. [[slnc 250]] It is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] Here is the plain definition, in general '
            'words. Each service keeps its own data, in its own database. No '
            'other service may read that database directly. If you want '
            'somebody else\'s data, you ask them for it. [[slnc 350]] Now the '
            'same thing in our online store. The shop has an Orders team and '
            'a Catalog team. Orders knows what each customer bought. Catalog '
            'knows what each product is called, what it costs, and how many '
            'are on the shelf. Each team gets a database of its own, and in '
            'this video they are two different kinds of database. '
            '[[slnc 300]] By the end you will have seen one shared database '
            'work well and then break, the split survive the same change, and '
            'the old join tried against two real engines. One of them refuses '
            'it out loud. The other one says nothing at all.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Customer cust-7 has two orders:', '  ord-101: 1 Stainless Steel Kettle',
              '  ord-102: 4 Blue Stoneware Mugs', '',
              'The order history page belongs to Orders.', 'It shows each order with its product name.', '',
              'The names belong to Catalog.', '',
              'The hand-built twin kept both databases', 'as maps inside one Java program.'],
        narration=(
            'Here is the scenario. Customer cust-7 has two orders. Order one '
            'oh one is one Stainless Steel Kettle. Order one oh two is four '
            'Blue Stoneware Mugs. [[slnc 250]] The order history page belongs '
            'to the Orders team. It shows each order with the product\'s name '
            'beside it. But the names belong to the Catalog team. So the page '
            'needs data from both teams. [[slnc 300]] The hand-built twin of '
            'this project told this story with two maps inside one Java '
            'program. This time the data lives in real databases, each in a '
            'container that the demo starts at the beginning and removes at '
            'the end.'
        ),
    ),
    dict(
        key='03-pg-words', kind='bullets', title="Postgres's Words",
        body=['Table: fixed columns, like a spreadsheet.', 'SQL: the language for asking it.', '',
              'Join: one answer from two tables.', 'Foreign key: a rule the database keeps.',
              'Transaction: changes kept or undone', '  together. Undoing them: rollback.', '',
              'Every error carries a 5-character code.'],
        narration=(
            'Before the first act, some words, each in plain language first. '
            '[[slnc 250]] PostgreSQL, usually called Postgres, keeps data in '
            'tables. Think of a spreadsheet with fixed column headings, where '
            'every row fills in the same columns. It is asked questions in a '
            'language called SQL. [[slnc 250]] Postgres can answer one '
            'question from two tables at once, by matching a value in one '
            'with a value in the other. That is called a join. [[slnc 250]] '
            'It can also keep a rule between two tables: a value in one must '
            'exist in the other. It refuses any change that would break the '
            'rule. That rule is called a foreign key. [[slnc 250]] And a group '
            'of changes that are kept together or undone together is a '
            'transaction. Undoing it is a rollback. [[slnc 250]] Every error '
            'Postgres gives has a five-character code, and the video will say '
            'those codes out loud.'
        ),
    ),
    dict(
        key='04-one', kind='console', title='One Shared Database',
        body="""ONE. One shared database: Postgres.
  database shop: products, orders,
  and a foreign key between them.

  the page is one SQL join:
    ord-101  Stainless Steel Kettle  x1
    ord-102  Blue Stoneware Mug      x4
  round trips to a database: 1

  delete SKU-KETTLE. Postgres refuses:
    ERROR 23503: violates foreign key
    constraint "orders_sku_fkey\"""",
        narration=(
            'Act one. Both teams keep their tables in one Postgres database, '
            'called shop. Catalog owns the products table. Orders owns the '
            'orders table. And a foreign key says every order must name a '
            'product that exists. [[slnc 250]] The order history page is one '
            'SQL join. Both rows come back with their names, and it takes one '
            'round trip: one question sent to the database. [[slnc 300]] Then '
            'the Catalog team tries to delete the kettle, which order one oh '
            'one still names. Postgres refuses, with error two three five '
            'zero three: the foreign key would be broken. [[slnc 250]] This '
            'is the arrangement working well. Fast, correct, and guarded by '
            'the database itself.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='The Rename',
        body="""TWO. Catalog renames product_name to title.
  ALTER TABLE products RENAME COLUMN
  product_name TO title: done.
  Catalog's own queries updated, tests green.

  the order history page, owned by Orders:
    ERROR 42703: column p.product_name
    does not exist

  nobody did anything wrong.""",
        narration=(
            'Act two. The Catalog team renames its column, from product name '
            'to title. The change is correct. They update their own queries, '
            'and their tests pass. [[slnc 250]] But the order history page '
            'belongs to the Orders team, and its query still names the old '
            'column. Postgres answers with error four two seven zero three: '
            'the column does not exist. [[slnc 300]] Nobody did anything '
            'wrong. The column was Catalog\'s. The query naming it was '
            'Orders\'. The break lives between two teams, where no test suite '
            'looks.'
        ),
    ),
    dict(
        key='06-mongo-words', kind='bullets', title="MongoDB's Words",
        body=['MongoDB: a document database.', '', 'Document: one record of named fields,',
              '  like one filled-in form.', 'Collection: a drawer of documents.',
              'Two documents need not share fields.', '',
              'Find: fetch the documents that match.', '$lookup: its join, into another',
              '  collection in the same database.'],
        narration=(
            'Now the second engine, and its words. [[slnc 250]] MongoDB is a '
            'document database. Think of a drawer of filled-in forms, where '
            'each form can have its own set of boxes. Each form is what '
            'MongoDB calls a document: one record of named fields. A drawer '
            'of them is a collection. There are no tables, and two documents '
            'in one collection need not have the same fields. [[slnc 250]] '
            'Asking MongoDB for the documents that match is called a find. '
            '[[slnc 250]] And MongoDB has its own kind of join. For each '
            'document, it attaches the matching documents from another '
            'collection in the same database. That step is called lookup, '
            'written with a dollar sign in front.'
        ),
    ),
    dict(
        key='07-three', kind='console', title='Two Services, Two Engines',
        body="""THREE. Two services, two engines.
  Orders: Postgres 18.6, 1 table.
  Catalog: MongoDB 8.3.11, 1 collection.
    SKU-KETTLE: ..., stock, wattage
    SKU-MUG: ..., stock, capacityMl

  one SQL query, one find, joined in Java:
  round trips to a database: 2

  rename name to title in every document:
  MongoDB changed 2 documents.
  the page is unchanged.""",
        narration=(
            'Act three is the split. Orders keeps Postgres, in a database of '
            'its own, holding one table. Catalog moves to MongoDB, in a '
            'database of its own, holding one collection of documents. '
            '[[slnc 250]] The kettle\'s document has a wattage. The mug\'s has '
            'a capacity in millilitres. Nobody changed a table to allow '
            'either. That is the usual reason a team wants its own database: '
            'a different kind of store that suits its data. [[slnc 300]] The '
            'page is now two questions. One SQL query to Orders for the '
            'customer\'s orders. One find to Catalog for both names at once. '
            'Java puts the answers side by side. Two round trips, where the '
            'join took one. [[slnc 300]] Then the Catalog team renames its '
            'name field to title, in every document. MongoDB changed two '
            'documents. The page is unchanged, because nothing outside '
            'Catalog ever named that field.'
        ),
    ),
    dict(
        key='08-diagram', kind='diagram', title='Who Can Reach What',
        body=None,
        narration=(
            'Here is who can reach what, in words. The order history page '
            'asks the Orders service, and then asks the Catalog service. The '
            'Orders service holds one connection, to its own Postgres '
            'database, and nothing else. The Catalog service holds one '
            'client, for its own MongoDB database, and nothing else. '
            '[[slnc 300]] Between the two databases there is no line at all. '
            'No join, no foreign key, and no shared transaction. No engine '
            'holds both halves. Hold on to that, because the next act tries '
            'to cross that gap anyway.'
        ),
    ),
    dict(
        key='09-code', kind='code', title='The Whole Pattern, In Two Constructors',
        body="""public OrderService(Postgres postgres, ...) {
    this.connection =
        postgres.connectTo("orders");
}

public CatalogService(Mongo mongo, ...) {
    this.client = mongo.newClient();
    this.products = client
        .getDatabase("catalog")
        .getCollection("products");
}""",
        narration=(
            'In the code, the whole pattern is two constructors. The Orders '
            'service is handed Postgres, and opens a connection to one '
            'database, called orders. The Catalog service is handed MongoDB, '
            'and opens a client for one database, called catalog, and one '
            'collection, called products. [[slnc 300]] What matters is what '
            'they are not handed. The Orders service has no MongoDB address '
            'and no MongoDB password. The Catalog service has no Postgres '
            'connection. The hand-built twin needed an exception class to say '
            'you may not. Here nothing says it. The rule is the wiring.'
        ),
    ),
    dict(
        key='10-four', kind='console', title='The Join, Tried Anyway',
        body="""FOUR. The join, tried anyway.
  from Orders, the old SQL join:
    ERROR 42P01: relation "products"
    does not exist
  across to shop, on the same server:
    ERROR 0A000: cross-database
    references are not implemented
  from Catalog, $lookup into orders:
    no error. 2 products came back:
    SKU-KETTLE with 0 orders,
    SKU-MUG with 0 orders.""",
        narration=(
            'Act four is the headline of this project. The old join is tried '
            'from both sides. [[slnc 250]] From the Orders side, the old SQL. '
            'Postgres answers with error four two P zero one: there is no '
            'table called products here. Then a reach across to the shop '
            'database, which sits on the very same Postgres server. Error '
            'zero A zero zero zero: cross-database references are not '
            'implemented. Postgres will not even join two of its own '
            'databases. [[slnc 300]] From the Catalog side, MongoDB\'s own '
            'join, pointed at a collection called orders. MongoDB has no such '
            'collection. The orders are in Postgres. And it does not '
            'complain. It treats the missing collection as empty, and hands '
            'back both products, each with zero orders. [[slnc 300]] That '
            'quiet answer is the dangerous one. A report built on it would '
            'say nobody ever bought a kettle, and no log anywhere would say '
            'why. The join is not forbidden. It cannot be written.'
        ),
    ),
    dict(
        key='11-five', kind='console', title='No Foreign Key Between Engines',
        body="""FIVE. No foreign key between two engines.
  Catalog deletes SKU-KETTLE:
  MongoDB deleted 1 document.
  nothing refused.

  Postgres still holds 1 order naming it.
    ord-101  (no longer in the catalogue)
    ord-102  Blue Stoneware Mug      x4

  in act ONE Postgres refused this delete.""",
        narration=(
            'Act five. The Catalog team deletes the kettle. MongoDB deleted '
            'one document, and nothing refused. [[slnc 250]] Postgres still '
            'holds one order naming the kettle, and it has no way of knowing '
            'the kettle has gone. The page has to decide what to show, and it '
            'shows: no longer in the catalogue. [[slnc 300]] In act one, '
            'Postgres refused this exact delete. Across two engines, nothing '
            'can. The rule that used to live in the database now lives in '
            'code, and in agreements between teams.'
        ),
    ),
    dict(
        key='12-six', kind='console', title='The Bill',
        body="""SIX. The bill.
  cust-7 checks out 2 more mugs.
  Orders: ord-103, in a Postgres transaction.
  Catalog: 2 mugs off the shelf in MongoDB.
  payment declined. Orders rolls back.
  Postgres: ord-103 is gone. orders: 2.
  MongoDB: SKU-MUG stock 38, was 40.

  MongoDB is stopped. the page:
    ord-101  (catalog unreachable)   x1
  2 containers, 2 drivers, 2 languages.""",
        narration=(
            'Act six is the bill. Customer cust-7 checks out two more mugs. '
            'Orders writes order one oh three inside a Postgres transaction. '
            'Catalog takes two mugs off the shelf in MongoDB. [[slnc 250]] '
            'Then the payment is declined, and Orders rolls back. Postgres '
            'forgets the order: the customer has two orders again. MongoDB '
            'keeps its change: thirty eight mugs, where there were forty. The '
            'rollback reached one engine, not both. In the shared database, '
            'the stock and the order would have been one transaction. '
            '[[slnc 300]] Then MongoDB is stopped. The page asks Orders, which '
            'answers. It asks Catalog, which does not. Every name reads: '
            'catalog unreachable. The page is half there. [[slnc 250]] And the '
            'shop now runs two containers, two drivers and two query '
            'languages, where it had one of each.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['✓ The whole argument: one join, a foreign', '   key, a rename that breaks somebody else.',
              '✓ The split: two calls, the rename harmless.', '',
              '✗ Two genuinely different engines.', '✗ A join that answers nothing, quietly.',
              '✗ A rollback that stops at its engine.', '✗ One database down, the other up.'],
        narration=(
            'So what did the hand-built simulation get right? The whole '
            'argument. One shared database answers the page in one join, and '
            'a foreign key protects it. A correct rename breaks somebody '
            'else\'s page. The split does the same page in two calls, and the '
            'rename becomes harmless. [[slnc 300]] What it left out was '
            'everything that needs real engines. Its two databases were the '
            'same kind of thing, so it could not show a team choosing a '
            'different store for different data. Its refusal was an exception '
            'it wrote itself, so it could not show a real engine answering a '
            'join with a quiet nothing. It had no transactions, so no '
            'rollback could stop halfway. And a map in memory is never down.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Two teams breaking each other? Give each', 'service its own database, and let each',
              'pick the engine that suits its data.', '',
              'Then say out loud what that gives up:', '1. the join: two questions and some code',
              '2. the foreign key: an agreement', '3. one transaction: two that can disagree',
              '4. both up: one can be down'],
        narration=(
            'The verdict. When two teams keep breaking each other, give each '
            'service its own database, and let each pick the engine that '
            'suits its data. [[slnc 250]] Then say out loud what that gives '
            'up. One. The join becomes two questions and some code. '
            '[[slnc 200]] Two. The foreign key becomes an agreement between '
            'teams. [[slnc 200]] Three. One transaction becomes two, and they '
            'can disagree. [[slnc 200]] Four. One engine can be down while '
            'the other is up. [[slnc 250]] And never trust an answer of '
            'nothing from a join, until you know where the other half lives.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['Postgres 18.6 and MongoDB 8.3.11,', 'JDBC 42.7.13, MongoDB driver 5.12.0,',
              'Testcontainers 2.0.5: two containers', 'the demo starts and removes.', '',
              'Too much for one small team: one database', 'keeps the join, the key and one transaction.',
              'Same shape of data? Two databases on one', 'engine is often enough.'],
        narration=(
            'What is real here? Two real databases. Postgres, version '
            'eighteen point six, and MongoDB, version eight point three point '
            'eleven, the newest releases, each in its own container. The demo '
            'starts both at the beginning and removes both at the end, each '
            'on a random free port. Java talks to them through the newest '
            'Postgres driver and the newest MongoDB driver. The one thing you '
            'need is a container runtime, such as Docker Desktop, switched on '
            'before you start. Every number and every error code in this '
            'video comes from the program\'s own output, and two runs one '
            'after the other print the same thing. [[slnc 300]] So when is '
            'this too much? If one small team owns both halves, one database '
            'keeps the join, the foreign key and the single transaction. And '
            'if the two teams\' data has the same shape, two databases on one '
            'engine is often enough. A second engine is one more thing to '
            'back up, upgrade, watch and learn.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Database per Service with Containers. [[slnc 250]] If you "
            'take one sentence away, take this one: once each service has its '
            'own engine, the join is not forbidden, it is impossible, and one '
            'engine will not even tell you. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are all '
            'in the repository. [[slnc 300]] If you try one exercise, create a '
            'real orders collection in the catalog database with one document '
            'in it, guess what the lookup will say, and then run it. '
            '[[slnc 300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of the '
            'series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
