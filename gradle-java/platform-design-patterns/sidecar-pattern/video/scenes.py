"""Scene definitions for the Sidecar teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the analogy is spoken in full before any class
name, and the incident is told as a story in order rather than left to a table.
The slides illustrate the narration; they never carry it.

Every figure spoken aloud comes from the captured output of `./gradlew run`,
which is deterministic by construction: the gateway recovers at a fixed
millisecond, the clock is a counter rather than a timer, and nothing is random.
DemoRunsTest pins the exact strings, so a change to the program that moved a
number would fail the build rather than quietly make this video wrong.

The running order mirrors the project. Scenes 2 to 6 are the problem, and they
take their time on purpose: the audience has to believe that nobody was
careless before the pattern can look like anything other than bureaucracy.
Scene 6 is the incident itself, and it is the pivot -- the failure and the cause
land in different repositories. Scenes 7 to 10 are the pattern. Scenes 11 to 13
are the bill: a second process per service, a second thing that can be down, and
a millisecond on every call. Scene 14 is the admission that the structure is
Decorator, which this project owes the audience and most write-ups skip.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Sidecar",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Sidecar pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Some jobs every service must '
            "do, but they are not any service's real work. [[slnc 300]] "
            'The Sidecar pattern moves such a job into a small, separate '
            'program. [[slnc 300]] That program runs right beside the '
            'service, on the same machine. [[slnc 300]] The service talks '
            'to its neighbour, and the neighbour talks to the outside '
            'world. [[slnc 600]] Think of a busy restaurant kitchen. '
            '[[slnc 300]] The chefs cook, and someone has to answer the '
            'phone. [[slnc 300]] Teach every chef to answer it, and they '
            'all stop cooking, each with a different idea of the closing '
            'time. [[slnc 300]] Put one person on the phone beside the '
            'kitchen, and when the closing time changes, you tell just '
            'that one person. [[slnc 700]] In our online store, cards are '
            'charged in four places, through one payment provider. [[slnc '
            '300]] And one night, that provider has a bad three hundred '
            'milliseconds. [[slnc 500]] By the end, you will know how '
            'four correct services can cause an incident nobody can be '
            'blamed for. [[slnc 300]] What this pattern costs. [[slnc '
            '300]] And how it differs from the Decorator pattern.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online shop that charges a card in four places:",
            "",
            "    checkout               a customer is watching",
            "    refunds                the coffee maker came back",
            "    subscription-billing   two in the morning",
            "    marketplace-payouts    paying the sellers, Fridays",
            "",
            "Four teams. Four repositories. Four release days.",
            "",
            "One payment provider at the other end of all four.",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] The shop takes money in '
            'four places. [[slnc 500]] Checkout charges a card while a '
            'customer watches. [[slnc 300]] If it is slow, they notice. '
            '[[slnc 400]] Refunds gives money back when a product is '
            'returned. [[slnc 300]] Nobody is watching, but it must '
            'happen. [[slnc 400]] Subscription billing runs at two in the '
            'morning, against thousands of saved cards, unattended. '
            '[[slnc 400]] And marketplace payouts pays the independent '
            'sellers every Friday. [[slnc 300]] Large amounts, and the '
            'sellers notice at once if it fails. [[slnc 600]] Four teams. '
            '[[slnc 200]] Four separate code bases. [[slnc 200]] Four '
            'release days. [[slnc 300]] And one payment provider behind '
            'all four. [[slnc 500]] Remember that last part. [[slnc 300]] '
            'Four unrelated programs, all talking to the same supplier.'
        ),
    ),
    dict(
        key="03-copies",
        kind="console",
        title="Sixteen Copies of Four Decisions",
        body="""Act 1 - each of the four had to decide the same four things
        before it could go live.

    service               attempts  backoff  deadline     tls
    checkout                     6     10ms    2000ms  TLS1.3
    refunds                      6     10ms    2000ms  TLS1.3
    subscription-billing         6     10ms    2000ms  TLS1.3
    marketplace-payouts          6     10ms    2000ms  TLS1.3

  copies of a cross-cutting decision: 16
  places to edit to change one:       4

  Not one of the sixteen is about checkout, refunds,
  subscriptions or payouts. They would be identical
  if the shop sold bicycles.""",
        narration=(
            'None of the four teams wanted to become experts on the '
            "payment provider's network. [[slnc 300]] But each had to "
            'answer the same four questions before going live. [[slnc '
            '600]] First: how many times should a failed attempt be '
            'retried? [[slnc 300]] The provider sometimes declines '
            'everything for a fraction of a second, and then is fine. '
            '[[slnc 300]] So the right answer is to wait a moment, and '
            'try again. [[slnc 300]] But how many times, and how long? '
            '[[slnc 400]] Second: when do you give up altogether? [[slnc '
            '400]] Third: which security settings does the connection '
            'use? [[slnc 400]] And fourth: what do you count, and what do '
            'you call the counters? [[slnc 600]] Four questions, four '
            'services: sixteen answers. [[slnc 300]] And not one of them '
            'is about checkout, refunds, subscriptions, or payouts. '
            '[[slnc 300]] They are all facts about a network, and a '
            "supplier's contract. [[slnc 500]] Nobody copied carelessly. "
            '[[slnc 300]] But once four versions exist, nothing brings '
            'them back together.'
        ),
    ),
    dict(
        key="04-march",
        kind="console",
        title="March — The Change Lands Three Times",
        body="""Act 2 - the provider writes to every merchant: at most three
        attempts per payment, and wait properly between them.

    service               attempts  backoff  deadline     tls
    checkout                     3    200ms    2000ms  TLS1.3
    refunds                      3    200ms    2000ms  TLS1.3
    marketplace-payouts          3    200ms    2000ms  TLS1.3
    subscription-billing         6     10ms    2000ms  TLS1.3

  Three pull requests. Three reviews. Three releases.
  One afternoon. Everybody goes home.

  Nothing throws. Nothing is logged.
  Every test in all four services still passes.""",
        narration=(
            'First demo: in March, the change lands three times. [[slnc '
            '400]] The provider writes to all its customers. [[slnc 300]] '
            'Retrying ten milliseconds after a failure does not help. '
            '[[slnc 300]] So from now on: at most three attempts per '
            'payment, and wait properly between them. [[slnc 600]] The '
            "shop's engineer does the obvious thing. [[slnc 300]] Opens "
            'checkout, changes two lines, gets it reviewed, and releases '
            'it. [[slnc 300]] Then refunds. [[slnc 200]] Then marketplace '
            'payouts. [[slnc 300]] Three changes, one afternoon, and '
            'everyone goes home. [[slnc 600]] Three. [[slnc 300]] Not '
            'four. [[slnc 500]] Subscription billing was not updated. '
            '[[slnc 300]] And nobody was careless. [[slnc 300]] Billing '
            'runs overnight, lives in its own code base, and had no work '
            'planned that month. [[slnc 300]] So nobody opened it. [[slnc '
            '500]] And nothing warns you. [[slnc 300]] Every test in all '
            'four services still passes. [[slnc 300]] Including '
            "billing's, because billing's own copy agrees with itself."
        ),
    ),
    dict(
        key="05-absence",
        kind="code",
        title="The Incident Is an Absence, Not a Mistake",
        body="""// CheckoutService, RefundsService, MarketplacePayoutsService
