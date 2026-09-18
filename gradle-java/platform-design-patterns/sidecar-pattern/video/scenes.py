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
            "Hello, and welcome. This video explains the Sidecar design pattern "
            "in Java, and it is written and presented by Jayasekhar Konduru. "
            "[[slnc 165]] Here is the simple definition. The Sidecar pattern "
            "means taking a job that every service has to do, but that is not "
            "any service's real work, and moving it into a small separate "
            "program that runs right beside the service on the same machine. "
            "The service talks to its neighbour, and the neighbour talks to the "
            "outside world. [[slnc 193]] Think of a busy restaurant kitchen. "
            "The chefs cook, and somebody has to answer the telephone. Teach "
            "every chef to do it, and every chef stops cooking when the phone "
            "rings, each with a slightly different idea of the closing time. "
            "Put one person on the phone beside the kitchen, and when the "
            "closing time changes you tell that one person. [[slnc 165]] And "
            "notice what it is not: not a call centre in another building. Same "
            "room, same shift, one per kitchen. [[slnc 193]] The rest of the "
            "video does this properly, by building a working Java project: an "
            "online shop that charges cards in four places, one payment "
            "provider behind all four, and a night when that provider had a bad "
            "three hundred milliseconds. [[slnc 150]] By the end you'll know "
            "why four correct services can produce an incident nobody can be "
            "blamed for, what this pattern charges you in exchange, and the "
            "honest answer to the objection that it is just a decorator."
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
            "So, imagine an online shop, and imagine it takes money in four "
            "different places. [[slnc 165]] Checkout charges a card while a "
            "customer sits watching a spinner. If it is slow, they notice. "
            "[[slnc 150]] Refunds gives money back when the copper coffee maker "
            "comes back in the post. Nobody is watching that one. It can take a "
            "minute, but it absolutely must happen. [[slnc 150]] Subscription "
            "billing runs at two in the morning against thousands of saved "
            "cards, alone, in the dark, unattended. [[slnc 150]] And "
            "marketplace payouts pays the independent sellers every Friday. "
            "Large amounts, and they notice immediately if it does not happen. "
            "[[slnc 193]] Four teams. Four repositories. Four release days. And "
            "one payment provider at the other end of all four of them. [[slnc "
            "165]] Hold on to that last part, because everything here comes out "
            "of it: four pieces of software with nothing to do with each other, "
            "all talking to the same supplier."
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
            "Now, none of those four teams wanted to become an expert on a "
            "payment provider's network behaviour. But every one of them had to "
            "answer the same four questions before going live, because the "
            "provider is across the internet, and the internet is not reliable. "
            "[[slnc 193]] How many times should a failed attempt be retried? "
            "The provider wobbles: every few days it declines everything for a "
            "fraction of a second, then is fine again. Nothing is broken and "
            "nobody needs paging, so the right answer is to wait a moment and "
            "ask again. But how many moments, and how long? [[slnc 165]] When "
            "do you give up altogether? A customer will not wait forever. "
            "[[slnc 165]] Which transport security profile do you present? "
            "[[slnc 165]] And what do you count, and what do you call the "
            "counters? [[slnc 220]] Four questions, four services, sixteen "
            "answers. And here is the important part: not one of those sixteen "
            "has anything to do with checkout, or refunds, or subscriptions, or "
            "payouts. They are all facts about a network and a supplier's "
            "contract. They would be identical if the shop sold bicycles. "
            "[[slnc 193]] And nobody copied dishonestly: two competent people "
            "reading the same documentation write almost the same twenty lines. "
            "But once four versions exist, nothing will bring them back "
            "together."
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
            "In March, the provider writes to all its merchants. Retrying ten "
            "milliseconds after a failure does not help anybody, it says. The "
            "failure has not had time to clear, and all you have done is spend "
            "capacity the provider then has to ration. So from now on: at most "
            "three attempts per payment, and wait properly between them. [[slnc "
            "193]] The shop's platform engineer does the obvious thing. Opens "
            "checkout, changes two lines, gets it reviewed, ships it. Then "
            "refunds. Then marketplace payouts. Three pull requests, three "
            "releases, one afternoon, and everybody goes home. [[slnc 220]] "
            "Three. Not four. [[slnc 193]] Subscription billing was not "
            "updated. And the whole pattern depends on you believing this next "
            "sentence: nobody was careless, and nobody was even wrong. [[slnc "
            "165]] Subscription billing runs overnight, so nobody was looking "
            "at it that week. It lives in its own repository, and it had no "
            "open work that sprint, so nobody opened it at all. [[slnc 193]] "
            "There was no fourth place to look unless you already knew there "
            "was a fourth place to look. [[slnc 193]] And nothing tells you. "
            "Every test in all four services still passes — including "
            "billing's, because billing tests its own copy, and its own copy is "
            "perfectly consistent with itself. A test can only check the code "
            "it can see."
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
            "Let me show you what that looks like in the code, because it is "
            "not what people expect. [[slnc 165]] Three of the four services "
            "have a method that applies the provider's review. It sets the "
            "attempts to three and the wait to two hundred milliseconds. The "
            "same two lines in all three. [[slnc 193]] The fourth service does "
            "not have that method. Not a wrong version of it. Not an old "
            "version. It simply is not there. [[slnc 220]] That distinction "
            "matters more than it sounds. If the fourth service held a wrong "
            "value, you could imagine a tool that compares the four and "
            "complains. An absence has nothing to compare. Nothing in any build "
            "or any pipeline knows that a fourth file exists. [[slnc 193]] This "
            "project has a test that asserts the method is missing, which is a "
            "strange thing to assert. It pins the lesson. The failure we are "
            "about to watch is not caused by bad code. It is caused by code "
            "that was never written, in a place nobody was looking."
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
            "Three weeks later, at two in the morning, the provider has one of "
            "its wobbles. Three hundred milliseconds of declining everything, "
            "then it is fine again. [[slnc 193]] And here is the detail that "
            "turns a stale copy into an incident. The contract allows the shop "
            "twelve attempts across the whole merchant account during an event "
            "like this — three per payment, four services, twelve. [[slnc 220]] "
            "Subscription billing is already running, because it always is at "
            "that hour, so it hits the wobble first. On the old policy it "
            "retries six times, quickly, and on the sixth it gets through. Six "
            "of the shop's twelve attempts, spent before checkout had finished "
            "its first payment. [[slnc 165]] Then checkout pays, on three "
            "attempts. Then refunds, on three. That is twelve. [[slnc 193]] "
            "Marketplace payouts arrives fourth. It makes one attempt, and the "
            "answer is not a decline — it is a refusal. A hundred and "
            "eighty-six pounds forty does not reach the sellers. [[slnc 220]] "
            "Now read two facts together, because this is the lesson of the "
            "video. Subscription billing — the service with the stale copy, the "
            "service that caused all of this — succeeded. It got its money. As "
            "far as the billing team will ever know, that night went perfectly. "
            "[[slnc 193]] And marketplace payouts, whose every line is correct, "
            "which was updated in March, failed, because it happened to arrive "
            "fourth."
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
            "So here is the pattern, in one sentence. Move the cross-cutting "
            "concern out of the service and into a separate process that runs "
            "beside it on the same machine. The service talks to its neighbour "
            "on the local machine and knows nothing else. The neighbour is the "
            "only thing that goes out to the internet. [[slnc 220]] Two phrases "
            "are carrying that sentence, and each rules out a near miss. [[slnc "
            "193]] Separate process. Not a library, not a base class, not a "
            "framework you extend. And beside. Same machine, same lifecycle, "
            "one proxy per service instance. Not a shared proxy somewhere on "
            "the network that everything routes through; that is a different "
            "pattern with different failure modes. [[slnc 193]] Now, the "
            "sceptical question is: why not write a shared library? Often that "
            "is the right answer, and we come back to it at the end. But hold "
            "on to what it does not fix. Updating the policy means publishing a "
            "new version and getting four teams to upgrade — the same problem "
            "with an extra step, because the fourth team still has to open "
            "their repository."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="Who Does What",
        body=None,
        narration=(
            "Let me name the pieces; they are all small. [[slnc 165]] One "
            "interface, called takes payments, asks two things: what is your "
            "name, and here is a payment, please pay it. [[slnc 165]] [[slnc "
            "193]] Four classes implement it the old way, each carrying its own "
            "four fields and its own retry loop — the sixteen copies, in code. "
            "[[slnc 193]] Then there is a fifth implementation, and it is "
            "almost empty. Its pay method is one line: hand the payment to the "
            "proxy. [[slnc 193]] The proxy is a class called sidecar. It holds "
            "the retry loop the four services used to hold, but it does not "
            "hold the numbers — it reads them from a configuration object. And "
            "here is the part worth hearing twice: all four proxies read the "
            "same configuration object. Not four equal copies. The same one. "
            "The test checks that with an identity assertion, not an equality "
            "one, because four equal copies would be March all over again with "
            "better manners. [[slnc 193]] Underneath sits the payment gateway, "
            "forty lines that fail on purpose, and it owns the call log. Every "
            "attempt count you hear in this video is recorded by the gateway, "
            "at the receiving end — never by a service counting its own "
            "attempts. That is the incident in one sentence: a service's belief "
            "about how many times it tried is exactly the thing that was wrong."
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
            "This is the one piece of code worth reading closely, and I will "
            "describe it rather than spell out syntax. [[slnc 165]] The pay "
            "method on the service is now one line long. Take the payment, hand "
            "it to the proxy, return what comes back. No retry loop, no attempt "
            "counter, no wait, no certificate, no deadline. They are not hidden "
            "elsewhere in the class. They are gone. [[slnc 220]] Next door, the "
            "proxy holds the loop that used to exist four times. But look at "
            "where its numbers come from. It has a field holding a "
            "configuration object, and the comment on that field says read, not "
            "owned. The proxy cannot change the policy; it is given the policy. "
            "[[slnc 193]] And there is one more line in that loop I want to "
            "point at now, so it is not a surprise later. Before every attempt, "
            "the proxy waits one millisecond. That is the hop: the cost of "
            "leaving your process, arriving next door, and coming back. It is "
            "in the source deliberately, because a pattern that only shows you "
            "its benefits is a sales pitch."
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
            "So let's run the same night again, with a proxy standing beside "
            "each of the four services. [[slnc 165]] Nothing about the world "
            "has improved. The gateway still has its bad three hundred "
            "milliseconds. The contract still allows twelve attempts. [[slnc "
            "193]] Subscription billing sends its payment to the proxy beside "
            "it. The proxy makes three attempts, waiting two hundred "
            "milliseconds and then four hundred, and on the third the wobble "
            "has passed and the card is charged. The service never knew there "
            "was more than one attempt. [[slnc 165]] Checkout, the same. "
            "Refunds, the same. And marketplace payouts — which failed "
            "completely last time — pays the sellers on its third attempt, like "
            "everybody else. Twelve attempts of twelve allowed, nobody refused. "
            "[[slnc 220]] Here is the sentence to take from this scene. The "
            "policy was not applied four times and missed once. It was stated "
            "once. [[slnc 193]] We did not make four teams more disciplined. We "
            "removed the possibility of four copies disagreeing, by making it "
            "impossible for there to be four."
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
            "Right — that is the pattern, and it works. Now the bill. There are "
            "three items on it, and all three are the price of the pattern, not "
            "mistakes made while applying it. [[slnc 193]] Item one is a table "
            "with three rows: read all three or none. [[slnc 165]] The copies "
            "of a cross-cutting decision fall from sixteen to four. The places "
            "you have to edit to change one policy fall from four to one. Those "
            "two rows are why you would do this. [[slnc 193]] The third row is "
            "why it is not free. The number of processes to run and patch goes "
            "from four to eight. You have doubled it. [[slnc 220]] But notice "
            "which row scales. Add a fifth service that takes payments, and the "
            "copies go from sixteen to twenty the old way. Beside the services, "
            "it is still four. [[slnc 193]] One more thing belongs here, and it "
            "is the mistake I would most like you to avoid. Retry counts, "
            "deadlines, certificates and counters are facts about the network. "
            "Whether a refund is allowed after ninety days is a fact about the "
            "shop. [[slnc 165]] The day that rule lives in a proxy's "
            "configuration file, somebody will read the whole refunds service "
            "looking for it, and it will not be there. Nothing will throw. They "
            "simply will not find it."
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
            "Item two. A healthy gateway, a healthy network, a healthy service, "
            "and a forty-seven pound ninety-nine coffee maker waiting to be "
            "paid for. But the proxy beside checkout failed to start after a "
            "patch. [[slnc 193]] Connection refused. [[slnc 165]] Now look at "
            "the number underneath, because that is the one that matters. "
            "Attempts that reached the gateway: zero. [[slnc 193]] Not one "
            "attempt left the machine, and the service cannot fall back on "
            "anything: we deleted its retry code on purpose two scenes ago. "
            "[[slnc 220]] So be honest about what happened here. You added a "
            "dependency to every call your service makes, in order to make "
            "those calls more reliable. [[slnc 193]] That trade is usually "
            "worth taking: a proxy on the same machine, doing one narrow job, "
            "fails far less often than the internet does. [[slnc 193]] But the "
            "shape of the failure is different from the one you replaced. When "
            "the internet has a bad moment, one call fails and the next one "
            "might not. When a sidecar goes, it takes every call that service "
            "makes, until somebody restarts it. Rarer, and wider."
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
            "Item three: the smallest number in this video, and the one most "
            "worth understanding. [[slnc 165]] The same payment, the same "
            "policy, the same wobble, measured twice. With the retry code "
            "inside the service: three attempts, six hundred milliseconds. With "
            "the retry code in a proxy next door: three attempts, six hundred "
            "and three. [[slnc 193]] Three milliseconds. One millisecond per "
            "attempt, for crossing into the process next door and coming back. "
            "[[slnc 220]] On a payment that already takes six hundred "
            "milliseconds, that is nothing. You would never measure it. [[slnc "
            "193]] But run the same arithmetic on an internal call between two "
            "of the shop's own services — the kind that takes two milliseconds "
            "— and one millisecond each way is a fifty per cent increase. "
            "[[slnc 193]] And it is worse, because where every service talks "
            "through a proxy, every hop is paid twice: once leaving the first, "
            "once entering the second. [[slnc 220]] That is the arithmetic that "
            "decides whether a service mesh belongs in your system. How long "
            "does your average call take, and how many hops does it make? Six "
            "hundred milliseconds and one hop, and this pattern is free. Two "
            "milliseconds and six hops, and it is not."
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
            "And now the admission this project owes you, which you may already "
            "have been waiting for. [[slnc 193]] Everything in this video "
            "happened inside one Java program. And in one program, a proxy that "
            "a service talks through is an object wrapping another object — "
            "which is the Decorator pattern, from earlier in this course. "
            "[[slnc 165]] The code is not new. So what makes this a different "
            "pattern? Not the code. Where the code runs. [[slnc 193]] A "
            "decorator is compiled into your jar, written in your language, and "
            "it changes when your service is rebuilt. [[slnc 165]] A sidecar is "
            "its own process. It may be written in a language nobody on your "
            "team knows. It changes when somebody restarts it, and your service "
            "is never opened. [[slnc 193]] That difference bought us the "
            "one-line policy change, and it is exactly what charged us the "
            "extra process, the extra failure and the extra millisecond. [[slnc "
            "220]] Which gives you the two questions that decide it. Does this "
            "concern need to change without rebuilding the service? Does it "
            "have to work for a service written in a language your library "
            "cannot support? [[slnc 193]] Yes to either, and it goes next door. "
            "No to both, and a shared library in your own process is cheaper, "
            "faster, and has one fewer thing that can fail."
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
            "Four things to take away. [[slnc 165]] First, count the copies, "
            "not the services. Four services each holding four decisions is "
            "sixteen things that can drift. Try it on your own system: if your "
            "biggest supplier wrote to you tomorrow, could you name every file "
            "you would have to open? [[slnc 193]] Second, the failure lands "
            "where the cause is not. The service that misbehaved stayed green "
            "all night. The service that failed was correct in every line. If "
            "you ever spend a day and a half reading a faultless service, this "
            "is the thing to suspect. [[slnc 193]] Third, you have met this "
            "pattern already and probably did not call it one. A log shipper "
            "beside your application. A metrics agent on every machine. A web "
            "server terminating encryption in front of your app. Every one of "
            "those exists for the same reason: it is not your service's job, "
            "and it is everybody's problem. [[slnc 193]] And fourth, the "
            "sentence that separates this from Decorator: it is where the code "
            "runs, not what the code is. [[slnc 165]] One warning. Everything "
            "on this list can be got wrong without anything failing. No test "
            "inside any one service will ever notice the four of them have "
            "drifted apart — because from inside each one, each one is right."
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
            "And that is the Sidecar pattern. Put the concern that is nobody's "
            "real work into a process that runs beside the service, so it can "
            "be changed without opening the service at all — and pay for that "
            "with an extra process, an extra thing that can be down, and a "
            "millisecond on every call. [[slnc 193]] The whole project is in "
            "the repository: the source, fifty-nine tests, the diagrams, and an "
            "animation that plays the night out both ways. All three costs are "
            "running code too, so you can stop the proxy yourself and watch "
            "every call fail at once. [[slnc 165]] If this was useful, please "
            "like the video and subscribe. Thanks very much for watching, and "
            "I'll see you in the next one."
        ),
    ),
]
