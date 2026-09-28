"""Scene definitions for the Client-Side Load Balancing teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)

The narration is written to stand on its own. A large share of the audience
listens rather than watches -- on a phone, in a pocket, on a commute -- so no
sentence points at the screen, the analogy is spoken in full before any class
name, and the code slides are described in words rather than read out as
syntax. The slides illustrate the narration; they never carry it.

Every number quoted in these scenes comes from the real output of
`./gradlew run`: 12/0/0 at 120ms, 4/4/4 at 320ms, 10/1/1 at 170ms, and
2/2/0 for the two-client act.

Layout limit: on "bullets" and "quote" slides the body starts at y=260 and
steps 60 pixels a line, and the footer sits at y~1022, so twelve body lines
is the maximum.
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Load Balancing",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'client-side Load Balancing pattern, in Java. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] When a service runs '
            'as several identical copies, something must decide which '
            'copy each request goes to. [[slnc 300]] Client-side load '
            'balancing means the caller makes that decision itself, '
            'fresh, on every request. [[slnc 300]] And because the rule '
            'is kept in one replaceable place, it can be swapped without '
            'touching anything else. [[slnc 600]] Think of a row of '
            'supermarket tills. [[slnc 300]] You look along the row, pick '
            'the shortest queue, and join it. [[slnc 700]] In our online '
            'store, the catalog service runs as three copies. [[slnc '
            '300]] And one of them is on older, slower hardware. [[slnc '
            '500]] By the end, you will know why sending every request to '
            'the first copy works, and still has to go. [[slnc 300]] Why '
            'taking fair turns is not the same as being quick. [[slnc '
            '300]] And two ways this pattern goes wrong, even when every '
            'caller behaves perfectly.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The shop's Catalog service is busy.",
            "So it runs as three copies of the same program:",
            "",
            "    catalog-1      answers in 10ms",
            "    catalog-2      answers in 10ms",
            "    catalog-3      answers in 60ms",
            "",
            "Any of the three can answer any question.",
            "All three give the same answer.",
            "",
            "The checkout needs a product name.",
            "Which of the three does it ask?",
        ],
        narration=(
            "Here is the scenario. [[slnc 400]] The shop's catalog "
            'service knows what each product is called, and what it '
            'costs. [[slnc 300]] It is busy, so it runs as three copies '
            'of the same program, on three machines. [[slnc 600]] Two of '
            'those machines answer in about ten milliseconds. [[slnc '
            '300]] The third takes sixty, because it is older hardware. '
            '[[slnc 300]] Nothing is broken. [[slnc 300]] One machine is '
            'simply slower, which is true of almost every real system. '
            '[[slnc 600]] The three copies are interchangeable. [[slnc '
            '300]] Ask any of them for a product name, and you get the '
            'same answer. [[slnc 500]] And that creates the problem. '
            '[[slnc 300]] When every copy gives the same answer, there is '
            'no right one to pick. [[slnc 300]] But something still has '
            'to pick. [[slnc 300]] So which copy does checkout ask?'
        ),
    ),
    dict(
        key="03-naive",
        kind="code",
        title="The Obvious Answer — Take The First One",
        body="""public final class FirstInstanceBalancer implements LoadBalancer {

    @Override
    public ServiceInstance choose(List<ServiceInstance> candidates) {
        return candidates.get(0);   // there it is
    }
}

