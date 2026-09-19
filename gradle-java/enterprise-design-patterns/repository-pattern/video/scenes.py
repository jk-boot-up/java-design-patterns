"""Scene definitions for the Repository teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Repository',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Repository '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: an '
            'interface that looks like a collection of your objects in '
            'memory, so the code that uses it asks for objects and never '
            'has to know where they are kept. [[slnc 350]] This is the '
            'fifth project in the enterprise category, and it hides the '
            'four before it behind one door. In our online store, the '
            'question is how to find customers in London who ordered in '
            'the last month. [[slnc 300]] By the end you will know why '
            'the same query in three places goes wrong, how to swap where '
            'customers live without touching the code that asks, and what '
            'that door costs.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Find customers in London', 'who have ordered in the last month.', '', 'Marketing wants it. Support wants it.', 'Reporting wants it.'],
        narration=(
            'Here is the scenario. The marketing team wants a list of '
            'customers in London who have ordered in the last month. '
            '[[slnc 300]] So does the support team. So does reporting. '
            '[[slnc 300]] Three places in the code need the same answer. '
            'The question is: where should the query live?'
        ),
    ),
    dict(
        key='03-three-ways', kind='console', title='SQL In The Service',
        body="""ONE. Three ways.
  marketing: [Ada, Grace]
  support:   [Ada, Grace, Ken]
  reports:   [Ada, Grace]

  three answers to one
  question. support is off
  by one day.""",
        narration=(
            'The naive way puts the query in each service, where it is '
            'needed. For one query, in one place, that is fine. [[slnc '
            '300]] Here it is written three times, each slightly '
            'differently. Marketing gets Ada and Grace. Reporting gets '
            'Ada and Grace. Support gets Ada, Grace and Ken. [[slnc 300]] '
            'Support wrote greater than or equal to where the others '
            'wrote greater than. One day off, one extra customer, and '
            'nobody noticed.'
        ),
    ),
    dict(
        key='04-schema', kind='console', title='A Schema Change',
        body="""TWO. The column city is
