"""Scene definitions for the Multiton teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Multiton',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Multiton pattern '
            'in Java, and it is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] The plain definition: a multiton is a '
            'singleton with a key. It keeps exactly one instance for each '
            'key, and hands back that same instance every time the key is '
            'asked for. [[slnc 350]] This is another project in the '
            'foundational category, whose subject is how an object gets '
            'hold of another, and how small idioms shape everyday Java. '
            'In our online store, there is one warehouse for each region, '
            'and every part of the shop must agree about which warehouse '
            'is which. [[slnc 300]] By the end you will see two copies of '
            'one warehouse disagree, see one warehouse per region, see '
            'the parts of the shop agree, see unknown regions refused, '
            'see two threads make two warehouses without a lock and one '
            'with an atomic create, and see the bill, which is leaked '
            'state and instances that live forever.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Warehouses in the UK, the EU', 'and the US.', '', 'Many parts of the shop reserve', 'stock.', '', 'All of them must see the same', 'stock for a region.', '', 'How do they share it?'],
        narration=(
            'Here is the scenario. The shop has a warehouse in the UK, '
            'one in the EU, and one in the US. Many parts of the shop '
            'reserve stock, and all of them must see the same stock for a '
            'region. [[slnc 300]] The question: how do they share it?'
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
            'First, a new one each time. Two callers each made a UK '
            'warehouse. They are not the same object. One has stock '
            'ninety, the other a hundred. The shop now believes two '
            'different things about one warehouse.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A private constructor.', '', 'A map from key to instance.', '', 'Ask for a key: you get the one', 'instance for it, made the first', 'time it is asked for.'],
        narration=(
            'The pattern. A private constructor. A map from key to '
            'instance. Ask for a key, and you get the one instance for '
            'it, made the first time it is asked for.'
        ),
    ),
    dict(
        key='05-one', kind='console', title='One Per Region',
        body="""TWO. One per region.
  UK asked twice: same object.
  EU: a different one.
  created so far: 2.""",
        narration=(
            'Second, one per region. Asked for the UK twice, it is the '
            'same object. Asked for the EU, it is a different one. '
            'Created so far: two.'
        ),
    ),
    dict(
        key='06-shared', kind='console', title='Shared, So They Agree',
        body="""THREE. Shared.
  one part reserved 10 in the UK.
  another part sees 90.
  the EU warehouse has 100.""",
        narration=(
            'Third, shared, so they agree. One part of the shop reserved '
            'ten in the UK. Another part, asking for the UK, sees stock '
            'ninety. The EU warehouse has a hundred.'
        ),
    ),
    dict(
        key='07-keys', kind='console', title='A Fixed Set Of Keys',
        body="""FOUR. A fixed set of keys.
  asked for MARS: refused.
  no warehouse in MARS.
  instances held: 3.""",
        narration=(
            'Fourth, a fixed set of keys. Asked for Mars, it is refused: '
            'no warehouse in Mars. Instances held: three.'
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
            'Fifth, two threads, one region. Look first, create second, '
            'with no lock: both threads looked before either created. Not '
            'the same object, and two were created. With an atomic create '
            'if absent, eight threads at once get the same object, and '
            'one is created.'
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
            'Last, the bill. One test reserved thirty. The next test '
            'starts, and asks for the UK: stock seventy, not a hundred. '
            'State leaks from one test to the next. The instances live as '
            'long as the program does, and nothing ever lets one go. And '
            'any code can reach any warehouse from anywhere, so who '
            'changed the stock is hard to say.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A static Map of instances and a', 'getInstance(key) method.', '', 'ConcurrentHashMap.computeIfAbsent', 'used to create on demand.', '', 'Currency.getInstance(code), Locale', 'constants and Charset.forName.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'static Map of instances and a getInstance(key) method. '
            'ConcurrentHashMap.computeIfAbsent used to create on demand. '
            'Currency.getInstance(code), Locale constants and '
            'Charset.forName. Enums, which are a multiton the language '
            'provides.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a multiton when there must be', 'exactly one object for each of a', 'small fixed set of keys. Create', 'with an atomic create-if-absent.', 'Give tests a way to reset. And', 'prefer passing the object in, when', 'you can, so that the sharing is', 'visible.'],
        narration=(
            'Here is my verdict, plainly. Use a multiton when there must '
            'be exactly one object for each of a small fixed set of keys. '
            'Create with an atomic create-if-absent. Give tests a way to '
            'reset. And prefer passing the object in, when you can, so '
            'that the sharing is visible.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. Every number quoted comes from '
            "this program's own output. Nothing depends on a clock, so "
            'every run is the same.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If an enum can name the fixed set,', 'use an enum. If the object can be', 'passed in, pass it in. A multiton', 'is global state with a key.'],
        narration=(
            'So when is it too much? If an enum can name the fixed set, '
            'use an enum. If the object can be passed in, pass it in. A '
            'multiton is global state with a key.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Multiton. [[slnc 250]] If you take one sentence away, "
            'take this one: a multiton gives exactly one instance for '
            'each key, and the price is global state that outlives every '
            'test. [[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'add a fourth region, and confirm that nothing else changes. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
