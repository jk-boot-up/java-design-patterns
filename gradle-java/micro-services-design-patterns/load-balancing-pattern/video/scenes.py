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
            "Hello, and welcome. This video explains the client-side Load "
            "Balancing pattern in Java, and it is written and presented by "
            "Jayasekhar Konduru. [[slnc 300]] Let's start with the simple "
            "definition. When a service runs as several identical copies, "
            "somebody has to decide which copy each request goes to. Client-side "
            "load balancing means the caller makes that decision itself, fresh, "
            "on every single request — and because the caller makes it, the "
            "decision can be swapped out without touching anything else. "
            "[[slnc 350]] That's the idea in a sentence. The rest of the video "
            "does it properly, by building a real working Java project: an online "
            "shop whose catalog service runs as three copies, one of which is on "
            "older, slower hardware. [[slnc 250]] By the end you'll know why "
            "sending every request to the first copy on the list is fast, "
            "correct, and still has to go; why taking fair turns is not the same "
            "as being quick; and — the part that usually gets skipped — the two "
            "ways this pattern goes wrong even when every caller is behaving "
            "perfectly."
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
            "Here is the situation. [[slnc 250]] The shop's catalog service — the "
            "thing that knows what a product is called and what it costs — is busy "
            "enough that one copy of it is not sensible any more. So it runs as "
            "three. Same program, started three times, on three machines. "
            "[[slnc 300]] Two of those machines answer a question in about ten "
            "milliseconds. The third takes sixty, because it is older hardware "
            "that nobody has got round to replacing. That difference is going to "
            "matter enormously, and notice that it is not a fault. Nothing is "
            "broken. One box is just slower than the others, which is true of "
            "almost every real cluster. [[slnc 350]] The important thing about the "
            "three is that they are interchangeable. Ask any of them for a product "
            "name and you get the same product name, because what an espresso "
            "machine is called does not depend on which machine you happen to ask. "
            "[[slnc 350]] And that is exactly what creates the problem. When "
            "everything gives the same answer, there is no right one to pick — but "
            "something still has to pick. So: which of the three does the checkout "
            "ask?"
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
            "The obvious answer is to take the first one on the list, and I want "
            "to be fair to it, because almost nobody chooses this on purpose. "
            "[[slnc 300]] You ask who is available, you get back a list, and you "
            "use the first thing in it. In the project that lives in a class "
            "called first instance balancer, and the whole of it is one line: "
            "return the first candidate. [[slnc 350]] There is no bug in that "
            "line. It returns the correct product name every time. It is not slow. "
            "It has no configuration to get wrong. [[slnc 300]] And here is the "
            "thing that makes it genuinely dangerous rather than merely wrong: "
            "there is a whole test file in this project written against it, and "
            "every test in that file passes. [[slnc 350]] So keep that in mind as "
            "we take it apart. What goes wrong here is not a mistake somebody "
            "made. It is three lines that nobody ever thought of as a decision."
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
            "So let's run it. Twelve requests, through the take-the-first "
            "strategy. [[slnc 300]] Catalog one gets twelve requests. That is one "
            "hundred percent of them. Catalog two gets nothing and catalog three "
            "gets nothing. [[slnc 350]] And now the number that makes this lesson "
            "difficult to teach: the twelve requests took one hundred and twenty "
            "milliseconds in total, and that is going to turn out to be the "
            "fastest number in this entire video. [[slnc 400]] Let that sit for a "
            "moment, because it is the opposite of what you expect from the bad "
            "version of a pattern. Nothing failed. Nothing was slow. Nothing timed "
            "out. Every answer was correct and arrived promptly. [[slnc 350]] The "
            "costs are all outside the program, which is precisely why nobody "
            "notices them. Two machines are being billed, monitored, patched and "
            "backed up, and they are doing nothing at all. The headroom the shop "
            "thinks it bought does not exist, because the traffic is not actually "
            "spread over three boxes. And when catalog one falls over, everything "
            "falls over, with two perfectly healthy machines sitting a couple of "
            "metres away."
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
            "Let me be concrete about the damage, because a hundred and twenty "
            "milliseconds hides all of it. [[slnc 300]] First, money. Three "
            "machines are on the bill and one is doing the work. [[slnc 250]] "
            "Second, and worse, the safety you thought you had bought is "
            "imaginary. The shop believes it can survive losing a machine. In fact "
            "it can survive losing two particular machines and not the third. "
            "[[slnc 300]] Third, the blast radius. When the busy box goes down, a "
            "hundred percent of requests go down with it. A rolling restart — an "
            "ordinary Tuesday afternoon deployment — is a full outage rather than a "
            "third of one. [[slnc 350]] And then the reason this survives code "
            "review for years. In a test environment there is usually one instance "
            "of everything. With one instance, take-the-first and take-turns "
            "produce exactly the same behaviour, request for request. They are "
            "indistinguishable. [[slnc 350]] So the sentence to take away is this: "
            "a concentration problem does not announce itself with a failing test. "
            "It announces itself on the night one machine dies, which is a very "
            "expensive time to find out."
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
            "The pattern is usually stated something like this. A client that has "
            "several interchangeable instances to choose from hands the choice to a "
            "replaceable policy, and makes that choice again on every request. "
            "[[slnc 350]] In plain words: don't take the first one, and put the "
            "choosing somewhere you can change it. [[slnc 300]] Two things in that "
            "are doing real work. [[slnc 250]] The first is replaceable. The rule "
            "for picking becomes an object, so you can swap take-turns for "
            "prefer-the-fast-one without editing the code that makes the request. "
            "[[slnc 300]] The second is on every request. This is not a setting "
            "you read at startup. It is a decision, remade twelve times in twelve "
            "requests, which is what lets it react to a machine that got slow five "
            "seconds ago. [[slnc 350]] And then there is a third part, which is "
            "not in most statements of the pattern and which this video will spend "
            "real time on: be honest about what one caller can see. Every caller "
            "here is choosing well, on its own, with no bugs — and we will watch "
            "them collectively get it wrong anyway."
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
            "Here is the everyday version, and it has nothing to do with "
            "computers. [[slnc 250]] You are in a supermarket. Six tills are open. "
            "Nobody is directing anybody. You look along the row, you pick the "
            "queue that looks shortest, and you join it. [[slnc 350]] Three things "
            "just happened, and all three are the pattern. [[slnc 250]] You chose. "
            "No member of staff assigned you a till. The decision was made at your "
            "end, by you. [[slnc 300]] You chose using what you could see, which "
            "was queue length — not who the fastest cashier is, and not whether "
            "the person at the front has forty items and a coupon problem. Your "
            "information was local and incomplete, and you used it anyway because "
            "it was better than nothing. [[slnc 300]] And you will choose again "
            "next week, from scratch. You have not written down which till is best. "
            "[[slnc 350]] Now picture the other supermarket, the one where a member "
            "of staff stands at the head of all six queues and tells each shopper "
            "where to go. Hold onto that person. They are going to come back at the "
            "end of this video, and they are going to win an argument."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So, the pieces. [[slnc 250]] On the left is the caller: the class in "
            "the project is called catalog client. It asks the cluster who is "
            "available, hands that list to the balancer it happens to be holding, "
            "calls whichever instance comes back, and then reports how long that "
            "took. That is the entire class. It contains no rule for picking at "
            "all. [[slnc 350]] In the middle is the load balancer itself, which is "
            "an interface with one real method. You give it a list of candidates "
            "and it gives you back one of them. One method, four different answers, "
            "depending on which implementation you passed in. [[slnc 300]] If that "
            "shape sounds familiar, it should: this is the Strategy pattern. Same "
            "structure, interchangeable implementations, a caller that never asks "
            "which one it is holding. What is new here is the subject matter. The "
            "thing being chosen is a machine, the choice is remade on every "
            "request, and the chooser knows something the network does not. "
            "[[slnc 350]] Below the interface there is a second method, called "
            "observed, and it has a default empty body. It is how the caller "
            "reports back how long a call took. It is empty by default because "
            "taking turns does not care how long anything took, and a strategy that "
            "does not learn should not be forced to write an empty method to say "
            "so. [[slnc 350]] And on the right are the four strategies: take the "
            "first, take turns, prefer the fastest, and pick at random. Notice the "
            "arrows all run leftwards, into the interface. Not one of them points "
            "at another strategy, and not one points at another client. That second "
            "absence is the pattern's ceiling, and we will come back to it."
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
            "This is the caller, and it is the punchline of the whole design, so "
            "it is worth going through slowly. [[slnc 300]] Line one: ask the "
            "cluster which instances are available right now. Not at startup — "
            "right now, on this request. [[slnc 250]] Line two: hand that list to "
            "the balancer and get one instance back. [[slnc 250]] Then note the "
            "time, call the instance you were given, and tell the balancer how many "
            "milliseconds it took. [[slnc 350]] Now the question to ask about this "
            "method is: where is the policy? [[slnc 300]] There isn't any. There is "
            "no if statement about which instance is fastest, no counter, no "
            "configuration, nothing that knows one machine from another. Swapping "
            "take-turns for prefer-the-fastest changes not one character in this "
            "file. [[slnc 350]] That is the property the pattern is buying, and it "
            "is worth saying what it costs you in exchange: the behaviour of your "
            "system is now somewhere other than where you read about the request. "
            "To know which machine gets called, you have to go and look at what was "
            "passed into the constructor."
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
            "The first real strategy is take turns, which everybody calls "
            "round-robin. It is a counter and a remainder: keep a number, add one "
            "to it each time, and use it to step along the list. That is the whole "
            "implementation. [[slnc 350]] Run the same twelve requests through it "
            "and the split is four, four, four. Thirty-three percent each. "
            "Perfectly, arithmetically even. [[slnc 300]] And it took three hundred "
            "and twenty milliseconds, against a hundred and twenty for the version "
            "we said was bad. [[slnc 400]] It is nearly three times slower, and it "
            "is the thing you should ship. [[slnc 350]] So let's say plainly what "
            "happened, because this is the single most useful sentence in the "
            "video: fair is not the same as fast. [[slnc 300]] Round-robin sent a "
            "third of the shop's traffic to the slowest machine the shop owns. It "
            "did that because it does not know what slow means. It was never told, "
            "it never measured anything, and it cannot tell a sixty millisecond box "
            "from a ten millisecond one. [[slnc 350]] What it bought in exchange is "
            "worth the time: all three machines are now in use, so the headroom is "
            "real, and losing any one of them costs you a third of your capacity "
            "instead of all of it. That is why, despite the number on the screen, "
            "round-robin is still the sensible default."
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
            "The clever strategy is prefer whichever instance has been fastest so "
            "far. It keeps a running average of how long each instance has taken "
            "for this caller, and it picks the lowest. [[slnc 300]] But look at "
            "what comes before the picking. There is a loop that says: if there is "
            "any instance here that I have never called, call that one. "
            "[[slnc 350]] Ask yourself why that loop has to exist. [[slnc 300]] "
            "Because a balancer that has never called catalog three has no opinion "
            "about catalog three, and the dangerous thing is not having no opinion "
            "— it is quietly inventing one. Without that loop, an instance that has "
            "never been tried either looks infinitely slow and is never tried, or "
            "looks infinitely fast and is hammered. Both are the balancer trusting "
            "a measurement it never took, which is just taking turns with extra "
            "confidence. [[slnc 350]] So the rule is: measure before you judge. "
            "Every instance gets exactly one request to prove itself, and after "
            "that it is on its record. [[slnc 300]] There is a test in the project "
            "whose name is simply that — least latency measures before it judges — "
            "and if you delete this loop, that is the test that goes red."
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
            "Here is the same twelve requests again, preferring the fast ones. "
            "[[slnc 300]] A hundred and seventy milliseconds, down from three "
            "hundred and twenty. And the slow box was asked exactly once — the once "
            "it took to find out that it was slow. [[slnc 350]] But the timing is "
            "not the important line here. The important line is the one underneath "
            "it, where the client says what it now believes: catalog one, ten "
            "milliseconds; catalog two, ten milliseconds; catalog three, sixty. "
            "[[slnc 400]] Nobody configured those numbers. They are not in a "
            "properties file, they were not passed in, and no operator typed them. "
            "The client worked them out from its own twelve requests. [[slnc 350]] "
            "And that is the entire argument for doing the balancing in the caller "
            "rather than in the middle of the network. How slow has this machine "
            "been, for me? is a question only the caller can answer. It depends on "
            "which rack the caller is in, which network path the packets take, and "
            "what the caller happens to be asking for. A balancer sitting somewhere "
            "in the middle measures its own view, and its own view is a different "
            "view. [[slnc 300]] A client in another data centre would have measured "
            "different numbers and would be right to."
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
            "Now the half that most explanations of this pattern leave out, and "
            "there are two parts to it. Neither part is a bug, which is what makes "
            "them worth your time. [[slnc 350]] Go back to those numbers for a "
            "second. Catalog two is exactly as fast as catalog one. Both ten "
            "milliseconds. And catalog two received one request out of twelve. "
            "[[slnc 300]] What happened is that the tie broke towards whichever "
            "one was measured first, so the client found a favourite and then kept "
            "it, forever. With one client that is harmless — you are still using a "
            "fast machine. [[slnc 350]] So now imagine a thousand clients in front "
            "of the same three machines. They all measure the same thing. They all "
            "reach the same conclusion. They all crowd onto the same instance. "
            "[[slnc 300]] And because they have all crowded onto it, it gets slow. "
            "So they all measure that, they all conclude it is slow, and they all "
            "leave it at the same time — for the next one, which they then make "
            "slow. [[slnc 350]] The cluster oscillates, the graphs look like a "
            "sawtooth, and not one client did anything wrong. That is called "
            "herding, and the fix is small: break ties at random. [[slnc 300]] But "
            "notice the shape of what just happened. The clever strategy brought a "
            "failure mode with it that the boring one does not have, and that is a "
            "large part of why taking turns is still the default."
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
            "And here is the second part, which is the more important of the two. "
            "[[slnc 300]] Two clients this time — say the website and the mobile "
            "app. Each has its own take-turns balancer. Each makes two requests. "
            "[[slnc 300]] Catalog one gets two requests, catalog two gets two "
            "requests, and catalog three gets nothing at all. [[slnc 400]] So "
            "which client made the mistake? [[slnc 400]] Neither. That is the "
            "answer, and it is worth sitting with. Each client took perfect turns. "
            "Each counter did exactly what a counter is supposed to do: started at "
            "the beginning of the list and stepped along it. [[slnc 350]] The "
            "problem is that the counter lives inside one client, so it counts one "
            "client's requests. Two counters that each start at zero produce a "
            "pattern that is correct twice over and wrong collectively. "
            "[[slnc 350]] And no amount of cleverness inside either client fixes "
            "it, because the missing thing is not intelligence. It is information. "
            "A client-side balancer can only balance the traffic it can see, and it "
            "can only ever see its own."
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
            "Which brings back the member of staff standing at the head of the six "
            "queues. [[slnc 300]] They can see all six queues and every shopper in "
            "the shop. No individual shopper can see that, no matter how carefully "
            "they look. [[slnc 350]] So when one caller's view is not good enough, "
            "the answer is not a cleverer caller. It is to put one balancer in "
            "front of the cluster and let it see every request. That is server-side "
            "load balancing — a load balancer, a proxy, a service mesh, an ingress. "
            "[[slnc 350]] And I want to say the unpopular part out loud, because "
            "pattern videos tend not to. Server-side balancing is simpler, it is "
            "easier to operate, it works with callers you do not control and cannot "
            "change, and it is the right answer more often than this pattern's fans "
            "admit. The price you pay is one more network hop and one more thing "
            "that can fail. [[slnc 350]] Client-side balancing earns its place when "
            "the caller knows something nobody else does — its own latencies, which "
            "rack it is in, which requests are cheap — or when you want no extra "
            "hop at all. [[slnc 300]] Both are real engineering. Knowing which "
            "situation you are in is the actual skill."
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
            "That's client-side load balancing. [[slnc 250]] The full source, the "
            "written notes, the diagrams and an animated walkthrough are all in the "
            "repository, and everything runs offline with nothing installed but a "
            "Java development kit — no Docker, no Kubernetes, no service mesh. "
            "[[slnc 300]] If you try one exercise, try this one. Go into the "
            "prefer-the-fastest balancer and delete the loop that tries every "
            "instance once, so that it goes straight to picking the lowest average. "
            "Then run the tests. [[slnc 300]] One test fails, and its name tells "
            "you exactly what you broke. Sit with the question it raises: what does "
            "the balancer now believe about a machine it has never called, and why "
            "is believing something worse than knowing nothing? [[slnc 350]] And if "
            "you have a little more time, change the slow instance to be as fast as "
            "the other two and run all four acts again. The clever strategy's "
            "advantage simply evaporates. That tells you something useful about when "
            "to reach for it at all. [[slnc 300]] If this helped, a like genuinely "
            "does help other people find it, and subscribe if you would like the "
            "rest of the series. [[slnc 250]] Thanks for watching, and I'll see you "
            "in the next one."
        ),
    ),
]
