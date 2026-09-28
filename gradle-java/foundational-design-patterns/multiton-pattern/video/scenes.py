"""Scene definitions for the Multiton teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Multiton',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Multiton pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A multiton is like a '
            'singleton, but with a key. [[slnc 300]] It keeps exactly one '
            'instance for each key. [[slnc 300]] And it hands back that '
            'same instance every time the key is asked for. [[slnc 600]] '
            "Think of a hotel's key cabinet. [[slnc 300]] There is "
            'exactly one hook for each room number. [[slnc 300]] Ask for '
            'room twelve, and you always get the same key. [[slnc 700]] '
            'In our online store, there is one warehouse for each region. '
            '[[slnc 300]] And every part of the shop must agree about '
            'which warehouse is which. [[slnc 500]] In this video, two '
            'copies of one warehouse disagree. [[slnc 300]] Then there is '
            'one warehouse per region, and everyone agrees. [[slnc 300]] '
            'We will hear unknown regions refused, a race between two '
            'threads, and then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Warehouses in the UK, the EU', 'and the US.', '', 'Many parts of the shop reserve', 'stock.', '', 'All of them must see the same', 'stock for a region.', '', 'How do they share it?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The shop has a warehouse '
            'in the UK, one in the EU, and one in the US. [[slnc 400]] '
            'Many parts of the shop reserve stock. [[slnc 300]] And all '
            'of them must see the same stock for a region. [[slnc 500]] '
            'So here is the question. [[slnc 300]] How do they share each '
            'warehouse?'
        ),
    ),
    dict(
        key='03-new', kind='console', title='A New One Each Time',
        body="""ONE. A new one each time.
  two callers each made a
  UK warehouse.
  same object: false.
  A has 90, B has 100.

  two beliefs about one
  warehouse.""",
        narration=(
            'First, the naive way: a new warehouse object each time. '
            '[[slnc 400]] Two callers each create a UK warehouse. [[slnc '
            '300]] They are not the same object. [[slnc 500]] One has a '
            'stock of ninety. [[slnc 300]] The other has a stock of one '
            'hundred. [[slnc 500]] The shop now believes two different '
            'things about one real warehouse.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A private constructor.', '', 'A map from key to instance.', '', 'Ask for a key: you get the one', 'instance for it, made the first', 'time it is asked for.'],
        narration=(
            'Now, the pattern. [[slnc 400]] The warehouse class has a '
            'private constructor. [[slnc 300]] So nobody outside can '
            'create one. [[slnc 500]] It keeps a map, from each region to '
            'its one warehouse. [[slnc 300]] Ask for a region, and you '
            'get the one warehouse for it. [[slnc 300]] It is created the '
            'first time that region is asked for.'
        ),
    ),
    dict(
        key='05-one', kind='console', title='One Per Region',
        body="""TWO. One per region.
  UK asked twice: same object.
  EU: a different one.
  created so far: 2.""",
        narration=(
            'Second demo: one warehouse per region. [[slnc 400]] Ask for '
            'the UK twice, and you get the same object. [[slnc 300]] Ask '
            'for the EU, and you get a different one. [[slnc 500]] '
            'Warehouses created so far: two.'
        ),
    ),
    dict(
        key='06-shared', kind='console', title='Shared, So They Agree',
        body="""THREE. Shared.
  one part reserved 10 in the UK.
  another part sees 90.
  the EU warehouse has 100.""",
        narration=(
            'Third demo: shared, so everyone agrees. [[slnc 400]] One '
            'part of the shop reserves ten items in the UK. [[slnc 300]] '
            'Another part asks for the UK warehouse, and sees a stock of '
            'ninety. [[slnc 500]] And the EU warehouse still has one '
            'hundred.'
        ),
    ),
    dict(
        key='07-keys', kind='console', title='A Fixed Set Of Keys',
        body="""FOUR. A fixed set of keys.
  asked for MARS: refused.
  no warehouse in MARS.
  instances held: 3.""",
        narration=(
            'Fourth demo: a fixed set of keys. [[slnc 400]] Someone asks '
            'for a warehouse on Mars. [[slnc 300]] It is refused: there '
            'is no warehouse in Mars. [[slnc 500]] Warehouses held: '
            'three.'
        ),
    ),
    dict(
        key='08-race', kind='console', title='Two Threads, One Region',
        body="""FIVE. Two threads.
  look first, create second:
  both looked before either
  created. created: 2.

  atomic create-if-absent,
  8 threads: same object.
  created: 1.""",
        narration=(
            'Fifth demo: two threads, one region. [[slnc 400]] First, the '
            'careless way. [[slnc 300]] Look in the map first, and create '
            'second, with no lock. [[slnc 300]] Both threads look before '
            'either one creates. [[slnc 300]] So two warehouses are '
            'created, and they are not the same object. [[slnc 600]] Now '
            'the careful way: an atomic, create if absent. [[slnc 300]] '
            'Eight threads ask at once. [[slnc 300]] They all get the '
            'same object. [[slnc 300]] And exactly one is created.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  a test reserved 30.
  the next test sees 70, not 100.
  state leaks between tests.

  instances live forever.

  any code can reach any
  warehouse.""",
        narration=(
            'Finally, the cost. [[slnc 400]] One test reserves thirty '
            'items. [[slnc 300]] The next test starts, and asks for the '
            'UK warehouse. [[slnc 300]] Its stock is seventy, not one '
            'hundred. [[slnc 500]] State leaks from one test into the '
            'next. [[slnc 300]] The warehouses live as long as the '
            'program does. [[slnc 300]] Nothing ever lets one go. [[slnc '
            '500]] And any code, anywhere, can reach any warehouse. '
            '[[slnc 300]] So finding out who changed the stock is hard.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A static Map of instances and a', 'getInstance(key) method.', '', 'ConcurrentHashMap.computeIfAbsent', 'used to create on demand.', '', 'Currency.getInstance(code), Locale', 'constants and Charset.forName.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a static map of instances, and a get '
            'instance method that takes a key. [[slnc 300]] Look for a '
            "concurrent map's compute if absent, used to create on "
            'demand. [[slnc 300]] In Java itself, look at Currency get '
            'instance, and Charset for name. [[slnc 300]] And enums, '
            'which are a multiton built into the language.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a multiton when there must be', 'exactly one object for each of a', 'small fixed set of keys. Create', 'with an atomic create-if-absent.', 'Give tests a way to reset. And', 'prefer passing the object in, when', 'you can, so that the sharing is', 'visible.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a multiton when '
            'there must be exactly one object, for each of a small, fixed '
            'set of keys. [[slnc 500]] Create the objects with an atomic, '
            'create if absent. [[slnc 300]] Give tests a way to reset. '
            '[[slnc 300]] And when you can, prefer passing the object in. '
            '[[slnc 300]] So that the sharing is visible.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If an enum can name the fixed set,', 'use an enum. If the object can be', 'passed in, pass it in. A multiton', 'is global state with a key.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If an enum can name '
            'the fixed set, use an enum. [[slnc 300]] If the object can '
            'be passed in, pass it in. [[slnc 400]] A multiton is global '
            'state, with a key.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Multiton pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A multiton '
            'gives exactly one instance for each key, and the price is '
            'global state that outlives every test. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Add a fourth region. '
            '[[slnc 300]] And confirm that nothing else in the shop has '
            'to change. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
