"""Scene definitions for the Lazy Load teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Lazy Load',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Lazy Load '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: load '
            'the object you asked for now, and load the things it refers '
            'to only when someone actually asks for them. [[slnc 350]] '
            'This is the fourth project in the enterprise category. In '
            'our online store, it is the difference between loading one '
            'order, and accidentally loading the shop. [[slnc 300]] By '
            'the end you will know four ways to do it, why it can make a '
            'page slower rather than faster, and why one of the most '
            'searched Java errors happens.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Load one order, to show it on a page.', '', 'An order has a customer.', 'The customer has other orders.', 'Those have lines, the lines have', 'products, the products, categories.'],
        narration=(
            'Here is the scenario. A page needs one order. That order has '
            'a customer. The customer has other orders. Those orders have '
            'lines, the lines have products, and the products have '
            'categories. [[slnc 300]] Everything is connected to '
            'everything. The question is: how much of that should loading '
            'one order drag in?'
        ),
    ),
    dict(
        key='03-eager', kind='console', title='Eager Loading',
        body="""ONE. Eager loading.
  one order asked for.
  objects created: 37
  database operations: 26

  no cycle, no obvious
  mistake.""",
        narration=(
            'The naive way is eager loading: load everything reachable, '
            'straight away. [[slnc 300]] The demo asks for one order. '
            'Thirty-seven objects are created. Twenty-six database '
            'operations are made. [[slnc 300]] And there is no cycle in '
            'that graph and no obvious mistake. It is just that '
            'everything is connected, so loading anything loads nearly '
            'everything.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Load the order now.', 'Load the rest when it is asked for.', '', 'The caller is not meant to notice.'],
        narration=(
            'The pattern is simple to say. Load the order now. Load the '
            'rest only when someone asks for it. The caller is not meant '
            'to notice the difference. [[slnc 300]] There are four common '
            'ways to build it, and you will meet all four in real code.'
        ),
    ),
    dict(
        key='05-variants', kind='console', title='Four Ways To Load Later',
        body="""TWO. Four ways.
  lazy initialisation: 0 before,
  1 after first use, 1 after 2nd
  virtual proxy: the same
  value holder:  the same
  ghost:         the same""",
        narration=(
            'Four variants. Lazy initialisation: a field is empty until a '
            'getter is called. A virtual proxy: a stand-in with the same '
            'interface, which loads the real thing on first use. A value '
            'holder: the caller knows it holds a promise, and asks for '
            'the value. And a ghost: an object created with only its id, '
            'which loads everything the first time anything is asked of '
            'it. [[slnc 300]] The demo counts each one. Zero queries '
            'before use. One query after the first use. Still one after '
            'the second. They cost nothing until needed.'
        ),
    ),
    dict(
        key='06-n-plus-one', kind='console', title='Cost One: N Plus One',
        body="""THREE. N+1.
  a page of 20 orders,
  each with its customer:

  lazy:    21 queries
  batched: 2 queries""",
        narration=(
            'Now the bill, and it is a heavy one. You have replaced one '
            'large query with many small ones. [[slnc 300]] A page lists '
            "twenty orders, and shows each customer's name. Lazily: one "
            'query for the orders, then one for each customer. Twenty-one '
            'queries. Batched: two. [[slnc 300]] In a real system every '
            'query is a round trip to the database. So the lazy page can '
            'be slower than the eager one it replaced. This is called N '
            'plus one.'
        ),
    ),
    dict(
        key='07-io', kind='console', title='Cost Two: A Field Is Now I/O',
        body="""FOUR. A field access is I/O.
  asking for a customer's name
  threw: the database failed to
  read.

  it looked like reading a field.
  it was a database call.""",
        narration=(
            "Second cost. Asking for a customer's name looks like reading "
            'a field. It is not. It is a database call. [[slnc 300]] So '
            'it can be slow, and it can fail. In this demo, the database '
            'is told to fail the next read, and asking for a name throws. '
            'Code that assumed a getter cannot fail now has an exception '
            'it never planned for.'
        ),
    ),
    dict(
        key='08-closed', kind='console', title='Cost Three: The Closed Session',
        body="""FIVE. The session closes.
  the object is created while
  the session is open.

  the session closes.

  the page asks for the name:
  cannot load: session closed""",
        narration=(
            'Third cost, and the one that catches people out. The object '
            'is created while its session is open. Nothing has been '
            'loaded yet. [[slnc 300]] Then the session closes, and the '
            'object is passed on to a page. The page asks for the name. '
            'The load needs the session. The session is gone. It fails. '
            '[[slnc 300]] The failure is where the object was used, not '
            'where it was created. That is what makes it hard to find.'
        ),
    ),
    dict(
        key='09-met', kind='bullets', title='Where You Have Met This',
        body=['That failure has a name in Hibernate:', 'LazyInitializationException.', '', 'It is one of the most searched', 'Java errors there is.'],
        narration=(
            'You have very likely met this. That failure has a name in '
            'Hibernate: lazy initialization exception. It is one of the '
            'most searched Java errors there is. [[slnc 300]] It is '
            'exactly act five: a lazy object, whose session has closed. '
            'Now you know the mechanism, not just the workaround.'
        ),
    ),
    dict(
        key='10-toydb', kind='bullets', title='The Toy Database',
        body=['Rows, a counter, and now a read', 'that can be told to fail.', '', 'Every count in this video', 'came from its counter.'],
        narration=(
            'A word about the database in these demos. It is a toy: rows, '
            'an operation counter, and now a read that can be told to '
            'fail. Every count in this video, the thirty-seven, the '
            'twenty-six, the twenty-one, came from that counter.'
        ),
    ),
    dict(
        key='11-real', kind='bullets', title='What Is Real Here',
        body=['The counts are real.', 'The round trip cost is not measured:', 'the toy database has no network.', '', 'N+1 is slow in a real system', 'because each query is a trip.'],
        narration=(
            'The same honest admission as everywhere in this course. The '
            'counts are real. The cost of a round trip is not measured, '
            'because the toy database has no network. [[slnc 300]] N plus '
            'one is slow in a real system because each query is a trip. '
            'Here you see the count, and you can supply the latency '
            'yourself.'
        ),
    ),
    dict(
        key='12-too-much', kind='bullets', title='When This Is Too Much',
        body=['If you almost always need the related', 'data, lazy loading only adds queries.', '', 'It earns its place when the related', 'data is large and rarely needed.'],
        narration=(
            'So when is it too much? If you almost always need the '
            'related data, lazy loading just adds queries. [[slnc 300]] '
            'It earns its place when the related data is large, and '
            'rarely needed.'
        ),
    ),
    dict(
        key='13-fixes', kind='bullets', title='What To Do About It',
        body=['Batch: one query for all the customers.', 'Join: fetch the parts you know you need.', 'Keep the session open until the page', 'is done, or load before you leave.'],
        narration=(
            'So what do you do about the bill? Batch: fetch all the '
            'customers in one query. Join: fetch the parts you know you '
            'will need, together. And keep the session open until the '
            'page is finished, or load what you need before you leave. '
            '[[slnc 300]] Each of those is a decision the lazy load made '
            'for you, and now you are making back.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Change the lazy list so it', 'fetches each customer only once.'],
        narration=(
            "That's the Lazy Load. [[slnc 250]] If you take one sentence "
            'away, take this one: lazy loading trades one big query for '
            'many small ones, and moves the failure to wherever the '
            'object is used. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'change the lazy list so each customer is fetched only once, '
            'and count the queries. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
