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
            'Hello, and welcome. This video explains the Splitter and '
            'Aggregator pattern in Java, using the real framework that '
            'does it for a living: Apache Camel. [[slnc 250]] It is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] '
            'Here is the plain definition, in general words. A splitter '
            'takes one message and turns it into several. Each of those '
            'pieces carries two things: which whole it came from, and '
            'its own place in that whole. An aggregator does the '
            'opposite. It holds pieces that belong together and sends '
            'out one message when a rule says they are ready. [[slnc '
            '350]] Now the same thing in our online store. A customer '
            'has three things in the basket, and the three products sit '
            'in three different warehouses: Leeds, Reading and Glasgow. '
            'The order is split into one shipment per warehouse, each '
            'warehouse picks and prices its own line, and the answers '
            'are gathered back into one price for the customer: two '
            'hundred and eighty three pounds and forty two pence. '
            '[[slnc 300]] By the end you will have seen the order split '
            'and gathered, seen an aggregator that will wait for ever '
            'because nobody gave it a deadline, seen a real deadline '
            'end that wait on its own, and seen the moment Camel '
            'declares an order finished when it is not.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['One basket, three lines.', '', 'Leeds, Reading and Glasgow', 'each hold one of them.', '', 'One worker walks all three,', 'one line after another.', '', 'Split it, and put it back?'],
        narration=(
            'Here is the scenario. One basket has three lines, and the '
            'three products sit in three different warehouses: Leeds, '
            'Reading and Glasgow. One worker takes the whole basket and '
            'walks all three, one line after another, while the other '
            'two warehouses do nothing. [[slnc 300]] The question is '
            'whether we can split the order between the three '
            'warehouses, and put the answers back together afterwards.'
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
            'First, one picker and one order. Order four four seven one '
            'has three lines, held in three warehouses. One worker walks '
            'all of them, one line after another. That is three steps of '
            'work on one thread, and the basket comes to two hundred and '
            'eighty three pounds and forty two pence. While that worker '
            'walks, the other two warehouses stand idle.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="Camel's Three Words",
        body=['A route is the path a message', 'takes, written down.', '', 'A correlation is the rule for', 'reading which order a message', 'belongs to.', '', 'A completion condition decides', 'when the gathering is finished.'],
        narration=(
            'Camel brings three words with it, and each one is simpler '
            'than it sounds. [[slnc 250]] A route is just the path a '
            'message takes, written down: where it starts, what happens '
            'to it, where it goes. [[slnc 250]] A correlation is the '
            'rule for reading, off each message, which order it belongs '
            'to. Here that is the order number. [[slnc 250]] And a '
            'completion condition is the rule that decides when the '
            'gathering has waited long enough. That third one is the '
            'whole of this video. You have to supply it yourself, and if '
            'you supply the wrong one, nothing ever comes out.'
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
            'Second, Camel splits the order. The split step sends out '
            'one message for each line: shipment one of three to Leeds, '
            'shipment two of three to Reading, shipment three of three '
            'to Glasgow. [[slnc 250]] Camel numbers the pieces itself, '
            'and it copies the order number onto every one of them. '
            'Nobody arranged that. And that number is the only thing '
            'that will put the order back together.'
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
            'Third, they come back in any order. The warehouses answered '
            'third, first, second. The aggregator does not care. It files '
            'each arrival under the place that arrival says it is, so the '
            'answer comes out in the customer\'s own line order, totalling '
            'the same two hundred and eighty three pounds and forty two '
            'pence the single worker reached. [[slnc 250]] Camel records '
            'why it finished, and the word it used was size: three '
            'messages had arrived, and three were expected.'
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
            'Fourth, and this is the part the hand-built version never '
            'had to face. Glasgow is closed. Its message reaches the '
            'warehouse and stops there, and nothing further along the '
            'path is told anything at all. Two shipments come back to an '
            'aggregator whose only completion condition is a count of '
            'three. [[slnc 250]] Two is not three. No answer comes out, '
            'one order sits open, and nothing will ever change that. An '
            'aggregator with only a count is a queue of orders that will '
            'never come out.'
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
            'Fifth, a deadline. The same thing happens to a second '
            'aggregator, and this one has a second completion condition: '
            'six hundred milliseconds, looked at every hundred. A '
            'background checker watches the clock the whole time. When '
            'the deadline passes, it ends the wait, and nobody asked it '
            'to. [[slnc 250]] Camel says the reason was timeout, not '
            'size. The answer carries two of three shipments, names '
            'Glasgow as the one that never came, and comes to two '
            'hundred and sixty five pounds and ninety seven pence: the '
            'basket, minus the Glasgow line. [[slnc 250]] The simulation '
            'had a clock the demo could push forward thirty minutes in '
            'one line. A real deadline needs something running.'
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
            'The difference between the aggregator that waits for ever '
            'and the one that gives up is two lines. Both gather by the '
            'order number, and both finish when as many messages have '
            'arrived as the order said there would be. The second one '
            'also names a deadline in milliseconds, and how often to '
            'look at the clock. [[slnc 250]] Whichever condition is met '
            'first ends the wait. Never write the first without the '
            'second.'
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
            'Last, the bill. A thousand orders each short of one '
            'shipment means a thousand orders held in the aggregator\'s '
            'memory, and memory is where Camel keeps them unless you say '
            'otherwise, so a restart throws every one of them away. '
            '[[slnc 300]] Then the surprise. Completion by size counts '
            'messages, not distinct pieces. Deliver the Reading shipment '
            'twice and three messages have arrived, so Camel declares '
            'the order finished, with only two of its three lines in it. '
            'The duplicate check is yours to write, and it is the '
            'difference between charging two hundred and sixty five '
            'pounds and ninety seven pence, and charging five hundred '
            'and fifteen pounds and ninety six.'
        ),
    ),
    dict(
        key='11-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['It got the whole shape right:', 'stamp, gather, de-duplicate,', 'give up.', '', 'It left out three things.', '', 'The condition is yours to supply.', 'The deadline needs a clock that', 'runs. And a lost piece is an', 'event, not a skipped line.'],
        narration=(
            'The hand-built partner project got the whole shape right. '
            'One message becomes several, each piece is stamped, the '
            'aggregator gathers by the stamp, counts a repeat once and '
            'gives up on an order that has waited too long. Every one of '
            'those lessons is true of Camel. [[slnc 300]] It left out '
            'three things, and they are the three this video is for. The '
            'completion condition is something you supply, and can leave '
            'out. The deadline needs something actually watching a clock '
            'while the rest of the program carries on. And a piece that '
            'never comes back is a real event, not a line the demo chose '
            'not to run.'
        ),
    ),
    dict(
        key='12-recognise', kind='bullets', title='How To Recognise It',
        body=['A split in one place and an', 'aggregate in another, joined', 'only by an identifier.', '', 'A completion size with no', 'timeout beside it.', '', 'A store of unfinished groups,', 'left in memory.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'split step in one place and an aggregate step in another, '
            'joined only by an identifier carried on the messages. A '
            'completion size with no timeout beside it, which is a queue '
            'of orders that will never come out. A completion condition '
            'read from a header, so the splitter tells the aggregator '
            'how many to expect. And a store of unfinished groups left '
            'in memory, which a restart empties.'
        ),
    ),
    dict(
        key='13-verdict', kind='bullets', title='The Verdict',
        body=['Split when the pieces can be', 'worked on separately and the', 'work is slow enough to pay.', '', 'Stamp every piece with what it', 'came from and where it sits.', '', 'Then say two things out loud:', 'when it is done, and when it has', 'waited long enough. Never only', 'the first.'],
        narration=(
            'Here is my verdict, plainly. Split when the pieces can be '
            'worked on separately, and the work is slow enough that '
            'doing several at once pays for the trouble. Give every '
            'piece the identity of the thing it came from and its own '
            'place in it. [[slnc 250]] Then, on the aggregator, say two '
            'things out loud: when it is done, and when it has waited '
            'long enough. Never set only the first. And write the '
            'duplicate check yourself, because the framework counts '
            'messages and you care about pieces.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Apache Camel 4.20.0, running', 'inside the demo itself.', '', 'No container, no broker,', 'no network call.', '', 'Every number quoted comes from', "the program's own output, and", 'two runs print the same thing.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'This is Apache Camel, version four point twenty, running '
            'inside the demo\'s own process. There is no container, no '
            'broker and no network call anywhere in the project, so it '
            'runs offline with nothing installed but a Java development '
            'kit. [[slnc 250]] Every number quoted in this video comes '
            'from the program\'s own output, and two runs one after the '
            'other print the same thing.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['If the pieces are quick, or each', 'needs the one before it,', 'splitting costs more than it', 'saves.', '', 'If nothing can go missing, the', 'hand-built version is smaller', 'and clearer.', '', 'And a framework has to be learned', 'before a route can be trusted.'],
        narration=(
            'So when is this too much? If the pieces are quick, or each '
            'piece needs the answer to the one before it, splitting '
            'costs more than it saves. If nothing can ever go missing, '
            'the hand-built partner project is smaller and clearer, and '
            'teaches the same idea. And a framework has to be learned '
            'before a route can be trusted: a route is easy to read and '
            'hard to guess.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Splitter and Aggregator with Camel. [[slnc 250]] If "
            'you take one sentence away, take this one: an aggregator '
            'with only a count will wait for ever, so the deadline is '
            'not a nicety, it is the other half of the pattern. [[slnc '
            '350]] The full source, the written notes, the diagrams and '
            'an animated walkthrough are all in the repository, running '
            'offline with nothing installed but a Java development kit. '
            '[[slnc 300]] If you try one exercise, take the deadline off '
            'the second aggregator and run it again, and watch the fifth '
            'act stop producing an answer at all. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, '
            'and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
