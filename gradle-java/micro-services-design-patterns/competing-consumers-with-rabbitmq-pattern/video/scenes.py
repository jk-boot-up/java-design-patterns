"""Scene definitions for the Competing Consumers with RabbitMQ teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of the broker's words in plain
language before using RabbitMQ's name for it, and never points at a picture the
listener cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Competing Consumers with RabbitMQ',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Competing Consumers pattern in Java, using a real message '
            'broker called RabbitMQ. [[slnc 300]] This video is presented '
            'by Jayasekhar Konduru. [[slnc 600]] First, a simple '
            'definition. [[slnc 300]] Competing consumers are several '
            'workers reading from one shared queue of jobs. [[slnc 300]] '
            'Each job goes to exactly one of them. [[slnc 300]] So adding '
            'a worker adds capacity, and nothing else has to change. '
            '[[slnc 700]] In our online store, every order becomes a pick '
            'order for the warehouse. [[slnc 300]] On a busy day, one '
            'picker cannot keep up. [[slnc 300]] So several pickers take '
            'orders from the same queue, and the broker decides who gets '
            'which. [[slnc 500]] By the end, you will hear one picker '
            'handed the whole queue, while another stands idle. [[slnc '
            '300]] A picker crash while holding five orders, and hand '
            'back three. [[slnc 300]] And three orders lost for good.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Orders arrive faster than one', 'picker can pick them.', '',
              'Add pickers. Change nothing else.', 'No order twice. None lost.', '',
              'The plain-Java version kept its', 'queue inside one program.', '',
              'This time the queue is a real', 'broker, and it hands work out.'],
        narration=(
            'Here is the scenario. [[slnc 400]] On a busy day, orders '
            'arrive faster than one warehouse picker can pick them. '
            '[[slnc 300]] And the queue grows. [[slnc 500]] The warehouse '
            'wants to add pickers, without rewriting anything. [[slnc '
            '300]] No order should be picked twice. [[slnc 300]] And none '
            "should be lost when a picker's handheld crashes halfway down "
            'an aisle. [[slnc 600]] The plain Java version kept its queue '
            'as a list inside one program. [[slnc 300]] Each worker '
            'reached in, and took a job when it was free. [[slnc 500]] '
            'This time, the queue lives in a real broker. [[slnc 300]] '
            'And the broker does not wait to be asked. [[slnc 300]] It '
            'hands work out. [[slnc 300]] That changes two things.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='One Picker, Then Three',
        body="""ONE. One picker, then three.
  12 orders, one picker.
  being picked: 1. waiting: 11.

  three pickers on the same queue.
  being picked: 3. waiting: 9.

  300 orders: 300 picked,
  300 different orders.
  every picker did some,
  and none did more than half.""",
        narration=(
            'First demo: one picker, then three. [[slnc 400]] Twelve '
            'orders are waiting, and one picker takes them one at a time. '
            '[[slnc 300]] One is being picked, and eleven wait. [[slnc '
            '500]] Put three pickers on the same queue. [[slnc 300]] Now '
            'three are being picked, and nine wait. [[slnc 300]] The '
            'pickers never talk to each other. [[slnc 300]] They only '
            'talk to the broker. [[slnc 600]] Then three pickers share '
            'three hundred orders. [[slnc 300]] All three hundred are '
            'picked, and they are three hundred different orders. [[slnc '
            '300]] None twice, and none missed. [[slnc 500]] How many '
            "each picker got is the broker's choice. [[slnc 300]] And it "
            'changes from run to run. [[slnc 300]] So the demo only says '
            'what always holds. [[slnc 300]] Every picker did some, and '
            'none did more than half.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="The Broker's Words",
        body=['A queue: a named rail where', 'orders wait, in order.', '',
              'A consumer: one worker taking', 'from it. Here, one picker.', '',
              'An acknowledgement: the picker', 'saying done, so the broker', 'may forget the order.'],
        narration=(
            'A real broker brings a few words with it. [[slnc 400]] Think '
            'of a restaurant kitchen, with one ticket rail and several '
            'cooks. [[slnc 300]] Order tickets go up on the rail. [[slnc '
            '300]] And a cook who is free takes the next one. [[slnc '
            '500]] The rail is what RabbitMQ calls a queue. [[slnc 300]] '
            'A named place where messages wait, in the order they '
            'arrived. [[slnc 500]] Each cook is what RabbitMQ calls a '
            'consumer. [[slnc 300]] In our store, each consumer is a '
            'warehouse picker. [[slnc 500]] When a picker finishes an '
            'order, it tells the broker it is done. [[slnc 300]] So the '
            'broker may forget it. [[slnc 300]] RabbitMQ calls that an '
            'acknowledgement. [[slnc 300]] Until it arrives, the broker '
            'keeps its own copy of the order.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='No Limit: One Takes Everything',
        body="""TWO. No limit: the first takes all.
  12 orders waiting.
  a slow picker starts first.
  no limit set.
  handed to it: 12. waiting: 0.

  a fast picker joins.
  handed to it: 0.

  picked by the slow picker: 12.
  by the fast one: 0.""",
        narration=(
            'Second demo, and this is the surprise at the heart of this '
            'video. [[slnc 400]] Back in the kitchen. [[slnc 300]] How '
            'many tickets may one cook take down at once? [[slnc 500]] '
            'RabbitMQ calls that number the prefetch. [[slnc 300]] It is '
            'how many orders the broker will hand one picker, before '
            'hearing done for any of them. [[slnc 500]] If nobody sets '
            'it, there is no limit. [[slnc 300]] That is the default. '
            '[[slnc 600]] Twelve orders are waiting. [[slnc 300]] A slow '
            'picker starts first, with no limit set. [[slnc 300]] The '
            'broker hands it all twelve at once. [[slnc 300]] And nothing '
            'is left waiting. [[slnc 500]] A fast picker joins a moment '
            'later. [[slnc 300]] And it is handed nothing at all. [[slnc '
            '300]] It stands idle, while the slow picker works through '
            'all twelve, one by one. [[slnc 500]] Competing consumers '
            'that do not compete.'
        ),
    ),
    dict(
        key='06-three', kind='console', title='Prefetch: How Many To Hold',
        body="""THREE. Prefetch: how many to hold.
  20 orders, prefetch 10.
  handed to the slow picker: 10.
  to the fast one: 10.

  the fast one picks its 10,
  and stands idle. waiting: 0.
  still held by the slow one: 10.

  the same 20, prefetch 1.
  the slow picker holds 1.
  the fast one picks the other 19.""",
        narration=(
            'Third demo: the same slow and fast pickers, now with a '
            'limit. [[slnc 400]] Twenty orders, and a prefetch of ten. '
            '[[slnc 300]] The broker hands each picker ten. [[slnc 500]] '
            'The fast one picks its ten, and then stands idle, with the '
            'queue empty. [[slnc 300]] Meanwhile, the slow one is still '
            'holding ten that nobody else can reach. [[slnc 600]] Now, a '
            'prefetch of one. [[slnc 300]] The slow picker holds just '
            'one. [[slnc 300]] And the fast one picks the other nineteen. '
            '[[slnc 600]] So prefetch is a trade, not a fix. [[slnc 300]] '
            'A prefetch of one shares the work fairly. [[slnc 300]] But '
            'every order costs a trip to the broker and back. [[slnc '
            '300]] A high prefetch keeps a fast picker busy. [[slnc 300]] '
            'But it lets a slow picker sit on work.'
        ),
    ),
    dict(
        key='07-diagram', kind='diagram', title='Where An Order Can Be',
        body=None,
        narration=(
            'Here is the whole picture, in words. [[slnc 400]] An order '
            'is always in one of three places. [[slnc 500]] It is waiting '
            'in the queue. [[slnc 300]] Or it has been handed to a '
            'picker, who has not yet said done. [[slnc 300]] Or it is '
            'gone, because a picker said done. [[slnc 500]] The prefetch '
            'decides how many orders each picker can hold in that middle '
            'place. [[slnc 600]] And here is the rule that holds the rest '
            'of this video together. [[slnc 300]] The broker only forgets '
            'an order when a picker says it is done.'
        ),
    ),
    dict(
        key='08-four', kind='console', title='A Picker Dies Mid-Work',
        body="""FOUR. A picker dies mid-work.
  prefetch 5. A is handed 5.
  picks ORD-1 and ORD-2.
  reserves stock for ORD-3, crashes.

  put back. waiting again: 3.

  B is handed ORD-3, ORD-4, ORD-5.
  marked as seen before: 3 of 3.

  deliveries: 8 for 5 orders.
  stock reserved for ORD-3: 2 times.""",
        narration=(
            'Fourth demo: a picker crashes halfway through its work. '
            '[[slnc 400]] Picker A may hold five orders, and is handed '
            'five. [[slnc 500]] It picks order one, and says done. [[slnc '
            '300]] It picks order two, and says done. [[slnc 300]] It '
            'starts order three by reserving the stock. [[slnc 300]] Then '
            'it crashes, before saying done. [[slnc 600]] The broker '
            'notices the connection has gone. [[slnc 300]] It does not '
            'know which orders picker A had started. [[slnc 300]] It only '
            'knows which ones it never heard done for. [[slnc 300]] So it '
            'puts all three back. [[slnc 600]] Picker B is handed orders '
            'three, four, and five. [[slnc 300]] All three are marked as '
            'seen before. [[slnc 300]] But only order three had really '
            'been started. [[slnc 500]] Eight deliveries, for five '
            'orders. [[slnc 300]] And the stock for order three was '
            'reserved twice. [[slnc 500]] The mark means this might be a '
            'repeat. [[slnc 300]] It never means this is one.'
        ),
    ),
    dict(
        key='09-five', kind='console', title='No Saying Done',
        body="""FIVE. No saying done.
  A: count each order done
  on handover.
  handed: 5. waiting: 0.

  the same crash on ORD-3.
  picked: 2.
  waiting again: 0.
  lost: 3.""",
        narration=(
            'Fifth demo: the same crash, with one setting changed. [[slnc '
            '400]] This time, picker A tells the broker not to wait for '
            'done at all. [[slnc 300]] Every order counts as finished the '
            'moment it is handed over. [[slnc 300]] RabbitMQ calls this '
            'automatic acknowledgement. [[slnc 600]] Picker A is handed '
            'five orders. [[slnc 300]] And the broker has already '
            'forgotten all five. [[slnc 500]] Picker A picks two, and '
            'crashes on order three. [[slnc 300]] Nothing goes back. '
            '[[slnc 300]] Nothing is waiting. [[slnc 300]] Three orders '
            'are lost. [[slnc 300]] And nobody will ever be handed them '
            'again.'
        ),
    ),
    dict(
        key='10-settings', kind='code', title='Two Settings, Two Lines',
        body="""// how many one picker may hold
