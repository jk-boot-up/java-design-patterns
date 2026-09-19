"""Scene definitions for the Callback teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Callback',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Callback pattern '
            'in Java, and it is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] The plain definition: a callback is a '
            'piece of code you hand to someone else, to be called when '
            'something you asked for has happened. [[slnc 350]] This is '
            'another project in the foundational category, whose subject '
            'is how an object gets hold of another, and how small idioms '
            'shape everyday Java. In our online store, a card payment '
            'takes a while to be answered, and the shop must not stand '
            'still until it is. [[slnc 300]] By the end you will see a '
            'caller asking again and again for an answer, see it hand '
            'over what to do and go on, see one callback told what '
            'happened, see a failing callback not stop the gateway, see '
            'answers arrive in another order and each callback still '
            'right, and see the bill, which is callbacks nested inside '
            'callbacks.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The payment gateway takes a', 'while to answer.', '', 'Meanwhile the shop has other', 'work,', '', 'and other orders to charge.', '', 'How do we hear the answer?'],
        narration=(
            'Here is the scenario. The payment gateway takes a while to '
            'answer a card charge. Meanwhile, the shop has other work to '
            'do, and other orders to charge. [[slnc 300]] The question: '
            'how do we hear the answer?'
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
            'First, ask, and keep asking. The answer arrived on the fifth '
            'look. Five looks were made, and four of them found nothing. '
            'And the caller could do nothing else in that time.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Hand over the code to run.', '', 'Go on with other work.', '', 'When the answer is ready, the', 'other side calls your code,', 'with the result.'],
        narration=(
            'The pattern. Hand over the code to run. Go on with other '
            'work. When the answer is ready, the other side calls your '
            'code, with the result.'
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
            'Second, say what to do, and go on. The charge is requested, '
            'and the caller goes on. The caller does other work. Then the '
            'callback runs: order one, paid.'
        ),
    ),
    dict(
        key='06-result', kind='console', title='What Happened Decides What To Do',
        body="""THREE. The result decides.
  one callback, told the result:
  ORD-1: ship it.
  ORD-2: ask for another card.""",
        narration=(
            'Third, what happened decides what to do. One callback, told '
            'the result. Order one was paid: ship it. Order two was '
            'declined: ask for another card.'
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
            'Fourth, when the callback itself fails. The first callback '
            'threw an error. The gateway went on, and order two was paid. '
            'The error was recorded: order one, the mail server was down. '
            'The one who asked never sees that exception, because it '
            "happened in someone else's call."
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
            'Fifth, answers in another order. Remembering the order in a '
            'field: both callbacks say order two. Each callback holding '
            'its own order id: order two paid, order one paid. The '
            'answers came in the other order, and each is right.'
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
            'Last, the bill. Pay, then reserve, then ship: three '
            'callbacks, each inside the one before, three levels deep. '
            'The lines run in one order, but are written in another. '
            'Every level needs its own handling for a failure. And each '
            'answer arrives with no stack that shows who asked.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A parameter named onSuccess,', 'onComplete or handler.', '', 'CompletableFuture.thenAccept(...),', 'and whenComplete(...).', '', 'Event handlers in a browser or in', 'Swing, and Node.js style'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'parameter named onSuccess, onComplete or handler. '
            'CompletableFuture.thenAccept(...), and whenComplete(...). '
            'Event handlers in a browser or in Swing, and Node.js style '
            'callbacks. Consumer<Result> passed to an async method.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a callback when you ask for', 'something that takes a while, and', 'want to go on. Pass the result to', 'it. Let each callback carry what', 'it needs, not read shared fields.', 'Decide who handles a failure in', 'the callback. When steps chain,', 'move to futures or an async style,', 'so the code reads in order.'],
        narration=(
            'Here is my verdict, plainly. Use a callback when you ask for '
            'something that takes a while, and want to go on. Pass the '
            'result to it. Let each callback carry what it needs, not '
            'read shared fields. Decide who handles a failure in the '
            'callback. When steps chain, move to futures or an async '
            'style, so the code reads in order.'
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
        body=['For work that is quick, a plain', 'return value is simpler. For', 'chains of steps, futures or', 'coroutines read better than nested', 'callbacks.'],
        narration=(
            'So when is it too much? For work that is quick, a plain '
            'return value is simpler. For chains of steps, futures or '
            'coroutines read better than nested callbacks.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Callback. [[slnc 250]] If you take one sentence away, "
            'take this one: a callback lets you go on while something '
            'takes time, and the price is code that runs out of written '
            'order, and failures that no caller sees. [[slnc 350]] The '
            'full source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, add a second callback that runs '
            'only when the payment fails, and check that the success one '
            'is not called. [[slnc 300]] If this helped, a like genuinely '
            'does help other people find it, and subscribe if you would '
            'like the rest of the series. [[slnc 250]] Thanks for '
            'watching.'
        ),
    ),
]
