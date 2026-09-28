"""Scene definitions for the Dead Letter Channel teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Dead Letter Channel',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Dead Letter Channel pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A dead letter '
            'channel is where a message goes when it cannot be handled, '
            'after a fixed number of tries. [[slnc 300]] So it stops '
            'blocking the messages behind it. [[slnc 300]] And someone '
            'can look at it later. [[slnc 600]] Think of the post '
            "office's undeliverable mail room. [[slnc 300]] A letter with "
            'an address nobody can read is set aside. [[slnc 300]] So the '
            'rest of the post still goes out on time. [[slnc 700]] In our '
            'online store, one order arrives garbled, and no amount of '
            'trying will read it. [[slnc 500]] In this video, that one '
            'bad message blocks everything behind it. [[slnc 300]] Then '
            'it is moved aside, after three tries, with its reason. '
            '[[slnc 300]] We will hear a slow moment that is not a dead '
            'letter, a message replayed after a fix, and then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Orders are handled one at a time.', '', 'Order 2 arrives garbled.', 'The handler can never read it.', '', 'Orders 3 and 4 are fine.', '', 'What should the worker do with', 'order 2?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Orders are handled one at '
            'a time, from a channel. [[slnc 300]] Order two arrives '
            'garbled. [[slnc 300]] The handler can never read it. [[slnc '
            '300]] But orders three and four are perfectly fine. [[slnc '
            '500]] So here is the question. [[slnc 300]] What should the '
            'worker do with order two?'
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
            'First, the naive way: a message that can never succeed. '
            '[[slnc 400]] Four orders arrive, and one is garbled. [[slnc '
            '300]] Only the first is handled. [[slnc 500]] The garbled '
            'order is tried again, and again, ten times, and never '
            'succeeds. [[slnc 300]] And orders three and four are stuck '
            'behind it. [[slnc 300]] They will wait forever.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Try a message a fixed number of', 'times.', '', 'If it still fails, move it to a', 'dead letter channel.', '', 'Keep the original, the attempts,', 'and the reason.', '', 'The line moves on.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Try each message a fixed '
            'number of times. [[slnc 300]] If it still fails, move it to '
            'a dead letter channel. [[slnc 500]] Keep the original '
            'message, the number of attempts, and the reason it failed. '
            '[[slnc 300]] And the line moves on.'
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
            'Second demo: a dead letter channel. [[slnc 400]] After three '
            'attempts, the garbled order is moved aside. [[slnc 500]] '
            'Orders one, three, and four are handled. [[slnc 300]] '
            'Nothing is left waiting. [[slnc 300]] And there is one dead '
            'letter. [[slnc 300]] Orders three and four went through.'
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
            'Third demo: it records why. [[slnc 400]] The dead letter '
            'records which order it was. [[slnc 300]] That it was tried '
            'three times. [[slnc 300]] The last error: cannot read the '
            'body of order two. [[slnc 300]] And which channel it came '
            'from. [[slnc 500]] The original message is kept exactly as '
            'it was. [[slnc 300]] So a person can look at it, and put it '
            'back later.'
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
            'Fourth demo: a slow moment is not a dead letter. [[slnc '
            '400]] Order three fails once, because of a timeout. [[slnc '
            '300]] Then it succeeds on the second try, and is handled. '
            '[[slnc 500]] Only order two, which fails every single time, '
            'becomes a dead letter. [[slnc 500]] Retrying is for '
            'temporary failures. [[slnc 300]] The dead letter channel is '
            'for failures that will never go away.'
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
            'Fifth demo: fix it, and replay. [[slnc 400]] The code that '
            'reads orders is fixed. [[slnc 300]] And the one dead letter '
            'is sent through again. [[slnc 500]] Order two is handled at '
            'last. [[slnc 300]] But notice the order. [[slnc 300]] It was '
            'handled after orders three and four. [[slnc 300]] Replaying '
            'does not restore the original order.'
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
            'Finally, the cost: nobody is looking. [[slnc 400]] Forty '
            'orders arrive, and half of them are garbled. [[slnc 300]] '
            'That makes twenty dead letters. [[slnc 300]] Each one is an '
            'order a customer was told had been accepted. [[slnc 500]] '
            'Yet the main channel looks perfectly healthy, with nothing '
            'waiting. [[slnc 300]] The loss is hidden in the dead letter '
            'channel. [[slnc 300]] And nothing tells anyone to look. '
            '[[slnc 500]] It needs an alert when it fills up, an owner, '
            'and a limit on how long messages may stay. [[slnc 300]] And '
            'every dead letter is a copy of customer data.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A queue named something-dlq or', 'dead-letter.', '', 'A maxReceiveCount on an SQS queue,', 'or x-dead-letter-exchange in', '', "Spring's DefaultErrorHandler with", 'a DeadLetterPublishingRecoverer.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a queue whose name ends in D L Q, or '
            'dead letter. [[slnc 300]] Look for a maximum receive count '
            'on an Amazon S Q S queue. [[slnc 300]] Or a dead letter '
            'exchange setting in RabbitMQ. [[slnc 300]] And look for a '
            'dashboard showing how many messages are in the dead letter '
            'queue.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a dead letter channel on every', 'channel where a message can fail', 'for ever. Retry a few times for', 'transient failures, then move the', 'message aside with its attempts', 'and its reason. Alert on the depth', 'of the dead letter channel, give', 'it an owner, and decide how long', 'messages stay. Make consumers safe'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a dead letter '
            'channel on every channel where a message could fail forever. '
            '[[slnc 500]] Retry a few times, for temporary failures. '
            '[[slnc 300]] Then move the message aside, with its attempts '
            'and its reason. [[slnc 500]] Raise an alert when the dead '
            'letter channel fills up. [[slnc 300]] Give it an owner. '
            '[[slnc 300]] Decide how long messages may stay. [[slnc 300]] '
            'And make sure handling a message twice is safe, so replays '
            'are safe.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a channel where failure is', 'impossible, or where losing a', 'message is fine, a dead letter', 'channel is more to run. Where a', 'message can be poison, its absence', 'is the outage.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a channel where '
            'failure is impossible, or where losing a message does not '
            'matter, a dead letter channel is more to run. [[slnc 400]] '
            'But where a message can be poison, not having one is the '
            'outage.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Dead Letter Channel pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A dead '
            'letter channel stops a poison message blocking the line, but '
            'it needs someone to look at it. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Add an alert that fires when there are '
            'more than five dead letters. [[slnc 300]] And write a test '
            'for it. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
