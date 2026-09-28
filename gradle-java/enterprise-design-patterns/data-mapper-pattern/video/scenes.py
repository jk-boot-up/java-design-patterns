"""Scene definitions for the Data Mapper teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key="01-poster", kind="poster", title="Data Mapper", body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Data Mapper pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A data mapper is a separate '
            'class that moves data between an object and its database '
            'rows. [[slnc 300]] So the object itself never knows it is '
            'being stored. [[slnc 600]] Think of a removal company. '
            '[[slnc 300]] Your furniture does not know how to pack '
            'itself. [[slnc 300]] The movers know how to wrap each piece, '
            'and where it goes in the van. [[slnc 700]] In our online '
            'store, the object is a customer. [[slnc 300]] And the '
            'question is: who should know how a customer is saved? [[slnc '
            '500]] By the end, you will know when it is fine for an '
            'object to save itself, and what that costs. [[slnc 300]] '
            'What a mapper does instead. [[slnc 300]] And how a '
            'hand-written mapping can lose a field, without any error.'
        ),
    ),
    dict(
        key="02-scenario", kind="bullets", title="The Scenario",
        body=[
            "The store has customers: a name, an email,",
            "a postal address, and loyalty points.",
            "",
            "They must be stored, and loaded again.",
            "",
            "Who should know how?",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] The online store has '
            'customers. [[slnc 300]] Each one has a name, an email '
            'address, a postal address, and loyalty points. [[slnc 500]] '
            'Customers must be stored in a database, and loaded again '
            'later. [[slnc 500]] So here is the question. [[slnc 300]] '
            'Who should know how that is done? [[slnc 300]] The customer, '
            'or something else?'
        ),
    ),
    dict(
        key="03-active-record", kind="console", title="Active Record Works",
        body="""ONE. Active Record.
    INSERT customers id=1
    SELECT customers id=1
    UPDATE customers id=1

  3 operations, one class,
  one table.""",
        narration=(
            'The simplest answer: the object saves itself. [[slnc 300]] '
            'This is called Active Record. [[slnc 500]] The customer has '
            'a save method, a find method, and knows its own table. '
            '[[slnc 500]] Listen to the database operations. [[slnc 300]] '
            'An insert. [[slnc 200]] A select. [[slnc 200]] An update. '
            '[[slnc 300]] Three operations, one class, one table. [[slnc '
            '500]] This works, and works well. [[slnc 300]] For a simple '
            'application, it is the right answer.'
        ),
    ),
    dict(
        key="04-cost", kind="console", title="The Cost",
        body="""TWO. The cost.
  ActiveRecordCustomer takes
  a Database, and names its
  own table and columns.

  a plain Customer changed its
  email with no database
  anywhere.""",
        narration=(
            'Now the cost. [[slnc 400]] The Active Record customer holds '
            'a database connection, and names its own table and columns. '
            '[[slnc 500]] So even a tiny rule, like, an email must '
            'contain an at sign, cannot be tested without a database. '
            '[[slnc 300]] And a change to the table is a change to the '
            'customer class itself. [[slnc 500]] Compare that with a '
            'plain customer, which has no storage code at all. [[slnc '
            '300]] It changes its email with no database anywhere in '
            'sight.'
        ),
    ),
    dict(
        key="05-shape", kind="console", title="A Shape It Cannot Say",
        body="""THREE. Two shapes.
  one customer, two tables:
    SELECT customers id=1
    SELECT addresses id=1

  one table, a second object:
    SELECT customers (all)
  2 summaries.""",
        narration=(
            'And there are shapes that one class per table simply cannot '
            'express. [[slnc 500]] First, one customer stored across two '
            'tables. [[slnc 300]] Loading it needs one query on the '
            'customers table, and one on the addresses table. [[slnc '
            '500]] Second, one table that feeds two different objects. '
            '[[slnc 300]] The customers table also produces a small '
            'summary, with just an I D and a name, for a list page. '
            '[[slnc 500]] An object that is its own table has no way to '
            'describe either shape.'
        ),
    ),
    dict(
        key="06-pattern", kind="bullets", title="The Pattern",
        body=[
            "A mapper class sits between the object",
            "and the rows.",
            "",
            "It is the only class that knows both.",
            "",
            "The object knows neither.",
        ],
        narration=(
            'Now, the pattern: a mapper class. [[slnc 400]] It sits '
            'between the object and the database rows. [[slnc 300]] And '
            'it is the only class that knows both. [[slnc 500]] To store '
            'a customer, the mapper writes a row in the customers table, '
            'and a row in the addresses table. [[slnc 300]] To load one, '
            'it reads both, and builds the customer. [[slnc 500]] The '
            'customer itself knows about neither.'
        ),
    ),
    dict(
        key="07-customer", kind="console", title="What The Customer Looks Like",
        body="""FOUR. The pattern.
  loaded back: Ada Lovelace,
  Leeds, 10 points

  Customer's fields:
    address email id
    loyaltyPoints name

  no table, no column, no SQL,
  no database.""",
        narration=(
            "The demo proves it, by listing the customer class's fields. "
            '[[slnc 400]] Address, email, I D, loyalty points, and name. '
            '[[slnc 300]] And its methods: change email, move to a new '
            'address, earn points. [[slnc 500]] No table. [[slnc 200]] No '
            'column. [[slnc 200]] No database code. [[slnc 500]] The '
            'customer loaded back as Ada Lovelace, in Leeds, with ten '
            'points. [[slnc 300]] It is only a customer, and it can be '
            'tested and understood as one.'
        ),
    ),
    dict(
        key="08-second-class", kind="bullets", title="The Bill: A Class Per Entity",
        body=[
            "Every domain object gets a mapper beside it.",
            "",
            "Loading a whole graph means deciding how",
            "far to go. That is the Lazy Load video.",
            "",
            "And you must know the mapper exists",
            "before you can debug a wrong value.",
        ],
        narration=(
            'Now the costs of the pattern. [[slnc 500]] First, a second '
            'class for every entity. [[slnc 300]] Each domain object gets '
            'a mapper beside it. [[slnc 500]] Second, loading a whole '
            'group of related objects means deciding how far to go. '
            '[[slnc 300]] That decision is the subject of the Lazy Load '
            'video. [[slnc 500]] Third, an extra step to follow. [[slnc '
            '300]] You must know the mapper exists, before you can track '
            'down a wrong value.'
        ),
    ),
    dict(
        key="09-silent-field", kind="console", title="The Bill: A Silent Field",
        body="""FIVE. A silent field.
  saved postcode:  LS1 4AB
  loaded postcode: null

  every call succeeded.
  nothing threw.
  the field is simply gone.""",
        narration=(
            'And the worst cost. [[slnc 400]] The mapping is written by '
            'hand, and it is easy to get quietly wrong. [[slnc 500]] This '
            'careless mapper forgets the postcode when it saves the '
            'address. [[slnc 300]] The demo saves the postcode L S one, '
            'four A B. [[slnc 300]] It loads back nothing. [[slnc 500]] '
            'Every call succeeded. [[slnc 300]] Nothing threw an error. '
            '[[slnc 300]] The field is simply gone. [[slnc 500]] The only '
            'defence is a test that saves an object, loads it back, and '
            'compares every field.'
        ),
    ),
    dict(
        key="10-toydb", kind="bullets", title="The Toy Database",
        body=[
            "Rows, not objects.",
            "Every operation counted.",
            "A write can be told to fail.",
            "Nothing needs installing.",
            "",
            "Every count in this video comes from it.",
        ],
        narration=(
            'A word about the database in these demos. [[slnc 400]] It is '
            'a toy, built for teaching. [[slnc 300]] It stores rows, not '
            'objects. [[slnc 300]] Every operation is counted, and '
            'printed. [[slnc 300]] A write can be told to fail, on '
            'demand. [[slnc 300]] And nothing needs installing. [[slnc '
            '500]] Every count in this video came from its counter, not '
            'from guessing.'
        ),
    ),
    dict(
        key="11-met", kind="bullets", title="Where You Have Met This",
        body=[
            "A JPA entity is the domain object.",
            "The EntityManager is the mapper.",
            "",
            "Hibernate writes the mapping code",
            "that act five shows can go wrong.",
        ],
        narration=(
            'You have almost certainly met this pattern already. [[slnc '
            "400]] In Java's persistence standard, J P A, an entity is "
            'the domain object. [[slnc 300]] And the entity manager is '
            'the mapper. [[slnc 500]] Hibernate writes the mapping code '
            'for you, so you usually only see annotations. [[slnc 300]] '
            'If you have ever fixed a mapping because a field did not '
            'come back, you have met the silent field problem.'
        ),
    ),
    dict(
        key="12-real", kind="bullets", title="What Is Real Here",
        body=[
            "The toy database is not a real database:",
            "no transactions, no indexes, no SQL parser.",
            "",
            "The operation lines are SQL-shaped, not SQL.",
            "The pattern is real. The database is a stand-in.",
        ],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] The toy '
            'database is not a real one. [[slnc 300]] It has no '
            'transactions, no indexes, and no query planner. [[slnc 300]] '
            'The operations it prints look like database commands, but '
            'they are not real ones. [[slnc 500]] The pattern is real. '
            '[[slnc 300]] The database is a stand-in that makes the '
            'counts easy to hear.'
        ),
    ),
    dict(
        key="13-too-much", kind="bullets", title="When This Is Too Much",
        body=[
            "A simple application, one class per table,",
            "a schema that rarely changes:",
            "",
            "Active Record is simpler,",
            "and it is the right answer.",
        ],
        narration=(
            'So, when is a mapper too much? [[slnc 400]] For a simple '
            'application, with one class per table, and tables that '
            'rarely change, Active Record is simpler, and it is the right '
            'answer. [[slnc 500]] Reach for a mapper when your objects '
            'and your tables stop matching one to one. [[slnc 300]] Or '
            'when you want to test your business logic with no database '
            'at all.'
        ),
    ),
    dict(
        key="14-outro", kind="outro", title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository. Write a test that saves a customer,",
            "loads it, and compares every field.",
        ],
        narration=(
            "That's the Data Mapper pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A mapper lets '
            'your business objects live without a database, and the price '
            'is an extra class you must test. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Write a test that saves a '
            'customer, loads it back, and compares every field. [[slnc '
            '300]] It would have caught the missing postcode. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
