"""Scene definitions for the Identity Map teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Identity Map',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Identity Map pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] An identity map keeps a '
            'list, for one session, from each I D to the one object '
            'loaded for it. [[slnc 300]] So asking for the same thing '
            'twice gives you the very same object. [[slnc 600]] Think of '
            "a library's loan desk. [[slnc 300]] If a book is already out "
            'on your card, the librarian does not print you a second '
            'copy. [[slnc 300]] You get the one you already have. [[slnc '
            '700]] In our online store, the thing loaded twice is a '
            'customer. [[slnc 500]] By the end, you will know how two '
            'copies of one customer silently lose a change. [[slnc 300]] '
            'Why overriding equals does not fix it. [[slnc 300]] How the '
            'map does. [[slnc 300]] And what the map costs.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['An order is loaded, and its customer with it.', '', 'Separately, the caller loads the same', 'customer by id.', '', 'It is one row in the database.'],
        narration=(
            'Here is the scenario. [[slnc 400]] An order page loads an '
            'order, together with the customer who placed it. [[slnc '
            '400]] Somewhere else, the same page loads that same customer '
            'directly, by I D. [[slnc 500]] It is one row in the '
            'database. [[slnc 300]] So here is the question. [[slnc 300]] '
            'How many objects should that be?'
        ),
    ),
    dict(
        key='03-two-objects', kind='console', title='Two Loads, Two Objects',
        body="""ONE. Two loads.
  same object (==): false

  3 selects: the order, its
  customer, and the same
  customer again.""",
        narration=(
            'First demo: two loads, two objects. [[slnc 400]] The naive '
            'loader builds a fresh object every time. [[slnc 500]] Load '
            'the order, and its customer comes with it. [[slnc 300]] Load '
            'customer seven by I D, and you get another object. [[slnc '
            '300]] Are they the same object? [[slnc 300]] No. [[slnc '
            '500]] Three database queries were made, for what is really '
            'one customer. [[slnc 300]] And two separate objects now both '
            'claim to be customer seven.'
        ),
    ),
    dict(
        key='04-lost-change', kind='console', title='The Lost Change',
        body="""TWO. The lost change.
  stored address:
  12 Mill Lane, Leeds
  stored email:
  ada@newmail.example

  the address change vanished.""",
        narration=(
            'Second demo: the lost change. [[slnc 400]] One of the two '
            'objects moves the customer to York. [[slnc 300]] The other '
            'changes her email address. [[slnc 500]] Both are saved. '
            '[[slnc 300]] And each save writes the whole row. [[slnc '
            '300]] So the second save writes the old address, Leeds, back '
            'over the new one. [[slnc 500]] The stored address is Leeds '
            'again. [[slnc 300]] The stored email is the new one. [[slnc '
            '300]] The move to York silently disappeared. [[slnc 500]] '
            'Nothing failed. [[slnc 300]] The last one to save simply '
            'won.'
        ),
    ),
    dict(
        key='05-equals', kind='console', title='equals() Is Not Enough',
        body="""THREE. equals().
  equals: true
  same object: false

  one says York, the other
  still says Leeds.

  equal, and still separately
  changeable.""",
        narration=(
            'Third demo: overriding equals is not enough. [[slnc 400]] A '
            'common first fix is to override the equals method. [[slnc '
            '300]] So two customers with the same I D count as equal. '
            '[[slnc 500]] Now the two objects are equal. [[slnc 300]] But '
            'they are still two separate objects. [[slnc 300]] One says '
            'York. [[slnc 300]] The other still says Leeds. [[slnc 500]] '
            'Equal is not the same as being the same object. [[slnc 300]] '
            'Each can still be changed on its own.'
        ),
    ),
    dict(
        key='06-pattern', kind='bullets', title='The Pattern',
        body=['A map, for one session, from id to object.', '', 'Ask for customer 7: look in the map first.', 'Only on a miss, go to the database,', 'then put the object in the map.'],
        narration=(
            'Now, the pattern: a map. [[slnc 400]] It lives for one '
            'session. [[slnc 300]] And it maps each I D to the one object '
            'loaded for it. [[slnc 500]] Ask for customer seven. [[slnc '
            '300]] First, look in the map. [[slnc 300]] Only if it is '
            'missing, go to the database, build the object, and put it in '
            'the map. [[slnc 500]] Every route to customer seven, '
            "including the order's customer, goes through the same map."
        ),
    ),
    dict(
        key='07-one-object', kind='console', title='One Map, One Object',
        body="""FOUR. The pattern.
  same object (==): true

  2 selects: the order's row,
  and the customer once.

  two more finds cost 0
  operations.""",
        narration=(
            'Fourth demo: one map, one object. [[slnc 400]] Now the '
            "order's customer, and customer seven loaded by I D, are the "
            'very same object. [[slnc 500]] Only two queries in total. '
            '[[slnc 300]] One for the order, and one for the customer. '
            '[[slnc 500]] Ask for customer seven twice more, and it costs '
            'no queries at all. [[slnc 300]] Both come straight from the '
            'map. [[slnc 500]] And with only one object, one change can '
            'no longer overwrite another.'
        ),
    ),
    dict(
        key='08-stale', kind='console', title='Cost One: The Map Is A Cache',
        body="""FIVE. Stale.
  another process changed
  the email.

  this session sees:
  ada@example.com
  a new session sees:
  ada@other.example""",
        narration=(
            'Now the costs. [[slnc 300]] The first: the map is a cache. '
            "[[slnc 500]] Another program changes the customer's email in "
            'the database. [[slnc 300]] This session asks again. [[slnc '
            '300]] And the map answers with the old email, because it has '
            'no reason to look. [[slnc 500]] A brand new session, with an '
            'empty map, sees the new email. [[slnc 500]] Speed and '
            'freshness are being traded. [[slnc 300]] And the map decides '
            'which one wins.'
        ),
    ),
    dict(
        key='09-memory', kind='console', title='Cost Two: It Holds Everything',
        body="""SIX. Memory.
  a bulk load of 1000
  customers:
  the session now holds
  1000 objects.""",
        narration=(
            'The second cost: the map holds on to everything. [[slnc '
            '400]] It keeps a reference to every object it has loaded. '
            '[[slnc 500]] A bulk load of one thousand customers leaves '
            'one thousand objects held in memory, until the session ends. '
            '[[slnc 500]] A long-running session with many loads is a '
            'memory problem waiting to happen.'
        ),
    ),
    dict(
        key='10-scope', kind='bullets', title='Cost Three: Scope Is A Decision',
        body=['Per request: too small, and the same', 'customer can be two objects again.', '', 'Per session: stale for as long as it lives.', '', 'Per application: stale, and it only grows.'],
        narration=(
            'The third cost: how long the map lives is a decision. [[slnc '
            '400]] And every choice is wrong in some way. [[slnc 500]] '
            'One map per request is always fresh. [[slnc 300]] But it may '
            'be too small, if two requests need to agree. [[slnc 400]] '
            'One map per session goes stale for as long as the session '
            'lives. [[slnc 400]] One map for the whole application goes '
            'stale, and only ever grows. [[slnc 500]] There is no choice '
            'that is free.'
        ),
    ),
    dict(
        key='11-toydb', kind='bullets', title='The Toy Database',
        body=['Rows, not objects.', 'Every operation counted.', 'Nothing needs installing.', '', 'Every count in this video', 'came from its counter.'],
        narration=(
            'A word about the database in these demos. [[slnc 400]] It is '
            'a toy. [[slnc 300]] It stores rows, not objects. [[slnc '
            '300]] It counts every operation. [[slnc 300]] And it needs '
            'nothing installed. [[slnc 500]] Every count in this video '
            'came from that counter, not from guessing.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['The JPA persistence context is', 'an identity map.', '', 'Load the same entity twice in one', 'transaction: you get one object,', 'and == is true.'],
        narration=(
            'You have almost certainly met this pattern already. [[slnc '
            "400]] In Java's persistence standard, J P A, the persistence "
            'context is an identity map. [[slnc 500]] Load the same '
            'entity twice, inside one transaction, and you get the very '
            'same object. [[slnc 300]] If a second lookup ever surprised '
            'you by not touching the database, this was why.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The pattern is real.', 'The database is a stand-in:', 'no transactions, no other processes.', '', 'Staleness is simulated by writing', 'to the table directly.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'pattern is real. [[slnc 300]] The database is a stand-in, '
            'with no real transactions, and no second program. [[slnc '
            '500]] The out-of-date data is simulated by writing to the '
            'table directly. [[slnc 300]] Which is exactly what another '
            'program would do.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['A request that loads a customer once', 'and never again does not need a map.', '', 'It earns its place when the same row', 'can be reached by two routes.'],
        narration=(
            'So, when is this too much? [[slnc 400]] A request that loads '
            'a customer once, and never again, gains nothing from a map. '
            '[[slnc 500]] It earns its place when the same row can be '
            'reached by two different routes, as it was here. [[slnc '
            '300]] And when two objects for one row would be a bug.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add an evict method to the session,', 'and decide when you would call it.'],
        narration=(
            "That's the Identity Map pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] One '
            'row should be one object, per session, and the session '
            'decides how long that stays true. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Add a method that removes '
            'one object from the map. [[slnc 300]] And decide when you '
            'would call it. [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
