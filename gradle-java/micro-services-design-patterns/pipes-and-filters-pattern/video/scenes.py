"""Scene definitions for the Pipes and Filters teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Pipes and Filters',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Pipes and '
            'Filters pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: pipes '
            'and filters breaks a job into small independent steps, '
            'called filters, joined end to end, so each step does one '
            'thing, and steps can be added, swapped or reused. [[slnc '
            '350]] This is another project in the microservices category, '
            'whose subject is how many small services stay reliable when '
            'they talk to each other. In our online store, the job is '
            'importing a file of orders from a partner. [[slnc 300]] By '
            'the end you will see one method do five jobs, see five small '
            'steps joined end to end, swap and add a step without '
            'touching the others, see bad lines rejected with reasons '
            'while the rest continue, see streaming keep memory small, '
            'and see the bill, which is that the steps must agree on a '
            'shape.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A partner sends a file of order', 'lines: customer, item, quantity.', '', 'Each line is parsed, checked,', 'priced, taxed, and formatted.', '', 'One method, or five steps?'],
        narration=(
            'Here is the scenario. A partner sends a file of order lines: '
            'a customer, an item, and a quantity. Each line must be '
            'parsed, checked, priced, taxed, and turned into a '
            'confirmation. [[slnc 300]] The question: one method, or five '
            'steps?'
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
            'First, one method does it all. Six lines go in, and three '
            'come out. Five separate jobs are inside one loop: parsing, '
            'checking, pricing, tax and formatting. And the three lines '
            'that were dropped left no trace of why.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Break the job into small steps.', '', 'Each step takes an item and', 'gives one back, or drops it and', 'says why.', '', 'Join them end to end.', '', 'Items flow through one at a time.'],
        narration=(
            'The pattern. Break the job into small steps. Each step takes '
            'an item and gives one back, or drops it and says why. Join '
            'them end to end. Items flow through, one at a time.'
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
            'Second, small steps, joined. The same job is now five steps: '
            'parse, validate, price, UK tax, format. The price step, run '
            'on its own, turns one parsed line into a priced one, sixteen '
            'hundred pence. It needs none of the others to be tested.'
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
            'Third, swap a step, add a step. With the UK tax step, two '
            'mugs cost nineteen pounds twenty. Swap it for the EU one, '
            'and they cost nineteen thirty six. Then add a new step in '
            'the middle. No other step changed. The pipeline is a list of '
            'steps, and the steps do not know each other.'
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
            'Fourth, bad lines are rejected, and the rest go on. Three '
            'orders come out. Three lines were rejected, each with the '
            'step that dropped it, and the reason: twelve is not a '
            'number, fifty of the blue mug is too many, and a line with '
            'only two fields. One bad line does not stop the file.'
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
            'Fifth, streaming, or one stage at a time. Ten thousand '
            'lines. Streaming, where each item goes all the way through '
            'before the next, holds one item at once. Running each stage '
            'over the whole batch holds twenty thousand. The results are '
            'the same. Only the memory differs.'
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
            'Last, the bill. If the steps pass loose maps, one step calls '
            'a field qty, and the next asks for quantity, and it fails at '
            'run time, in the later step. Typed items catch that when '
            'compiling, but now every step depends on the type before it, '
            'and changing one means changing its neighbours. And an error '
            'shows up in the step that noticed it, which may be far from '
            'the step that caused it.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A chain of .map(...).filter(...)', 'on a stream.', '', 'A Unix pipeline with |.', '', "Spring Batch's reader, processor", 'and writer, and Camel routes.'],
        narration=(
            'How do you recognise this in code you did not write? A chain '
            'of .map(...).filter(...) on a stream. A Unix pipeline with '
            "|. Spring Batch's reader, processor and writer, and Camel "
            'routes. A list of processors, each with one process method.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use pipes and filters when a job', 'is a sequence of independent', 'transformations, when steps will', 'change or be reused, and when', 'items can be handled one at a', 'time. Type the items between', 'steps, report rejects with the', 'step and the reason, and stream', 'where the data is large. Keep a'],
        narration=(
            'Here is my verdict, plainly. Use pipes and filters when a '
            'job is a sequence of independent transformations, when steps '
            'will change or be reused, and when items can be handled one '
            'at a time. Type the items between steps, report rejects with '
            'the step and the reason, and stream where the data is large. '
            'Keep a pipeline short enough to read. Do not use it where '
            'steps need the whole batch.'
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
        body=['For a job with two simple steps, a', 'pipeline is more structure than', 'the job. Where every step needs', 'the whole batch, a pipeline gains', 'nothing.'],
        narration=(
            'So when is it too much? For a job with two simple steps, a '
            'pipeline is more structure than the job. Where every step '
            'needs the whole batch, a pipeline gains nothing.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Pipes and Filters. [[slnc 250]] If you take one "
            'sentence away, take this one: pipes and filters make each '
            'step small and replaceable, and the price is that the steps '
            'must agree on the shape between them. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, add a step that removes duplicate '
            'customers, and see what it needs to hold. [[slnc 300]] If '
            'this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
