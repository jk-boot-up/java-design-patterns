"""Scene definitions for the Splitter and Aggregator with Camel teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, explains each of Camel's words in plain
language before using it, and never points at a picture the listener cannot see.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Splitter and Aggregator with Camel',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Splitter and Aggregator pattern, in Java, using Apache '
            'Camel. [[slnc 300]] This video is presented by Jayasekhar '
            'Konduru. [[slnc 600]] First, a simple definition. [[slnc '
            '300]] A splitter takes one message and turns it into '
            'several. [[slnc 300]] Each piece carries two things: which '
            'whole it came from, and its own place in that whole. [[slnc '
            '500]] An aggregator does the opposite. [[slnc 300]] It holds '
            'pieces that belong together. [[slnc 300]] And sends out one '
            'message, when a rule says they are ready. [[slnc 600]] In '
            'our online store, a basket has three items, in three '
            'different warehouses: Leeds, Reading, and Glasgow. [[slnc '
            '300]] The order is split into one shipment per warehouse. '
            '[[slnc 300]] Each warehouse prices its own line. [[slnc '
            '300]] And the answers are gathered back into one price: two '
            'hundred and eighty-three pounds forty-two. [[slnc 500]] By '
            'the end, you will hear an aggregator that waits forever, '
            'because nobody gave it a deadline. [[slnc 300]] A real '
            'deadline ending that wait. [[slnc 300]] And the moment Camel '
            'declares an order finished, when it is not.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['One basket, three lines.', '', 'Leeds, Reading and Glasgow', 'each hold one of them.', '', 'One worker walks all three,', 'one line after another.', '', 'Split it, and put it back?'],
        narration=(
            'Here is the scenario. [[slnc 400]] One basket has three '
            'items. [[slnc 300]] And the three products sit in three '
            'different warehouses: Leeds, Reading, and Glasgow. [[slnc '
            '500]] One worker takes the whole basket, and walks all '
            'three, one after another. [[slnc 300]] While the other two '
            'warehouses do nothing. [[slnc 500]] So here is the question. '
            '[[slnc 300]] Can we split the order between the three '
            'warehouses, and put the answers back together?'
        ),
    ),
    dict(
        key='03-one', kind='console', title='One Picker, One Order',
        body="""ONE. One picker.
  order ORD-4471, 3 lines,
  in 3 warehouses.

  3 steps of work on 1 thread.
  the basket comes to GBP 283.42.""",
        narration=(
            'First, one picker, and one order. [[slnc 400]] Order four '
            'four seven one has three lines, in three warehouses. [[slnc '
            '300]] One worker handles every line, one after another. '
            '[[slnc 500]] Three steps of work, on one thread. [[slnc '
            '300]] And the basket comes to two hundred and eighty-three '
            'pounds forty-two. [[slnc 300]] While that worker walks, the '
            'other two warehouses stand idle.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="Camel's Three Words",
        body=['A route is the path a message', 'takes, written down.', '', 'A correlation is the rule for', 'reading which order a message', 'belongs to.', '', 'A completion condition decides', 'when the gathering is finished.'],
        narration=(
            'Camel brings three words with it, and each is simpler than '
            'it sounds. [[slnc 500]] A route is the path a message takes, '
            'written down. [[slnc 300]] Where it starts, what happens to '
            'it, and where it goes. [[slnc 500]] A correlation is the '
            'rule for reading which order a message belongs to. [[slnc '
            '300]] Here, that is the order number. [[slnc 500]] And a '
            'completion condition is the rule that decides when the '
            'gathering is finished. [[slnc 500]] That third word is the '
            'heart of this video. [[slnc 300]] You must supply it '
            'yourself. [[slnc 300]] And if you supply the wrong one, '
            'nothing ever comes out.'
        ),
    ),
    dict(
        key='05-split', kind='console', title='Camel Splits The Order',
        body="""TWO. Split.
  shipment 1 of 3 to Leeds.
  shipment 2 of 3 to Reading.
  shipment 3 of 3 to Glasgow.

  Camel numbered the pieces, and
  copied the order number on.""",
        narration=(
            'Second demo: Camel splits the order. [[slnc 400]] The split '
            'step sends out one message for each line. [[slnc 300]] '
            'Shipment one of three, to Leeds. [[slnc 200]] Shipment two '
            'of three, to Reading. [[slnc 200]] Shipment three of three, '
            'to Glasgow. [[slnc 500]] Camel numbers the pieces itself. '
            '[[slnc 300]] And it copies the order number onto every one '
            'of them. [[slnc 300]] That number is the only thing that '
            'will put the order back together.'
        ),
    ),
    dict(
        key='06-order', kind='console', title='They Come Back In Any Order',
        body="""THREE. Any order.
  they answered: 3, 1, 2.

  completed by: size.
  3 of 3 shipments,
  total GBP 283.42,
  in the customer's line order.""",
        narration=(
            'Third demo: the answers come back in any order. [[slnc 400]] '
            'The warehouses answer third, then first, then second. [[slnc '
            '500]] The aggregator does not mind. [[slnc 300]] It files '
            'each answer under the place that answer says it belongs. '
            "[[slnc 300]] So the result comes out in the customer's own "
            'order, totalling two hundred and eighty-three pounds '
            'forty-two. [[slnc 500]] And Camel records why it finished: '
            'size. [[slnc 300]] Three messages had arrived, and three '
            'were expected.'
        ),
    ),
    dict(
        key='07-condition', kind='console', title='The Completion Condition',
        body="""FOUR. Glasgow is closed.
  shipments back: 2 of 3.
  answers out: 0.
  orders still open: 1.

  2 is not 3. nothing comes out,
  and nothing ever will.""",
        narration=(
            'Fourth demo, and this is what the hand-built version never '
            'faced. [[slnc 400]] The Glasgow warehouse is closed. [[slnc '
            '300]] Its message reaches the warehouse, and stops there. '
            '[[slnc 500]] Two shipments come back, to an aggregator whose '
            'only rule is a count of three. [[slnc 300]] Two is not '
            'three. [[slnc 500]] No answer comes out. [[slnc 300]] One '
            'order sits open. [[slnc 300]] And nothing will ever change '
            'that. [[slnc 500]] An aggregator with only a count is a '
            'queue of orders that will never come out.'
        ),
    ),
    dict(
        key='08-deadline', kind='console', title='A Deadline',
        body="""FIVE. A deadline.
  600 ms, checked every 100.

  completed by: timeout.
  2 of 3 shipments,
  missing [Glasgow],
  gathered so far GBP 265.97.""",
        narration=(
            'Fifth demo: a deadline. [[slnc 400]] The same thing happens '
            'to a second aggregator. [[slnc 300]] But this one has a '
            'second rule: a deadline of six hundred milliseconds, checked '
            'every hundred. [[slnc 500]] A background checker watches the '
            'clock the whole time. [[slnc 300]] When the deadline passes, '
            'it ends the wait, by itself. [[slnc 500]] Camel records the '
            'reason as timeout, not size. [[slnc 300]] The answer carries '
            'two of three shipments. [[slnc 300]] It names Glasgow as the '
            'one that never came. [[slnc 300]] And it comes to two '
            'hundred and sixty-five pounds ninety-seven: the basket, '
            'without the Glasgow item.'
        ),
    ),
    dict(
        key='09-route', kind='code', title='The Whole Difference',
        body="""from("direct:gather-with-timeout")
  .aggregate(header("orderId"), fold)
    .completionSize(header("shipmentCount"))
    .completionTimeout(600)
    .completionTimeoutCheckerInterval(100)
  .process(this::publish);""",
        narration=(
            'The difference between waiting forever, and giving up, is '
            'two lines. [[slnc 400]] Both aggregators gather by the order '
            'number. [[slnc 300]] And both finish when the expected '
            'number of messages has arrived. [[slnc 500]] The second one '
            'also names a deadline in milliseconds, and how often to '
            'check the clock. [[slnc 500]] Whichever rule is met first '
            'ends the wait. [[slnc 300]] So never write the count, '
            'without the deadline.'
        ),
    ),
    dict(
        key='10-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  1000 orders held in memory,
  and a restart loses them all.

  a shipment delivered twice:
  finished at 2 of 3 lines.
  GBP 265.97 with the check,
  GBP 515.96 without it.""",
        narration=(
            'Finally, the costs. [[slnc 400]] A thousand orders, each '
            'missing one shipment, means a thousand orders held in '
            'memory. [[slnc 300]] And memory is where Camel keeps them, '
            'unless told otherwise. [[slnc 300]] So a restart throws '
            'every one of them away. [[slnc 600]] Then the surprise. '
            '[[slnc 300]] Completing by size counts messages, not '
            'different pieces. [[slnc 500]] Deliver the Reading shipment '
            'twice, and three messages have arrived. [[slnc 300]] So '
            'Camel declares the order finished, with only two of its '
            'three lines. [[slnc 500]] The duplicate check is yours to '
            'write. [[slnc 300]] With it, the customer pays two hundred '
            'and sixty-five pounds ninety-seven. [[slnc 300]] Without it, '
            'they pay five hundred and fifteen pounds ninety-six.'
        ),
    ),
    dict(
        key='11-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['It got the whole shape right:', 'stamp, gather, de-duplicate,', 'give up.', '', 'It left out three things.', '', 'The condition is yours to supply.', 'The deadline needs a clock that', 'runs. And a lost piece is an', 'event, not a skipped line.'],
        narration=(
            'The hand-built partner video got the whole shape right. '
            '[[slnc 400]] Split, stamp each piece, gather by the stamp, '
            'count a repeat once, and give up after waiting too long. '
            '[[slnc 300]] All of that is true of Camel too. [[slnc 600]] '
            'But it left out three things. [[slnc 400]] The completion '
            'rule is something you must supply, and can forget. [[slnc '
            '300]] The deadline needs something actually watching a '
            'clock, while the rest of the program carries on. [[slnc '
            '300]] And a piece that never comes back is a real event, not '
            'a line the demo chose to skip.'
        ),
    ),
    dict(
        key='12-recognise', kind='bullets', title='How To Recognise It',
        body=['A split in one place and an', 'aggregate in another, joined', 'only by an identifier.', '', 'A completion size with no', 'timeout beside it.', '', 'A store of unfinished groups,', 'left in memory.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a split step in one place, and an aggregate '
            'step in another, joined only by an I D on the messages. '
            '[[slnc 300]] Look for a completion size, with no timeout '
            'beside it. [[slnc 300]] That is a queue of orders that may '
            'never come out. [[slnc 300]] And look for unfinished groups '
            'kept only in memory, which a restart will empty.'
        ),
    ),
    dict(
        key='13-verdict', kind='bullets', title='The Verdict',
        body=['Split when the pieces can be', 'worked on separately and the', 'work is slow enough to pay.', '', 'Stamp every piece with what it', 'came from and where it sits.', '', 'Then say two things out loud:', 'when it is done, and when it has', 'waited long enough. Never only', 'the first.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Split when the pieces '
            'can be worked on separately, and the work is slow enough to '
            'make parallel work worthwhile. [[slnc 300]] Stamp every '
            'piece with what it came from, and its place. [[slnc 500]] '
            'Then, on the aggregator, state two things clearly. [[slnc '
            '300]] When it is done. [[slnc 300]] And when it has waited '
            'long enough. [[slnc 300]] Never set only the first. [[slnc '
            '500]] And write the duplicate check yourself. [[slnc 300]] '
            'Because the framework counts messages, and you care about '
            'pieces.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Apache Camel 4.20.0, running', 'inside the demo itself.', '', 'No container, no broker,', 'no network call.', '', 'Every number quoted comes from', "the program's own output, and", 'two runs print the same thing.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] This is '
            'Apache Camel, version four point twenty, running inside the '
            "demo's own program. [[slnc 300]] There is no container, no "
            'broker, and no network call. [[slnc 300]] So it runs '
            'offline, with nothing installed except a Java development '
            'kit. [[slnc 500]] Every number you heard comes from the '
            "program's own output. [[slnc 300]] And two runs, one after "
            'the other, print the same results.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['If the pieces are quick, or each', 'needs the one before it,', 'splitting costs more than it', 'saves.', '', 'If nothing can go missing, the', 'hand-built version is smaller', 'and clearer.', '', 'And a framework has to be learned', 'before a route can be trusted.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If the pieces are '
            'quick, or each one needs the answer from the one before, '
            'splitting costs more than it saves. [[slnc 400]] If nothing '
            'can ever go missing, the hand-built version is smaller, and '
            'clearer. [[slnc 400]] And a framework must be learned before '
            'a route can be trusted. [[slnc 300]] A route is easy to '
            'read, but hard to guess.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Splitter and Aggregator, with Camel. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] An '
            'aggregator with only a count will wait forever, so the '
            'deadline is not a nice extra, it is the other half of the '
            'pattern. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Remove the deadline from the second aggregator, and '
            'run it again. [[slnc 300]] Then listen as the deadline demo '
            'stops producing any answer at all. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
