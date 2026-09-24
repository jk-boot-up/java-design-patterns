"""Scene definitions for the Queue-Based Load Leveling with SQS teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of the service's words in plain
language before using Amazon's name for it, and never points at a picture the
listener cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Queue-Based Load Leveling with SQS',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Queue-Based Load '
            'Leveling pattern in Java, using a real Amazon queue, running '
            'on your own machine. [[slnc 250]] It is written and presented '
            'by Jayasekhar Konduru. [[slnc 300]] Here is the plain '
            'definition, in general words. When work arrives in bursts, '
            'faster than a service can handle it, you put a queue in '
            'between. The burst waits in line, and the service keeps its '
            'own steady pace. It works like a post office the day before a '
            'holiday. A crowd arrives at once, a machine at the door hands '
            'out numbered tickets, and the clerk serves one person after '
            'another, never rushed. [[slnc 350]] Now the same thing in our '
            'online store. A sale sends a hundred orders in the same '
            'moment. Checkout puts every order on a queue and tells the '
            'customer at once that the order is received. The packing '
            'service takes orders off the queue at its own pace, ten at a '
            'time. [[slnc 300]] By the end you will have seen the depth a '
            'real burst builds, an order that is taken but not removed, a '
            'slow packer that packs one order twice, a packer that stops '
            'and loses nothing, and the bill for all of it.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A sale: 100 orders arrive at once.', 'The packing service does 10 a round.', '',
              'Checkout puts every order on a queue,', 'and answers the customer at once.', '',
              'The hand-built partner project kept', 'its queue in memory, with its own clock.', '',
              'This time the queue is Amazon SQS,', 'and the rules are Amazon\'s.'],
        narration=(
            'Here is the scenario. The shop runs a sale, and in its first '
            'second a hundred orders arrive at once. The packing service '
            'picks the items and packs the parcels, and it can do ten '
            'orders a round, however many are waiting. [[slnc 300]] So '
            'checkout does not call the packing service directly. It puts '
            'each order on a queue, a waiting line for work, and tells the '
            'customer straight away that the order is received. '
            '[[slnc 250]] The hand-built partner project in this course '
            'kept its queue in memory, with a clock it made up for itself. '
            'This time the queue is Amazon\'s queue service, and the rules '
            'it plays by are Amazon\'s rules.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='A Burst Lands On The Queue',
        body="""ONE. A burst lands on the queue.
  100 orders arrive at once.

  11 orders in one request:
  Maximum number of entries per
  request are 10. You have sent 11.

  so the burst goes as 10 requests
  of 10. SQS reports 100 waiting
  and 0 in flight.
  kept for 345600 seconds, 4 days.""",
        narration=(
            'First, the burst. The queue service is called S Q S, short '
            'for Simple Queue Service. A hundred orders arrive at once, '
            'and checkout sends them to S Q S. [[slnc 250]] It tries '
            'eleven orders in one request, and S Q S refuses, in its own '
            'words: the maximum number of entries per request is ten. '
            'That is not a rule this program made up. It is the service '
            'saying no. [[slnc 250]] So the burst goes as ten requests of '
            'ten. S Q S now reports a hundred orders waiting, and none in '
            'flight. Nobody was refused. And S Q S will keep an order that '
            'nobody takes for three hundred and forty five thousand, six '
            'hundred seconds. That is four days.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="The Service's Words",
        body=['Waiting: on the queue, not taken yet.', 'The number waiting is the depth.', '',
              'In flight: taken by a packer, but', 'not finished. Hidden, not removed.', '',
              'Visibility timeout: how long SQS', 'hides a taken order before it', 'hands it out again.', '',
              'LocalStack plays SQS, on this', 'machine, in one container.'],
        narration=(
            'The real service brings a few words with it, and each one is '
            'simpler than it sounds. [[slnc 250]] An order that nobody has '
            'taken yet is waiting. The number of waiting orders is the '
            'depth of the queue. [[slnc 250]] When a packer takes an order, '
            'S Q S does not remove it. It hides it from everyone else, '
            'until the packer says it is finished by deleting it. An order '
            'that is taken but not yet deleted is what S Q S calls in '
            'flight. [[slnc 250]] And how long S Q S hides a taken order, '
            'before it gives up waiting and hands it out again, is what '
            'S Q S calls the visibility timeout. [[slnc 250]] None of this '
            'is on Amazon here. A program called LocalStack answers exactly '
            'as S Q S would, in one small sealed box on this machine, '
            'called a container. The demo switches it on at the start and '
            'off at the end.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='The Packer Keeps Its Own Pace',
        body="""TWO. The packer keeps its own pace.
  asks for 11 at once: Value 11 for
  parameter MaxNumberOfMessages is
  invalid. Must be between 1 and 10.

  it takes 10. SQS now reports
  90 waiting and 10 in flight.

  waiting after each round: 90, 80,
  70, 60, 50, 40, 30, 20, 10, 0.
  100 packed in 10 rounds.""",
        narration=(
            'Second, the packer. It asks S Q S for eleven orders at once, '
            'and S Q S refuses again: it hands out between one and ten. '
            '[[slnc 250]] So it takes ten. And for a moment S Q S reports '
            'ninety waiting, and ten in flight. Those ten are neither on '
            'the line nor gone. They are taken, and hidden, and not yet '
            'finished. [[slnc 250]] The packer packs the ten parcels, and '
            'only then deletes them. Round after round, the depth falls by '
            'ten: ninety, eighty, seventy, and so on, down to zero. A '
            'hundred orders packed in ten rounds, and the packer never did '
            'more than ten at once. That is the pattern working.'
        ),
    ),
    dict(
        key='06-diagram', kind='diagram', title='Where The Orders Live',
        body=None,
        narration=(
            'Here is the whole picture in words. There are four parts, in '
            'order. Checkout comes first: it sends the burst to the queue, '
            'ten orders to a request. The S Q S queue is second: it counts '
            'the orders waiting and the orders in flight, and it lives in '
            'neither checkout nor the packers. The packer is third: it '
            'takes up to ten, packs them, and then deletes them. A second '
            'packer is last: it is handed any order whose timeout ran out. '
            '[[slnc 300]] The one rule that holds it together is the '
            'order of the last two steps. Pack first, and delete only '
            'after the parcel is packed.'
        ),
    ),
    dict(
        key='07-three', kind='console', title='Taken Is Not Removed',
        body="""THREE. Taken is not removed.
  the default timeout is 30 seconds.
  this queue's timeout is 2 seconds.

  a packer takes ORD-2001 and stops.
  SQS reports 0 waiting, 1 in flight.
  a second packer is given 0 orders.

  ORD-2001 comes back once the 2
  seconds have passed: true.
  SQS has handed it out 2 times.""",
        narration=(
            'Third, the heart of it. S Q S hides a taken order for thirty '
            'seconds, unless you choose a different time. This queue hides '
            'it for two seconds. [[slnc 250]] A packer takes order two '
            'thousand and one, and stops before it finishes. It never '
            'deletes it. S Q S reports no orders waiting, and one in '
            'flight. A second packer asks at once, and is given nothing. '
            '[[slnc 300]] The second packer keeps asking. Once the two '
            'seconds have passed, order two thousand and one comes back, '
            'and S Q S says it has now handed it out two times. '
            '[[slnc 250]] S Q S never knew the first packer had stopped. '
            'It only knew the time had run out.'
        ),
    ),
    dict(
        key='08-why', kind='bullets', title='Why Hide, And Not Remove?',
        body=['If SQS removed an order when it was', 'taken, a packer that crashed would', 'lose it for good.', '',
              'So SQS hides it, and waits for', 'the delete that says: finished.', '',
              'No delete in time: it goes back.', '',
              'The price: an order can be', 'handed out more than once.'],
        narration=(
            'Why does S Q S hide an order, instead of removing it? Think '
            'of a coat check. An attendant lifts a coat to fetch it, and '
            'drapes a cloth over its hook. If the attendant comes back and '
            'says done, the coat is gone for good. If the attendant never '
            'comes back, the cloth comes off by itself, and the next '
            'attendant can take the coat. [[slnc 300]] If S Q S removed '
            'an order the moment it was taken, a packer that crashed '
            'would lose that order for ever. So S Q S waits for the '
            'delete that says finished, and if it does not come in time, '
            'the order goes back on the line. [[slnc 250]] The price is '
            'simple to say. An order can be handed out more than once.'
        ),
    ),
    dict(
        key='09-four', kind='console', title='A Slow Packer',
        body="""FOUR. A slow packer.
  packer A takes ORD-3001 and needs
  longer than 2 seconds.

  the time runs out, and packer B
  is given ORD-3001 too.

  both pack it and both delete it.
  ORD-3001 was packed 2 times:
  two parcels for one order.""",
        narration=(
            'Fourth, that price, paid. Packer A takes order three '
            'thousand and one. It has not stopped. It is just slow, and '
            'it needs longer than two seconds. [[slnc 250]] The two '
            'seconds run out. S Q S does not know packer A is still '
            'working, so it hands order three thousand and one to packer '
            'B as well. [[slnc 250]] Both packers pack it, and both '
            'delete it. Order three thousand and one was packed two '
            'times. The customer gets two parcels for one order, and the '
            'shop pays for both.'
        ),
    ),
    dict(
        key='10-still', kind='console', title='Still Working',
        body="""  packer A takes ORD-3002 and, before
  its time runs out, tells SQS it is
  still working: hide it 10 seconds
  more.

  packer B asks SQS to hold its
  question open for 3 seconds.
  it is given 0 orders.

  ORD-3002 was packed 1 time.""",
        narration=(
            'There is a cure. Packer A takes order three thousand and '
            'two, and before its two seconds run out, it tells S Q S: I '
            'am still working, hide it for ten seconds more. S Q S calls '
            'this changing the message\'s visibility. [[slnc 300]] Packer '
            'B asks for orders, and this time it asks S Q S to hold the '
            'question open for three seconds, well past the old timeout, '
            'rather than answer straight away. S Q S calls that long '
            'polling. Packer B is given nothing. [[slnc 250]] Packer A '
            'finishes, and deletes. Order three thousand and two was '
            'packed one time.'
        ),
    ),
    dict(
        key='11-five', kind='console', title='The Packer Stops Half Way',
        body="""FIVE. The packer stops half way.
  100 orders, a 2-second timeout.
  the packer takes 10, finishes 3,
  and its process stops.

  SQS reports 90 waiting and
  7 in flight. nothing is lost.
  they come back: 97 waiting.

  packed: 100, lost: 0.
  handed out a second time: 7.""",
        narration=(
            'Fifth, the moment the hand-built project could not survive. '
            'Its last act stopped the program holding its queue, and '
            'seventy orders were lost. [[slnc 250]] Here, a hundred orders '
            'wait on a queue with a two second timeout. The packer takes '
            'ten, finishes three, and its process stops. [[slnc 250]] S Q '
            'S reports ninety waiting, and seven in flight. Nothing is '
            'lost. The seven are only hidden. When the timeout runs out '
            'they come back, and ninety seven are waiting. A new packer '
            'drains the queue. [[slnc 250]] Packed, a hundred. Lost, none. '
            'Seven orders were handed out a second time, and that was '
            'safe, because the packer that stopped had not packed them. '
            'The queue outlived the program that was reading it.'
        ),
    ),
    dict(
        key='12-six', kind='console', title='The Bill',
        body="""SIX. The bill.
  a queue that holds at most 50?
  Unknown Attribute MaximumDepth.

  15 in and 10 out a round, for 20
  rounds. SQS refused none.
  waiting: 100, and growing.

  100 orders, 10 to a request:
  30 requests. one at a time: 300.
  1 container for 1 queue service.""",
        narration=(
            'Last, the bill. The hand-built project could give its queue '
            'a limit of fifty orders. The demo asks S Q S for the same, '
            'and S Q S does not know the setting. There is no limit to '
            'set. [[slnc 250]] Then orders arrive at fifteen a round, and '
            'the packer does ten, for twenty rounds. S Q S refused none. '
            'A hundred are waiting, and the number keeps growing. Nothing '
            'warns you. The depth is a number you have to ask S Q S for, '
            'and act on. [[slnc 250]] The demo also counts every request '
            'S Q S receives. A hundred orders, sent, taken and deleted '
            'ten to a request, cost thirty requests. One at a time, they '
            'cost three hundred. Here that was one container, for one '
            'queue service.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['It got the shape right: a burst', 'waits, the worker keeps its pace,', 'the price is waiting.', '',
              'It left out:', '',
              'Taken is not removed: in flight.', 'A slow worker, packing twice.',
              'A queue that outlives the worker.', 'No limit to set, 10 per request.'],
        narration=(
            'The hand-built partner project got the shape right. A burst '
            'waits on a queue, the worker keeps its own pace, and the '
            'price is waiting. A queue fed faster than it is drained grows '
            'for ever. All of that holds on real S Q S, with the same '
            'numbers. [[slnc 300]] It left out four things. In the '
            'simulation an order was waiting or done, and nothing in '
            'between. The real queue has a third state, in flight, with a '
            'clock on it. That clock means a slow worker can pack an order '
            'twice. It also means a worker that dies loses nothing, '
            'because the queue lives outside it. And the real queue has '
            'no limit to set, and takes and gives ten at a time.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Use a queue when bursts come and the', 'caller does not need the answer now.', '',
              'Then say four things out loud:', '',
              '1. A timeout longer than the slowest', '   work, and say still working.',
              '2. Delete only after the work.', '3. Doing an order twice does no harm.',
              '4. Watch the depth yourself.'],
        narration=(
            'Here is my verdict, plainly. Use a queue to level load when '
            'bursts come, and the caller does not need the answer straight '
            'away. Then say four things out loud, because the service will '
            'not assume them. [[slnc 250]] One. Set the visibility timeout '
            'longer than your slowest piece of work, and when work runs '
            'long, tell the queue you are still working. [[slnc 200]] Two. '
            'Delete an order only after the work is done. [[slnc 200]] '
            'Three. Make handling an order twice do no harm, because one '
            'day it will happen. [[slnc 200]] Four. Watch the depth '
            'yourself, because the queue will never refuse the backlog.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['LocalStack 4.14.0, held back: later', 'images need an account.',
              'AWS SDK for Java 2.55.4,', 'Testcontainers 2.0.5.', '',
              'Too much if load is steady and', 'the service copes, or if the caller',
              'needs the answer now.', '',
              'One more service to run.'],
        narration=(
            'What is real here? The queue is played by LocalStack, '
            'version four point fourteen, in a container the demo starts '
            'and stops itself. That version is held back on purpose: the '
            'newer ones refuse to start without a LocalStack account. The '
            'code is plain Amazon code, using the newest Amazon library '
            'for Java, and would run unchanged against Amazon itself. The '
            'one thing you need is a container runtime, such as Docker '
            'Desktop, switched on before you start. Every number in this '
            'video is the program\'s own output, and two runs print the '
            'same thing. [[slnc 300]] So when is this too much? If load '
            'is steady and the service copes, a queue is one more thing '
            'to run and pay for. And if the caller needs the answer now, '
            'such as a price or a stock check, a queue is the wrong shape.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Queue-Based Load Leveling with S Q S. [[slnc 250]] If "
            'you take one sentence away, take this one: a taken order is '
            'only hidden, so delete it after the work, and make doing it '
            'twice harmless. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository. [[slnc 300]] If you try one exercise, give '
            'the slow packer\'s queue a ten second timeout instead of two, '
            'predict what packer B is given, and run it to see if you '
            'were right. [[slnc 300]] If this helped, a like genuinely '
            'does help other people find it, and subscribe if you would '
            'like the rest of the series. [[slnc 250]] Thanks for '
            'watching.'
        ),
    ),
]