renamed to town.

  marketing: []
  support:   []
  reports:   []

  nothing threw.""",
        narration=(
            'Then the schema changes. The city column is renamed to town. '
            '[[slnc 300]] Every service returns an empty list. Nothing '
            'threw. No error at all. The word city was a string in all '
            'three places, and each one had to be found by hand. [[slnc '
            '300]] Miss one, and a list is quietly empty in production.'
        ),
    ),
    dict(
        key='05-pattern', kind='bullets', title='The Pattern',
        body=['An interface that looks like a', 'collection of customers.', '', 'add, findById, findByCity...', '', 'The caller asks for customers.', 'It does not know a database exists.'],
        narration=(
            'The pattern is an interface that looks like a collection of '
            'customers in memory. It has add, find by id, and finders for '
            'the questions the business asks. [[slnc 300]] The caller '
            'asks for customers. It does not know a database exists, or a '
            'table, or a column.'
        ),
    ),
    dict(
        key='06-caller', kind='console', title='The Caller Knows Only The Interface',
        body="""THREE. The pattern.
  [Ada, Grace]

  MarketingService's
  constructor takes:
  CustomerRepository

  no database, no table,
  no column.""",
        narration=(
            'Here is the marketing service now. Ada and Grace, the right '
            'answer. [[slnc 300]] Look at what it knows. Its constructor '
            'takes one thing: a customer repository. It imports no '
            'database, names no table, and mentions no column. The query '
            'lives in one place, behind the door.'
        ),
    ),
    dict(
        key='07-swap', kind='console', title='Swap The Store',
        body="""FOUR. Swap the store.
  in memory: [Ada, Grace]
  database:  [Ada, Grace]

  the whole change, one line:
  - new InMemory...
  + new ToyDatabase...

  MarketingService untouched.""",
        narration=(
            'Now the strongest moment. There are two repositories behind '
            'the same door. One keeps customers in a list. The other uses '
            'the database. [[slnc 300]] The same marketing service runs '
            'against both. Ada and Grace, either way. [[slnc 300]] The '
            'whole change is one line, where the service is built: swap '
            'the in-memory repository for the database one. The marketing '
            'service itself is untouched.'
        ),
    ),
    dict(
        key='08-methods', kind='console', title='Cost One: A Method Per Question',
        body="""FIVE. A method per question.
    findByCity
    findByCityAndOrderedAfter
    findByCityAndOrderDate
    AfterAndStatusIn ...

  a specification fixes it,
  and costs a concept.""",
        narration=(
            'Now the bill. First, the interface grows. Every new business '
            'question adds a method. Find by city. Find by city and '
            'ordered after. Find by city and order date after and status '
            'in. [[slnc 300]] Until the interface is a query language, '
            'with worse ergonomics. [[slnc 300]] A specification fixes '
            'it. You combine small conditions, in city London, ordered '
            'after seventy, has a pending order, with no new method. The '
            'price is one more concept to learn.'
        ),
    ),
    dict(
        key='09-leak', kind='console', title='Cost Two: The Leak',
        body="""SIX. The leak.
  one question, 6 customers:
  7 database operations.

  one for the customers, then
  one per customer for their
  orders.

  the caller cannot say join.""",
        narration=(
            'Second cost. The door hides the database, and performance '
            'sometimes needs it. [[slnc 300]] One question, against six '
            'customers, costs seven database operations. One for the '
            "customers, then one for each customer's orders. [[slnc 300]] "
            'The caller cannot say join. It cannot say, fetch the orders '
            'together. Fixing that means the interface has to learn about '
            'the database again.'
        ),
    ),
    dict(
        key='10-swap-claim', kind='bullets', title='Cost Three: The Swap Is Rarely Used',
        body=['It lets you swap the database.', '', 'That is claimed far more often', 'than it is used.', '', 'The real benefit: callers speak', 'the language of the domain.'],
        narration=(
            'Third cost, and it is about honesty. A repository is often '
            'sold as a way to swap the database. That is claimed far more '
            'often than it is ever used. [[slnc 300]] The real benefit is '
            'different. Callers speak in the language of the domain: '
            'customers, orders. They do not speak tables and columns.'
        ),
    ),
    dict(
        key='11-toydb', kind='bullets', title='The Toy Database',
        body=['Rows, and a counter.', '', 'Every count in this video, the seven,', 'came from its counter.'],
        narration=(
            'A word about the database in these demos. It is a toy: rows, '
            'and a counter. Every count in this video, including the '
            'seven, came from that counter.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['A Spring Data repository interface', 'is this pattern.', '', 'save, findById, findByCity:', 'collection-shaped methods.', '', 'The framework writes the rest.'],
        narration=(
            'You have met this. A Spring Data repository interface is '
            'this pattern. Save, find by id, find by city: '
            'collection-shaped methods, and the framework writes the '
            'implementation. [[slnc 300]] A later project in this '
            'category builds exactly that.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The pattern is real.', 'The database is a stand-in with', 'no query planner.', '', 'The seven operations are a fair', 'picture of a repository with', 'no way to say join.'],
        narration=(
            'The same honest admission as everywhere in this course. The '
            'pattern is real. The database is a stand-in, with no query '
            'planner to rescue the seven operations. [[slnc 300]] The '
            'count is a fair picture of a repository that cannot say '
            'join.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['A handful of queries, in one place:', 'a repository is an extra layer.', '', 'It earns its place when the same', 'question is asked from several places.'],
        narration=(
            'So when is it too much? For an application with a handful of '
            'queries, all in one place, a repository is an extra layer. '
            '[[slnc 300]] It earns its place when the same questions are '
            'asked from several places, or when the domain should not '
            'know about storage at all.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Write a specification for', 'customers with no orders.'],
        narration=(
            "That's the Repository. [[slnc 250]] If you take one sentence "
            'away, take this one: a repository lets the caller speak the '
            'language of the domain, but every question still needs '
            'somewhere to live. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'write a specification for customers with no orders, and use '
            'it without adding a repository method. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
