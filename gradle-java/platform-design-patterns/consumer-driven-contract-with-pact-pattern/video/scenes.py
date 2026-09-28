"""Scene definitions for the Consumer-Driven Contract with Pact teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Consumer-Driven Contract with Pact',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Consumer-Driven Contract pattern in Java, using a library '
            'called Pact. [[slnc 300]] This video is presented by '
            'Jayasekhar Konduru. [[slnc 600]] First, a simple definition. '
            '[[slnc 300]] Each consumer of a service writes down exactly '
            "what it needs from the service's answers. [[slnc 300]] And "
            'the service checks every new release against those needs, '
            "before it goes out. [[slnc 600]] With Pact, a consumer's "
            'test writes those needs into a file, called a pact. [[slnc '
            "300]] The service's build replays that file against the real "
            'service, and fails on any difference. [[slnc 700]] In our '
            "online store, a renamed field in the catalog's price service "
            'broke checkout. [[slnc 500]] By the end, you will hear that '
            'break happen for real customers. [[slnc 300]] Two consumers '
            'write real pact files. [[slnc 300]] The service replays '
            'them, and passes. [[slnc 300]] A rename caught before '
            'release, with a name attached. [[slnc 300]] And what a pact '
            'cannot catch.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Consumer-Driven Contract, the', 'hand-built video, writes contracts', 'as data.', '', 'It shows a verifier naming the', 'consumer and the field.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'This video builds on the plain Java Consumer-Driven Contract '
            'video. [[slnc 300]] If you have not seen it, start there. '
            "[[slnc 500]] That video writes each consumer's contract as "
            'simple data. [[slnc 300]] And it shows a checker that names '
            'the consumer and the field when a release breaks one. [[slnc '
            '500]] This video uses the same example. [[slnc 300]] It does '
            'not teach the pattern again. [[slnc 300]] It shows what Pact '
            'does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Pact JVM, a', 'library.', '', 'You need only Java. There is no', 'server, container or account.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before any code, what is Pact? [[slnc 400]] Pact is a '
            "library for contract testing. [[slnc 500]] A consumer's test "
            'uses it to write down what the consumer needs, into a pact '
            "file. [[slnc 300]] The service's build uses it to replay "
            'that file against the real service. [[slnc 300]] And the '
            'build fails if the answer is different. [[slnc 500]] You '
            'only need Java. [[slnc 300]] There is no server, no '
            'container, and no account. [[slnc 500]] And a promise. '
            '[[slnc 300]] Skipping this video loses none of the pattern. '
            '[[slnc 300]] The plain Java video teaches all of it.'
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
            'First demo: nobody told the consumer. [[slnc 400]] The '
            'catalog renamed the field price cents, to just price, and '
            'released it. [[slnc 500]] A customer checks out two mugs. '
            '[[slnc 300]] The order fails. [[slnc 300]] It was found in '
            'production, by a customer.'
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
            'Second demo: each consumer writes a pact. [[slnc 400]] Each '
            "consumer's own code is run against a fake catalog that Pact "
            'provides. [[slnc 300]] And it works. [[slnc 500]] As a '
            "result, two pact files are written. [[slnc 300]] Checkout's "
            'pact says: price cents, a whole number, and product code, '
            "some text. [[slnc 300]] Reports' pact says: product code, "
            'some text.'
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
            'Third demo: the service replays the pacts. [[slnc 400]] Pact '
            'replays each pact against the real catalog service, over '
            'real web requests. [[slnc 500]] Two checks, and no problems. '
            '[[slnc 300]] It is safe to release.'
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
            'Fourth demo: the rename is caught. [[slnc 400]] The pacts '
            'are replayed against the renamed release. [[slnc 300]] Two '
            'checks, and one fails. [[slnc 500]] For checkout, Pact '
            'reports that the answer is missing price cents. [[slnc 300]] '
            'The build fails, and names the consumer and the field. '
            '[[slnc 300]] The reports pact still passes.'
        ),
    ),
    dict(
        key='08-safe', kind='console', title='Adding Is Safe',
        body="""FIVE. Adding is safe.
  a release that adds a stock
  field.
  checked 2, problems: none.""",
        narration=(
            'Fifth demo: adding is safe. [[slnc 400]] A new release adds '
            'a stock field. [[slnc 300]] Two checks, and no problems. '
            '[[slnc 300]] Adding a field breaks nobody.'
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
            'Finally, the bill. [[slnc 400]] A new release sends the '
            'price in pounds, not pence, in the same field. [[slnc 300]] '
            'The field is still there, and still a number. [[slnc 300]] '
            'So the check passes. [[slnc 500]] A customer checks out two '
            'mugs. [[slnc 300]] The total comes out as thirty-two, when '
            'it should be thirty-two hundred pence. [[slnc 600]] A pact '
            'checks the shape of the answer, not its meaning. [[slnc '
            '300]] And every consumer must keep its pact up to date. '
            '[[slnc 300]] Otherwise the check protects nobody.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Consumers write pacts for what', 'they read.', '', 'Providers verify in their build.', '', 'Share the pact files, or use a', 'broker.', '', 'Test meaning separately.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Let each consumer '
            'write a pact for what it reads, and only that. [[slnc 300]] '
            "Run the service's check in its own build, against the real "
            'service. [[slnc 300]] Keep the pact files where that build '
            'can find them, or in a shared store called a pact broker. '
            '[[slnc 300]] And add separate tests for meaning, because a '
            'pact only checks shape.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A `@Pact` method or', '`ConsumerPactBuilder` in a', "consumer's tests.", '', '`@Provider` and `@PactFolder` or', "`@PactBroker` in a provider's", 'tests.', '', 'A `pacts` folder of JSON files.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            "400]] In a consumer's tests, look for Pact annotations, or a "
            "pact builder. [[slnc 300]] In a service's tests, look for "
            'annotations naming the provider, and where the pacts are '
            'kept. [[slnc 300]] Or look for a folder of pact files.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Many microservice teams, and Pact', 'Broker or PactFlow in their', 'pipelines.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In many '
            'microservice teams, using a pact broker, or the hosted '
            'service PactFlow, in their build pipelines.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Pact JVM 4.7.5.', '', 'JUnit 5.10.2.', '', 'Java 21.'],
        narration=(
            'For the record, here is what was used. [[slnc 300]] Pact for '
            'Java, version four point seven point five. [[slnc 300]] '
            'JUnit, version five point ten. [[slnc 300]] And Java '
            'twenty-one.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: real pact', "files, Pact's own mock, and a real", 'HTTP server for the provider.', '', 'The consumers and the catalog are', 'small, and made for the demo.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            "Everything is real: real pact files, Pact's own fake "
            'service, and a real web server for the catalog. [[slnc 300]] '
            'The consumers and the catalog are small, and made just for '
            'this demo.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['If provider and consumer are one', 'team with one release, an ordinary', 'test is enough. Pact pays off', 'across teams that release apart.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If the service and '
            'its consumer belong to one team, released together, an '
            'ordinary test is enough. [[slnc 400]] Pact pays off between '
            'teams that release separately.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a third consumer that reads the currency, and see its pact pass..'],
        narration=(
            "That's Consumer-Driven Contract, with Pact. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] '
            'Pact tells a service who a change will break before it '
            'ships, but it still cannot see a change of meaning. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Add a third '
            'consumer that reads the currency. [[slnc 300]] And check '
            'that its pact passes. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
