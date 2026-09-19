"""Scene definitions for the Gateway teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Gateway',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Gateway pattern '
            'in Java, and it is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] The plain definition: a gateway is one '
            'class that wraps access to an outside system. The rest of '
            'the program speaks its own language, and can be tested '
            'without the real thing. [[slnc 350]] This is another project '
            'in the enterprise category, whose subject is how a business '
            'application organises its logic, its data and its requests. '
            'In our online store, the outside thing is a payment '
            'provider. [[slnc 300]] By the end you will see three places '
            "call a payment provider's client directly, see one door put "
            'in front of it, test the shop with no network, keep the '
            "network's habits in one class, swap provider without "
            'touching the shop, and see the bill, which is what the door '
            'cannot say.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The store takes payments through', 'an outside provider.', '', 'Checkout, renewals and gift cards', 'all charge a card.', '', "The provider's client: maps of", 'strings, and two-digit codes.', '', 'Who talks to it?'],
        narration=(
            'Here is the scenario. The online store takes payments '
            'through an outside provider. Checkout, subscription '
            'renewals, and gift card top ups all need to charge a card. '
            "The provider's client uses maps of strings, and two digit "
            'result codes. [[slnc 300]] The question: who talks to it?'
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
            "First, the provider's client, everywhere. Checkout, "
            'subscription renewal and the gift card top up each build the '
            "provider's request and read its result codes. All three "
            'work. And one of them, the gift card, forgot the currency '
            'field. Nobody has noticed yet.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One class wraps the outside', 'system.', '', "It speaks the shop's language:", 'approved, declined, unavailable.', '', "Only it knows the provider's", 'fields and codes.', '', 'The shop depends on the door.'],
        narration=(
            'The pattern. One class wraps the outside system. It speaks '
            "the shop's language: approved, declined, unavailable. Only "
            "that class knows the provider's fields and codes. And the "
            'rest of the shop depends on the door, not on what is behind '
            'it.'
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
            'Second, one door. The shop asks twice. The first is '
            'approved, and comes back with a receipt. The second is '
            'declined. Checkout has no field name and no result code in '
            'it. It speaks approved, declined and unavailable.'
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
            'Third, tests that never leave the process. A fake gateway, '
            'told what to answer, gives approved, then declined, then '
            'unavailable. Three questions, and zero network calls. A real '
            'provider cannot be told to be down on demand. The fake can.'
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
            "Fourth, one place for the network's habits. The provider "
            'times out once, then answers. The gateway retries, and the '
            'shop is told: paid. Two network calls were made, and one '
            'line was logged. Two timeouts in a row, and the shop is told '
            'unavailable. The retry rule lives in one class.'
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
            'Fifth, another provider, the same shop. The same checkout '
            'runs on Acme, and on a second provider whose client has a '
            'completely different shape. Checkout was not changed. It was '
            'given a different gateway.'
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
            'Last, the bill. Acme can hold a payment and capture part of '
            'it later. The gateway interface has one method: charge. To '
            'use partial capture, a method must be added to the interface '
            'and to all three gateways. And BetaPay cannot do it at all, '
            'so the interface must say what happens then. A door in the '
            "shop's words can only say what every provider can say."
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['An interface named for what the', 'program needs, with an', '', 'A Fake or InMemory implementation', 'used in tests.', '', "A class that imports the vendor's", 'SDK, which nothing else does.'],
        narration=(
            'How do you recognise this in code you did not write? An '
            'interface named for what the program needs, with an '
            'implementation named for the vendor. A Fake or InMemory '
            'implementation used in tests. A class that imports the '
            "vendor's SDK, which nothing else does. A wrapper around "
            'RestTemplate, WebClient, or a mail sender.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Put a gateway in front of any', 'outside system your program', 'depends on: a payment provider, a', 'mail server, a remote API. Keep it', "small and in the program's own", "words. Put the system's habits in", 'it: codes, retries, timeouts. Give', 'tests a fake. Expect the interface', 'to be the common ground, and'],
        narration=(
            'Here is my verdict, plainly. Put a gateway in front of any '
            'outside system your program depends on: a payment provider, '
            'a mail server, a remote API. Keep it small and in the '
            "program's own words. Put the system's habits in it: codes, "
            'retries, timeouts. Give tests a fake. Expect the interface '
            'to be the common ground, and decide on purpose what to do '
            'about features that only one provider has.'
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
        body=['For a call made in one place to a', 'system that will never change, a', 'wrapper is one more class to read.', 'It earns its place with several', 'callers, or a need for a fake.'],
        narration=(
            'So when is it too much? For a call made in one place to a '
            'system that will never change, a wrapper is one more class '
            'to read. It earns its place with several callers, or a need '
            'for a fake.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Gateway. [[slnc 250]] If you take one sentence away, "
            'take this one: a gateway lets the shop speak its own '
            'language to the outside, at the price of only saying what '
            'every provider can say. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, add a refund method to the gateway, and '
            'see how many classes must change. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