public void applyPolicyReview() {
    maxAttempts = 3;
    firstBackoffMillis = 200;
}

// SubscriptionBillingService
//    ... there is no such method here. That is the whole fault.

// and the test that says so:
assertTrue(!methods.contains("applyPolicyReview"),
        "the point of this project is that nobody wrote this method here");""",
        narration=(
            'Here is what that looks like in the code. [[slnc 400]] Three '
            'of the four services have a method that applies the '
            "provider's new rules. [[slnc 300]] It sets three attempts, "
            'and a two-hundred-millisecond wait. [[slnc 600]] The fourth '
            'service simply does not have that method. [[slnc 300]] Not a '
            'wrong version. [[slnc 300]] Not an old version. [[slnc 300]] '
            'It is not there at all. [[slnc 600]] That matters. [[slnc '
            '300]] A wrong value could be spotted by comparing the four. '
            '[[slnc 300]] But an absence has nothing to compare. [[slnc '
            '300]] Nothing in any build knows the fourth file exists. '
            '[[slnc 600]] One test in this project checks that the method '
            'is missing. [[slnc 300]] The failure we are about to hear is '
            'not caused by bad code. [[slnc 300]] It is caused by code '
            'that was never written, in a place nobody looked.'
        ),
    ),
    dict(
        key="06-night",
        kind="console",
        title="Two In The Morning, Three Weeks Later",
        body="""Act 3 - the gateway has a bad 300ms. The contract allows the shop
        12 attempts across the whole account: 3 per payment, 4 services.
        The 13th is not declined. It is refused.

    subscription-billing  £12.99   6x, 310ms    pay_SUB-90118
    checkout              £47.99   3x, 600ms    pay_ORD-4417
    refunds               £22.50   3x, 600ms    pay_REF-3820
    marketplace-payouts   £186.40  —            NOT PAID
      429 refused — the account's 12-attempt allowance is spent

  What the gateway counted, from its own end:
    subscription-billing  6 attempts
    marketplace-payouts   1 attempt
    total                 13 of 12 allowed, 1 refused""",
        narration=(
            'Second demo: two in the morning, three weeks later. [[slnc '
            '400]] The provider has one of its wobbles. [[slnc 300]] For '
            'three hundred milliseconds it declines everything, and then '
            'it is fine. [[slnc 600]] Here is the detail that turns a '
            'stale copy into an incident. [[slnc 300]] During a wobble, '
            'the contract allows the shop twelve attempts in total. '
            '[[slnc 300]] Three per payment, for four services. [[slnc '
            '600]] Subscription billing is already running, so it hits '
            'the wobble first. [[slnc 300]] Using the old rules, it '
            'retries six times, quickly. [[slnc 300]] And on the sixth, '
            "it gets through. [[slnc 300]] It has spent six of the shop's "
            'twelve attempts. [[slnc 500]] Then checkout pays, using '
            'three attempts. [[slnc 300]] Then refunds, using three. '
            '[[slnc 300]] That makes twelve. [[slnc 500]] Marketplace '
            'payouts arrives fourth. [[slnc 300]] It makes one attempt, '
            'and is refused. [[slnc 300]] A hundred and eighty-six pounds '
            'forty does not reach the sellers. [[slnc 600]] Now put two '
            'facts together. [[slnc 300]] Subscription billing, the '
            'service with the old rules, the one that caused this, '
            'succeeded. [[slnc 300]] As far as its team will ever know, '
            'the night went perfectly. [[slnc 500]] And marketplace '
            'payouts, which is correct in every line, failed. [[slnc '
            '300]] Because it happened to arrive fourth.'
        ),
    ),
    dict(
        key="07-pattern",
        kind="quote",
        title="The Pattern",
        body=[
            "Move the cross-cutting concern out of the service",
            "and into a separate process running beside it",
            "on the same machine.",
            "",
            "The service talks to localhost and knows nothing else.",
            "The proxy is the only thing that leaves the machine.",
            "",
            "separate process · not a library, not a base class",
            "beside · same machine, one per service instance",
        ],
        narration=(
            'Here is the pattern, in one sentence. [[slnc 400]] Move the '
            'shared job out of the service, into a separate program '
            'running beside it, on the same machine. [[slnc 300]] The '
            'service only talks to its neighbour. [[slnc 300]] And the '
            'neighbour, called a proxy, is the only thing that goes out '
            'to the internet. [[slnc 600]] Two phrases matter. [[slnc '
            '500]] Separate program. [[slnc 300]] Not a library, and not '
            'a shared base class. [[slnc 400]] And beside. [[slnc 300]] '
            'Same machine, started and stopped together, one proxy per '
            'service. [[slnc 300]] Not one shared proxy somewhere on the '
            'network. [[slnc 600]] Why not just write a shared library? '
            '[[slnc 300]] Often, that is the right answer, and we come '
            'back to it at the end. [[slnc 300]] But a library does not '
            'fix this. [[slnc 300]] Changing the rules still means a new '
            'version, and four teams upgrading. [[slnc 300]] And the '
            'fourth team still has to open their code.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 300]] They are all small. "
            '[[slnc 600]] One interface, called takes payments. [[slnc '
            '300]] It asks for a name, and it pays a payment. [[slnc '
            '500]] Four classes implement it the old way. [[slnc 300]] '
            'Each carries its own settings, and its own retry loop. '
            '[[slnc 300]] Those are the sixteen copies, in code. [[slnc '
            '500]] A fifth version is almost empty. [[slnc 300]] Its pay '
            'method has one line: hand the payment to the proxy. [[slnc '
            '500]] The proxy is a class called sidecar. [[slnc 300]] It '
            'holds the retry loop the four services used to hold. [[slnc '
            '300]] But it does not own the numbers. [[slnc 300]] It reads '
            'them from one shared settings object. [[slnc 300]] All four '
            'proxies read the very same object. [[slnc 300]] Not four '
            'equal copies, which would be March all over again. [[slnc '
            '500]] And underneath sits a payment gateway that fails on '
            'purpose. [[slnc 300]] Every attempt count in this video is '
            'recorded by the gateway, at the receiving end. [[slnc 300]] '
            'Never by a service counting its own attempts. [[slnc 300]] '
            "Because a service's belief about how often it tried is "
            'exactly what was wrong.'
        ),
    ),
    dict(
        key="09-code",
        kind="code",
        title="What Is Left In The Service",
        body="""// the whole of ServiceBehindASidecar.pay
