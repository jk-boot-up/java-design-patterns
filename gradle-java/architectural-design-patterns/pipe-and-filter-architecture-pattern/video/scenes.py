"""Scene definitions for the Pipe and Filter Architecture teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Pipe and Filter Architecture',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Pipe and Filter Architecture pattern, in Java. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Pipe and Filter '
            'splits work into stages that run at the same time. [[slnc '
            '300]] The stages are joined by waiting lines, called pipes. '
            '[[slnc 300]] Each stage can then be sized and limited on its '
            'own. [[slnc 600]] Think of a car wash. [[slnc 300]] One '
            'station soaps, one scrubs, and one dries. [[slnc 300]] While '
            'one car is being dried, the next is being scrubbed, and the '
            'next is being soaped. [[slnc 700]] In our online store, '
            'orders arrive faster than we can process them. [[slnc 300]] '
            'So how should we organise the work? [[slnc 500]] In this '
            'video, we split the work into stages, and find the slowest '
            'one. [[slnc 300]] We widen only that stage, limit the '
            'waiting lines, and then look at the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Every order is parsed,', 'priced and packed.', '', 'Parsing takes 1 tick,', 'pricing 3, packing 1.', '', 'An order arrives every tick.', '', 'How should we organise', 'the work?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Every order goes through '
            'three jobs. [[slnc 300]] It is parsed, then priced, then '
            'packed. [[slnc 500]] We measure time in ticks. [[slnc 300]] '
            'Parsing takes one tick. [[slnc 200]] Pricing takes three '
            'ticks. [[slnc 200]] Packing takes one tick. [[slnc 400]] And '
            'a new order arrives every tick. [[slnc 500]] So how should '
            'we organise the work?'
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
            'First, the simple way: one big step. [[slnc 400]] One worker '
            'does all three jobs for an order, which takes five ticks. '
            '[[slnc 300]] Then it starts the next order. [[slnc 400]] But '
            'a new order arrives every tick. [[slnc 500]] After thirty '
            'ticks, only five orders are finished.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Split the work into stages.', '', 'Each stage has a waiting line', 'in front of it.', '', 'Stages work at the same time,', 'and each can be sized and', 'limited on its own.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Split the work into stages. '
            '[[slnc 300]] Put a waiting line in front of each stage. '
            '[[slnc 400]] The stages all work at the same time. [[slnc '
            '300]] And each stage can be sized, and limited, on its own.'
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
            'Second demo: three stages, with waiting lines. [[slnc 400]] '
            'The same work is split into parse, price, and pack. [[slnc '
            '300]] Each stage works while the others work. [[slnc 500]] '
            'After thirty ticks, eight orders are finished, instead of '
            'five. [[slnc 400]] Parse can take a new order while price is '
            'still busy with the last one.'
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
            'Third demo: the slowest stage sets the pace. [[slnc 400]] '
            "Let's count who is waiting in front of each stage. [[slnc "
            '300]] Parse: one. [[slnc 200]] Price: nineteen. [[slnc 200]] '
            'Pack: none. [[slnc 500]] Pricing takes three ticks. [[slnc '
            '300]] So only one order leaves pricing every three ticks, '
            'however fast the other stages are. [[slnc 400]] And orders '
            'pile up in front of it.'
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
            'Fourth demo: widen only the slow stage. [[slnc 400]] We give '
            'pricing three workers instead of one. [[slnc 500]] After '
            'thirty ticks, twenty-two orders are finished. [[slnc 300]] '
            'And every waiting line is down to one. [[slnc 500]] Parse '
            'and pack were not changed at all. [[slnc 300]] Now they '
            'handle one order per tick. [[slnc 300]] And that is the new '
            'limit.'
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
            'Fifth demo: a limit on each waiting line. [[slnc 400]] With '
            'no limit, nineteen orders pile up in one line. [[slnc 400]] '
            'With a limit of three, no more than three ever wait. [[slnc '
            '300]] And fourteen orders are turned away at the door. '
            '[[slnc 500]] The number finished is still eight, the same as '
            'before. [[slnc 500]] Here is what happens. [[slnc 300]] When '
            'a line is full, the stage before it must hold on to its '
            'order. [[slnc 300]] That pressure passes back, stage by '
            'stage, all the way to the door. [[slnc 400]] This push-back '
            'is called backpressure.'
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
            'Finally, the cost. [[slnc 400]] Imagine the pricing stage '
            'crashes. [[slnc 300]] Twenty orders were inside it, either '
            'waiting or being worked on. [[slnc 400]] Those orders were '
            'accepted from customers. [[slnc 300]] And now they are gone. '
            '[[slnc 300]] Unless the waiting lines are stored somewhere '
            'that survives a crash. [[slnc 500]] There is a second cost. '
            '[[slnc 300]] Each order now passes through three stages and '
            'two waiting lines. [[slnc 300]] So whenever it has to wait, '
            'one order takes longer than its five ticks of actual work.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Stages joined by queues, as in a', 'log-processing or ETL system.', '', 'Worker pools with a bounded queue', 'in front, such as', '', 'BlockingQueue between producer and', 'consumer threads.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for stages joined by queues, as in log '
            'processing, or systems that extract, transform and load '
            'data. [[slnc 400]] Look for pools of workers with a limited '
            "queue in front, such as Java's Thread Pool Executor. [[slnc "
            '300]] Look for a Blocking Queue between threads that produce '
            'work and threads that consume it. [[slnc 300]] And look for '
            'reactive streams, where each stage asks for only as many '
            'items as it can handle.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use stages when the work has parts', 'of different speed and you want', 'throughput. Find the slowest', 'stage, and widen only that one.', 'Put a limit on each waiting line', 'so that trouble pushes back to the', 'door. Keep the lines somewhere', 'that survives a crash if the', 'orders matter.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use stages when parts '
            'of the work run at different speeds, and you want more '
            'orders finished per minute. [[slnc 500]] Then follow three '
            'rules. [[slnc 300]] One. [[slnc 200]] Find the slowest '
            'stage, and widen only that one. [[slnc 300]] Two. [[slnc '
            '200]] Put a limit on every waiting line, so trouble pushes '
            'back to the door. [[slnc 300]] Three. [[slnc 200]] If the '
            'orders matter, keep the lines somewhere that survives a '
            'crash.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'time is counted in ticks, not by the clock, so every run '
            'gives the same result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If the work is short, or the', 'stages are about equally fast, a', 'single step is simpler, and the', 'queues only add delay. Stages pay', 'off when parts differ in speed, or', 'need separate scaling.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If the work is '
            'short, or the stages all take about the same time, a single '
            'step is simpler. [[slnc 300]] The waiting lines would only '
            'add delay. [[slnc 400]] Stages pay off when the parts run at '
            'different speeds, or need to grow separately.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Pipe and Filter Architecture. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Pipe '
            'and Filter lets stages run together and be sized on their '
            'own, and the price is the lines between them, and the orders '
            'lost if a stage crashes. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Make parsing take two ticks instead of one. '
            '[[slnc 300]] Then work out which stage is now the slowest. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
