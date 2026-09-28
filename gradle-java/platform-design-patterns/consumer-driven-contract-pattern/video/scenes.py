"""Scene definitions for the Consumer-Driven Contract teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Consumer-Driven Contract',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Consumer-Driven Contract pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A service has '
            'consumers: other services that call it and read its answers. '
            '[[slnc 300]] With consumer-driven contracts, each consumer '
            'writes down exactly what it needs from the answer. [[slnc '
            '300]] And the service checks every new release against those '
            'written needs, before it goes out. [[slnc 600]] Think of a '
            'restaurant supplier. [[slnc 300]] Each restaurant writes '
            'down exactly what it relies on. [[slnc 300]] Before the '
            "supplier changes a product, it checks every restaurant's "
            'list. [[slnc 700]] In our online store, the catalog team '
            'renamed a field in the price service, and checkout broke. '
            '[[slnc 500]] By the end, you will hear a rename break '
            'checkout for real customers. [[slnc 300]] Consumers write '
            'down what they read. [[slnc 300]] A rename caught before '
            'release, with a name attached. [[slnc 300]] Why adding a '
            'field is safe. [[slnc 300]] And the bill: a contract checks '
            'shape, not meaning.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Checkout reads a price and a', 'sku from the catalog.', '', 'Reports reads only the sku.', '', 'The catalog team wants to', 'change the shape of the answer.', '', 'How do they know who breaks?'],
        narration=(
            "Here is the scenario. [[slnc 400]] The catalog's price "
            'service answers with a few fields. [[slnc 300]] Checkout '
            'reads two of them: the product code, and the price in pence. '
            '[[slnc 300]] The reports service reads only the product '
            'code. [[slnc 500]] The catalog team wants to change the '
            'shape of the answer. [[slnc 500]] So here is the question. '
            '[[slnc 300]] How do they know who will break?'
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
            'First demo: nobody told the consumer. [[slnc 400]] The '
            'catalog renamed the field price cents, to just price. [[slnc '
            '300]] And released it. [[slnc 500]] A customer checks out '
            'two mugs. [[slnc 300]] The order fails. [[slnc 500]] The '
            'problem was found in production, by a customer.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Each consumer writes down what', 'it reads: field names and types.', '', 'The provider runs its real', 'answer against every contract', 'before a release.', '', 'A break names who and what.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Each consumer writes down '
            'what it reads: the field names, and their types. [[slnc '
            '300]] That written list is the contract. [[slnc 500]] Before '
            'every release, the service checks its real answer against '
            'every contract. [[slnc 300]] If something breaks, the check '
            'names which consumer, and which field.'
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
            'Second demo: consumers write it down. [[slnc 400]] '
            "Checkout's contract says: price cents, a whole number, and "
            "product code, some text. [[slnc 300]] Reports' contract "
            'says: product code, some text. [[slnc 500]] Each lists only '
            'the fields it actually reads, and their types.'
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
            'Third demo: the service checks itself. [[slnc 400]] The '
            "catalog's real answer is checked against both contracts. "
            '[[slnc 300]] No problems. [[slnc 300]] It is safe to '
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
            'Fourth demo: the rename is caught. [[slnc 400]] The same '
            'check runs on the renamed release. [[slnc 300]] It reports: '
            'checkout expects price cents, a whole number, and it is '
            'missing. [[slnc 500]] The build fails. [[slnc 300]] And it '
            'names the consumer, and the field.'
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
            'Fifth demo: adding is safe. [[slnc 400]] A release adds a '
            "new stock field. [[slnc 300]] No problems, because nobody's "
            'contract is broken. [[slnc 600]] And the rename again, '
            'checked one consumer at a time. [[slnc 300]] Checkout: one '
            'problem. [[slnc 300]] Reports: none. [[slnc 300]] Reports '
            'never used that field.'
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
            'Finally, the bill. [[slnc 400]] A new release sends the '
            'price in pounds, not pence, in the same field. [[slnc 300]] '
            'The field is still there, and still a number. [[slnc 300]] '
            'So the check passes. [[slnc 500]] A customer checks out two '
            'mugs. [[slnc 300]] The total comes out as thirty-two, when '
            'it should be thirty-two hundred pence. [[slnc 600]] A '
            'contract checks the shape of the answer, not its meaning. '
            '[[slnc 300]] And every consumer must keep its contract up to '
            'date. [[slnc 300]] Otherwise the check protects nobody.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Pact files, or Spring Cloud', 'Contract stubs.', '', 'A provider build that fails with a', "consumer's name in the message.", '', 'A consumer test that runs against', 'a stub generated from its own'],
        narration=(
            'How can you spot this in a system someone else built? [[slnc '
            '400]] Look for contract files from tools like Pact, or '
            "Spring Cloud Contract. [[slnc 300]] Look for a service's "
            "build that fails with a consumer's name in the message. "
            '[[slnc 300]] Look for a consumer test that runs against a '
            'fake service, generated from its own contract. [[slnc 300]] '
            "Or a shared folder of contracts that the service's build "
            'reads.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Let consumers state what they use,', 'and let providers check against it', 'before every release. Keep', 'contracts small: only the fields', 'read. Share them where the', "provider's build can find them.", 'Add tests for meaning where shape', 'is not enough.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Let consumers state '
            'what they use. [[slnc 300]] Let the service check against '
            'those contracts before every release. [[slnc 500]] Keep '
            'contracts small: only the fields actually read. [[slnc 300]] '
            "Keep them where the service's build can find them. [[slnc "
            '300]] And add tests for meaning, where shape is not enough.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] "
            'Nothing depends on a real clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If provider and consumer are one', 'team with one release, an ordinary', 'test is enough. Contracts pay off', 'across teams that release apart.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If the service and '
            'its consumer belong to one team, released together, an '
            'ordinary test is enough. [[slnc 400]] Contracts pay off '
            'between teams that release separately.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Consumer-Driven Contract pattern. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] A '
            'consumer-driven contract tells a service who a change will '
            'break before it ships, and the price is keeping contracts up '
            'to date, and their blindness to meaning. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 300]] It runs '
            'offline, with nothing installed except a Java development '
            'kit. [[slnc 500]] Here is one exercise to try. [[slnc 300]] '
            'Add a contract for a third consumer that reads the currency. '
            '[[slnc 300]] And check that it passes. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
