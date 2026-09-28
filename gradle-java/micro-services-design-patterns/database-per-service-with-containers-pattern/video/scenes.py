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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Database per Service pattern in Java, using two real '
            'databases: PostgreSQL and MongoDB. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Each service keeps its own '
            'data, in its own database. [[slnc 300]] No other service may '
            'read that database directly. [[slnc 300]] If you want '
            "someone else's data, you ask them for it. [[slnc 700]] In "
            'our online store, there is an Orders team and a Catalog '
            'team. [[slnc 300]] Orders knows what each customer bought. '
            "[[slnc 300]] Catalog knows each product's name, price, and "
            'stock. [[slnc 300]] Each team gets a database of its own. '
            '[[slnc 300]] And here, they are two different kinds of '
            'database. [[slnc 500]] By the end, you will hear one shared '
            'database work well, and then break. [[slnc 300]] The split '
            'survive the same change. [[slnc 300]] And the old join tried '
            'against two real databases. [[slnc 300]] One refuses it out '
            'loud. [[slnc 300]] The other says nothing at all.'
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
            'Here is the scenario. [[slnc 400]] One customer has two '
            'orders. [[slnc 300]] Order one oh one is one Stainless Steel '
            'Kettle. [[slnc 300]] Order one oh two is four Blue Stoneware '
            'Mugs. [[slnc 600]] The order history page belongs to the '
            'Orders team. [[slnc 300]] It shows each order, with the '
            "product's name beside it. [[slnc 300]] But the names belong "
            'to the Catalog team. [[slnc 300]] So the page needs data '
            'from both teams. [[slnc 600]] The plain Java version told '
            'this story with two simple maps, inside one Java program. '
            '[[slnc 300]] This time, the data lives in real databases. '
            '[[slnc 300]] Each runs in a container that the demo starts '
            'at the beginning, and removes at the end.'
        ),
    ),
    dict(
        key='03-pg-words', kind='bullets', title="Postgres's Words",
        body=['Table: fixed columns, like a spreadsheet.', 'SQL: the language for asking it.', '',
              'Join: one answer from two tables.', 'Foreign key: a rule the database keeps.',
              'Transaction: changes kept or undone', '  together. Undoing them: rollback.', '',
              'Every error carries a 5-character code.'],
        narration=(
            'Before the first demo, some words, in plain language. [[slnc '
            '500]] PostgreSQL, usually called Postgres, keeps data in '
            'tables. [[slnc 300]] Think of a spreadsheet with fixed '
            'column headings. [[slnc 300]] Every row fills in the same '
            'columns. [[slnc 300]] You ask it questions in a language '
            'called S Q L. [[slnc 500]] Postgres can answer one question '
            'from two tables at once, by matching values between them. '
            '[[slnc 300]] That is called a join. [[slnc 500]] It can also '
            'keep a rule between two tables. [[slnc 300]] A value in one '
            'must exist in the other. [[slnc 300]] That rule is called a '
            'foreign key, and Postgres refuses any change that breaks it. '
            '[[slnc 500]] A group of changes that are kept together, or '
            'undone together, is called a transaction. [[slnc 300]] '
            'Undoing it is called a rollback.'
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
            'First demo: one shared database. [[slnc 400]] Both teams '
            'keep their tables in one Postgres database. [[slnc 300]] '
            'Catalog owns the products table. [[slnc 300]] Orders owns '
            'the orders table. [[slnc 300]] And a foreign key says every '
            'order must name a product that exists. [[slnc 600]] The '
            'order history page is one S Q L join. [[slnc 300]] Both '
            'orders come back with their names. [[slnc 300]] And it takes '
            'one round trip, meaning one question sent to the database. '
            '[[slnc 600]] Then the Catalog team tries to delete the '
            'kettle. [[slnc 300]] But order one oh one still names it. '
            '[[slnc 300]] So Postgres refuses, because the foreign key '
            'would be broken. [[slnc 500]] This is the shared database '
            'working well. [[slnc 300]] Fast, correct, and guarded by the '
            'database itself.'
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
            'Second demo: a rename. [[slnc 400]] The Catalog team renames '
            'its column, from product name to title. [[slnc 300]] The '
            'change is correct. [[slnc 300]] They update their own '
            'queries, and their tests pass. [[slnc 600]] But the order '
            'history page belongs to the Orders team. [[slnc 300]] And '
            'its query still uses the old column name. [[slnc 300]] '
            'Postgres answers with an error: that column does not exist. '
            '[[slnc 600]] Nobody did anything wrong. [[slnc 300]] The '
            'column belonged to Catalog. [[slnc 300]] The query that '
            'named it belonged to Orders. [[slnc 300]] The break lives '
            'between two teams, where no test suite looks.'
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
            'Now the second database, and its words. [[slnc 400]] MongoDB '
            'is a document database. [[slnc 300]] Think of a drawer of '
            'filled-in forms, where each form can have its own set of '
            'boxes. [[slnc 500]] Each form is called a document: one '
            'record of named fields. [[slnc 300]] A drawer of them is '
            'called a collection. [[slnc 300]] There are no tables. '
            '[[slnc 300]] And two documents in one collection do not need '
            'the same fields. [[slnc 500]] Asking MongoDB for matching '
            'documents is called a find. [[slnc 500]] MongoDB also has '
            'its own kind of join, called lookup. [[slnc 300]] For each '
            'document, it attaches the matching documents from another '
            'collection, in the same database.'
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
            'Third demo: the split. [[slnc 400]] Orders keeps Postgres, '
            'in a database of its own, with one table. [[slnc 300]] '
            'Catalog moves to MongoDB, in a database of its own, with one '
            "collection. [[slnc 600]] The kettle's document has a "
            "wattage. [[slnc 300]] The mug's document has a capacity in "
            'millilitres. [[slnc 300]] Nobody had to change a table to '
            'allow either. [[slnc 300]] That is a common reason for a '
            'team to want its own database: a kind of store that suits '
            'its data. [[slnc 600]] The page is now two questions. [[slnc '
            "300]] One S Q L query to Orders, for the customer's orders. "
            '[[slnc 300]] One find to Catalog, for both names at once. '
            '[[slnc 300]] Java puts the answers side by side. [[slnc '
            '300]] Two round trips, where the join took one. [[slnc 600]] '
            'Then the Catalog team renames its name field to title, in '
            'every document. [[slnc 300]] And the page is unchanged. '
            '[[slnc 300]] Because nothing outside Catalog ever named that '
            'field.'
        ),
    ),
    dict(
        key='08-diagram', kind='diagram', title='Who Can Reach What',
        body=None,
        narration=(
            'Here is who can reach what, in words. [[slnc 400]] The order '
            'history page asks the Orders service, and then the Catalog '
            'service. [[slnc 500]] The Orders service holds one '
            'connection, to its own Postgres database, and nothing else. '
            '[[slnc 300]] The Catalog service holds one connection, to '
            'its own MongoDB database, and nothing else. [[slnc 600]] '
            'Between the two databases, there is nothing at all. [[slnc '
            '300]] No join, no foreign key, and no shared transaction. '
            '[[slnc 300]] No database holds both halves. [[slnc 300]] '
            'Remember that, because the next demo tries to cross that gap '
            'anyway.'
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
            'In the code, the whole pattern is two constructors. [[slnc '
            '400]] The Orders service is given Postgres, and connects to '
            'one database, called orders. [[slnc 300]] The Catalog '
            'service is given MongoDB, and connects to one database, '
            'called catalog. [[slnc 600]] What matters is what they are '
            'not given. [[slnc 300]] The Orders service has no MongoDB '
            'address, and no MongoDB password. [[slnc 300]] The Catalog '
            'service has no Postgres connection. [[slnc 500]] The plain '
            'Java version needed special code to say: you may not. [[slnc '
            '300]] Here, nothing needs to say it. [[slnc 300]] The rule '
            'is in how things are connected.'
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
            'Fourth demo, and this is the headline of the project. [[slnc '
            '400]] The old join is tried from both sides. [[slnc 600]] '
            'From the Orders side, the old S Q L query. [[slnc 300]] '
            'Postgres answers with an error: there is no products table '
            'here. [[slnc 500]] Then the query reaches across to the old '
            'shared database, on the very same Postgres server. [[slnc '
            '300]] Another error: Postgres cannot join across two of its '
            "own databases. [[slnc 600]] From the Catalog side, MongoDB's "
            'own join, pointed at a collection called orders. [[slnc '
            '300]] MongoDB has no such collection. [[slnc 300]] The '
            'orders are in Postgres. [[slnc 500]] And MongoDB does not '
            'complain. [[slnc 300]] It treats the missing collection as '
            'empty. [[slnc 300]] And it returns both products, each with '
            'zero orders. [[slnc 600]] That quiet answer is the dangerous '
            'one. [[slnc 300]] A report built on it would say nobody ever '
            'bought a kettle. [[slnc 300]] And no log anywhere would say '
            'why. [[slnc 500]] The join is not forbidden. [[slnc 300]] It '
            'simply cannot be written.'
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
            'Fifth demo: no foreign key between two databases. [[slnc '
            '400]] The Catalog team deletes the kettle. [[slnc 300]] '
            'MongoDB deletes one document. [[slnc 300]] And nothing '
            'refuses. [[slnc 600]] Postgres still holds one order that '
            'names the kettle. [[slnc 300]] And it has no way of knowing '
            'the kettle has gone. [[slnc 300]] The page has to decide '
            'what to show. [[slnc 300]] It shows: no longer in the '
            'catalogue. [[slnc 600]] In the first demo, Postgres refused '
            'this exact delete. [[slnc 300]] Across two databases, '
            'nothing can. [[slnc 300]] That rule now lives in code, and '
            'in agreements between teams.'
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
            'Sixth demo: the bill. [[slnc 400]] The customer checks out '
            'two more mugs. [[slnc 300]] Orders writes order one oh '
            'three, inside a Postgres transaction. [[slnc 300]] Catalog '
            'takes two mugs off the shelf, in MongoDB. [[slnc 600]] Then '
            'the payment is declined, and Orders rolls back. [[slnc 300]] '
            'Postgres forgets the order. [[slnc 300]] The customer has '
            'two orders again. [[slnc 500]] But MongoDB keeps its change. '
            '[[slnc 300]] Thirty-eight mugs, where there were forty. '
            '[[slnc 300]] The rollback reached one database, not both. '
            '[[slnc 300]] In the shared database, the stock and the order '
            'would have been one transaction. [[slnc 600]] Then MongoDB '
            'is stopped. [[slnc 300]] The page asks Orders, which '
            'answers. [[slnc 300]] It asks Catalog, which does not. '
            '[[slnc 300]] So every name reads: catalog unreachable. '
            '[[slnc 300]] The page is only half there. [[slnc 600]] And '
            'the shop now runs two containers, two drivers, and two query '
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
            'So what did the plain Java version get right? [[slnc 400]] '
            'The whole argument. [[slnc 300]] One shared database answers '
            'the page in one join, protected by a foreign key. [[slnc '
            "300]] A correct rename breaks somebody else's page. [[slnc "
            '300]] The split builds the same page in two calls, and the '
            'rename becomes harmless. [[slnc 600]] What it left out was '
            'everything that needs real databases. [[slnc 500]] Its two '
            'databases were the same kind of thing. [[slnc 300]] So it '
            'could not show a team choosing a different store for '
            'different data. [[slnc 400]] Its refusal was code it wrote '
            'itself. [[slnc 300]] So it could not show a real database '
            'answering a join with a quiet nothing. [[slnc 400]] It had '
            'no transactions, so no rollback could stop halfway. [[slnc '
            '400]] And a map in memory is never down.'
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
            'So, here is the verdict. [[slnc 400]] When two teams keep '
            'breaking each other, give each service its own database. '
            '[[slnc 300]] And let each team pick the kind of database '
            'that suits its data. [[slnc 600]] Then be honest about what '
            'that gives up. [[slnc 500]] One. [[slnc 200]] The join '
            'becomes two questions, and some code. [[slnc 400]] Two. '
            '[[slnc 200]] The foreign key becomes an agreement between '
            'teams. [[slnc 400]] Three. [[slnc 200]] One transaction '
            'becomes two, and they can disagree. [[slnc 400]] Four. '
            '[[slnc 200]] One database can be down while the other is up. '
            '[[slnc 600]] And never trust an empty answer from a join, '
            'until you know where the other half lives.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['Postgres 18.6 and MongoDB 8.3.11,', 'JDBC 42.7.13, MongoDB driver 5.12.0,',
              'Testcontainers 2.0.5: two containers', 'the demo starts and removes.', '',
              'Too much for one small team: one database', 'keeps the join, the key and one transaction.',
              'Same shape of data? Two databases on one', 'engine is often enough.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] There are '
            'two real databases. [[slnc 300]] Postgres, version eighteen '
            'point six. [[slnc 300]] And MongoDB, version eight point '
            'three point eleven. [[slnc 300]] Each runs in its own '
            'container, which the demo starts and removes by itself. '
            '[[slnc 300]] You just need Docker switched on first. [[slnc '
            "300]] Every number you heard comes from the program's own "
            'output. [[slnc 600]] So, when is this too much? [[slnc 300]] '
            'If one small team owns both halves, one database keeps the '
            'join, the foreign key, and the single transaction. [[slnc '
            "300]] If both teams' data has the same shape, two databases "
            'on the same kind of engine is often enough. [[slnc 300]] A '
            'second kind of database is one more thing to back up, '
            'update, watch, and learn.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Database per Service, with Containers. [[slnc 400]] "
            'If you remember one sentence, make it this one. [[slnc 300]] '
            'Once each service has its own database, the join is not '
            'forbidden, it is impossible, and one database will not even '
            'tell you. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Create a real orders collection in the catalog '
            'database, with one document in it. [[slnc 300]] Guess what '
            'the lookup will return, and then run it. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
