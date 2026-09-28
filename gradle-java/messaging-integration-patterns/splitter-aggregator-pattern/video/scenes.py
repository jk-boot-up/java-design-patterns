"""Scene definitions for the Splitter and Aggregator teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Splitter and Aggregator',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Splitter and Aggregator pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A splitter breaks '
            'one message into several smaller ones. [[slnc 300]] Each '
            'piece carries an I D, and its place, like part two of three. '
            '[[slnc 300]] An aggregator collects the pieces by that I D, '
            'and puts them back together as one. [[slnc 600]] Think of a '
            'group shopping trip. [[slnc 300]] One list is torn into '
            'three, and each friend fetches their part. [[slnc 300]] At '
            'the till, everything is put back together into one basket. '
            '[[slnc 700]] In our online store, one order has lines in '
            'aisles far apart, and several people pick it at once. [[slnc '
            '500]] In this video, we split an order, let the parts finish '
            'out of order, and put it back together. [[slnc 300]] We will '
            'handle a missing part with a timeout. [[slnc 300]] And then '
            'hear the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['An order has three lines,', 'in aisles far apart.', '', 'One picker does them in a row.', '', 'Other pickers stand idle.', '', 'Split it, and put it back?'],
        narration=(
            'Here is the scenario. [[slnc 400]] An order has three lines, '
            'in aisles far apart. [[slnc 300]] One picker does them one '
            'after another. [[slnc 300]] Meanwhile, other pickers stand '
            'idle. [[slnc 500]] So here is the question. [[slnc 300]] Can '
            'we split the order between pickers, and put it back together '
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
            'First, the simple way: one message, one picker. [[slnc 400]] '
            'An order of three lines is picked by one person, one line '
            'after another. [[slnc 500]] Three steps in a row, in aisles '
            'far apart. [[slnc 300]] While the other pickers stand idle.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A splitter breaks the order into', 'one message for each line.', '', "Each carries the order's id, and", 'its place: part 2 of 3.', '', 'An aggregator collects them by', 'id, and puts them back.'],
        narration=(
            'Now, the pattern. [[slnc 400]] A splitter breaks the order '
            'into one message for each line. [[slnc 300]] Each message '
            "carries the order's I D, and its own place: for example, "
            'part two of three. [[slnc 500]] Then an aggregator collects '
            'them by the I D. [[slnc 300]] And puts them back together.'
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
            'Second demo: split it. [[slnc 400]] The order becomes three '
            'parts. [[slnc 300]] Part one of three. [[slnc 200]] Part two '
            'of three. [[slnc 200]] Part three of three. [[slnc 500]] '
            "Each part carries the order's I D, and its own place. [[slnc "
            '300]] That is what makes it possible to put them back '
            'together.'
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
            'Third demo: the parts can finish in any order. [[slnc 400]] '
            'Suppose the three pickers finish in the order three, then '
            'one, then two. [[slnc 500]] Nothing guarantees the parts '
            'come back in the order they went out.'
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
            'Fourth demo: gather them by the I D. [[slnc 400]] Part three '
            'arrives, and the aggregator waits. [[slnc 300]] Part one '
            'arrives, and it waits. [[slnc 300]] Part two arrives, and '
            'the order is complete. [[slnc 500]] The three lines are back '
            'in their original order. [[slnc 300]] Even though they '
            'arrived out of order.'
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
            'Fifth demo: a part never arrives. [[slnc 400]] Parts one and '
            "three arrive. [[slnc 300]] But part two's picker has gone "
            'home. [[slnc 500]] After twenty-nine minutes, the aggregator '
            'is still waiting. [[slnc 300]] After thirty, it gives up. '
            '[[slnc 500]] It has two of the three lines. [[slnc 300]] '
            'Part two is named as missing. [[slnc 300]] And the result '
            'says clearly that it is not complete. [[slnc 500]] Without a '
            'timeout, it would wait forever. [[slnc 300]] And so would '
            'the customer.'
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
            'Finally, the cost. [[slnc 400]] A thousand orders, each '
            'missing one part, means a thousand orders held in memory, '
            'waiting. [[slnc 500]] A part delivered twice must be counted '
            'only once. [[slnc 300]] Here, it is, and the duplicate is '
            'noted. [[slnc 500]] And two orders sharing the same I D '
            'would get mixed into one. [[slnc 300]] So the I D that ties '
            'the parts together must be unique.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A message that carries a', 'correlationId, a sequenceNumber', '', "Spring Integration's splitter and", "aggregator, Camel's split and", '', 'A map keyed by an id, holding what', 'has arrived so far.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for messages that carry a correlation I D, '
            'a sequence number, and a total count. [[slnc 300]] Look for '
            "Spring Integration's splitter and aggregator, or Apache "
            "Camel's split and aggregate. [[slnc 300]] Look for a map, "
            'keyed by an I D, holding what has arrived so far. [[slnc '
            '300]] And look for a timeout on collecting the results of a '
            'batch.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a splitter and aggregator when', 'one message contains parts that', 'can be worked on separately, and', 'the work is slow enough that doing', 'it in parallel pays. Number every', 'part and carry the id and the', 'total. Aggregate with a timeout,', 'drop duplicates, and decide what', 'to do with a partial result. Watch'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a splitter and '
            'aggregator when one message contains parts that can be '
            'worked on separately. [[slnc 300]] And when the work is slow '
            'enough that doing it in parallel pays off. [[slnc 500]] '
            'Number every part, and carry the I D and the total. [[slnc '
            '300]] Collect with a timeout. [[slnc 300]] Ignore '
            'duplicates. [[slnc 300]] And decide what to do with a '
            'partial result. [[slnc 500]] Also, keep an eye on how many '
            'orders are waiting to be completed.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] Time "
            'is simulated, not read from the clock, so every run gives '
            'the same result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If the parts are quick, or depend', 'on each other, splitting is', 'overhead. If order matters between', 'the parts, an aggregator needs', 'more than the parts.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If the parts are '
            'quick, or depend on each other, splitting is just overhead. '
            '[[slnc 400]] And if the order between the parts matters, the '
            'aggregator needs more than just the parts.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Splitter and Aggregator pattern. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] A '
            'splitter and aggregator share work by carrying an I D and a '
            'place, and the price is state to hold, and a timeout to '
            'choose. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Make the aggregator reject any part whose total count '
            'disagrees with the first part it saw. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
