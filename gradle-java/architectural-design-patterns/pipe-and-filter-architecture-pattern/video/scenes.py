"""Scene definitions for the Pipe and Filter Architecture teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Pipe and Filter Architecture',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Pipe and Filter '
            'Architecture pattern in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] The plain '
            'definition: pipe and filter architecture splits work into '
            'stages that run at the same time, joined by waiting lines. '
            'Each stage can then be sized and limited on its own. [[slnc '
            '350]] This is another project in the architecture category, '
            'whose subject is how a whole application is arranged, and '
            'who may depend on whom. In our online store, orders arrive '
            'faster than we can process them, and the question is how to '
            'organise the work. [[slnc 300]] By the end you will see one '
            'big step finish few orders, see three stages overlap and '
            'finish more, see the slowest stage set the pace and a line '
            'pile up in front of it, see only that stage widened, see a '
            'limit on the lines push back on the door, and see the bill, '
            'which is orders lost when a stage crashes.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Every order is parsed,', 'priced and packed.', '', 'Parsing takes 1 tick,', 'pricing 3, packing 1.', '', 'An order arrives every tick.', '', 'How should we organise', 'the work?'],
        narration=(
            'Here is the scenario. Every order is parsed, priced and '
            'packed. Parsing takes one tick, pricing takes three, and '
            'packing takes one. An order arrives every tick. [[slnc 300]] '
            'The question: how should we organise the work?'
        ),
    ),
    dict(
        key='03-one', kind='console', title='One Big Step',
        body="""ONE. One big step.
  5 ticks for each order,
  one at a time.
  an order arrives every tick.

  after 30 ticks: 5 done.""",
        narration=(
            'First, one big step. One worker does all three jobs, five '
            'ticks for each order. An order arrives every tick. After '
            'thirty ticks, five orders are done.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Split the work into stages.', '', 'Each stage has a waiting line', 'in front of it.', '', 'Stages work at the same time,', 'and each can be sized and', 'limited on its own.'],
        narration=(
            'The pattern. Split the work into stages. Each stage has a '
            'waiting line in front of it. The stages work at the same '
            'time, and each can be sized and limited on its own.'
        ),
    ),
    dict(
        key='05-three', kind='console', title='Stages With Waiting Lines',
        body="""TWO. Three stages.
  each works while the others do.
  after 30 ticks: 8 done.

  parse takes a new order while
  price is on the last one.""",
        narration=(
            'Second, stages with waiting lines. The same work in three '
            'stages, each working while the others do. After thirty '
            'ticks, eight orders are done. Parse takes a new order while '
            'price is still on the last one.'
        ),
    ),
    dict(
        key='06-slow', kind='console', title='The Slowest Stage Sets The Pace',
        body="""THREE. The slowest sets the pace.
  waiting: parse 1, price 19,
  pack 0.

  price takes 3 ticks, so one
  order leaves every 3 ticks.
  orders pile up in front.""",
        narration=(
            'Third, the slowest stage sets the pace. Waiting in front of '
            'each stage: parse one, price nineteen, pack none. Price '
            'takes three ticks, so one order leaves every three ticks, '
            'however fast parse and pack are. Orders pile up in front of '
            'it.'
        ),
    ),
    dict(
        key='07-wide', kind='console', title='Widen Only The Slow Stage',
        body="""FOUR. Widen the slow stage.
  three price workers.
  after 30 ticks: 22 done.
  waiting: 1, 1, 1.

  parse and pack untouched.
  their one a tick is the new
  limit.""",
        narration=(
            'Fourth, widen only the slow stage. Three price workers. '
            'After thirty ticks, twenty two orders are done, and the '
            'lines are short. Parse and pack were not touched. Now they '
            'take one order a tick, and that is the new limit.'
        ),
    ),
    dict(
        key='08-limit', kind='console', title='A Limit On Each Line',
        body="""FIVE. A limit on each line.
  no limit: 19 waiting.
  limit 3: 3 waiting, and 14
  refused at the door.
  done: 8, the same.

  a full line makes the stage
  before it hold on. that is
  backpressure.""",
        narration=(
            'Fifth, a limit on each line. With no limit, nineteen orders '
            'wait in one line. With a limit of three, no more than three '
            'wait, and fourteen orders are refused at the door. Orders '
            'done is eight, the same as without a limit. A full line '
            'makes the stage before it hold its order, and so on, back to '
            'the door. That push-back is called backpressure.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  the price stage crashes.
  20 orders were in it.
  accepted, and gone, unless the
  lines are kept somewhere that
  survives.

  and one order can wait in
  every line it passes.""",
        narration=(
            'Last, the bill. The price stage crashes. Twenty orders were '
            'in it, waiting or being worked on. They were accepted from '
            'customers, and are gone, unless the lines are kept somewhere '
            'that survives. And an order now passes through three stages '
            'and two waiting lines, so a single order takes longer than '
            'its five ticks of work, whenever it has to wait.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Stages joined by queues, as in a', 'log-processing or ETL system.', '', 'Worker pools with a bounded queue', 'in front, such as', '', 'BlockingQueue between producer and', 'consumer threads.'],
        narration=(
            'How do you recognise this in code you did not write? Stages '
            'joined by queues, as in a log-processing or ETL system. '
            'Worker pools with a bounded queue in front, such as '
            'ThreadPoolExecutor. BlockingQueue between producer and '
            'consumer threads. Reactive streams and their request-n '
            'backpressure.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use stages when the work has parts', 'of different speed and you want', 'throughput. Find the slowest', 'stage, and widen only that one.', 'Put a limit on each waiting line', 'so that trouble pushes back to the', 'door. Keep the lines somewhere', 'that survives a crash if the', 'orders matter.'],
        narration=(
            'Here is my verdict, plainly. Use stages when the work has '
            'parts of different speed and you want throughput. Find the '
            'slowest stage, and widen only that one. Put a limit on each '
            'waiting line so that trouble pushes back to the door. Keep '
            'the lines somewhere that survives a crash if the orders '
            'matter.'
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
        body=['If the work is short, or the', 'stages are about equally fast, a', 'single step is simpler, and the', 'queues only add delay. Stages pay', 'off when parts differ in speed, or', 'need separate scaling.'],
        narration=(
            'So when is it too much? If the work is short, or the stages '
            'are about equally fast, a single step is simpler, and the '
            'queues only add delay. Stages pay off when parts differ in '
            'speed, or need separate scaling.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Pipe and Filter Architecture. [[slnc 250]] If you "
            'take one sentence away, take this one: pipe and filter '
            'architecture lets stages run together and be sized on their '
            'own, and the price is the lines between them, and the orders '
            'lost if a stage crashes. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, make parse two ticks and see which stage '
            'is now the slowest. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
