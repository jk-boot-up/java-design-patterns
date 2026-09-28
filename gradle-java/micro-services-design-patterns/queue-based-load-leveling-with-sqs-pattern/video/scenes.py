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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Queue-Based Load Leveling pattern in Java, using a real '
            'Amazon queue, running on your own machine. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] When work arrives '
            'in bursts, faster than a service can handle it, you put a '
            'queue in between. [[slnc 300]] The burst waits in line. '
            '[[slnc 300]] And the service keeps its own steady pace. '
            '[[slnc 600]] It works like a post office the day before a '
            'holiday. [[slnc 300]] A crowd arrives at once, and a machine '
            'at the door hands out numbered tickets. [[slnc 300]] The '
            'clerk serves one person after another, never rushed. [[slnc '
            '700]] In our online store, a sale sends a hundred orders in '
            'the same moment. [[slnc 300]] Checkout puts every order on a '
            'queue, and tells the customer at once that it is received. '
            '[[slnc 300]] The packing service takes orders off the queue '
            'at its own pace, ten at a time. [[slnc 500]] By the end, you '
            'will hear a real burst fill the queue. [[slnc 300]] An order '
            'that is taken, but not removed. [[slnc 300]] A slow packer '
            'that packs one order twice. [[slnc 300]] A packer that '
            'stops, and loses nothing. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A sale: 100 orders arrive at once.', 'The packing service does 10 a round.', '',
              'Checkout puts every order on a queue,', 'and answers the customer at once.', '',
              'The hand-built partner project kept', 'its queue in memory, with its own clock.', '',
              'This time the queue is Amazon SQS,', 'and the rules are Amazon\'s.'],
        narration=(
            'Here is the scenario. [[slnc 400]] The shop runs a sale, and '
            'in its first second, a hundred orders arrive at once. [[slnc '
            '300]] The packing service can handle ten orders per round, '
            'however many are waiting. [[slnc 600]] So checkout does not '
            'call the packing service directly. [[slnc 300]] It puts each '
            'order on a queue, a waiting line for work. [[slnc 300]] And '
            'it tells the customer straight away that the order is '
            'received. [[slnc 600]] The plain Java version kept its queue '
            'in memory, with a made-up clock. [[slnc 300]] This time, the '
            "queue is Amazon's queue service. [[slnc 300]] And the rules "
            "it plays by are Amazon's rules."
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
            'First demo: a burst lands on the queue. [[slnc 400]] The '
            'queue service is called S Q S, short for Simple Queue '
            'Service. [[slnc 300]] A hundred orders arrive at once, and '
            'checkout sends them to S Q S. [[slnc 600]] It tries to send '
            'eleven orders in one request. [[slnc 300]] And S Q S '
            'refuses. [[slnc 300]] The most it accepts in one request is '
            'ten. [[slnc 300]] That is not a rule this program made up. '
            '[[slnc 300]] It is the real service saying no. [[slnc 600]] '
            'So the burst goes as ten requests, of ten orders each. '
            '[[slnc 300]] S Q S now reports a hundred orders waiting. '
            '[[slnc 300]] Nobody was refused. [[slnc 300]] And S Q S will '
            'keep an order that nobody takes for four days.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="The Service's Words",
        body=['Waiting: on the queue, not taken yet.', 'The number waiting is the depth.', '',
              'In flight: taken by a packer, but', 'not finished. Hidden, not removed.', '',
              'Visibility timeout: how long SQS', 'hides a taken order before it', 'hands it out again.', '',
              'LocalStack plays SQS, on this', 'machine, in one container.'],
        narration=(
            'The real service brings a few words with it. [[slnc 300]] '
            'Each one is simpler than it sounds. [[slnc 500]] An order '
            'that nobody has taken yet is waiting. [[slnc 300]] The '
            'number of waiting orders is the depth of the queue. [[slnc '
            '600]] When a packer takes an order, S Q S does not remove '
            'it. [[slnc 300]] It hides it from everyone else. [[slnc '
            '300]] Until the packer says it has finished, by deleting it. '
            '[[slnc 300]] An order that is taken, but not yet deleted, is '
            'called in flight. [[slnc 600]] And how long S Q S hides a '
            'taken order, before handing it out again, is called the '
            'visibility timeout. [[slnc 600]] None of this is really on '
            'Amazon here. [[slnc 300]] A program called LocalStack '
            'answers exactly as S Q S would. [[slnc 300]] It runs in a '
            'container, a small sealed box on this machine, that the demo '
            'switches on and off.'
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
            'Second demo: the packer keeps its own pace. [[slnc 400]] It '
            'asks S Q S for eleven orders at once. [[slnc 300]] And S Q S '
            'refuses again. [[slnc 300]] It hands out between one and '
            'ten. [[slnc 500]] So the packer takes ten. [[slnc 300]] For '
            'a moment, S Q S reports ninety waiting, and ten in flight. '
            '[[slnc 300]] Those ten are neither in the line, nor gone. '
            '[[slnc 300]] They are taken, hidden, and not yet finished. '
            '[[slnc 600]] The packer packs the ten parcels, and only then '
            'deletes them. [[slnc 300]] Round after round, the depth '
            'falls by ten. [[slnc 300]] Ninety, eighty, seventy, and so '
            'on, down to zero. [[slnc 500]] A hundred orders packed in '
            'ten rounds. [[slnc 300]] And the packer never did more than '
            'ten at once. [[slnc 300]] That is the pattern working.'
        ),
    ),
    dict(
        key='06-diagram', kind='diagram', title='Where The Orders Live',
        body=None,
        narration=(
            'Here is the whole picture, in words. [[slnc 400]] There are '
            'four parts, in order. [[slnc 500]] First, checkout. [[slnc '
            '300]] It sends the burst to the queue, ten orders per '
            'request. [[slnc 400]] Second, the S Q S queue. [[slnc 300]] '
            'It counts the orders waiting, and the orders in flight. '
            '[[slnc 300]] It lives outside both checkout and the packers. '
            '[[slnc 400]] Third, the packer. [[slnc 300]] It takes up to '
            'ten orders, packs them, and then deletes them. [[slnc 400]] '
            'Fourth, a second packer. [[slnc 300]] It is handed any order '
            'whose timeout ran out. [[slnc 600]] The rule that holds it '
            'together is the order of the last two steps. [[slnc 300]] '
            'Pack first. [[slnc 300]] Delete only after the parcel is '
            'packed.'
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
            'Third demo, and this is the heart of it. [[slnc 400]] By '
            'default, S Q S hides a taken order for thirty seconds. '
            '[[slnc 300]] This queue hides it for only two seconds. '
            '[[slnc 600]] A packer takes order two thousand and one. '
            '[[slnc 300]] Then it stops, before it finishes. [[slnc 300]] '
            'It never deletes the order. [[slnc 500]] S Q S reports no '
            'orders waiting, and one in flight. [[slnc 300]] A second '
            'packer asks straight away, and is given nothing. [[slnc '
            '600]] The second packer keeps asking. [[slnc 300]] Once the '
            'two seconds have passed, order two thousand and one comes '
            'back. [[slnc 300]] And S Q S says it has now handed it out '
            'twice. [[slnc 600]] S Q S never knew the first packer had '
            'stopped. [[slnc 300]] It only knew the time had run out.'
        ),
    ),
    dict(
        key='08-why', kind='bullets', title='Why Hide, And Not Remove?',
        body=['If SQS removed an order when it was', 'taken, a packer that crashed would', 'lose it for good.', '',
              'So SQS hides it, and waits for', 'the delete that says: finished.', '',
              'No delete in time: it goes back.', '',
              'The price: an order can be', 'handed out more than once.'],
        narration=(
            'Why does S Q S hide an order, instead of removing it? [[slnc '
            '400]] Think of a coat check. [[slnc 300]] An attendant lifts '
            'a coat off its hook, and drapes a cloth over the hook. '
            '[[slnc 300]] If the attendant comes back and says done, the '
            'coat is gone for good. [[slnc 300]] If the attendant never '
            'comes back, the cloth comes off, and the next attendant can '
            'take the coat. [[slnc 600]] If S Q S removed an order the '
            'moment it was taken, a packer that crashed would lose it '
            'forever. [[slnc 300]] So S Q S waits for the delete that '
            'says finished. [[slnc 300]] If it does not come in time, the '
            'order goes back in line. [[slnc 600]] The price is simple. '
            '[[slnc 300]] An order can be handed out more than once.'
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
            'Fourth demo: that price, paid. [[slnc 400]] Packer A takes '
            'order three thousand and one. [[slnc 300]] It has not '
            'stopped. [[slnc 300]] It is just slow, and needs more than '
            'two seconds. [[slnc 600]] The two seconds run out. [[slnc '
            '300]] S Q S does not know packer A is still working. [[slnc '
            '300]] So it hands order three thousand and one to packer B '
            'as well. [[slnc 600]] Both packers pack it, and both delete '
            'it. [[slnc 300]] The order was packed twice. [[slnc 300]] '
            'The customer gets two parcels for one order. [[slnc 300]] '
            'And the shop pays for both.'
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
            'There is a cure. [[slnc 400]] Packer A takes order three '
            'thousand and two. [[slnc 300]] Before its two seconds run '
            'out, it tells S Q S: I am still working, hide it for ten '
            'seconds more. [[slnc 600]] Packer B asks for orders. [[slnc '
            '300]] This time it asks S Q S to hold its question open for '
            'three seconds, rather than answer at once. [[slnc 300]] That '
            'is called long polling. [[slnc 300]] Packer B is given '
            'nothing. [[slnc 600]] Packer A finishes, and deletes the '
            'order. [[slnc 300]] Order three thousand and two was packed '
            'once.'
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
            'Fifth demo, the moment the plain Java version could not '
            'survive. [[slnc 400]] In its last demo, the program holding '
            'the queue stopped, and seventy orders were lost. [[slnc '
            '600]] Here, a hundred orders wait on a queue with a '
            'two-second timeout. [[slnc 300]] The packer takes ten, '
            'finishes three, and then its program stops. [[slnc 600]] S Q '
            'S reports ninety waiting, and seven in flight. [[slnc 300]] '
            'Nothing is lost. [[slnc 300]] The seven are only hidden. '
            '[[slnc 500]] When the timeout runs out, they come back, and '
            'ninety-seven are waiting. [[slnc 300]] A new packer clears '
            'the queue. [[slnc 600]] A hundred packed. [[slnc 300]] None '
            'lost. [[slnc 300]] Seven orders were handed out a second '
            'time. [[slnc 300]] And that was safe, because the packer '
            'that stopped had not packed them. [[slnc 500]] The queue '
            'outlived the program reading it.'
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
            'Finally, the bill. [[slnc 400]] The plain Java version could '
            'give its queue a limit of fifty orders. [[slnc 300]] The '
            'demo asks S Q S for the same. [[slnc 300]] And S Q S does '
            'not know that setting. [[slnc 300]] There is no limit to '
            'set. [[slnc 600]] Then orders arrive at fifteen per round, '
            'and the packer handles ten, for twenty rounds. [[slnc 300]] '
            'S Q S refuses none. [[slnc 300]] A hundred are waiting, and '
            'the number keeps growing. [[slnc 300]] Nothing warns you. '
            '[[slnc 300]] You have to ask for the depth yourself, and act '
            'on it. [[slnc 600]] The demo also counts every request S Q S '
            'receives. [[slnc 300]] A hundred orders, sent, taken, and '
            'deleted ten at a time, cost thirty requests. [[slnc 300]] '
            'One at a time, they would cost three hundred.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['It got the shape right: a burst', 'waits, the worker keeps its pace,', 'the price is waiting.', '',
              'It left out:', '',
              'Taken is not removed: in flight.', 'A slow worker, packing twice.',
              'A queue that outlives the worker.', 'No limit to set, 10 per request.'],
        narration=(
            'The plain Java version got the shape right. [[slnc 400]] A '
            'burst waits on a queue. [[slnc 300]] The worker keeps its '
            'own pace. [[slnc 300]] And the price is waiting. [[slnc '
            '300]] All of that holds on real S Q S, with the same '
            'numbers. [[slnc 600]] But it left out four things. [[slnc '
            '500]] First, in the plain version an order was either '
            'waiting, or done. [[slnc 300]] The real queue has a third '
            'state, in flight, with a clock on it. [[slnc 400]] Second, '
            'that clock means a slow worker can pack an order twice. '
            '[[slnc 400]] Third, a worker that dies loses nothing, '
            'because the queue lives outside it. [[slnc 400]] And fourth, '
            'the real queue has no limit to set, and handles ten orders '
            'at a time.'
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
            'So, here is the verdict. [[slnc 400]] Use a queue when '
            'bursts come, and the caller does not need the answer '
            'straight away. [[slnc 500]] Then settle four things, because '
            'the service will not. [[slnc 500]] One. [[slnc 200]] Set the '
            'visibility timeout longer than your slowest work. [[slnc '
            '300]] And when work runs long, tell the queue you are still '
            'working. [[slnc 400]] Two. [[slnc 200]] Delete an order only '
            'after the work is done. [[slnc 400]] Three. [[slnc 200]] '
            'Make handling an order twice harmless, because one day it '
            'will happen. [[slnc 400]] Four. [[slnc 200]] Watch the depth '
            'yourself, because the queue will never refuse a backlog.'
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
            'A quick, honest note about this demo. [[slnc 400]] The queue '
            'is played by LocalStack, version four point fourteen, in a '
            'container the demo starts and stops by itself. [[slnc 300]] '
            'That version is held back on purpose, because newer ones '
            'need a LocalStack account. [[slnc 500]] The code is ordinary '
            'Amazon code, using the newest Amazon library for Java. '
            '[[slnc 300]] It would run unchanged against Amazon itself. '
            '[[slnc 300]] You just need Docker switched on first. [[slnc '
            "300]] Every number you heard comes from the program's own "
            'output. [[slnc 600]] So, when is this too much? [[slnc 300]] '
            'If the load is steady and the service copes, a queue is one '
            'more thing to run and pay for. [[slnc 300]] And if the '
            'caller needs the answer now, like a price or a stock check, '
            'a queue is the wrong shape.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Queue-Based Load Leveling, with S Q S. [[slnc 400]] "
            'If you remember one sentence, make it this one. [[slnc 300]] '
            'A taken order is only hidden, so delete it after the work, '
            'and make doing it twice harmless. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            "one exercise to try. [[slnc 300]] Give the slow packer's "
            'queue a ten-second timeout, instead of two. [[slnc 300]] '
            'Guess what packer B will be given, and then run it to check. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
