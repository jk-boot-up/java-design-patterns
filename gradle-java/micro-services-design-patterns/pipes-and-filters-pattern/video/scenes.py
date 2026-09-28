"""Scene definitions for the Pipes and Filters teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Pipes and Filters',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Pipes and Filters pattern, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Pipes and filters breaks a '
            'job into small, independent steps, called filters. [[slnc '
            '300]] The steps are joined end to end, by pipes. [[slnc '
            '300]] Each step does one thing, and steps can be added, '
            'swapped, or reused. [[slnc 600]] Think of a car wash. [[slnc '
            '300]] The car rolls through: soap, then brushes, then rinse, '
            'then dry. [[slnc 300]] Each station does one job, and you '
            'can add a wax station without changing the others. [[slnc '
            '700]] In our online store, the job is importing a file of '
            'orders from a partner. [[slnc 500]] By the end, you will '
            'hear one method do five jobs. [[slnc 300]] Then five small '
            'steps joined end to end. [[slnc 300]] A step swapped, and a '
            'step added, without touching the others. [[slnc 300]] Bad '
            'lines rejected, with reasons. [[slnc 300]] Memory kept '
            'small. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A partner sends a file of order', 'lines: customer, item, quantity.', '', 'Each line is parsed, checked,', 'priced, taxed, and formatted.', '', 'One method, or five steps?'],
        narration=(
            'Here is the scenario. [[slnc 400]] A partner sends a file of '
            'order lines. [[slnc 300]] Each line has a customer, an item, '
            'and a quantity. [[slnc 500]] Each line must be read, '
            'checked, priced, taxed, and turned into a confirmation. '
            '[[slnc 500]] So here is the question. [[slnc 300]] One big '
            'method, or five small steps?'
        ),
    ),
    dict(
        key='03-one', kind='console', title='One Method Does It All',
        body="""ONE. One method.
  6 lines in, 3 out.

  5 jobs in one loop.

  the 3 dropped lines left no
  trace of why.""",
        narration=(
            'First demo: one method does it all. [[slnc 400]] Six lines '
            'go in. [[slnc 300]] Three come out. [[slnc 500]] Five '
            'separate jobs are packed into one loop. [[slnc 300]] '
            'Reading, checking, pricing, tax, and formatting. [[slnc '
            '500]] And the three lines that were dropped left no trace of '
            'why.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Break the job into small steps.', '', 'Each step takes an item and', 'gives one back, or drops it and', 'says why.', '', 'Join them end to end.', '', 'Items flow through one at a time.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Break the job into small '
            'steps. [[slnc 300]] Each step takes an item, and gives one '
            'back. [[slnc 300]] Or it drops the item, and says why. '
            '[[slnc 500]] Join the steps end to end. [[slnc 300]] And '
            'items flow through, one at a time.'
        ),
    ),
    dict(
        key='05-steps', kind='console', title='Small Steps, Joined',
        body="""TWO. Steps.
  parse | validate | price |
  uk-tax | format.

  the price step alone:
  netPence 1600.

  no need for the others.""",
        narration=(
            'Second demo: small steps, joined. [[slnc 400]] The same job '
            'is now five steps. [[slnc 300]] Read the line. [[slnc 200]] '
            'Check it. [[slnc 200]] Price it. [[slnc 200]] Add U K tax. '
            '[[slnc 200]] Format the confirmation. [[slnc 600]] The price '
            'step can run on its own. [[slnc 300]] It turns one read line '
            'into a priced one: sixteen pounds. [[slnc 300]] So it can be '
            'tested without any of the other steps.'
        ),
    ),
    dict(
        key='06-swap', kind='console', title='Swap A Step, Add A Step',
        body="""THREE. Swap, add.
  uk tax: £19.20.
  eu tax: £19.36.

  a new step in the middle:
  no other step changed.""",
        narration=(
            'Third demo: swap a step, and add a step. [[slnc 400]] With '
            'the U K tax step, two mugs cost nineteen pounds twenty. '
            '[[slnc 300]] Swap it for the European tax step, and they '
            'cost nineteen pounds thirty-six. [[slnc 600]] Then add a '
            'brand new step in the middle. [[slnc 300]] No other step '
            'changed. [[slnc 500]] The pipeline is just a list of steps. '
            '[[slnc 300]] And the steps do not know about each other.'
        ),
    ),
    dict(
        key='07-reject', kind='console', title='Bad Lines Are Rejected, And The Rest Go On',
        body="""FOUR. Rejects.
  3 orders out.
  3 rejected:
  parse: 'twelve' is not a
  number.
  validate: 50 of MUG-BLUE.
  parse: 3 fields needed.""",
        narration=(
            'Fourth demo: bad lines are rejected, and the rest carry on. '
            '[[slnc 400]] Three orders come out. [[slnc 300]] Three lines '
            'were rejected. [[slnc 300]] Each one names the step that '
            'dropped it, and the reason. [[slnc 500]] One says: twelve, '
            'written as a word, is not a number. [[slnc 300]] One says: '
            'fifty blue mugs is too many. [[slnc 300]] And one line had '
            'only two of its three fields. [[slnc 500]] One bad line does '
            'not stop the whole file.'
        ),
    ),
    dict(
        key='08-stream', kind='console', title='Streaming, Or One Stage At A Time',
        body="""FIVE. Streaming.
  10000 lines.
  streaming: 1 item held.
  a stage at a time: 20000.

  same results, different
  memory.""",
        narration=(
            'Fifth demo: streaming, or one stage at a time. [[slnc 400]] '
            'Ten thousand lines. [[slnc 500]] With streaming, each item '
            'goes all the way through before the next one starts. [[slnc '
            '300]] So only one item is held in memory at once. [[slnc '
            '500]] Running each step over the whole file before the next '
            'step holds twenty thousand items. [[slnc 500]] The results '
            'are the same. [[slnc 300]] Only the memory used is '
            'different.'
        ),
    ),
    dict(
        key='09-shape', kind='console', title='The Bill: The Steps Must Agree On The Shape',
        body="""SIX. The bill.
  loose maps: qty vs quantity,
  fails at run time.

  typed items: caught when
  compiling, but each step
  depends on the one before.

  errors appear far from cause.""",
        narration=(
            'Finally, the bill. [[slnc 300]] The steps must agree on the '
            'shape of the data between them. [[slnc 600]] Suppose the '
            'steps pass simple bags of named values. [[slnc 300]] One '
            'step calls a field q t y. [[slnc 300]] The next asks for '
            'quantity, spelled out. [[slnc 300]] It fails only when the '
            'program runs, inside the later step. [[slnc 600]] If the '
            'steps pass proper Java types instead, the compiler catches '
            'that mistake. [[slnc 300]] But now every step depends on the '
            'shape the step before it produces. [[slnc 300]] So changing '
            'one step can mean changing its neighbours. [[slnc 600]] And '
            'an error shows up in the step that noticed it. [[slnc 300]] '
            'Which may be far from the step that caused it.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A chain of .map(...).filter(...)', 'on a stream.', '', 'A Unix pipeline with |.', '', "Spring Batch's reader, processor", 'and writer, and Camel routes.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a chain of map and filter calls on a '
            'Java stream. [[slnc 300]] Look for a Unix command line with '
            'vertical bars joining commands together. [[slnc 300]] Look '
            "for Spring Batch's reader, processor, and writer, or Apache "
            'Camel routes. [[slnc 300]] Or a list of processors, each '
            'with one process method.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use pipes and filters when a job', 'is a sequence of independent', 'transformations, when steps will', 'change or be reused, and when', 'items can be handled one at a', 'time. Type the items between', 'steps, report rejects with the', 'step and the reason, and stream', 'where the data is large. Keep a'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use pipes and filters '
            'when a job is a series of independent changes to each item. '
            '[[slnc 300]] When steps will change, or be reused. [[slnc '
            '300]] And when items can be handled one at a time. [[slnc '
            '600]] Give the data between steps a proper type. [[slnc '
            '300]] Report every rejected item, with the step and the '
            'reason. [[slnc 300]] Stream the data when it is large. '
            '[[slnc 300]] And keep the pipeline short enough to read. '
            '[[slnc 500]] Do not use it when a step needs the whole batch '
            'at once.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] "
            'Nothing depends on a real clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a job with two simple steps, a', 'pipeline is more structure than', 'the job. Where every step needs', 'the whole batch, a pipeline gains', 'nothing.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a job with only '
            'two simple steps, a pipeline is more structure than the job '
            'itself. [[slnc 400]] And when every step needs the whole '
            'batch, a pipeline gains nothing.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Pipes and Filters pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Pipes '
            'and filters make each step small and replaceable, and the '
            'price is that the steps must agree on the shape of the data '
            'between them. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            'is one exercise to try. [[slnc 300]] Add a step that removes '
            'duplicate customers. [[slnc 300]] Then notice what that step '
            'needs to remember. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
