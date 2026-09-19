"""Scene definitions for the Dead Letter Channel teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Dead Letter Channel',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Dead Letter '
            'Channel pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'dead letter channel is where a message goes when it cannot '
            'be handled after a fixed number of tries, so that it stops '
            'blocking the messages behind it, and can be looked at later. '
            '[[slnc 350]] This is the fourth project in the messaging and '
            'integration category, whose subject is how separate systems '
            'exchange messages safely. In our online store, one order '
            'arrives with a garbled body that no amount of trying will '
            'read. [[slnc 300]] By the end you will see one bad message '
            'block everything behind it, see it moved aside after three '
            'tries with its reason, see a slow day not treated as a dead '
            'letter, see a message replayed after a fix, and see the '
            'bill, which is that nobody is looking.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Orders are handled one at a time.', '', 'Order 2 arrives garbled.', 'The handler can never read it.', '', 'Orders 3 and 4 are fine.', '', 'What should the worker do with', 'order 2?'],
        narration=(
            'Here is the scenario. Orders are handled one at a time from '
            'a channel. Order two arrives garbled, and the handler can '
            'never read it. Orders three and four are perfectly fine. '
            '[[slnc 300]] The question: what should the worker do with '
            'order two?'
        ),
    ),
    dict(
        key='03-poison', kind='console', title='A Message That Can Never Succeed',
        body="""ONE. Poison.
  4 orders, one garbled.
  handled: ORD-1.
  waiting: 3.
  attempts made: 11.

  orders 3 and 4 are stuck.""",
        narration=(
            'First, a message that can never succeed. Four orders, and '
            'one is garbled. Only the first is handled. The garbled one '
            'is tried again and again, ten times, and never succeeds. '
            'Orders three and four are stuck behind it, and will wait '
            'forever.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Try a message a fixed number of', 'times.', '', 'If it still fails, move it to a', 'dead letter channel.', '', 'Keep the original, the attempts,', 'and the reason.', '', 'The line moves on.'],
        narration=(
            'The pattern. Try a message a fixed number of times. If it '
            'still fails, move it to a dead letter channel. Keep the '
            'original message, the number of attempts, and the reason. '
            'And the line moves on.'
        ),
    ),
    dict(
        key='05-dlc', kind='console', title='A Dead Letter Channel',
        body="""TWO. Moved aside.
  after 3 attempts.
  handled: ORD-1, 3, 4.
  waiting: 0.
  dead letters: 1.

  orders 3 and 4 went through.""",
        narration=(
            'Second, a dead letter channel. After three attempts, the '
            'garbled order is moved aside. Orders one, three and four are '
            'handled. Nothing is waiting. There is one dead letter. '
            'Orders three and four went through.'
        ),
    ),
    dict(
        key='06-why', kind='console', title='It Says Why',
        body="""THREE. It says why.
  ORD-2: 3 attempts.
  last error: cannot read the
  body of ORD-2.
  from channel: orders.

  the original is kept.""",
        narration=(
            'Third, it says why. The dead letter records which order it '
            'was, three attempts, the last error, and which channel it '
            'came from. The original message is kept exactly, so that a '
            'person can look at it, and put it back.'
        ),
    ),
    dict(
        key='07-slow', kind='console', title='A Slow Day Is Not A Dead Letter',
        body="""FOUR. Slow, not dead.
  ORD-3 times out once, and
  succeeds on the second try.
  only ORD-2 is a dead letter.

  retry is for the first kind of
  failure, the dead letter for
  the second.""",
        narration=(
            'Fourth, a slow day is not a dead letter. Order three fails '
            'once, on a timeout, and succeeds on the second attempt. It '
            'is handled. Only order two, which fails every single time, '
            'is a dead letter. Retrying is for the first kind of failure. '
            'The dead letter channel is for the second.'
        ),
    ),
    dict(
        key='08-replay', kind='console', title='Fix It, And Replay',
        body="""FIVE. Replay.
  the parser is fixed.
  1 dead letter replayed.
  handled: 1, 3, 4, 2.
  dead: 0.

  order 2 came last. replay does
  not restore the order.""",
        narration=(
            'Fifth, fix it, and replay. The parser is fixed, and the one '
            'dead letter is replayed. Order two is handled at last. But '
            'look at the order: it was handled after three and four. '
            'Replay does not restore the original order.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill: Nobody Is Looking',
        body="""SIX. The bill.
  40 orders, half garbled:
  20 dead letters.

  the main channel: 0 waiting,
  looks healthy.

  nothing tells anyone to look.

  needs an alert, an owner, a
  limit on age.""",
        narration=(
            'Last, the bill. Forty orders, half of them garbled. Twenty '
            'dead letters, and each was an order that a customer was told '
            'was accepted. The main channel looks perfectly healthy: '
            'nothing waiting. The loss is in the dead letter channel, and '
            'nothing tells anyone to look. It needs an alert on its '
            'depth, an owner, and a limit on how long a message may stay. '
            'And each one is a copy of customer data.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A queue named something-dlq or', 'dead-letter.', '', 'A maxReceiveCount on an SQS queue,', 'or x-dead-letter-exchange in', '', "Spring's DefaultErrorHandler with", 'a DeadLetterPublishingRecoverer.'],
        narration=(
            'How do you recognise this in code you did not write? A queue '
            'named something-dlq or dead-letter. A maxReceiveCount on an '
            "SQS queue, or x-dead-letter-exchange in RabbitMQ. Spring's "
            'DefaultErrorHandler with a DeadLetterPublishingRecoverer. A '
            'dashboard with a count of messages in the dead letter queue.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a dead letter channel on every', 'channel where a message can fail', 'for ever. Retry a few times for', 'transient failures, then move the', 'message aside with its attempts', 'and its reason. Alert on the depth', 'of the dead letter channel, give', 'it an owner, and decide how long', 'messages stay. Make consumers safe'],
        narration=(
            'Here is my verdict, plainly. Use a dead letter channel on '
            'every channel where a message can fail for ever. Retry a few '
            'times for transient failures, then move the message aside '
            'with its attempts and its reason. Alert on the depth of the '
            'dead letter channel, give it an owner, and decide how long '
            'messages stay. Make consumers safe to replay.'
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
        body=['For a channel where failure is', 'impossible, or where losing a', 'message is fine, a dead letter', 'channel is more to run. Where a', 'message can be poison, its absence', 'is the outage.'],
        narration=(
            'So when is it too much? For a channel where failure is '
            'impossible, or where losing a message is fine, a dead letter '
            'channel is more to run. Where a message can be poison, its '
            'absence is the outage.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Dead Letter Channel. [[slnc 250]] If you take one "
            'sentence away, take this one: a dead letter channel keeps a '
            'poison message from blocking the line, and needs someone to '
            'look at it. [[slnc 350]] The full source, the written notes, '
            'the diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'add an alert that fires when the dead letter count passes '
            'five, and test it. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
