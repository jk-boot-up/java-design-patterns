"""Scene definitions for the Identity Map teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Identity Map',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Identity Map '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: keep '
            'a map, for one session, from an id to the one object loaded '
            'for it, so asking for the same thing twice gives you the '
            'same object. [[slnc 350]] This is the second project in the '
            'enterprise category. It solves a problem the Data Mapper '
            'creates: once objects and rows are separate, one row can '
            'become two objects. In our online store, the row is a '
            'customer. [[slnc 300]] By the end you will know how two '
            'copies of one customer lose a change silently, why '
            'overriding equals does not fix it, how the map does, and '
            'what the map costs.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['An order is loaded, and its customer with it.', '', 'Separately, the caller loads the same', 'customer by id.', '', 'It is one row in the database.'],
        narration=(
            'Here is the scenario. An order page loads an order, and the '
            'customer who placed it. [[slnc 300]] Somewhere else, the '
            'same code loads that same customer directly, by id. [[slnc '
            '300]] It is one row in the database. The question this video '
            'answers is: how many objects should that be?'
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
            'The naive mapper builds a fresh object on every load. [[slnc '
            '300]] Load the order, and its customer comes with it. Load '
            'customer seven by id, and you get another. Are they the same '
            'object? False. Three selects went to the database, for what '
            'is one customer. [[slnc 300]] Two objects now both say they '
            'are customer seven.'
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
            'Now the bug. One of the two objects moves her to York. The '
            'other changes her email. Each does its job. [[slnc 300]] '
            'Both are saved, and each save writes the whole row. The '
            'second save writes the old address back over the first. '
            '[[slnc 300]] The stored address is Leeds again. The stored '
            'email is the new one. The move to York silently disappeared. '
            'Nothing failed. The last writer simply won.'
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
            'A common first fix is to override equals, so two customers '
            'with the same id are equal. [[slnc 300]] The demo does that. '
            'The two objects are now equal. But they are still two '
            'objects. One says York. The other still says Leeds. [[slnc '
            '300]] Equal is not the same as the same. Each object is '
            'still free to be changed on its own.'
        ),
    ),
    dict(
        key='06-pattern', kind='bullets', title='The Pattern',
        body=['A map, for one session, from id to object.', '', 'Ask for customer 7: look in the map first.', 'Only on a miss, go to the database,', 'then put the object in the map.'],
        narration=(
            'The pattern is a map. It lives for one session, and maps an '
            'id to the one object loaded for it. [[slnc 300]] Ask for '
            'customer seven. Look in the map first. Only if it is '
            'missing, go to the database, build the object, and put it in '
            'the map. [[slnc 300]] Every route to customer seven, the '
            "order's customer included, goes through the same map."
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
            "Same demo, with the map. The order's customer, and customer "
            'seven loaded by id, are the same object. True. [[slnc 300]] '
            "Two selects in all: the order's own row, and the customer, "
            'once. [[slnc 300]] Ask for customer seven twice more, and it '
            'costs zero operations. Both come from the map. And with only '
            'one object, one change can no longer overwrite another.'
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
            'Now the bill. First cost: the map is a cache. [[slnc 300]] '
            "Another process changes the customer's email in the "
            'database. This session asks again, and the map answers with '
            'the old email. It has no reason to look. [[slnc 300]] A '
            'brand new session, with an empty map, sees the new one. '
            'Speed and freshness are being traded, and the map decides '
            'which wins.'
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
            'Second cost. The map holds a reference to every object it '
            'has loaded. [[slnc 300]] A bulk load of one thousand '
            'customers leaves one thousand objects held, until the '
            'session ends. A long-running session with a lot of loads is '
            'a memory problem waiting to happen.'
        ),
    ),
    dict(
        key='10-scope', kind='bullets', title='Cost Three: Scope Is A Decision',
        body=['Per request: too small, and the same', 'customer can be two objects again.', '', 'Per session: stale for as long as it lives.', '', 'Per application: stale, and it only grows.'],
        narration=(
            'Third cost: scope is a decision, and every choice is wrong '
            'in some way. [[slnc 300]] Per request is safe from '
            'staleness, but too small if two requests need to agree. Per '
            'session goes stale for as long as the session lives. Per '
            'application is stale, and only ever grows. [[slnc 300]] '
            'There is no scope that is free.'
        ),
    ),
    dict(
        key='11-toydb', kind='bullets', title='The Toy Database',
        body=['Rows, not objects.', 'Every operation counted.', 'Nothing needs installing.', '', 'Every count in this video', 'came from its counter.'],
        narration=(
            'A word about the database in these demos. It is a toy. It '
            'stores rows, not objects, it counts every operation, and it '
            'needs nothing installed. [[slnc 300]] Every count in this '
            'video, the three selects, the two, the zero, came from that '
            'counter, not from guessing.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['The JPA persistence context is', 'an identity map.', '', 'Load the same entity twice in one', 'transaction: you get one object,', 'and == is true.'],
        narration=(
            'You have almost certainly met this. The persistence context '
            'in JPA is an identity map. [[slnc 300]] Load the same entity '
            'twice inside one transaction, and you get the same object. '
            'That is why double equals is true there. If a second find '
            'ever surprised you by not touching the database, this was '
            'why.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The pattern is real.', 'The database is a stand-in:', 'no transactions, no other processes.', '', 'Staleness is simulated by writing', 'to the table directly.'],
        narration=(
            'The same honest admission as everywhere in this course. The '
            'pattern is real. The database is a stand-in. There are no '
            'real transactions here, and no second process. [[slnc 300]] '
            'Staleness in act five is simulated by writing to the table '
            'directly, which is exactly what another process would do.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['A request that loads a customer once', 'and never again does not need a map.', '', 'It earns its place when the same row', 'can be reached by two routes.'],
        narration=(
            'So when is it too much? A request that loads a customer '
            'once, and never again, gains nothing from a map. [[slnc '
            '300]] It earns its place when the same row can be reached by '
            'two different routes, as it was here, and when two objects '
            'for one row would be a bug.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add an evict method to the session,', 'and decide when you would call it.'],
        narration=(
            "That's the Identity Map. [[slnc 250]] If you take one "
            'sentence away, take this one: one row should be one object, '
            'per session, and the session decides how long that stays '
            'true. [[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'add an evict method to the session, and decide when you '
            'would call it. [[slnc 300]] If this helped, a like genuinely '
            'does help other people find it, and subscribe if you would '
            'like the rest of the series. [[slnc 250]] Thanks for '
            'watching.'
        ),
    ),
]
