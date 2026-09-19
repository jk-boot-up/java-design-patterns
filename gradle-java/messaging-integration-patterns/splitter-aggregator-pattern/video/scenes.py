"""Scene definitions for the Splitter and Aggregator teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Splitter and Aggregator',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Splitter and '
            'Aggregator pattern in Java, and it is written and presented '
            'by Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'splitter breaks one message into several, each carrying an '
            'id and its place. An aggregator collects the pieces by that '
            'id, and puts them back together as one. [[slnc 350]] This is '
            'the third project in the messaging and integration category, '
            'whose subject is how separate systems exchange messages '
            'safely. In our online store, the order with several lines, '
            'in aisles far apart, is picked by several people at once. '
            '[[slnc 300]] By the end you will see an order picked by one '
            'person, see it split into parts that carry their place, see '
            'the parts finish out of order and come back together, see a '
            'missing part handled by a timeout, and see the bill, which '
            'is memory for every open order and the care duplicates need.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['An order has three lines,', 'in aisles far apart.', '', 'One picker does them in a row.', '', 'Other pickers stand idle.', '', 'Split it, and put it back?'],
        narration=(
            'Here is the scenario. An order has three lines, in aisles '
            'far apart. One picker does them one after another, and other '
            'pickers stand idle. [[slnc 300]] The question: can we split '
            'the order between pickers, and put it back together '
            'afterwards?'
        ),
    ),
    dict(
        key='03-one', kind='console', title='One Message, One Picker',
        body="""ONE. One picker.
  an order of 3 lines, picked
  one after another.

  3 steps in a row.
  the other pickers are idle.""",
        narration=(
            'First, one message, one picker. An order of three lines is '
            'picked by one person, one line after another. Three steps of '
            'work in a row, in aisles that are far apart, while the other '
            'pickers stand idle.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A splitter breaks the order into', 'one message for each line.', '', "Each carries the order's id, and", 'its place: part 2 of 3.', '', 'An aggregator collects them by', 'id, and puts them back.'],
        narration=(
            'The pattern. A splitter breaks the order into one message '
            "for each line. Each carries the order's id, and its own "
            'place: part two of three. An aggregator collects them by the '
            'id, and puts them back together.'
        ),
    ),
    dict(
        key='05-split', kind='console', title='Split It',
        body="""TWO. Split.
  ORD-1 part 1 of 3.
  ORD-1 part 2 of 3.
  ORD-1 part 3 of 3.

  each carries the id and its
  place.""",
        narration=(
            'Second, split it. The order becomes three parts. Part one of '
            'three, part two of three, part three of three. Each carries '
            "the order's id, and its own place. That is what lets them be "
            'put back together.'
        ),
    ),
    dict(
        key='06-order', kind='console', title='The Parts Finish In Any Order',
        body="""THREE. Any order.
  suppose they finish 3, 1, 2.

  nothing guarantees the parts
  come back in the order they
  went.""",
        narration=(
            'Third, the parts finish in any order. Suppose the three '
            'pickers finish in the order three, one, two. Nothing '
            'guarantees that the parts come back in the order they went.'
        ),
    ),
    dict(
        key='07-gather', kind='console', title='Gather Them By The Id',
        body="""FOUR. Gather.
  part 3 arrives: waiting.
  part 1 arrives: waiting.
  part 2 arrives: complete,
  in the original line order.""",
        narration=(
            'Fourth, gather them by the id. Part three arrives, and the '
            'aggregator waits. Part one arrives, and it waits. Part two '
            'arrives, and the order is complete: the three lines, back in '
            'their original order, from parts that arrived out of order.'
        ),
    ),
    dict(
        key='08-missing', kind='console', title='A Part Never Arrives',
        body="""FIVE. A missing part.
  parts 1 and 3 arrive.
  29 minutes: still waiting.
  30 minutes: gives up.
  2 of 3 lines, missing part 2,
  complete: false.

  no timeout, no end.""",
        narration=(
            'Fifth, a part never arrives. Parts one and three arrive. '
            "Part two's picker has gone home. After twenty nine minutes, "
            'nothing has expired. After thirty, the aggregator gives up. '
            'It has two of three lines, part two is named as missing, and '
            'the result says it is not complete. Without a timeout, it '
            'would wait forever, and so would the customer.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  1000 orders, each missing a
  part: 1000 held in memory.

  a part twice: counted once.

  two orders with the same id
  would mix. the id must be
  unique.""",
        narration=(
            'Last, the bill. A thousand orders, each missing one part, '
            'means a thousand orders held in memory, waiting. A part '
            'delivered twice is counted once, and noted. And two orders '
            'with the same id would be mixed into one, so the id that '
            'ties the parts together has to be unique.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A message that carries a', 'correlationId, a sequenceNumber', '', "Spring Integration's splitter and", "aggregator, Camel's split and", '', 'A map keyed by an id, holding what', 'has arrived so far.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'message that carries a correlationId, a sequenceNumber and a '
            "sequenceSize. Spring Integration's splitter and aggregator, "
            "Camel's split and aggregate. A map keyed by an id, holding "
            'what has arrived so far. A timeout on collecting the results '
            'of a batch.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a splitter and aggregator when', 'one message contains parts that', 'can be worked on separately, and', 'the work is slow enough that doing', 'it in parallel pays. Number every', 'part and carry the id and the', 'total. Aggregate with a timeout,', 'drop duplicates, and decide what', 'to do with a partial result. Watch'],
        narration=(
            'Here is my verdict, plainly. Use a splitter and aggregator '
            'when one message contains parts that can be worked on '
            'separately, and the work is slow enough that doing it in '
            'parallel pays. Number every part and carry the id and the '
            'total. Aggregate with a timeout, drop duplicates, and decide '
            'what to do with a partial result. Watch the number of open '
            'aggregations.'
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
        body=['If the parts are quick, or depend', 'on each other, splitting is', 'overhead. If order matters between', 'the parts, an aggregator needs', 'more than the parts.'],
        narration=(
            'So when is it too much? If the parts are quick, or depend on '
            'each other, splitting is overhead. If order matters between '
            'the parts, an aggregator needs more than the parts.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Splitter and Aggregator. [[slnc 250]] If you take one "
            'sentence away, take this one: a splitter and aggregator '
            'share work by carrying an id and a place, and the price is '
            'state to hold and a timeout to choose. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, make the aggregator reject a part '
            'whose total disagrees with the first part it saw. [[slnc '
            '300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of '
            'the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
