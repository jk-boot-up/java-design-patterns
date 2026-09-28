"""Scene definitions for the Gateway teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Gateway',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Gateway pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A gateway is one class that '
            'wraps access to an outside system. [[slnc 300]] The rest of '
            'the program speaks its own language. [[slnc 300]] And it can '
            'be tested without the real outside system. [[slnc 600]] '
            'Think of a travel adapter plug. [[slnc 300]] Your charger '
            'stays the same in every country. [[slnc 300]] Only the '
            'adapter knows the shape of the foreign socket. [[slnc 700]] '
            'In our online store, the outside system is a payment '
            'provider. [[slnc 500]] In this video, three places call the '
            'provider directly. [[slnc 300]] Then one door is put in '
            'front of it. [[slnc 300]] We will test the shop with no '
            "network, keep the network's quirks in one class, and swap "
            'provider without touching the shop. [[slnc 300]] And then '
            'the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The store takes payments through', 'an outside provider.', '', 'Checkout, renewals and gift cards', 'all charge a card.', '', "The provider's client: maps of", 'strings, and two-digit codes.', '', 'Who talks to it?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The online store takes '
            'payments through an outside provider. [[slnc 500]] Checkout, '
            'subscription renewals, and gift card top-ups all need to '
            "charge a card. [[slnc 500]] The provider's own client code "
            'uses maps of text values, and two-digit result codes. [[slnc '
            '500]] So here is the question. [[slnc 300]] Who should talk '
            'to it?'
        ),
    ),
    dict(
        key='03-direct', kind='console', title="The Provider's Client, Everywhere",
        body="""ONE. Everywhere.
  checkout, renewal, gift card.
  three places build the
  provider's fields and read
  its codes.

  one forgot the currency.""",
        narration=(
            "First, the naive way: the provider's client, everywhere. "
            '[[slnc 400]] Checkout, subscription renewal, and gift card '
            "top-up each build the provider's request themselves. [[slnc "
            "300]] And each reads the provider's result codes. [[slnc "
            '500]] All three work. [[slnc 300]] But one of them, the gift '
            'card, forgot the currency field. [[slnc 300]] And nobody has '
            'noticed yet.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One class wraps the outside', 'system.', '', "It speaks the shop's language:", 'approved, declined, unavailable.', '', "Only it knows the provider's", 'fields and codes.', '', 'The shop depends on the door.'],
        narration=(
            'Now, the pattern. [[slnc 400]] One class wraps the outside '
            "system. [[slnc 300]] It speaks the shop's language: "
            'approved, declined, or unavailable. [[slnc 500]] Only that '
            "class knows the provider's fields and codes. [[slnc 300]] "
            'And the rest of the shop depends on the door, not on what is '
            'behind it.'
        ),
    ),
    dict(
        key='05-door', kind='console', title='One Door',
        body="""TWO. One door.
  first: paid, AC-4999.
  second: card declined.

  Checkout has no field name
  and no code in it.""",
        narration=(
            'Second demo: one door. [[slnc 400]] The shop asks for two '
            'payments. [[slnc 300]] The first is approved, and comes back '
            'with a receipt. [[slnc 300]] The second is declined. [[slnc '
            '500]] The checkout code contains no provider field names, '
            'and no result codes. [[slnc 300]] It only speaks of '
            'approved, declined, and unavailable.'
        ),
    ),
    dict(
        key='06-fake', kind='console', title='Tests That Never Leave The Process',
        body="""THREE. A fake.
  paid; declined; unavailable.

  asked of the fake: 3 times.
  network calls made: 0.

  told to fail on demand.""",
        narration=(
            'Third demo: tests that never leave the program. [[slnc 400]] '
            'A fake gateway is told what to answer. [[slnc 300]] It gives '
            'approved, then declined, then unavailable. [[slnc 500]] '
            'Three questions, and zero network calls. [[slnc 500]] A real '
            'provider cannot be told to go down on demand. [[slnc 300]] '
            'The fake can.'
        ),
    ),
    dict(
        key='07-habits', kind='console', title="One Place For The Network's Habits",
        body="""FOUR. Habits.
  a timeout, then an answer:
  paid. 2 network calls.

  two timeouts: unavailable.

  the retry rule lives in one
  class.""",
        narration=(
            "Fourth demo: one place for the network's quirks. [[slnc "
            '400]] The provider times out once, and then answers. [[slnc '
            '300]] The gateway tries again, and the shop is simply told: '
            'paid. [[slnc 300]] Two network calls were made. [[slnc 500]] '
            'If it times out twice in a row, the shop is told: '
            'unavailable. [[slnc 500]] The retry rule lives in one class.'
        ),
    ),
    dict(
        key='08-swap', kind='console', title='Another Provider, The Same Shop',
        body="""FIVE. Another provider.
  on Acme: AC-4999.
  on BetaPay: BP-4999.

  Checkout was not changed.
  it was given another gateway.""",
        narration=(
            'Fifth demo: another provider, the same shop. [[slnc 400]] '
            'The same checkout runs on the Acme provider. [[slnc 300]] '
            'And then on a second provider, called BetaPay, whose client '
            'has a completely different shape. [[slnc 500]] The checkout '
            'was not changed at all. [[slnc 300]] It was simply given a '
            'different gateway.'
        ),
    ),
    dict(
        key='09-limit', kind='console', title='The Bill: What The Door Cannot Say',
        body="""SIX. The bill.
  Acme can capture part of a
  payment later.
  the interface has: charge.

  a new method on the interface
  and all 3 gateways.

  BetaPay cannot do it at all.""",
        narration=(
            'Finally, the cost: what the door cannot say. [[slnc 400]] '
            'Acme can hold a payment, and collect only part of it later. '
            '[[slnc 300]] But the gateway interface has just one method: '
            'charge. [[slnc 500]] To use that feature, a method must be '
            'added to the interface, and to all three gateways. [[slnc '
            '300]] And BetaPay cannot do it at all. [[slnc 300]] So the '
            'interface must say what happens then. [[slnc 500]] A door '
            "that speaks the shop's language can only say what every "
            'provider can say.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['An interface named for what the', 'program needs, with an', '', 'A Fake or InMemory implementation', 'used in tests.', '', "A class that imports the vendor's", 'SDK, which nothing else does.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for an interface named after what the '
            'program needs, with an implementation named after the '
            'vendor. [[slnc 300]] Look for a fake, or in-memory, version '
            'used in tests. [[slnc 300]] Look for one class that imports '
            "the vendor's library, which nothing else imports. [[slnc "
            '300]] And look for wrappers around web clients, or mail '
            'senders.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Put a gateway in front of any', 'outside system your program', 'depends on: a payment provider, a', 'mail server, a remote API. Keep it', "small and in the program's own", "words. Put the system's habits in", 'it: codes, retries, timeouts. Give', 'tests a fake. Expect the interface', 'to be the common ground, and'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Put a gateway in front '
            'of any outside system your program depends on. [[slnc 300]] '
            'A payment provider, a mail server, or a remote service. '
            "[[slnc 500]] Keep it small, and in your program's own words. "
            "[[slnc 300]] Put the outside system's quirks inside it: "
            'codes, retries, and timeouts. [[slnc 300]] Give your tests a '
            'fake. [[slnc 500]] And expect the interface to cover only '
            'what all providers share. [[slnc 300]] Decide on purpose '
            'what to do about features only one provider has.'
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
        body=['For a call made in one place to a', 'system that will never change, a', 'wrapper is one more class to read.', 'It earns its place with several', 'callers, or a need for a fake.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a call made in '
            'one place, to a system that will never change, a wrapper is '
            'just one more class to read. [[slnc 400]] A gateway earns '
            'its place when there are several callers, or when you need a '
            'fake for testing.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Gateway pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] A gateway lets your '
            'program speak its own language to the outside world, at the '
            'price of only saying what every provider can say. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Add a refund '
            'method to the gateway. [[slnc 300]] Then count how many '
            'classes had to change. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