amqp.basicQos(1);

// false: I will say done myself
amqp.basicConsume(queue, false,
    onHandedOver, tag -> {});

// after the work, not before
amqp.basicAck(receipt, false);""",
        narration=(
            'In the code, both settings are small enough to miss. [[slnc '
            '400]] Before a picker starts listening, one call sets its '
            'prefetch: how many orders it may hold. [[slnc 300]] Leave '
            'that call out, and there is no limit. [[slnc 600]] Then, '
            'when it starts listening, a yes or no says whether the '
            'broker should count orders as done when they are handed '
            'over. [[slnc 300]] Say no, and the picker must say done '
            'itself. [[slnc 300]] After the work, never before.'
        ),
    ),
    dict(
        key='11-six', kind='console', title='The Bill',
        body="""SIX. The bill.
  ORD-13 crashes every picker.
  3 pickers, delivered 3 times,
  marked seen before on 2,
  picked 0 times.
  waiting again: 1.

  safe to run twice:
  8 deliveries for 5 orders.

  left unset, one picker took
  12 of 12 while another stood idle.""",
        narration=(
            'Finally, the bill. [[slnc 400]] Order thirteen is a poison '
            'order. [[slnc 300]] Something in it crashes every picker '
            'that takes it. [[slnc 500]] Three pickers take it, one after '
            'another. [[slnc 300]] And each one crashes. [[slnc 300]] It '
            'was delivered three times, and picked none. [[slnc 300]] And '
            'it is waiting again. [[slnc 500]] The broker cannot tell a '
            'poison order from a slow one. [[slnc 300]] On an ordinary '
            'queue, it will hand it out forever, unless somebody sets a '
            'limit. [[slnc 600]] Two more costs. [[slnc 300]] Every '
            'picker must be safe to run twice, because the fourth demo '
            'made eight deliveries for five orders. [[slnc 300]] And '
            'prefetch is a number somebody has to choose. [[slnc 300]] '
            'Left unset, one picker took all twelve orders, while another '
            'stood idle.'
        ),
    ),
    dict(
        key='12-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['It got the shape right: one queue,', 'workers that never talk, each',
              'order once, give back on failure.', '',
              'It left out:', '',
              'A broker that pushes, and by', 'default pushes everything.',
              'Handed over is not started.', 'Saying done is a choice.',
              'A mark that says yes, not how many.'],
        narration=(
            'The plain Java version got the shape right. [[slnc 400]] One '
            'queue. [[slnc 200]] Workers that never talk to each other. '
            '[[slnc 200]] Each order handled once. [[slnc 200]] And a '
            'failed order given back, and taken over. [[slnc 300]] All of '
            'that is true on RabbitMQ. [[slnc 600]] But it left out four '
            'things. [[slnc 500]] First, a real broker pushes work out. '
            '[[slnc 300]] And by default, it pushes everything to whoever '
            'is listening first. [[slnc 400]] Second, handed over is not '
            'the same as started. [[slnc 300]] So a crash hands back more '
            'than the one order that failed. [[slnc 400]] Third, saying '
            'done is a choice. [[slnc 300]] And the other choice loses '
            'orders. [[slnc 400]] Fourth, the plain version counted '
            'attempts. [[slnc 300]] But an ordinary RabbitMQ queue only '
            'marks an order as seen before: yes or no.'
        ),
    ),
    dict(
        key='13-verdict', kind='bullets', title='The Verdict',
        body=['Share one queue when one worker', 'cannot keep up, and order does', 'not matter.', '',
              'Then say three things out loud:', '',
              '1. Set a prefetch. Never no limit.',
              '2. Say done after the work, and', '   be safe to see an order twice.',
              '3. Limit how often one order', '   may be handed out.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Share one queue '
            'between several pickers when one cannot keep up, and the '
            'order of the work does not matter. [[slnc 500]] Then settle '
            'three things, because the broker will not assume any of '
            'them. [[slnc 500]] One. [[slnc 200]] Set a prefetch. [[slnc '
            '300]] One for fairness, higher for speed, but never the '
            'default of no limit. [[slnc 400]] Two. [[slnc 200]] Say done '
            'after the work is finished. [[slnc 300]] And make every '
            'picker safe to see the same order twice. [[slnc 400]] Three. '
            '[[slnc 200]] Limit how often one order may be handed out. '
            '[[slnc 300]] Or a poison order goes round forever.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['RabbitMQ 4.3.6, Alpine build, in a', 'container the demo starts and stops,',
              'on a port picked at random.', '',
              'The Java client 5.36.0, and', 'Testcontainers 2.0.5.', '',
              'Every exact number comes from', "the program's own output. The",
              'split between equal pickers is', 'described, not counted.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'broker is RabbitMQ, version four point three point six, the '
            'newest release. [[slnc 300]] It runs in a container that the '
            'demo starts and stops by itself. [[slnc 300]] Nothing is '
            'installed, and nothing is left running. [[slnc 300]] You '
            'just need Docker switched on first. [[slnc 500]] Every exact '
            "number you heard comes from the program's own output. [[slnc "
            '300]] The one thing that changes between runs is how the '
            'broker splits orders between equal pickers. [[slnc 300]] So '
            'that is described in words, and the tests check it as a '
            'range.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['If one worker keeps up, one', 'worker is simpler and keeps order.', '',
              'If order matters, split the', 'queue by key first.', '',
              'If losing an order on a crash is', 'fine, write that decision down.', '',
              'A broker is a separate system.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If one picker keeps '
            'up, one picker is simpler, and keeps orders in order. [[slnc '
            '400]] If the order of the work matters, competing pickers '
            'are the wrong shape, until the queue is split by key. [[slnc '
            '400]] If losing an order in a crash is acceptable, counting '
            'done on handover is faster. [[slnc 300]] But that should be '
            'a decision somebody wrote down, not a default nobody '
            'noticed. [[slnc 400]] And a broker is one more system to '
            'run, secure, update, and watch.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Competing Consumers, with RabbitMQ. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] '
            'The broker only forgets an order when a picker says done, '
            'and a picker that crashes hands back everything it was '
            'holding, not just what it had started. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Give the slow picker in '
            'the second demo a prefetch of one. [[slnc 300]] Guess how '
            'many orders each picker will get, and then run it. [[slnc '
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
