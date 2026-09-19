"""Scene definitions for the Data Mapper teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key="01-poster", kind="poster", title="Data Mapper", body=None,
        narration=(
            "Hello, and welcome. This video explains the Data Mapper "
            "pattern in Java, and it is written and presented by "
            "Jayasekhar Konduru. [[slnc 300]] The plain definition: a "
            "mapper class moves data between an object and its database "
            "rows, so the object itself never knows it is stored. "
            "[[slnc 350]] This is the first project in the enterprise "
            "category, and the others assume it. In our online store, "
            "the object is a customer, and the question is who should "
            "know how a customer is saved. [[slnc 300]] By the end you "
            "will know when it is fine for an object to save itself, "
            "what that costs, what a mapper does instead, and how a "
            "hand-written mapping can lose a field without any error."
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
            "Here is the scenario. The online store has customers. Each "
            "has a name, an email address, a postal address and loyalty "
            "points. [[slnc 300]] They must be stored in a database, and "
            "loaded again later. [[slnc 300]] The question this video "
            "answers: who should know how that happens? Should the "
            "customer, or something else?"
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
            "The simplest answer: the object saves itself. It is called "
            "Active Record. The customer has a save method, and a find "
            "method, and knows its own table. [[slnc 300]] Watch the "
            "operations against the toy database. An insert. A select. "
            "An update. Three operations, one class, one table. "
            "[[slnc 300]] This works, and it works well. For a simple "
            "application it is the right answer, and nothing in this "
            "video says otherwise."
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
            "Now the cost. The Active Record customer holds a database "
            "and names its own table and columns. [[slnc 300]] So a "
            "rule as small as, an email must contain an at sign, cannot "
            "be tested without a database. And a change to the schema "
            "is a change to the domain object itself. [[slnc 300]] "
            "Compare a plain customer, with no storage in it at all. It "
            "changes its email with no database anywhere in sight."
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
            "And there are shapes one class per table cannot say at "
            "all. [[slnc 300]] First, one customer stored across two "
            "tables. Loading it takes a select on customers and a "
            "select on addresses. [[slnc 300]] Second, one table feeding "
            "two different objects. The customers table also produces a "
            "smaller summary, with just an id and a name, for a list "
            "page. Two summaries, from one select. [[slnc 300]] An "
            "object that is its own table has no way to describe either."
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
            "The pattern is a mapper class. It sits between the object "
            "and the rows, and it is the only class that knows both. "
            "[[slnc 300]] To store a customer, the mapper writes a row "
            "in customers and a row in addresses. To load one, it reads "
            "both, and builds the customer. [[slnc 300]] The customer "
            "itself knows neither."
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
            "The demo proves it by printing the customer class. Its "
            "fields: address, email, id, loyalty points, and name. Its "
            "methods: change email, move to a new address, earn points, "
            "and getters. [[slnc 300]] No table. No column. No SQL. No "
            "database. It loaded back as Ada Lovelace, in Leeds, with "
            "ten points. [[slnc 300]] It is only a customer, and can be "
            "tested and understood as one."
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
            "Now the bill. First, a second class for every entity. Each "
            "domain object gets a mapper beside it. [[slnc 300]] Second, "
            "loading a whole object graph means deciding how far to "
            "go. That decision is the subject of the Lazy Load video. "
            "[[slnc 300]] Third, an indirection. You must know the "
            "mapper exists before you can debug a wrong value."
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
            "The worst part of the bill. The mapping is written by "
            "hand, and it is easy to get subtly wrong. [[slnc 300]] "
            "This careless mapper forgets the postcode when it writes "
            "the address. The demo saves L S one four A B. It loads "
            "back null. [[slnc 300]] Every call succeeded. Nothing "
            "threw. The field is simply gone. The only defence is a "
            "test that saves an object, loads it, and compares every "
            "field."
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
            "A word about the database in these demos. It is a toy, "
            "built for teaching. It stores rows, not objects. Every "
            "operation is counted and printed. A write can be told to "
            "fail, on demand. And nothing needs installing. [[slnc 300]] "
            "Every count in this video came from its counter, not from "
            "guessing. The rest of this category uses the same one."
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
            "You have almost certainly met this already. A JPA entity "
            "is the domain object. The entity manager is the mapper. "
            "[[slnc 300]] Hibernate writes the mapping code, so you "
            "usually only see it as annotations. If you have ever fixed "
            "a mapping because a field did not come back, you have "
            "lived act five."
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
            "The same honest admission as everywhere in this course. "
            "The toy database is not a real one. It has no transactions, "
            "no indexes, no query planner. The operation lines it "
            "prints are shaped like SQL, they are not SQL. [[slnc 300]] "
            "The pattern is real. The database is a stand-in that makes "
            "the counts easy to see."
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
            "So when is a mapper too much? For a simple application, "
            "with one class for each table and a schema that rarely "
            "changes, Active Record is simpler, and it is the right "
            "answer. [[slnc 300]] Reach for a mapper when the objects "
            "and the tables stop matching one to one, or when you want "
            "to test the domain with no database at all."
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
            "That's the Data Mapper. [[slnc 250]] If you take one "
            "sentence away, take this one: a mapper lets the domain "
            "live without a database, and the price is a class you must "
            "test. [[slnc 350]] The full source, the written notes, the "
            "diagrams and an animated walkthrough are all in the "
            "repository, running offline with nothing installed but a "
            "Java development kit. [[slnc 300]] If you try one "
            "exercise, write a test that saves a customer, loads it, "
            "and compares every field. It would have caught act five. "
            "[[slnc 300]] If this helped, a like genuinely does help "
            "other people find it, and subscribe if you would like the "
            "rest of the series. [[slnc 250]] Thanks for watching."
        ),
    ),
]
