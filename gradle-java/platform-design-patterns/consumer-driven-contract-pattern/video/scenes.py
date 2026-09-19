"""Scene definitions for the Consumer-Driven Contract teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Consumer-Driven Contract',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Consumer-Driven '
            'Contract pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'consumer driven contract lets each consumer of a service '
            'write down exactly what it needs. The provider then checks '
            'every release against those contracts, before it goes out. '
            '[[slnc 350]] This is another project in the platform '
            'category, whose subject is how software is shipped, run and '
            'operated. In our online store, the catalog team renamed a '
            'field in the price service, and the checkout broke in '
            'production. [[slnc 300]] By the end you will see a rename '
            'break checkout in production, see consumers write down what '
            'they read, see the provider check itself and pass, see a '
            'rename caught before release with a name attached, see that '
            'adding a field is safe, and see the bill, which is that a '
            'contract checks shape and not meaning.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Checkout reads a price and a', 'sku from the catalog.', '', 'Reports reads only the sku.', '', 'The catalog team wants to', 'change the shape of the answer.', '', 'How do they know who breaks?'],
        narration=(
            'Here is the scenario. The checkout reads a price and a sku '
            "from the catalog's price service. The reports service reads "
            'only the sku. The catalog team wants to change the shape of '
            'the answer. [[slnc 300]] The question: how do they know who '
            'will break?'
        ),
    ),
    dict(
        key='03-nobody', kind='console', title='Nobody Told The Consumer',
        body="""ONE. Nobody told the consumer.
  the catalog renamed
  priceCents to price.
  checkout, 2 mugs: failed.

  found in production,
  by a customer.""",
        narration=(
            'First, nobody told the consumer. The catalog renamed price '
            'cents to price, and released. Checkout, two mugs: the order '
            'failed. It was found in production, by a customer.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Each consumer writes down what', 'it reads: field names and types.', '', 'The provider runs its real', 'answer against every contract', 'before a release.', '', 'A break names who and what.'],
        narration=(
            'The pattern. Each consumer writes down what it reads: field '
            'names, and types. The provider runs its real answer against '
            'every contract, before a release. A break names who, and '
            'what.'
        ),
    ),
    dict(
        key='05-write', kind='console', title='The Consumer Writes It Down',
        body="""TWO. Write it down.
  checkout: sku string,
  priceCents integer.
  reports: sku string.

  each lists only what it reads,
  and the types.""",
        narration=(
            "Second, the consumer writes it down. Checkout's contract: "
            "price cents, an integer, and sku, a string. Reports' "
            'contract: sku, a string. Each lists only the fields it '
            'reads, and their types.'
        ),
    ),
    dict(
        key='06-check', kind='console', title='The Provider Checks Itself',
        body="""THREE. The provider checks.
  the real answer, against both
  contracts.
  problems: none.
  safe to release.""",
        narration=(
            "Third, the provider checks itself. The catalog's real answer "
            'is checked against both contracts. No problems. Safe to '
            'release.'
        ),
    ),
    dict(
        key='07-caught', kind='console', title='The Rename Is Caught',
        body="""FOUR. The rename is caught.
  problems: checkout expects
  priceCents (integer): missing.

  the build fails, naming the
  consumer and the field.""",
        narration=(
            'Fourth, the rename is caught. The same check on the renamed '
            'release reports: checkout expects price cents, an integer, '
            'and it is missing. The build fails, and it names the '
            'consumer and the field.'
        ),
    ),
    dict(
        key='08-safe', kind='console', title='Adding Is Safe',
        body="""FIVE. Adding is safe.
  a stock field added:
  problems: none.

  the rename, per consumer:
  checkout 1 problem,
  reports 0.
  reports never used the field.""",
        narration=(
            'Fifth, adding is safe, and only the affected are named. A '
            'release that adds a stock field: no problems. And the rename '
            'again, per consumer: checkout, one problem; reports, none. '
            'Reports never used that field.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  pounds sent, not pence, in the
  same field: problems: none.
  it passes.

  checkout, 2 mugs: 32,
  should be 3200.

  a contract checks shape,
  not meaning.""",
        narration=(
            'Last, the bill. A release that now sends pounds, not pence, '
            'in the same field: no problems. It passes. Checkout, two '
            'mugs: total thirty two, where it should be thirty two '
            'hundred. A contract checks the shape, and not the meaning. '
            'And every consumer must keep its contract up to date, or the '
            'check protects nobody.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Pact files, or Spring Cloud', 'Contract stubs.', '', 'A provider build that fails with a', "consumer's name in the message.", '', 'A consumer test that runs against', 'a stub generated from its own'],
        narration=(
            'How do you recognise this in code you did not write? Pact '
            'files, or Spring Cloud Contract stubs. A provider build that '
            "fails with a consumer's name in the message. A consumer test "
            'that runs against a stub generated from its own contract. A '
            "broker or folder of contracts that the provider's pipeline "
            'reads.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Let consumers state what they use,', 'and let providers check against it', 'before every release. Keep', 'contracts small: only the fields', 'read. Share them where the', "provider's build can find them.", 'Add tests for meaning where shape', 'is not enough.'],
        narration=(
            'Here is my verdict, plainly. Let consumers state what they '
            'use, and let providers check against it before every '
            'release. Keep contracts small: only the fields read. Share '
            "them where the provider's build can find them. Add tests for "
            'meaning where shape is not enough.'
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
        body=['If provider and consumer are one', 'team with one release, an ordinary', 'test is enough. Contracts pay off', 'across teams that release apart.'],
        narration=(
            'So when is it too much? If provider and consumer are one '
            'team with one release, an ordinary test is enough. Contracts '
            'pay off across teams that release apart.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Consumer-Driven Contract. [[slnc 250]] If you take "
            'one sentence away, take this one: a consumer driven contract '
            'lets a provider learn who a change breaks before it ships, '
            'and the price is keeping contracts up to date, and their '
            'blindness to meaning. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, add a contract for a third consumer that '
            'reads the currency, and see it pass. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