// no bug, no slowness, no failing test, nothing to notice""",
        narration=(
            'The obvious answer is: take the first one on the list. '
            '[[slnc 300]] Almost nobody chooses this on purpose. [[slnc '
            '500]] You ask which copies are available, you get a list, '
            'and you use the first. [[slnc 300]] In the project, the '
            'whole rule is one line: return the first one. [[slnc 600]] '
            'There is no bug in that line. [[slnc 300]] It always returns '
            'the correct product name. [[slnc 300]] It is not slow. '
            '[[slnc 300]] And every test written against it passes. '
            '[[slnc 600]] So keep this in mind. [[slnc 300]] What goes '
            'wrong here is not a mistake. [[slnc 300]] It is a decision '
            'nobody realised they were making.'
        ),
    ),
    dict(
        key="04-first",
        kind="console",
        title="Twelve Requests, One Machine",
        body="""$ ./gradlew run

1. Always the first on the list
    catalog-1   12 requests (100%)   10ms each
    catalog-2    0 requests ( 0%)   10ms each
    catalog-3    0 requests ( 0%)   60ms each
  12 requests took 120ms in total

  it is not slow -- catalog-1 happens to be a fast box. It is
  wasteful: the shop is paying for three instances and using one,
  and when catalog-1 falls over it takes every request with it.""",
        narration=(
            'First demo: twelve requests, always to the first copy. '
            '[[slnc 400]] Catalog one gets all twelve requests. [[slnc '
            '300]] Catalog two gets none. [[slnc 300]] Catalog three gets '
            'none. [[slnc 600]] And the twelve requests took a hundred '
            'and twenty milliseconds in total. [[slnc 300]] That will '
            'turn out to be the fastest result in this whole video. '
            '[[slnc 600]] Nothing failed. [[slnc 300]] Nothing was slow. '
            '[[slnc 300]] Every answer was correct. [[slnc 600]] The '
            'costs are all outside the program, which is why nobody '
            'notices them. [[slnc 300]] Two machines are paid for, and do '
            'nothing. [[slnc 300]] The spare capacity the shop thinks it '
            'bought does not exist. [[slnc 300]] And when catalog one '
            'falls over, everything falls over. [[slnc 300]] While two '
            'healthy machines sit idle.'
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Really Hurts",
        body=[
            "It is not slow. It is not wrong. Tests pass.",
            "",
            "  paying for three machines, using one",
            "  the headroom you bought does not exist",
            "  catalog-1 dies, and the whole shop dies",
            "  a rolling restart hits 100% of traffic",
            "",
            "And in a test environment there is one instance,",
            "so take-the-first and take-turns look identical.",
            "",
            "A concentration problem does not announce",
            "itself with a failing test.",
        ],
        narration=(
            "Let's be clear about the damage. [[slnc 500]] First, money. "
            '[[slnc 300]] Three machines are on the bill, and one does '
            'the work. [[slnc 500]] Second, the safety is imaginary. '
            '[[slnc 300]] The shop believes it can survive losing a '
            'machine. [[slnc 300]] But it cannot survive losing catalog '
            'one. [[slnc 500]] Third, the damage when it fails. [[slnc '
            '300]] When the busy machine goes down, every request goes '
            'down with it. [[slnc 300]] An ordinary release, restarting '
            'machines one by one, becomes a full outage. [[slnc 600]] And '
            'here is why it survives code review for years. [[slnc 300]] '
            'In a test environment, there is usually only one copy of '
            'everything. [[slnc 300]] With one copy, taking the first and '
            'taking turns behave exactly the same. [[slnc 600]] So '
            'remember this. [[slnc 300]] A problem like this never shows '
            'up as a failing test. [[slnc 300]] It shows up on the night '
            'one machine dies.'
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Load Balancing Pattern",
        body=[
            "A client with several interchangeable instances to",
            "choose from delegates the choice to a replaceable",
            "policy, and remakes that choice on every request.",
            "",
            "— the pattern as usually stated",
            "",
            "In plain words: don't take the first one.",
            "Put the choosing somewhere you can change it.",
            "And then be honest about what one caller",
            "can and cannot see.",
        ],
        narration=(
            'Here is the pattern, as it is usually stated. [[slnc 400]] A '
            'caller with several interchangeable copies to choose from '
            'hands the choice to a replaceable rule. [[slnc 300]] And it '
            'makes that choice again, on every request. [[slnc 500]] In '
            'plain words: do not just take the first one. [[slnc 300]] '
            'Put the choosing somewhere you can change it. [[slnc 600]] '
            'Two words in that do real work. [[slnc 500]] The first is '
            'replaceable. [[slnc 300]] The rule for picking becomes its '
            'own object. [[slnc 300]] So you can swap one rule for '
            'another without editing the code that makes the request. '
            '[[slnc 500]] The second is every request. [[slnc 300]] It is '
            'not a setting read at startup. [[slnc 300]] It is a decision '
            'made again each time, so it can react to a machine that got '
            'slow five seconds ago. [[slnc 600]] And there is a third '
            'part, which most descriptions leave out. [[slnc 300]] Be '
            'honest about what one caller can see. [[slnc 300]] Later, '
            'every caller will choose well on its own, and together they '
            'will still get it wrong.'
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="An Analogy",
        body=[
            "A row of supermarket tills.",
            "",
            "Six tills open. Nobody is directing anybody.",
            "You look along the row, pick the shortest queue,",
            "and join it.",
            "",
            "  you chose — no member of staff assigned you",
            "  you chose on what you could see",
            "  you will choose again next week",
            "",
            "Now the other shop: one member of staff",
            "standing at the head of all six queues.",
        ],
        narration=(
            'Here is the everyday version. [[slnc 400]] You are in a '
            'supermarket, with six tills open. [[slnc 300]] Nobody '
            'directs anybody. [[slnc 300]] You look along the row, pick '
            'the shortest queue, and join it. [[slnc 600]] Three things '
            'just happened, and all three are the pattern. [[slnc 500]] '
            'You chose. [[slnc 300]] No member of staff assigned you a '
            'till. [[slnc 500]] You chose using what you could see: the '
            'length of each queue. [[slnc 300]] Not which cashier is '
            'fastest, or who has a trolley full of shopping. [[slnc 300]] '
            'Your information was partial, but better than nothing. '
            '[[slnc 500]] And next week, you will choose again, from '
            'scratch. [[slnc 600]] Now picture another supermarket. '
            '[[slnc 300]] One member of staff stands at the front of all '
            'six queues, and tells each shopper where to go. [[slnc 300]] '
            'Remember that person. [[slnc 300]] They come back at the end '
            'of this video, and they win an argument.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 500]] First, the caller, "
            'called the catalog client. [[slnc 300]] It asks which copies '
            'are available. [[slnc 300]] It hands that list to its '
            'balancer. [[slnc 300]] It calls whichever copy comes back. '
            '[[slnc 300]] Then it reports how long that took. [[slnc '
            '300]] That is all. [[slnc 300]] It contains no rule for '
            'picking. [[slnc 600]] Second, the load balancer itself. '
            '[[slnc 300]] You give it a list of copies, and it gives you '
            'back one of them. [[slnc 300]] There are four different '
            'versions of it. [[slnc 500]] If that sounds familiar, it is '
            'the Strategy pattern. [[slnc 300]] Interchangeable rules, '
            'and a caller that never asks which one it holds. [[slnc '
            '500]] The balancer also has a way to be told how long each '
            'call took. [[slnc 300]] Rules that do not learn simply '
            'ignore it. [[slnc 600]] Third, the four rules. [[slnc 300]] '
            'Take the first. [[slnc 200]] Take turns. [[slnc 200]] Prefer '
            'the fastest. [[slnc 200]] And pick at random. [[slnc 500]] '
            'None of them knows about any other caller. [[slnc 300]] And '
            "that limit is the pattern's ceiling, as we will see."
        ),
    ),
    dict(
        key="09-client-code",
        kind="code",
        title="The Caller — Five Lines, No Policy",
        body="""public String productName(String sku) {
    List<ServiceInstance> candidates = cluster.instances();
    ServiceInstance chosen = balancer.choose(candidates);

    long startedAt = clock.millis();
    String name = cluster.call(chosen, sku);
    balancer.observed(chosen, clock.millis() - startedAt);
    return name;
}

// ask who's up, choose, call, report back how long it took""",
        narration=(
            "Here is the caller's code, step by step. [[slnc 500]] First, "
            'ask which copies are available, right now, on this request. '
            '[[slnc 300]] Second, hand that list to the balancer, and get '
            'one copy back. [[slnc 300]] Then note the time, call that '
            'copy, and tell the balancer how many milliseconds it took. '
            '[[slnc 600]] Now ask: where is the rule for picking? [[slnc '
            "500]] There isn't one. [[slnc 300]] No check for which copy "
            'is fastest. [[slnc 300]] No counter. [[slnc 300]] Nothing '
            'that knows one machine from another. [[slnc 300]] Swapping '
            'one rule for another changes nothing in this code. [[slnc '
            '600]] That is what the pattern buys. [[slnc 300]] And here '
            'is the cost. [[slnc 300]] To know which machine gets called, '
            'you must look at which rule was passed in when the caller '
            'was created.'
        ),
    ),
    dict(
        key="10-round-robin",
        kind="console",
        title="Take Turns — Fair, And Not Fast",
        body="""2. Round-robin: take turns
    catalog-1    4 requests (33%)   10ms each
    catalog-2    4 requests (33%)   10ms each
    catalog-3    4 requests (33%)   60ms each
  12 requests took 320ms in total

  a perfectly even split, which sends a third of the shop's
  traffic to the slowest machine it owns.

  // the whole strategy: candidates.get(Math.floorMod(next++, size))""",
        narration=(
            'Second demo: take turns. [[slnc 300]] This is usually called '
            'round-robin. [[slnc 500]] It is simply a counter. [[slnc '
            '300]] Add one each time, and use it to step along the list. '
            '[[slnc 600]] Twelve requests, and the split is four, four, '
            'and four. [[slnc 300]] Perfectly even. [[slnc 500]] And it '
            'took three hundred and twenty milliseconds. [[slnc 300]] '
            'Against a hundred and twenty for the version we called bad. '
            '[[slnc 600]] It is nearly three times slower. [[slnc 300]] '
            'And it is still the one you should ship. [[slnc 600]] Here '
            'is the most useful sentence in this video. [[slnc 300]] Fair '
            'is not the same as fast. [[slnc 500]] Round-robin sent a '
            'third of the traffic to the slowest machine. [[slnc 300]] '
            'Because it does not know what slow means. [[slnc 300]] It '
            'never measures anything. [[slnc 600]] But look at what it '
            'bought. [[slnc 300]] All three machines are now used. [[slnc '
            '300]] So the spare capacity is real. [[slnc 300]] And losing '
            'one machine costs a third of the capacity, not all of it. '
            '[[slnc 300]] That is why round-robin is still the sensible '
            'default.'
        ),
    ),
    dict(
        key="11-least-latency",
        kind="code",
        title="Prefer The Fast Ones — Measure First",
        body="""public ServiceInstance choose(List<ServiceInstance> candidates) {
    for (ServiceInstance candidate : candidates) {
        if (!averageMillis.containsKey(candidate.instanceId())) {
            return candidate;   // never tried; measure it before judging it
        }
    }
    return candidates.stream()
            .min(comparing(a -> averageMillis.get(a.instanceId())))
            .orElseThrow();
}""",
        narration=(
            'The clever rule is: prefer whichever copy has been fastest '
            'so far. [[slnc 300]] It keeps an average time for each copy, '
            'and picks the lowest. [[slnc 600]] But before picking, it '
            'does one thing first. [[slnc 300]] If there is any copy it '
            'has never called, it calls that one. [[slnc 600]] Why does '
            'that step have to exist? [[slnc 500]] Because a balancer '
            'that has never called catalog three knows nothing about it. '
            '[[slnc 300]] The danger is not knowing nothing. [[slnc 300]] '
            'The danger is quietly inventing an opinion. [[slnc 500]] '
            'Without that step, a copy never tried would either look '
            'endlessly slow, and never be tried. [[slnc 300]] Or look '
            'endlessly fast, and be flooded. [[slnc 600]] So the rule is: '
            'measure before you judge. [[slnc 300]] Every copy gets one '
            'request to prove itself. [[slnc 300]] After that, it is '
            'judged on its record. [[slnc 300]] And if you delete that '
            'step, one test fails, and its name says exactly that.'
        ),
    ),
    dict(
        key="12-learned",
        kind="console",
        title="It Learned That On Its Own",
        body="""3. Least latency: try each once, then prefer the fast ones
    catalog-1   10 requests (83%)   10ms each
    catalog-2    1 requests ( 8%)   10ms each
    catalog-3    1 requests ( 8%)   60ms each
  12 requests took 170ms in total

  the client now believes: catalog-1 10ms, catalog-2 10ms, catalog-3 60ms
  it learned that on its own, from its own requests. Nothing told it.""",
        narration=(
            'Third demo: the same twelve requests, preferring the '
            'fastest. [[slnc 500]] A hundred and seventy milliseconds, '
            'down from three hundred and twenty. [[slnc 300]] And the '
            'slow machine was asked only once: the one time it took to '
            'find out that it was slow. [[slnc 600]] Then the client says '
            'what it now believes. [[slnc 300]] Catalog one: ten '
            'milliseconds. [[slnc 200]] Catalog two: ten. [[slnc 200]] '
            'Catalog three: sixty. [[slnc 600]] Nobody set those numbers. '
            '[[slnc 300]] They are not in a settings file, and nobody '
            'typed them in. [[slnc 300]] The client worked them out from '
            'its own twelve requests. [[slnc 600]] That is the whole '
            'argument for balancing inside the caller. [[slnc 300]] How '
            'slow has this machine been, for me? [[slnc 300]] Only the '
            'caller can answer that. [[slnc 300]] It depends on where the '
            'caller is, and what it is asking for. [[slnc 300]] A caller '
            'in another data centre would measure different numbers, and '
            'be right to.'
        ),
    ),
    dict(
        key="13-herding",
        kind="bullets",
        title="The Half That Gets Skipped: Herding",
        body=[
            "Look again: catalog-2 is exactly as fast as",
            "catalog-1 — both 10ms — and it got 1 request in 12.",
            "",
            "The tie broke towards whoever was measured first.",
            "The client found a favourite and kept it.",
            "",
            "Harmless with one client. Now imagine a thousand:",
            "",
            "  all measure the same thing",
            "  all reach the same conclusion",
            "  all crowd the same instance, making it slow",
            "  all leave it together",
        ],
        narration=(
            'Now the part most explanations skip. [[slnc 300]] It has two '
            'halves, and neither is a bug. [[slnc 600]] Look again at '
            'those numbers. [[slnc 300]] Catalog two is exactly as fast '
            'as catalog one. [[slnc 300]] But it got only one request out '
            'of twelve. [[slnc 500]] The tie was broken in favour of '
            'whichever was measured first. [[slnc 300]] So the client '
            'found a favourite, and kept it forever. [[slnc 300]] With '
            'one client, that is harmless. [[slnc 600]] Now imagine a '
            'thousand clients, in front of the same three machines. '
            '[[slnc 300]] They all measure the same thing. [[slnc 300]] '
            'They all choose the same favourite. [[slnc 300]] And they '
            'all crowd onto it. [[slnc 500]] So it gets slow. [[slnc '
            '300]] They all notice, and all leave it at once, for the '
            'next one. [[slnc 300]] Which they then make slow. [[slnc '
            '500]] The load swings back and forth, and not one client did '
            'anything wrong. [[slnc 300]] This is called herding. [[slnc '
            '300]] The fix is small: break ties at random. [[slnc 600]] '
            'But notice what happened. [[slnc 300]] The clever rule '
            'brought a problem that the simple one does not have. [[slnc '
            '300]] That is a big part of why taking turns is still the '
            'default.'
        ),
    ),
    dict(
        key="14-blind",
        kind="console",
        title="Two Perfect Clients, One Idle Machine",
        body="""4. Two clients, each taking perfect turns
    catalog-1    2 requests (50%)   10ms each
    catalog-2    2 requests (50%)   10ms each
    catalog-3    0 requests ( 0%)   60ms each

  each client did exactly the right thing on its own and they still
  left catalog-3 with nothing to do, because a client-side balancer
  can only balance the traffic it can see -- its own.""",
        narration=(
            'Fourth demo, and this is the more important half. [[slnc '
            '400]] Now there are two clients: say, the website and the '
            'mobile app. [[slnc 300]] Each has its own take-turns '
            'balancer. [[slnc 300]] And each makes two requests. [[slnc '
            '600]] Catalog one gets two requests. [[slnc 300]] Catalog '
            'two gets two requests. [[slnc 300]] And catalog three gets '
            'nothing at all. [[slnc 600]] So which client made the '
            'mistake? [[slnc 500]] Neither. [[slnc 300]] Each took '
            'perfect turns. [[slnc 300]] Each counter started at the top '
            'of the list, and stepped along it. [[slnc 600]] The problem '
            'is that each counter lives inside one client. [[slnc 300]] '
            "So it only counts that client's requests. [[slnc 300]] Two "
            'counters, each correct, are wrong together. [[slnc 600]] And '
            'no cleverness inside either client can fix it. [[slnc 300]] '
            'What is missing is not intelligence. [[slnc 300]] It is '
            'information. [[slnc 300]] A client-side balancer can only '
            'balance the traffic it can see. [[slnc 300]] And it can only '
            'ever see its own.'
        ),
    ),
    dict(
        key="15-costs",
        kind="quote",
        title="When To Stop Doing This",
        body=[
            "Remember the member of staff at the head of",
            "the six queues? They can see all six queues",
            "and every shopper. No shopper can.",
            "",
            "When one caller's view is not good enough,",
            "the answer is not a cleverer caller.",
            "It is one balancer in front of the cluster,",
            "seeing every request.",
            "",
            "That is simpler, easier to operate, and right",
            "more often than this pattern's fans admit.",
        ],
        narration=(
            'Which brings back the member of staff at the front of the '
            'six queues. [[slnc 500]] They can see every queue, and every '
            'shopper. [[slnc 300]] No single shopper can, however '
            "carefully they look. [[slnc 600]] So when one caller's view "
            'is not good enough, the answer is not a cleverer caller. '
            '[[slnc 300]] It is one balancer in front of all the copies, '
            'seeing every request. [[slnc 300]] That is called '
            'server-side load balancing. [[slnc 600]] And here is the '
            'part pattern videos rarely say. [[slnc 300]] Server-side '
            'balancing is simpler, and easier to run. [[slnc 300]] It '
            'works with callers you do not control. [[slnc 300]] And it '
            'is the right answer more often than people admit. [[slnc '
            '300]] The price is one more network hop, and one more thing '
            'that can fail. [[slnc 600]] Client-side balancing earns its '
            'place when the caller knows something nobody else does. '
            '[[slnc 300]] Like its own response times, or where it sits. '
            '[[slnc 300]] Or when you want no extra hop at all. [[slnc '
            '500]] Both are real engineering. [[slnc 300]] Knowing which '
            'situation you are in is the real skill.'
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that deletes",
            "the measure-first loop, and the one that makes all three",
            "instances equally fast and watches the clever strategy",
            "stop being worth it.",
        ],
        narration=(
            "That's client-side Load Balancing. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Let '
            'the caller choose a copy on every request with a replaceable '
            'rule, but remember it can only balance the traffic it can '
            'see. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            'is one exercise to try. [[slnc 300]] In the '
            'prefer-the-fastest rule, delete the step that tries every '
            'copy once. [[slnc 300]] Then run the tests. [[slnc 300]] One '
            'test fails, and its name tells you what you broke. [[slnc '
            '300]] Ask yourself: what does the balancer now believe about '
            'a machine it has never called? [[slnc 500]] If this helped, '
            'a like really does help other people find it. [[slnc 300]] '
            "And subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
