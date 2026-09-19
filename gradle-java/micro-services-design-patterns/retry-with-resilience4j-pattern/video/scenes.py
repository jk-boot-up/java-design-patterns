"""Scene definitions for the Retry with Resilience4j teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Retry with Resilience4j',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Retry with '
            'Backoff pattern with Resilience4j, in Java, and it is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] It '
            'is the framework version of the Retry with Backoff video. '
            'That one retried a flaky payment gateway with a growing wait '
            'between attempts, and showed why a retry is safe only when '
            'the failure is temporary and doing the operation twice '
            'cannot do it twice. This one shows the same idea inside '
            'Resilience4j. [[slnc 350]] The plain definition, in short: '
            'in Resilience4j, a retry is an annotation on a method, and '
            'the attempts and the waits are configuration. [[slnc 300]] '
            'By the end you will see the retry as an annotation and four '
            'settings, then see the three ways it goes wrong: retrying '
            'what should not be retried, charging twice, and retries that '
            'multiply.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Retry with Backoff, the hand-built', 'video, retries a flaky payment gateway,', 'waiting longer each time.', '', 'It shows a retry is safe only if', 'doing it twice cannot do it twice.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Retry with Backoff video. If you have '
            'not seen it, start there. It retries a flaky payment '
            'gateway, waiting longer each time, and shows that a retry is '
            'safe only when the failure is temporary and doing the '
            'operation twice cannot do it twice. [[slnc 300]] This one '
            'uses the same example. It does not teach the pattern again. '
            'It shows what Resilience4j does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Resilience4j.', '', 'It contains the retry, with its', 'waits and its exception lists.', '', 'It runs inside Spring Boot,', 'through an annotation.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Resilience4j is. '
            'Resilience4j is a library of resilience patterns for Java. '
            'It contains a retry with configurable waits and exception '
            'lists, and a Spring Boot module that turns it into an '
            'annotation. [[slnc 300]] And a promise: skipping this video '
            'loses none of the pattern. The hand-built one teaches all of '
            'it.'
        ),
    ),
    dict(
        key='04-flaky', kind='console', title='A Flaky Call, Retried',
        body="""ONE. A flaky call.
  the gateway times out twice.
  the caller gets: R-1.
  gateway calls: 3.""",
        narration=(
            'First, the good case. The gateway times out twice. The third '
            'attempt works. The caller receives a receipt, and never sees '
            'the two failures. Three calls reached the gateway.'
        ),
    ),
    dict(
        key='05-backoff', kind='console', title='Backoff',
        body="""TWO. Backoff.
  waits before each retry:
  1 ms, then 2 ms.

  each wait is twice the last.""",
        narration=(
            'Second, backoff. Before the first retry, one millisecond. '
            'Before the second, two. Each wait doubles. In production the '
            'numbers would be larger, but the shape is the same. A '
            'struggling gateway is given room to recover.'
        ),
    ),
    dict(
        key='06-giveup', kind='console', title='Giving Up',
        body="""THREE. Giving up.
  the gateway never answers.
  after 3 attempts the caller
  gets GatewayTimeout.""",
        narration=(
            'Third, giving up. If the gateway never answers, the retry '
            'stops after three attempts. The caller gets the timeout '
            'exception. A retry has to end, and this is how.'
        ),
    ),
    dict(
        key='07-which', kind='console', title='Not Everything Is Worth Retrying',
        body="""FOUR. What to retry.
  declined card, timeouts only:
  1 attempt.

  retrying everything:
  3 attempts, same answer.""",
        narration=(
            'Fourth, what to retry. A declined card will decline again. '
            'With a list that retries only timeouts, there is one '
            'attempt. With the default, which retries everything, there '
            'are three. [[slnc 300]] Three attempts against a card that '
            'will not change its mind, and a customer waiting.'
        ),
    ),
    dict(
        key='08-twice', kind='console', title='A Retry Can Charge Twice',
        body="""FIVE. Charged twice.
  the answer was lost.
  no key: [4999, 4999].

  with a key: [4999].""",
        narration=(
            'Fifth, the danger the partner video warned about. The charge '
            'went through, but the answer was lost, so the retry charged '
            'again. Without a key, two charges of forty nine ninety nine. '
            '[[slnc 300]] With an idempotency key, the gateway recognises '
            'the repeat and charges once. The library cannot supply this. '
            'You must.'
        ),
    ),
    dict(
        key='09-multiply', kind='console', title='Retries Multiply',
        body="""SIX. Multiply.
  checkout: 3 attempts.
  each: 3 gateway attempts.

  one customer, one dead
  gateway: 9 calls.""",
        narration=(
            'Last, layers. Checkout has a retry, and so does the payments '
            'client below it. Three attempts, each making three. One '
            'customer and one dead gateway make nine calls. Add a third '
            'layer and it is twenty seven. [[slnc 300]] Retry in one '
            'layer only, and choose which.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Retry temporary failures only.', '', 'Send an idempotency key.', '', 'Retry in one layer.', '', 'Keep attempts and waits small.'],
        narration=(
            'My verdict, plainly. Retry only temporary failures. Send an '
            'idempotency key with every call that changes something. '
            'Retry in one layer, not two. And keep the attempts and the '
            'waits small.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Retry with a name.', '', 'resilience4j.retry in configuration.', '', 'retry-exceptions and', 'ignore-exceptions.'],
        narration=(
            'How do you recognise this in code you did not write? A retry '
            'annotation with a name. Settings under resilience four j '
            'retry. And retry exceptions or ignore exceptions lists.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Any Spring service that calls', 'a payment, email or shipping', 'provider over the network.'],
        narration=(
            'You have met this in any Spring service that calls a '
            'payment, email or shipping provider over the network.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Resilience4j 2.4.0.', '', 'No web server, no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. '
            'Resilience four j two point four point zero. No web server, '
            'and no web starter.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the real retry', 'and the real annotation.', '', 'Waits are one and two milliseconds,', 'and the values shown are the', 'ones Resilience4j chose.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: the real retry and the real annotation. '
            'The waits are one and two milliseconds, and the values shown '
            'are the ones Resilience4j chose, not measured.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a failure that will not go', 'away, a retry only delays the', 'error.'],
        narration=(
            'So when is it too much? For a failure that will not go away, '
            'a retry only delays the error.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Remove the retry from the', 'checkout layer and rerun act six.'],
        narration=(
            "That's Retry with Resilience4j. [[slnc 250]] If you take one "
            'sentence away, take this one: Resilience4j gives you the '
            'retry as configuration, and safety is still your decision. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, remove the '
            'retry from the checkout layer, and rerun act six. [[slnc '
            '300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of '
            'the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
