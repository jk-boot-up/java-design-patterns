"""Scene definitions for the Callback teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Callback',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Callback pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A callback is a piece of '
            'code you hand to someone else. [[slnc 300]] They call it '
            'when the thing you asked for has happened. [[slnc 600]] '
            'Think of leaving your phone number with a shop. [[slnc 300]] '
            'You do not stand at the counter waiting. [[slnc 300]] They '
            'call you when your order is ready. [[slnc 700]] In our '
            'online store, a card payment takes a while to be answered. '
            '[[slnc 300]] And the shop must not stand still until it is. '
            '[[slnc 500]] In this video, a caller keeps asking for an '
            'answer, again and again. [[slnc 300]] Then it hands over '
            'what to do, and carries on. [[slnc 300]] We will hear a '
            'failing callback, answers arriving out of order, and the '
            'cost of nesting callbacks.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The payment gateway takes a', 'while to answer.', '', 'Meanwhile the shop has other', 'work,', '', 'and other orders to charge.', '', 'How do we hear the answer?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The payment gateway takes '
            'a while to answer a card charge. [[slnc 400]] Meanwhile, the '
            'shop has other work to do. [[slnc 300]] And other orders to '
            'charge. [[slnc 500]] So here is the question. [[slnc 300]] '
            'How do we hear the answer?'
        ),
    ),
    dict(
        key='03-poll', kind='console', title='Ask, And Keep Asking',
        body="""ONE. Ask, and keep asking.
  the answer came on the 5th look.
  4 looks found nothing.

  the caller could do nothing
  else in that time.""",
        narration=(
            'First, the naive way: ask, and keep asking. [[slnc 400]] Is '
            'it done yet? [[slnc 200]] Is it done yet? [[slnc 500]] The '
            'answer arrived on the fifth look. [[slnc 300]] Four looks '
            'found nothing. [[slnc 300]] And the caller could do nothing '
            'else in all that time.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Hand over the code to run.', '', 'Go on with other work.', '', 'When the answer is ready, the', 'other side calls your code,', 'with the result.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Hand over the code you want '
            'run. [[slnc 300]] Carry on with other work. [[slnc 300]] '
            'When the answer is ready, the other side calls your code, '
            'and passes it the result.'
        ),
    ),
    dict(
        key='05-say', kind='console', title='Say What To Do, And Go On',
        body="""TWO. Say what to do.
  charge requested; the caller
  goes on.
  the caller does other work.
  then the callback runs:
  ORD-1 paid.""",
        narration=(
            'Second demo: say what to do, and carry on. [[slnc 400]] The '
            'charge is requested, together with a callback. [[slnc 300]] '
            'And the caller carries on straight away. [[slnc 400]] The '
            'caller does some other work. [[slnc 300]] Then the payment '
            'is answered, and the callback runs: order one, paid.'
        ),
    ),
    dict(
        key='06-result', kind='console', title='What Happened Decides What To Do',
        body="""THREE. The result decides.
  one callback, told the result:
  ORD-1: ship it.
  ORD-2: ask for another card.""",
        narration=(
            'Third demo: the result decides what happens. [[slnc 400]] '
            'One callback is given the result each time. [[slnc 500]] '
            'Order one was paid, so the callback says: ship it. [[slnc '
            '300]] Order two was declined, so the callback says: ask for '
            'another card.'
        ),
    ),
    dict(
        key='07-fail', kind='console', title='When The Callback Fails',
        body="""FOUR. The callback fails.
  the first callback threw.
  the gateway went on:
  ORD-2 paid.
  recorded: ORD-1, the mail server
  was down.

  the one who asked never sees it.""",
        narration=(
            'Fourth demo: when the callback itself fails. [[slnc 400]] '
            'The first callback throws an error. [[slnc 300]] But the '
            'gateway carries on, and order two is paid. [[slnc 500]] The '
            'error is recorded: order one, the mail server was down. '
            '[[slnc 500]] The code that asked for the payment never sees '
            'that error. [[slnc 300]] Because it happened inside someone '
            "else's call."
        ),
    ),
    dict(
        key='08-order', kind='console', title='Answers In Another Order',
        body="""FIVE. Another order.
  the order in a field:
  both say ORD-2.

  each callback holding its own
  order id: ORD-2 paid,
  ORD-1 paid.
  each is right.""",
        narration=(
            'Fifth demo: answers arriving in a different order. [[slnc '
            '400]] First, a version that remembers the current order in a '
            'shared field. [[slnc 300]] The answers arrive in reverse '
            'order. [[slnc 300]] And both callbacks say order two. [[slnc '
            '300]] One of them is wrong. [[slnc 500]] Now a version where '
            'each callback carries its own order I D. [[slnc 300]] Order '
            'two, paid. [[slnc 300]] Order one, paid. [[slnc 500]] The '
            'answers came in a different order, and each one is right.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  pay, reserve, ship: 3 callbacks,
  each inside the one before.

  the lines run in one order and
  are written in another.

  each level needs its own failure
  handling, and no stack shows
  who asked.""",
        narration=(
            'Finally, the cost. [[slnc 400]] Pay, then reserve the stock, '
            'then ship. [[slnc 300]] Three callbacks, each one inside the '
            'one before, three levels deep. [[slnc 500]] The steps run in '
            'one order, but are written in another. [[slnc 300]] Every '
            'level needs its own failure handling. [[slnc 300]] And each '
            'answer arrives with no trace of who originally asked.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A parameter named onSuccess,', 'onComplete or handler.', '', 'CompletableFuture.thenAccept(...),', 'and whenComplete(...).', '', 'Event handlers in a browser or in', 'Swing, and Node.js style'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for parameters named on success, on '
            'complete, or handler. [[slnc 300]] Look for Completable '
            'Future methods like then accept, and when complete. [[slnc '
            '300]] Look for event handlers, in a browser or in a desktop '
            'app. [[slnc 300]] And look for a function passed into a '
            'method that works in the background.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a callback when you ask for', 'something that takes a while, and', 'want to go on. Pass the result to', 'it. Let each callback carry what', 'it needs, not read shared fields.', 'Decide who handles a failure in', 'the callback. When steps chain,', 'move to futures or an async style,', 'so the code reads in order.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a callback when '
            'you ask for something that takes a while, and you want to '
            'carry on. [[slnc 500]] Pass the result into the callback. '
            '[[slnc 300]] Let each callback carry what it needs, instead '
            'of reading shared fields. [[slnc 300]] Decide who handles a '
            'failure inside the callback. [[slnc 500]] And when steps '
            'start chaining together, move to futures, so the code reads '
            'in the order it runs.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every result you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For work that is quick, a plain', 'return value is simpler. For', 'chains of steps, futures or', 'coroutines read better than nested', 'callbacks.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For work that is '
            'quick, simply returning a value is easier. [[slnc 400]] And '
            'for chains of steps, futures read much better than nested '
            'callbacks.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Callback pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A callback lets '
            'you carry on while something takes time, and the price is '
            'code that runs out of written order, and failures no caller '
            'sees. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Add a second callback, which only runs when the '
            'payment fails. [[slnc 300]] And check that the success '
            'callback is not called. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
