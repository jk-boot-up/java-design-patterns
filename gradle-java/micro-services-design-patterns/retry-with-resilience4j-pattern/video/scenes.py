"""Scene definitions for the Retry with Resilience4j teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Retry with Resilience4j',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Retry with Backoff pattern in Java, using a library called '
            'Resilience four J. [[slnc 300]] This video is presented by '
            'Jayasekhar Konduru. [[slnc 600]] First, a simple definition. '
            '[[slnc 300]] When a call fails for a reason that might not '
            'happen again, you try again. [[slnc 300]] Each time, you '
            'wait a little longer first. [[slnc 300]] And you only do it '
            'if doing the job twice cannot do it twice. [[slnc 600]] In '
            'Resilience four J, a retry is an annotation on a method. '
            '[[slnc 300]] The number of attempts, and the waits, are '
            'settings. [[slnc 700]] In our online store, checkout calls a '
            'flaky payment gateway. [[slnc 500]] By the end, you will '
            'hear the retry built from one annotation and a few settings. '
            '[[slnc 300]] Then the three ways it goes wrong. [[slnc 300]] '
            'Retrying what should not be retried. [[slnc 300]] Charging a '
            'customer twice. [[slnc 300]] And retries that multiply.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Retry with Backoff, the hand-built', 'video, retries a flaky payment gateway,', 'waiting longer each time.', '', 'It shows a retry is safe only if', 'doing it twice cannot do it twice.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video builds on the plain Java Retry with Backoff '
            'video. [[slnc 300]] If you have not seen it, start there. '
            '[[slnc 500]] That video retries a flaky payment gateway, '
            'waiting longer each time. [[slnc 300]] And it shows that a '
            'retry is only safe when the failure is temporary. [[slnc '
            '300]] And when doing the operation twice cannot do it twice. '
            '[[slnc 500]] This video uses the same example. [[slnc 300]] '
            'It does not teach the pattern again. [[slnc 300]] It shows '
            'what Resilience four J does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Resilience4j.', '', 'It contains the retry, with its', 'waits and its exception lists.', '', 'It runs inside Spring Boot,', 'through an annotation.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before any code, what is Resilience four J? [[slnc 400]] It '
            'is a library of resilience patterns for Java. [[slnc 300]] '
            'It includes a retry, with settings for the waits, and lists '
            'of which errors to retry. [[slnc 300]] It also has a Spring '
            'Boot module that turns the retry into an annotation. [[slnc '
            '500]] And a promise. [[slnc 300]] Skipping this video loses '
            'none of the pattern. [[slnc 300]] The plain Java video '
            'teaches all of it.'
        ),
    ),
    dict(
        key='04-flaky', kind='console', title='A Flaky Call, Retried',
        body="""ONE. A flaky call.
  the gateway times out twice.
  the caller gets: R-1.
  gateway calls: 3.""",
        narration=(
            'First demo: the good case. [[slnc 400]] The gateway times '
            'out twice. [[slnc 300]] The third attempt works. [[slnc '
            '500]] The caller receives a receipt. [[slnc 300]] And it '
            'never sees the two failures. [[slnc 300]] Three calls '
            'reached the gateway.'
        ),
    ),
    dict(
        key='05-backoff', kind='console', title='Backoff',
        body="""TWO. Backoff.
  waits before each retry:
  1 ms, then 2 ms.

  each wait is twice the last.""",
        narration=(
            'Second demo: backoff. [[slnc 400]] Before the first retry, '
            'the wait is one millisecond. [[slnc 300]] Before the second, '
            'two milliseconds. [[slnc 300]] Each wait doubles. [[slnc '
            '500]] In a real system, the numbers would be bigger, but the '
            'shape is the same. [[slnc 300]] A struggling gateway is '
            'given room to recover.'
        ),
    ),
    dict(
        key='06-giveup', kind='console', title='Giving Up',
        body="""THREE. Giving up.
  the gateway never answers.
  after 3 attempts the caller
  gets GatewayTimeout.""",
        narration=(
            'Third demo: giving up. [[slnc 400]] This time, the gateway '
            'never answers. [[slnc 300]] The retry stops after three '
            'attempts. [[slnc 300]] And the caller gets the timeout '
            'error. [[slnc 500]] A retry has to end somewhere. [[slnc '
            '300]] And this is how.'
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
            'Fourth demo: what is worth retrying? [[slnc 400]] A declined '
            'card will be declined again. [[slnc 500]] With a setting '
            'that retries only timeouts, there is one attempt. [[slnc '
            '300]] With the default, which retries every error, there are '
            'three. [[slnc 500]] Three attempts, against a card that will '
            'not change its mind. [[slnc 300]] And a customer left '
            'waiting.'
        ),
    ),
    dict(
        key='08-twice', kind='console', title='A Retry Can Charge Twice',
        body="""FIVE. Charged twice.
  the answer was lost.
  no key: [4999, 4999].

  with a key: [4999].""",
        narration=(
            'Fifth demo: the danger the plain Java video warned about. '
            '[[slnc 400]] The charge went through, but the reply was '
            'lost. [[slnc 300]] So the retry charged again. [[slnc 500]] '
            'Without a key, there are two charges of forty-nine pounds '
            'ninety-nine. [[slnc 500]] With an idempotency key, the '
            'gateway recognises the repeat. [[slnc 300]] And it charges '
            'only once. [[slnc 500]] The library cannot supply that key. '
            '[[slnc 300]] You must.'
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
            'Last demo: retries in layers. [[slnc 400]] Checkout has a '
            'retry. [[slnc 300]] And the payment client underneath it '
            'also has one. [[slnc 500]] Checkout makes three attempts. '
            '[[slnc 300]] And each of those makes three attempts of its '
            'own. [[slnc 300]] So one customer and one dead gateway make '
            'nine calls. [[slnc 300]] Add a third layer, and it is '
            'twenty-seven. [[slnc 500]] So retry in one layer only, and '
            'choose which one.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Retry temporary failures only.', '', 'Send an idempotency key.', '', 'Retry in one layer.', '', 'Keep attempts and waits small.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Retry only temporary '
            'failures. [[slnc 300]] Send an idempotency key with every '
            'call that changes something. [[slnc 300]] Retry in one '
            'layer, not two. [[slnc 300]] And keep the number of '
            'attempts, and the waits, small.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Retry with a name.', '', 'resilience4j.retry in configuration.', '', 'retry-exceptions and', 'ignore-exceptions.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a retry annotation, with a name. [[slnc 300]] '
            'Look for retry settings in the configuration file. [[slnc '
            '300]] And look for lists of which errors to retry, and which '
            'to ignore.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Any Spring service that calls', 'a payment, email or shipping', 'provider over the network.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In any Spring '
            'service that calls a payment, email, or shipping provider '
            'over the network.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Resilience4j 2.4.0.', '', 'No web server, no web starter.'],
        narration=(
            'For the record, here is what was used. [[slnc 300]] Spring '
            'Boot, version four point one point one. [[slnc 300]] '
            'Resilience four J, version two point four point zero. [[slnc '
            '300]] There is no web server, and no web starter.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the real retry', 'and the real annotation.', '', 'Waits are one and two milliseconds,', 'and the values shown are the', 'ones Resilience4j chose.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is real: the real retry, and the real annotation. '
            '[[slnc 300]] The waits are only one and two milliseconds. '
            '[[slnc 300]] And the values you heard are the ones '
            'Resilience four J chose, not measured times.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a failure that will not go', 'away, a retry only delays the', 'error.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a failure that '
            'will not go away, a retry only delays the error.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Remove the retry from the', 'checkout layer and rerun act six.'],
        narration=(
            "That's Retry, with Resilience four J. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] '
            'Resilience four J gives you the retry as settings, but '
            'deciding whether it is safe is still your job. [[slnc 500]] '
            'The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Remove the retry '
            'from the checkout layer. [[slnc 300]] Then run the last demo '
            'again, and count the calls. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