public Receipt pay(Payment payment) {
    return sidecar.send(payment);         // localhost, and nothing else
}

// and the proxy next door, holding what used to be in four places
private final SidecarConfig config;       // read, not owned

for (int attempt = 1; attempt <= config.maxAttempts(); attempt++) {
    clock.waitFor(HOP_MILLIS);            // the bill, one line
    ...
}""",
        narration=(
            'Here is the code that matters, in words. [[slnc 500]] The '
            "service's pay method is now one line long. [[slnc 300]] Hand "
            'the payment to the proxy, and return what comes back. [[slnc '
            '300]] No retry loop, no counter, no wait, no deadline. '
            '[[slnc 300]] They are not hidden elsewhere. [[slnc 300]] '
            'They are gone. [[slnc 600]] Next door, the proxy holds the '
            'loop that used to exist four times. [[slnc 300]] But it '
            'reads its numbers from the shared settings. [[slnc 300]] The '
            'proxy cannot change the rules. [[slnc 300]] It is given '
            'them. [[slnc 600]] And one more line, pointed out now so it '
            'is no surprise later. [[slnc 300]] Before each attempt, the '
            'proxy waits one millisecond. [[slnc 300]] That stands for '
            'the cost of hopping to the program next door, and back. '
            '[[slnc 300]] It is there on purpose, because showing only '
            'the benefits would be a sales pitch.'
        ),
    ),
    dict(
        key="10-repaired",
        kind="console",
        title="The Same Night, With A Proxy Beside Each Service",
        body="""Act 4 - the same wobble, the same 12-attempt allowance, the same
        four payments. The only difference is where the retry loop runs.

    subscription-billing  £12.99   3x, 603ms    pay_SUB-90118
    checkout              £47.99   3x, 603ms    pay_ORD-4417
    refunds               £22.50   3x, 603ms    pay_REF-3820
    marketplace-payouts   £186.40  3x, 603ms    pay_PAY-7741

    total                 12 of 12 allowed, 0 refused

  maxAttempts=3 firstBackoff=200ms deadline=2000ms tls=TLS1.3
  — read by all four proxies, from one object

  The policy was not applied four times and missed once.
  It was stated once.""",
        narration=(
            'Third demo: the same night, with a proxy beside each '
            'service. [[slnc 400]] Nothing about the world has improved. '
            '[[slnc 300]] The provider still has its bad three hundred '
            'milliseconds. [[slnc 300]] The contract still allows twelve '
            'attempts. [[slnc 600]] Subscription billing hands its '
            'payment to the proxy beside it. [[slnc 300]] The proxy makes '
            'three attempts. [[slnc 300]] It waits two hundred '
            'milliseconds, then four hundred. [[slnc 300]] On the third '
            'attempt, the wobble has passed, and the card is charged. '
            '[[slnc 300]] The service never knew there was more than one '
            'attempt. [[slnc 500]] Checkout, the same. [[slnc 300]] '
            'Refunds, the same. [[slnc 300]] And marketplace payouts, '
            'which failed last time, pays the sellers on its third '
            'attempt. [[slnc 300]] Twelve attempts, out of twelve '
            'allowed. [[slnc 300]] Nobody refused. [[slnc 600]] The rules '
            'were not applied four times, and missed once. [[slnc 300]] '
            'They were stated once. [[slnc 500]] We did not make four '
            'teams more careful. [[slnc 300]] We made it impossible for '
            'four copies to exist.'
        ),
    ),
    dict(
        key="11-bill-one",
        kind="console",
        title="The Bill, Part One — Twice As Many Things To Run",
        body="""Act 5 - read all three rows or none of them.

                                            before     after
  copies of a cross-cutting decision            16         4
  places to edit for one policy change           4         1
  processes to run and patch                     4         8

  Add a fifth service that takes payments:
    the old way   16 -> 20
    beside them    4 ->  4     (that method takes no argument)

  Network facts may move out. Shop facts may not.
  "Refunds are refused after ninety days" is not a proxy setting.""",
        narration=(
            'That is the pattern, and it works. [[slnc 300]] Now the '
            'bill, with three items. [[slnc 600]] Item one: counting. '
            '[[slnc 300]] Copies of the shared rules fall from sixteen to '
            'four. [[slnc 300]] Places to edit for one rule change fall '
            'from four to one. [[slnc 300]] That is why you would do '
            'this. [[slnc 500]] But programs to run and update rise from '
            'four to eight. [[slnc 300]] You have doubled them. [[slnc '
            '600]] Now add a fifth service that takes payments. [[slnc '
            '300]] The old way, copies go from sixteen to twenty. [[slnc '
            '300]] With sidecars, still four. [[slnc 600]] And one '
            'mistake to avoid. [[slnc 300]] Retry counts, deadlines, and '
            'security settings are facts about the network. [[slnc 300]] '
            'Whether a refund is allowed after ninety days is a fact '
            'about the shop. [[slnc 300]] If that business rule ends up '
            "in a proxy's settings file, someone will search the whole "
            'refunds service for it. [[slnc 300]] And it will not be '
            'there.'
        ),
    ),
    dict(
        key="12-bill-two",
        kind="console",
        title="The Bill, Part Two — A Second Thing That Can Be Down",
        body="""Act 6 - the gateway is fine. The network is fine. The service is
        fine. The proxy beside checkout failed to start after a patch.

    connection refused to localhost — no sidecar beside checkout

    attempts that reached the gateway: 0

  Zero. The request never left the machine, and the service has
  no retry code left to fall back on: we deleted it, on purpose.

  When a sidecar goes, it does not take one call with it.
  It takes every call that service makes.""",
        narration=(
            'Item two: a second thing that can be down. [[slnc 400]] The '
            'provider is fine. [[slnc 300]] The network is fine. [[slnc '
            '300]] The service is fine. [[slnc 300]] A customer is '
            'waiting to pay forty-seven pounds ninety-nine. [[slnc 500]] '
            'But the proxy beside checkout failed to start after an '
            'update. [[slnc 300]] The connection is refused. [[slnc 600]] '
            'Attempts that reached the payment provider: zero. [[slnc '
            '300]] Not one attempt left the machine. [[slnc 300]] And the '
            'service cannot fall back, because we deleted its retry code '
            'on purpose. [[slnc 600]] So be honest about what happened. '
            '[[slnc 300]] To make every call more reliable, you added a '
            'new dependency to every call. [[slnc 500]] That is usually '
            'worth it. [[slnc 300]] A proxy on the same machine, doing '
            'one small job, fails far less often than the internet. '
            '[[slnc 500]] But the failure has a different shape. [[slnc '
            '300]] When the internet wobbles, one call fails, and the '
            'next may work. [[slnc 300]] When a sidecar dies, every call '
            'that service makes fails, until someone restarts it. [[slnc '
            '300]] Rarer, but wider.'
        ),
    ),
    dict(
        key="13-bill-three",
        kind="console",
        title="The Bill, Part Three — One Millisecond, On Every Call",
        body="""Act 7 - the same payment, the same policy, the same wobble.

    retry code inside the service      3 attempts, 600ms
    retry code in a proxy next door    3 attempts, 603ms

  3 milliseconds, which is 1ms per attempt for crossing to a
  neighbouring process and back.

  On a 600ms payment          nothing
  On a 2ms internal call      fifty per cent
  And every hop is paid twice: leaving one, entering the next.

  That is the arithmetic that decides whether a service mesh
  belongs in your system. Arithmetic, not taste.""",
        narration=(
            'Item three: the smallest number in this video. [[slnc 500]] '
            'The same payment, the same rules, the same wobble, measured '
            'twice. [[slnc 300]] With the retry code inside the service: '
            'three attempts, six hundred milliseconds. [[slnc 300]] With '
            'the retry code in the proxy next door: three attempts, six '
            'hundred and three. [[slnc 500]] Three milliseconds. [[slnc '
            '300]] One per attempt, for the hop next door, and back. '
            '[[slnc 600]] On a payment that takes six hundred '
            'milliseconds, you would never notice. [[slnc 500]] But on an '
            "internal call between two of the shop's own services, taking "
            'two milliseconds, one extra millisecond is a fifty percent '
            'increase. [[slnc 300]] And if every service talks through a '
            'proxy, every hop is paid twice: once leaving, once arriving. '
            '[[slnc 600]] So ask two questions about your system. [[slnc '
            '300]] How long does a typical call take? [[slnc 300]] And '
            'how many hops does it make? [[slnc 300]] Six hundred '
            'milliseconds and one hop, and this pattern is free. [[slnc '
            '300]] Two milliseconds and six hops, and it is not.'
        ),
    ),
    dict(
        key="14-decorator",
        kind="quote",
        title="The Admission — This Is Decorator, Until You Deploy It",
        body=[
            "An object wrapping another object is Decorator.",
            "In one program, that is exactly what Sidecar is.",
            "",
            "What differs is not the code. It is where the code runs.",
            "",
            "Does this concern have to change without a rebuild?",
            "Must it work for a language your library does not support?",
            "",
            "Yes to either → next door.",
            "No to both → a library in your own process is cheaper.",
        ],
        narration=(
            'Now an honest admission. [[slnc 400]] Everything in this '
            'video ran inside one Java program. [[slnc 300]] And in one '
            'program, a proxy wrapped around a service is just one object '
            'wrapping another. [[slnc 300]] That is the Decorator '
            'pattern. [[slnc 600]] So what makes Sidecar different? '
            '[[slnc 300]] Not the code. [[slnc 300]] Where the code runs. '
            '[[slnc 500]] A decorator is built into your program, written '
            'in your language. [[slnc 300]] It changes when your service '
            'is rebuilt. [[slnc 500]] A sidecar is its own program. '
            '[[slnc 300]] It may be written in a language nobody on your '
            'team knows. [[slnc 300]] It changes when someone restarts '
            'it, without your service ever being opened. [[slnc 600]] '
            'That difference bought the one-place rule change. [[slnc '
            '300]] And it also cost the extra program, the extra failure, '
            'and the extra millisecond. [[slnc 600]] So ask two '
            'questions. [[slnc 300]] Must this job change without '
            'rebuilding the service? [[slnc 300]] Must it work for '
            'services written in languages your library cannot support? '
            '[[slnc 500]] Yes to either, and it goes next door. [[slnc '
            '300]] No to both, and a shared library inside your program '
            'is cheaper, faster, and one less thing to fail.'
        ),
    ),
    dict(
        key="15-takeaway",
        kind="bullets",
        title="What to Take Away",
        body=[
            "Count the copies, not the services.",
            "Four services holding four decisions each is sixteen things.",
            "",
            "The failure lands where the cause is not.",
            "The service with the stale copy succeeded, and stayed green.",
            "",
            "You have met this already, and did not call it a pattern.",
            "The log shipper. The metrics agent. The nginx in front of your app.",
            "",
            "It is where the code runs, not what the code is.",
            "And no test inside any one service will ever tell you otherwise.",
        ],
        narration=(
            'Here are four things to remember. [[slnc 500]] One. [[slnc '
            '200]] Count the copies, not the services. [[slnc 300]] Four '
            'services, each holding four decisions, is sixteen things '
            'that can drift apart. [[slnc 300]] If your biggest supplier '
            'changed its rules tomorrow, could you name every file you '
            'would need to open? [[slnc 500]] Two. [[slnc 200]] The '
            'failure lands away from the cause. [[slnc 300]] The service '
            'that misbehaved stayed healthy all night. [[slnc 300]] The '
            'one that failed was correct in every line. [[slnc 500]] '
            'Three. [[slnc 200]] You have met this pattern before, maybe '
            'without the name. [[slnc 300]] A log shipper beside your '
            'application. [[slnc 300]] A metrics agent on every machine. '
            '[[slnc 300]] A web server handling encryption in front of '
            'your app. [[slnc 300]] Each exists because the job is not '
            "your service's work, but it is everybody's problem. [[slnc "
            '500]] Four. [[slnc 200]] What separates this from Decorator '
            'is where the code runs, not what it is. [[slnc 600]] And one '
            'warning. [[slnc 300]] No test inside any one service will '
            'ever notice the four have drifted apart. [[slnc 300]] '
            'Because from inside each one, each one is right.'
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, 59 tests, diagrams and an interactive animation",
            "are in the repository — including all three costs.",
            "",
            "Run it yourself:  ./gradlew run",
        ],
        narration=(
            "That's the Sidecar pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Put the job that is '
            "nobody's real work into a program beside the service, so it "
            'can change without opening the service, and pay for it with '
            'an extra program, an extra thing that can fail, and a little '
            'delay on every call. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 300]] It runs offline, with '
            'nothing installed except a Java development kit. [[slnc '
            '500]] Here is one exercise to try. [[slnc 300]] Stop the '
            'proxy beside checkout yourself. [[slnc 300]] And hear every '
            'one of its calls fail at once. [[slnc 500]] If this helped, '
            'a like really does help other people find it. [[slnc 300]] '
            "And subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
