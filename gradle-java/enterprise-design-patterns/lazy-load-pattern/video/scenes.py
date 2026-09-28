"""Scene definitions for the Lazy Load teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Lazy Load',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Lazy Load pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Load the object you asked '
            'for now. [[slnc 300]] And load the things it refers to only '
            'when someone actually asks for them. [[slnc 600]] Think of a '
            'video streaming service. [[slnc 300]] It does not download '
            'the whole film before you start. [[slnc 300]] It fetches '
            'each part just before you watch it. [[slnc 700]] In our '
            'online store, this is the difference between loading one '
            'order, and accidentally loading the whole shop. [[slnc 500]] '
            'By the end, you will know four ways to do it. [[slnc 300]] '
            'Why it can make a page slower, not faster. [[slnc 300]] And '
            'why one of the most searched Java errors happens.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Load one order, to show it on a page.', '', 'An order has a customer.', 'The customer has other orders.', 'Those have lines, the lines have', 'products, the products, categories.'],
        narration=(
            'Here is the scenario. [[slnc 400]] A page needs to show one '
            'order. [[slnc 500]] That order has a customer. [[slnc 300]] '
            'The customer has other orders. [[slnc 300]] Those orders '
            'have lines. [[slnc 300]] The lines have products. [[slnc '
            '300]] And the products have categories. [[slnc 500]] '
            'Everything is connected to everything. [[slnc 300]] So how '
            'much of that should loading one order drag in?'
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
            'First, the naive way: eager loading. [[slnc 400]] Load '
            'everything that can be reached, straight away. [[slnc 500]] '
            'The demo asks for one order. [[slnc 300]] Thirty-seven '
            'objects are created. [[slnc 300]] And twenty-six database '
            'queries are made. [[slnc 500]] There is no mistake here, and '
            'no loop in the data. [[slnc 300]] Everything is simply '
            'connected. [[slnc 300]] So loading anything loads nearly '
            'everything.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Load the order now.', 'Load the rest when it is asked for.', '', 'The caller is not meant to notice.'],
        narration=(
            'Now, the pattern, and it is simple to say. [[slnc 400]] Load '
            'the order now. [[slnc 300]] Load the rest only when someone '
            'asks for it. [[slnc 300]] And the caller should not notice '
            'the difference. [[slnc 500]] There are four common ways to '
            'build it, and you will meet all four in real code.'
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
            'Second demo: four ways to load later. [[slnc 500]] One: lazy '
            'initialisation. [[slnc 300]] A field stays empty, until its '
            'getter is first called. [[slnc 400]] Two: a virtual proxy. '
            '[[slnc 300]] A stand-in, with the same interface, that loads '
            'the real object on first use. [[slnc 400]] Three: a value '
            'holder. [[slnc 300]] The caller knows it holds a promise, '
            'and asks for the value. [[slnc 400]] Four: a ghost. [[slnc '
            '300]] An object created with only its I D, which loads '
            'everything the first time anything is asked of it. [[slnc '
            '600]] The demo counts each one. [[slnc 300]] Zero queries '
            'before use. [[slnc 300]] One query after the first use. '
            '[[slnc 300]] And still just one, after the second. [[slnc '
            '300]] They cost nothing, until needed.'
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
            'Now the costs, and they are heavy. [[slnc 400]] The first: '
            'you have swapped one big query for many small ones. [[slnc '
            "500]] A page lists twenty orders, and shows each customer's "
            'name. [[slnc 300]] With lazy loading: one query for the '
            'orders, then one query for each customer. [[slnc 300]] '
            'Twenty-one queries in all. [[slnc 300]] With batching: just '
            'two. [[slnc 500]] In a real system, every query is a round '
            'trip to the database. [[slnc 300]] So the lazy page can be '
            'slower than the eager one it replaced. [[slnc 300]] This '
            'problem is called N plus one.'
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
            'The second cost: reading a field is now a database call. '
            "[[slnc 400]] Asking for a customer's name looks like reading "
            'a field. [[slnc 300]] But it is not. [[slnc 300]] It is a '
            'trip to the database. [[slnc 500]] So it can be slow, and it '
            'can fail. [[slnc 300]] In this demo, the database is told to '
            'fail the next read. [[slnc 300]] And asking for a name '
            'throws an error. [[slnc 500]] Code that assumed a getter '
            'could never fail now has an error it never planned for.'
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
            'The third cost catches people out. [[slnc 400]] An object is '
            'created while its database session is open. [[slnc 300]] But '
            'nothing has been loaded yet. [[slnc 500]] Then the session '
            'closes. [[slnc 300]] And the object is passed on to a page. '
            "[[slnc 500]] The page asks for the customer's name. [[slnc "
            '300]] The load needs the session. [[slnc 300]] But the '
            'session is gone. [[slnc 300]] So it fails. [[slnc 500]] The '
            'failure appears where the object was used, not where it was '
            'created. [[slnc 300]] That is what makes it so hard to track '
            'down.'
        ),
    ),
    dict(
        key='09-met', kind='bullets', title='Where You Have Met This',
        body=['That failure has a name in Hibernate:', 'LazyInitializationException.', '', 'It is one of the most searched', 'Java errors there is.'],
        narration=(
            'You have very likely met this before. [[slnc 400]] In '
            'Hibernate, that failure has a name: Lazy Initialization '
            'Exception. [[slnc 300]] It is one of the most searched Java '
            'errors there is. [[slnc 500]] It is exactly what we just '
            'heard. [[slnc 300]] A lazy object, whose session has closed. '
            '[[slnc 300]] Now you know the cause, not just the '
            'workaround.'
        ),
    ),
    dict(
        key='10-toydb', kind='bullets', title='The Toy Database',
        body=['Rows, a counter, and now a read', 'that can be told to fail.', '', 'Every count in this video', 'came from its counter.'],
        narration=(
            'A word about the database in these demos. [[slnc 400]] It is '
            'a toy. [[slnc 300]] It has rows, an operation counter, and '
            'now a read that can be told to fail. [[slnc 500]] Every '
            'count in this video, the thirty-seven, the twenty-six, and '
            'the twenty-one, came from that counter.'
        ),
    ),
    dict(
        key='11-real', kind='bullets', title='What Is Real Here',
        body=['The counts are real.', 'The round trip cost is not measured:', 'the toy database has no network.', '', 'N+1 is slow in a real system', 'because each query is a trip.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'counts are real. [[slnc 300]] But the time for each round '
            'trip is not measured, because the toy database has no '
            'network. [[slnc 500]] N plus one is slow in a real system, '
            'because each query is a trip. [[slnc 300]] Here you hear the '
            'count, and you can imagine the delay.'
        ),
    ),
    dict(
        key='12-too-much', kind='bullets', title='When This Is Too Much',
        body=['If you almost always need the related', 'data, lazy loading only adds queries.', '', 'It earns its place when the related', 'data is large and rarely needed.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If you almost always '
            'need the related data, lazy loading only adds extra queries. '
            '[[slnc 400]] It earns its place when the related data is '
            'large, and rarely needed.'
        ),
    ),
    dict(
        key='13-fixes', kind='bullets', title='What To Do About It',
        body=['Batch: one query for all the customers.', 'Join: fetch the parts you know you need.', 'Keep the session open until the page', 'is done, or load before you leave.'],
        narration=(
            'So what do you do about the costs? [[slnc 500]] Batch: fetch '
            'all the customers in one query. [[slnc 300]] Join: fetch the '
            'parts you know you will need, together, up front. [[slnc '
            '300]] And keep the session open until the page is finished. '
            '[[slnc 300]] Or load what you need, before the session '
            'closes. [[slnc 500]] Each of those is a decision the lazy '
            'load made for you, which you are now taking back.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Change the lazy list so it', 'fetches each customer only once.'],
        narration=(
            "That's the Lazy Load pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Lazy loading '
            'trades one big query for many small ones, and moves any '
            'failure to wherever the object is used. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Change the lazy list, so '
            'each customer is fetched only once. [[slnc 300]] Then count '
            'the queries again. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
