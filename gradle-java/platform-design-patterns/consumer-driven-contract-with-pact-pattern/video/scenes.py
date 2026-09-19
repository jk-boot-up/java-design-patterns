"""Scene definitions for the Consumer-Driven Contract with Pact teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Consumer-Driven Contract with Pact',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Consumer-Driven '
            'Contract pattern with Pact, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Consumer-Driven Contract video. '
            'That one let each consumer write its contract as data, and '
            'let the provider check its real answer against every '
            'contract, naming the consumer and the field. It also showed '
            'that a contract cannot see a change of meaning. This one '
            'shows the same idea inside Pact. [[slnc 350]] The plain '
            "definition, in short: with Pact, a consumer's test writes a "
            "pact file. The provider's build replays that file against "
            'the real service, and fails on any difference. [[slnc 300]] '
            'By the end you will see a rename break checkout in '
            'production, see two consumers write real pact files, see the '
            'provider replay them over real HTTP and pass, see a rename '
            'caught before release with a name attached, see that adding '
            'a field is safe, and see what a pact cannot catch.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Consumer-Driven Contract, the', 'hand-built video, writes contracts', 'as data.', '', 'It shows a verifier naming the', 'consumer and the field.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'This video assumes the Consumer-Driven Contract video. If '
            "you have not seen it, start there. It writes each consumer's "
            'contract as data, and shows a verifier that names the '
            'consumer and the field when a release breaks one. [[slnc '
            '300]] This one uses the same example. It does not teach the '
            'pattern again. It shows what Pact does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Pact JVM, a', 'library.', '', 'You need only Java. There is no', 'server, container or account.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before the first line of code, what Pact is. Pact is a '
            'library for contract testing. A consumer test uses it to '
            'write down what the consumer needs, into a pact file. The '
            "provider's build uses it to replay the file against the real "
            'service, and fail if the answer differs. [[slnc 300]] And a '
            'promise: skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-nobody', kind='console', title='Nobody Told The Consumer',
        body="""ONE. Nobody told the consumer.
  the catalog renamed priceCents
  to price.
  checkout, 2 mugs: failed.

  found in production, by a
  customer.""",
        narration=(
            'First, nobody told the consumer. The catalog renamed price '
            'cents to price, and released. Checkout, two mugs: the order '
            'failed. It was found in production, by a customer.'
        ),
    ),
    dict(
        key='05-write', kind='console', title='The Consumer Writes A Pact',
        body="""TWO. The consumer writes a pact.
  each client runs against Pact's
  mock, and agrees.
  2 pact files written.
  checkout: priceCents integer,
  sku string.
  reports: sku string.""",
        narration=(
            "Second, the consumer writes a pact. Each consumer's own "
            "client is run against Pact's mock of the catalog, and "
            "agrees. Two pact files are written. Checkout's pact: price "
            "cents, an integer, and sku, a string. Reports' pact: sku, a "
            'string.'
        ),
    ),
    dict(
        key='06-replay', kind='console', title='The Provider Replays The Pacts',
        body="""THREE. The provider replays.
  Pact replays each pact against
  the real catalog, over HTTP.
  checked: 2, problems: none.
  safe to release.""",
        narration=(
            'Third, the provider replays the pacts. Pact replays each '
            'pact against the real catalog, over HTTP. Two interactions '
            'checked, no problems. Safe to release.'
        ),
    ),
    dict(
        key='07-caught', kind='console', title='The Rename Is Caught',
        body="""FOUR. The rename is caught.
  checked 2, failed 1.
  checkout: the actual map is
  missing priceCents.

  the build fails, naming the
  consumer and the field.
  reports' pact still passes.""",
        narration=(
            'Fourth, the rename is caught. On the renamed release: two '
            'interactions checked, one failed. Checkout: the actual map '
            'is missing the following keys: price cents. The build fails, '
            "and Pact names the consumer and the field. Reports' pact "
            'still passes.'
        ),
    ),
    dict(
        key='08-safe', kind='console', title='Adding Is Safe',
        body="""FIVE. Adding is safe.
  a release that adds a stock
  field.
  checked 2, problems: none.""",
        narration=(
            'Fifth, adding is safe. A release that adds a stock field: '
            'two interactions checked, no problems. Adding a field breaks '
            'nobody.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  pounds sent, not pence, in the
  same field: problems none.
  it passes.

  checkout, 2 mugs: 32,
  should be 3200.

  a pact checks shape, not meaning.""",
        narration=(
            'Last, the bill. A release that now sends pounds, not pence, '
            'in the same field: no problems. It passes. Checkout, two '
            'mugs: total thirty two, where it should be thirty two '
            'hundred. A pact checks the shape, and not the meaning. And '
            'every consumer must keep its pact up to date, or the check '
            'protects nobody.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Consumers write pacts for what', 'they read.', '', 'Providers verify in their build.', '', 'Share the pact files, or use a', 'broker.', '', 'Test meaning separately.'],
        narration=(
            'My verdict, plainly. Let each consumer write a pact for what '
            "it reads, and only that. Run the provider's verification in "
            'its build, against the real service. Keep pact files where '
            "the provider's build can find them, or in a broker. And add "
            'tests for meaning, since a pact checks only shape.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A `@Pact` method or', '`ConsumerPactBuilder` in a', "consumer's tests.", '', '`@Provider` and `@PactFolder` or', "`@PactBroker` in a provider's", 'tests.', '', 'A `pacts` folder of JSON files.'],
        narration=(
            'How do you recognise this in code you did not write? A @Pact '
            "method or ConsumerPactBuilder in a consumer's tests. "
            "@Provider and @PactFolder or @PactBroker in a provider's "
            'tests. A pacts folder of JSON files.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Many microservice teams, and Pact', 'Broker or PactFlow in their', 'pipelines.'],
        narration=(
            'You have met this in many microservice teams, and pact '
            'broker or pactflow in their pipelines.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Pact JVM 4.7.5.', '', 'JUnit 5.10.2.', '', 'Java 21.'],
        narration=(
            'For the record. Pact JVM, 4.7.5. JUnit, 5.10.2. Java, 21.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: real pact', "files, Pact's own mock, and a real", 'HTTP server for the provider.', '', 'The consumers and the catalog are', 'small, and made for the demo.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            "Everything is real: real pact files, Pact's own mock, and a "
            'real HTTP server for the provider. The consumers and the '
            'catalog are small, and made for the demo.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['If provider and consumer are one', 'team with one release, an ordinary', 'test is enough. Pact pays off', 'across teams that release apart.'],
        narration=(
            'So when is it too much? If provider and consumer are one '
            'team with one release, an ordinary test is enough. Pact pays '
            'off across teams that release apart.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a third consumer that reads the currency, and see its pact pass..'],
        narration=(
            "That's Consumer-Driven Contract with Pact. [[slnc 250]] If "
            'you take one sentence away, take this one: Pact lets a '
            'provider learn who a change breaks before it ships, and it '
            'still cannot tell a change of meaning. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository. [[slnc 300]] If you '
            'try one exercise, add a third consumer that reads the '
            'currency, and see its pact pass. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
