"""Scene definitions for the Repository teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Repository',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Repository pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A repository is an interface '
            'that looks like a collection of your objects, held in '
            'memory. [[slnc 300]] So the code that uses it simply asks '
            'for objects. [[slnc 300]] And never has to know where they '
            "are kept. [[slnc 600]] Think of a library's front desk. "
            '[[slnc 300]] You ask for a book by title. [[slnc 300]] You '
            'never need to know which shelf, which room, or which '
            'building it came from. [[slnc 700]] In our online store, the '
            'question is how to find customers in London who ordered in '
            'the last month. [[slnc 500]] By the end, you will know why '
            'the same query in three places goes wrong. [[slnc 300]] How '
            'to change where customers are stored, without touching the '
            'code that asks. [[slnc 300]] And what that costs.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Find customers in London', 'who have ordered in the last month.', '', 'Marketing wants it. Support wants it.', 'Reporting wants it.'],
        narration=(
            'Here is the scenario. [[slnc 400]] The marketing team wants '
            'a list of customers in London, who have ordered in the last '
            'month. [[slnc 300]] So does the support team. [[slnc 300]] '
            'So does reporting. [[slnc 500]] Three places in the code '
            'need the same answer. [[slnc 300]] So where should the query '
            'live?'
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
            'First, the naive way: the database query sits inside each '
            'service. [[slnc 400]] For one query, in one place, that is '
            'fine. [[slnc 500]] But here it is written three times, each '
            'slightly differently. [[slnc 300]] Marketing gets Ada and '
            'Grace. [[slnc 300]] Reporting gets Ada and Grace. [[slnc '
            '300]] Support gets Ada, Grace, and Ken. [[slnc 500]] Support '
            'wrote, on or after, where the others wrote, after. [[slnc '
            "300]] One day's difference, one extra customer, and nobody "
            'noticed.'
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
            'Then the database changes. [[slnc 400]] The column called '
            'city is renamed to town. [[slnc 500]] Now every service '
            'returns an empty list. [[slnc 300]] Nothing threw an error. '
            '[[slnc 300]] Not one. [[slnc 500]] The word city was written '
            'as text in all three places. [[slnc 300]] Each one had to be '
            'found by hand. [[slnc 300]] Miss one, and a list is quietly '
            'empty in production.'
        ),
    ),
    dict(
        key='05-pattern', kind='bullets', title='The Pattern',
        body=['An interface that looks like a', 'collection of customers.', '', 'add, findById, findByCity...', '', 'The caller asks for customers.', 'It does not know a database exists.'],
        narration=(
            'Now, the pattern. [[slnc 400]] An interface that looks like '
            'a collection of customers in memory. [[slnc 300]] It has '
            'add, find by I D, and finder methods for the questions the '
            'business asks. [[slnc 500]] The caller asks for customers. '
            '[[slnc 300]] It does not know that a database, a table, or a '
            'column exists.'
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
            'Third demo: the caller only knows the interface. [[slnc '
            '400]] Here is the marketing service now. [[slnc 300]] It '
            'gets Ada and Grace, the right answer. [[slnc 500]] And '
            'listen to what it knows. [[slnc 300]] Its constructor takes '
            'one thing: a customer repository. [[slnc 300]] It knows no '
            'database, names no table, and mentions no column. [[slnc '
            '500]] The query lives in one place, behind the door.'
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
            'Fourth demo, and the strongest moment: swapping the store. '
            '[[slnc 400]] There are two repositories behind the same '
            'interface. [[slnc 300]] One keeps customers in a simple '
            'list, in memory. [[slnc 300]] The other uses the database. '
            '[[slnc 500]] The same marketing service runs against both. '
            '[[slnc 300]] Ada and Grace, either way. [[slnc 500]] The '
            'whole change is one line, where the service is created. '
            '[[slnc 300]] Swap the in-memory repository for the database '
            'one. [[slnc 300]] The marketing service itself is untouched.'
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
            'Now the costs. [[slnc 300]] The first: the interface keeps '
            'growing. [[slnc 500]] Every new business question adds a '
            'method. [[slnc 300]] Find by city. [[slnc 200]] Find by '
            'city, and ordered after a date. [[slnc 200]] Find by city, '
            'and ordered after a date, and with a certain status. [[slnc '
            '500]] Until the interface becomes a query language, only '
            'clumsier. [[slnc 500]] The Specification pattern fixes this. '
            '[[slnc 300]] You combine small conditions, like, in London, '
            'and has a pending order, with no new method. [[slnc 300]] '
            'The price is one more idea to learn.'
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
            'The second cost: the database leaks through. [[slnc 400]] '
            'The door hides the database. [[slnc 300]] But sometimes, '
            'good performance needs it. [[slnc 500]] One question, '
            'against six customers, costs seven database queries. [[slnc '
            '300]] One for the customers, and then one for each '
            "customer's orders. [[slnc 500]] The caller has no way to "
            'say: fetch the orders together, in one go. [[slnc 300]] '
            'Fixing that means the interface must learn about the '
            'database again.'
        ),
    ),
    dict(
        key='10-swap-claim', kind='bullets', title='Cost Three: The Swap Is Rarely Used',
        body=['It lets you swap the database.', '', 'That is claimed far more often', 'than it is used.', '', 'The real benefit: callers speak', 'the language of the domain.'],
        narration=(
            'The third cost is about honesty. [[slnc 400]] A repository '
            'is often sold as a way to swap your database. [[slnc 300]] '
            'That is claimed far more often than it ever happens. [[slnc '
            '500]] The real benefit is different. [[slnc 300]] The '
            'calling code speaks in the language of the business: '
            'customers, and orders. [[slnc 300]] Not tables, and columns.'
        ),
    ),
    dict(
        key='11-toydb', kind='bullets', title='The Toy Database',
        body=['Rows, and a counter.', '', 'Every count in this video, the seven,', 'came from its counter.'],
        narration=(
            'A word about the database in these demos. [[slnc 400]] It is '
            'a toy: just rows, and a counter. [[slnc 300]] Every count in '
            'this video, including the seven, came from that counter.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['A Spring Data repository interface', 'is this pattern.', '', 'save, findById, findByCity:', 'collection-shaped methods.', '', 'The framework writes the rest.'],
        narration=(
            'You have met this pattern before. [[slnc 400]] A Spring Data '
            'repository interface is exactly this pattern. [[slnc 300]] '
            'Save, find by I D, find by city: methods shaped like a '
            'collection. [[slnc 300]] And the framework writes the rest '
            'for you. [[slnc 300]] Spring Data has its own video in this '
            'series.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The pattern is real.', 'The database is a stand-in with', 'no query planner.', '', 'The seven operations are a fair', 'picture of a repository with', 'no way to say join.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'pattern is real. [[slnc 300]] The database is a stand-in, '
            'with no query optimiser to rescue the seven queries. [[slnc '
            '300]] The count is a fair picture of a repository that '
            'cannot combine queries.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['A handful of queries, in one place:', 'a repository is an extra layer.', '', 'It earns its place when the same', 'question is asked from several places.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For an application '
            'with only a few queries, all in one place, a repository is '
            'an extra layer. [[slnc 500]] It earns its place when the '
            'same questions are asked from several places. [[slnc 300]] '
            'Or when the business code should not know about storage at '
            'all.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Write a specification for', 'customers with no orders.'],
        narration=(
            "That's the Repository pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A repository '
            'lets the caller speak the language of the business, but '
            'every question still needs somewhere to live. [[slnc 500]] '
            'The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Write a '
            'specification for customers with no orders. [[slnc 300]] And '
            'use it, without adding any new repository method. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
