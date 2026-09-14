"""Scene definitions for the Service Discovery teaching video.

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
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Service Discovery",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Service Discovery "
            "pattern in Java, and it is written and presented by Jayasekhar "
            "Konduru. [[slnc 300]] Let's start with the simple definition. "
            "Service discovery means that instead of writing a service's address "
            "into the code that calls it, you keep a shared list of who is "
            "running right now, and the caller asks that list every time it needs "
            "an address. Programs put themselves on the list when they start, and "
            "they drop off it when they stop. [[slnc 350]] That's the idea in a "
            "sentence. The rest of the video does it properly, by building a real "
            "working Java project: an online shop whose pricing service runs as "
            "several copies of itself, and a checkout that has to reach one of "
            "them. [[slnc 250]] By the end you'll know why a written-down address "
            "turns an ordinary deployment into an outage, what a lease is and why "
            "a registration has to expire, and — the part that usually gets "
            "skipped — why the list is guaranteed to be wrong for a few seconds "
            "at a time, and what a caller has to do about that."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The shop's Pricing service is busy.",
            "So it runs as three copies of the same program:",
            "",
            "    pricing-1      10.0.1.145:8081",
            "    pricing-2      10.0.1.146:8082",
            "    pricing-3      10.0.1.147:8083",
            "",
            "Any of the three can answer any question.",
            "All three give the same answer.",
            "",
            "The checkout needs a price. So it needs an address.",
            "Which one does it call, and how does it know?",
        ],
        narration=(
            "Here is the situation. [[slnc 250]] The shop's pricing service is "
            "busy enough that one copy of it is not sensible any more, so it runs "
            "as three. They are the same program, started three times, on three "
            "machines. [[slnc 300]] The important thing about those three is that "
            "they are interchangeable. Any of them can answer any question, and "
            "they all give the same answer, because the price of an espresso "
            "machine does not depend on which machine you happen to ask. "
            "[[slnc 350]] Now the checkout needs a price. To ask for one it needs "
            "an address. [[slnc 300]] And that raises a question which has no "
            "interesting answer in a single program, and no easy one here: which "
            "of the three does it call, and how does it find out?"
        ),
    ),
    dict(
        key="03-naive",
        kind="code",
        title="The Obvious Answer — Write It Down",
        body="""public final class HardcodedPricingClient {

    // the address somebody pasted in when there was one instance
    private static final String PRICING_INSTANCE = "pricing-1";

    public Money price(String sku) {
        return cluster.endpoint(pinned).invoke(sku);
    }
}

// four lines, and every one of them is correct""",
        narration=(
            "The obvious answer is to write the address down, and I want to be "
            "fair to it, because this is what every system starts with and "
            "starting there is right. [[slnc 300]] The class in the project is "
            "called hardcoded pricing client. It holds one string, pricing dash "
            "one, and it calls it. That is the whole class. [[slnc 350]] There is "
            "no bug in it. It is four lines and every one of them is correct. It "
            "is fast, it has no dependencies, it cannot be misconfigured, and "
            "every test you would think to write against it passes. When the shop "
            "had one pricing instance, this was exactly the right amount of code. "
            "[[slnc 350]] So keep that in mind as we break it. What goes wrong "
            "here is not a mistake somebody made. It is the world changing "
            "underneath a decision that was correct when it was taken."
        ),
    ),
    dict(
        key="04-deploy",
        kind="console",
        title="Then Somebody Deploys Pricing",
        body="""$ ./gradlew run

==================================================================
1. A hardcoded address, and a routine deployment
==================================================================
  before the deploy: £449.99
      0ms ->    10ms  pricing-1        OK        £449.99
     10ms ->    10ms  Registry         DEREGISTER pricing-1 left cleanly
  after the deploy:  pricing-1 did not answer

  two healthy instances are sitting idle. The client cannot use them,
  because it was told about one machine and has no way to learn
  about another.""",
        narration=(
            "Then somebody deploys pricing. [[slnc 250]] A rolling deployment "
            "stops the first instance so it can be replaced with a new version. "
            "That is not a fault. That is Tuesday afternoon. [[slnc 350]] And the "
            "checkout is now down. Not slow. Down. It asks for a price and gets "
            "nothing back, and it will go on getting nothing back until somebody "
            "changes it. [[slnc 350]] Now here is the part that stings. At that "
            "exact moment, pricing two and pricing three are up, healthy, and "
            "doing nothing, three metres away in the same rack. The client cannot "
            "use either of them. [[slnc 300]] And no amount of care inside that "
            "client would help, because a constant is not a question you can ask "
            "again later. It was told about one machine, once, and it has no way "
            "of ever finding out about another."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Really Hurts",
        body=[
            "✗ A routine deployment is an outage.",
            "✗ Scaling up buys you nothing — start pricing-4 and no",
            "  existing caller will ever send it a single request.",
            "✗ A crash has no fallback, because there is nothing",
            "  to fall back to.",
            "",
            "The real diagnosis:",
            "  the set of running instances changes several times a",
            "  day. The source code of the callers changes about",
            "  once a fortnight.",
            "",
            "A fast-moving fact, stored in a slow-moving artefact.",
        ],
        narration=(
            "It is worth naming the damage properly, because it is wider than one "
            "outage. [[slnc 300]] A routine deployment takes the caller down. "
            "Scaling up buys you nothing at all — start a fourth instance for a "
            "busy Friday and no existing caller will ever send it a single "
            "request, so you are paying for capacity that cannot be reached. And "
            "a crash has no fallback, because there is nothing to fall back to. "
            "[[slnc 400]] But none of those is the diagnosis. The diagnosis is "
            "this. [[slnc 300]] The set of running instances changes several times "
            "a day — every deployment, every autoscaling event, every crash. The "
            "source code of the callers changes about once a fortnight. A "
            "fast-moving fact has been stored inside a slow-moving artefact. "
            "[[slnc 350]] And that is why the usual first suggestion does not "
            "work. Move the address into a configuration file and you have moved "
            "the fact one step, and improved the ratio slightly. A human still "
            "has to edit that file, and restart the process, and — worst of all — "
            "that human still has to notice."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Service Discovery Pattern",
        body=[
            "Instances register themselves with a registry when",
            "they start, renew that registration periodically, and",
            "deregister when they stop. Callers query the registry",
            "for the current instances of a service.",
            "",
            "— the pattern as usually stated",
            "",
            "In plain words: don't write the address down.",
            "Ask, every time. And be ready to be told wrong.",
        ],
        narration=(
            "The pattern is usually stated something like this. Instances "
            "register themselves with a registry when they start, renew that "
            "registration from time to time, and deregister when they stop; and "
            "callers query the registry for the current instances of a service. "
            "[[slnc 350]] In plain words: don't write the address down. Ask, "
            "every time. [[slnc 300]] And then there is a second half, which is "
            "not in most statements of the pattern and which this video is going "
            "to spend real time on: be ready to be told wrong. [[slnc 350]] "
            "Notice what the first half fixes. An instance is reachable the "
            "moment it starts, with no configuration change anywhere. A polite "
            "shutdown is invisible to callers. Scaling up works. Nobody edits "
            "anything. [[slnc 350]] And notice what it cannot fix, which is that "
            "a program which has crashed cannot send a message saying it has "
            "crashed. For a few seconds after a crash, the list will confidently "
            "hand out the address of something that is not there. That is not a "
            "flaw in any particular registry. It is the shape of the problem."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="An Analogy",
        body=[
            "A taxi rank.",
            "",
            "You could keep the mobile number of a driver called Dave.",
            "It works beautifully — until the evening Dave is off. Then",
            "it keeps not working, while eleven other drivers in town",
            "would happily take you.",
            "",
            "Or you go to the rank and take whoever is at the front.",
            "Drivers join when a shift starts and leave when it ends.",
            "",
            "And if that driver has just been called away, you don't",
            "stand there insisting. You take the next one.",
        ],
        narration=(
            "The analogy to hold on to is a taxi rank. [[slnc 300]] One way to "
            "get a taxi is to keep the mobile number of a driver called Dave. "
            "That works beautifully, and it keeps working, right up until the "
            "evening Dave is off. And then it goes on not working, while eleven "
            "other drivers in town would happily take you, because your phone "
            "knows about Dave and nobody else. [[slnc 400]] The other way is a "
            "taxi rank. You know no driver's name at all. You go to the rank and "
            "take whoever is at the front. Drivers join the rank when they start "
            "a shift and leave it when they finish, and none of that requires you "
            "to learn anything or change anything. [[slnc 350]] The rank is the "
            "registry. The drivers are the instances. [[slnc 300]] And now here "
            "is the detail that makes this more than a nice picture, so listen "
            "for it. What do you do if you get into a car whose driver has just "
            "been called away? [[slnc 300]] You do not stand there insisting. "
            "You take the next one. [[slnc 350]] Hold on to that, because in the "
            "code it turns out to be four lines, and without them the whole "
            "pattern falls over exactly when you need it."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So, the pieces. [[slnc 250]] At the top there is the caller: the "
            "class in the project is called discovering pricing client. It holds a "
            "reference to the registry rather than to an instance, and that one "
            "difference is the entire pattern. It holds a source of addresses "
            "where the old version held an address. [[slnc 350]] In the middle "
            "sits the registry itself, called service registry. It keeps one entry "
            "per instance, and each entry is a lease with a timestamp on it. "
            "[[slnc 300]] To the side of it is that lease — a tiny record holding "
            "the instance and the time of its last heartbeat. It is the only thing "
            "in the project that stores a time, and it is what turns an ordinary "
            "map into something that forgets. [[slnc 350]] On the right are the "
            "pricing instances, and the direction of the arrows there is worth "
            "saying out loud, because it is easy to get backwards. The arrows run "
            "from the instances into the registry. Instances announce themselves. "
            "Nothing in this system ever calls out to a service to ask whether it "
            "is alive. [[slnc 300]] The reason is neat: a registry that polled "
            "everybody would need a list of who everybody is, and building that "
            "list is the original problem again, one level up. [[slnc 350]] And "
            "kept deliberately beside the pattern rather than inside it is the "
            "hardcoded client, so that the comparison is something you can run "
            "rather than something I assert."
        ),
    ),
    dict(
        key="09-registry-code",
        kind="code",
        title="The Registry — and the One Line That Matters",
        body="""public void register(ServiceInstance instance) {
    leases.put(instance.instanceId(),
               new Lease(instance, clock.millis()));
}

public void heartbeat(String instanceId) { ... }   // renews the lease

public List<ServiceInstance> instances(String serviceName) {
    for (Lease lease : leases.values()) {
        if (clock.millis() - lease.lastHeartbeatAt() > LEASE_MILLIS) {
            expired.add(lease.instance().instanceId());   // <- the whole idea
        } else {
            live.add(lease.instance());
        }
    }
    ...
}""",
        narration=(
            "Now the registry, and most of it is deliberately boring. "
            "[[slnc 300]] Registering is putting an entry in a map. Deregistering "
            "is removing one. A heartbeat is putting the same entry back with a "
            "fresher timestamp. If the class stopped there it would be a phone "
            "book. [[slnc 400]] What makes it a registry is one comparison, and it "
            "lives in the method that answers the question who is running. The "
            "comparison is: take the current time, subtract the time of this "
            "entry's last heartbeat, and if the difference is bigger than the "
            "lease, throw the entry away. [[slnc 350]] In this project the lease "
            "is three thousand milliseconds. [[slnc 300]] Ask yourself why a "
            "registration needs to expire at all. Instances deregister when they "
            "shut down, so why not trust them? [[slnc 350]] Because a program "
            "that has crashed cannot send a message saying it has crashed. The "
            "registry cannot detect death. It can only notice silence — and "
            "silence is the one thing a dead process is extremely reliable at "
            "producing. [[slnc 350]] Two small details worth hearing. The expiry "
            "happens when somebody asks, not on a timer, so there is no "
            "background thread anywhere in this project. And a heartbeat from an "
            "instance the registry has never heard of does nothing at all, "
            "quietly, because otherwise a stray heartbeat could walk a "
            "deregistered instance back onto the list."
        ),
    ),
    dict(
        key="10-client-code",
        kind="code",
        title="The Caller — Ask, Then Try The Next One",
        body="""public Money price(String sku) {
    List<ServiceInstance> candidates = registry.instances("Pricing");

    for (ServiceInstance instance : candidates) {
        try {
            return cluster.endpoint(instance).invoke(sku);
        } catch (ServiceUnavailableException e) {
            log.note("Client", "STALE", instance.instanceId()
                    + " was on the list but is not answering");
            lastFailure = e;
        }
    }
    throw lastFailure;      // everything offered is down: an honest answer
}""",
        narration=(
            "And here is the caller. There are two separate behaviours in this "
            "short method and it is worth pulling them apart. [[slnc 350]] The "
            "first is discovery. Ask the registry who is running, then call one of "
            "them. Notice when the asking happens: at the top of every single "
            "call, not once when the program starts. That matters more than it "
            "looks. A client that looks the list up once and keeps it for the life "
            "of the process has reinvented the hardcoded address with extra steps. "
            "[[slnc 400]] The second behaviour is the loop. If the instance it was "
            "given does not answer, it notes the word stale, and it moves down the "
            "list to the next name. [[slnc 350]] That is the taxi driver who has "
            "been called away. It is a loop and a caught exception, and it is the "
            "difference between discovery that works and discovery that only works "
            "on good days. [[slnc 350]] And look at the last line, because it is "
            "also a decision. When every instance it was offered is dead, the "
            "client fails. It does not hang, and it does not invent a price. "
            "Everything is down is a real answer, and the client is allowed to "
            "give it."
        ),
    ),
    dict(
        key="11-timeline",
        kind="console",
        title="A Deployment, and a Scale-Up, With a Registry",
        body="""==================================================================
2. The same deployment, with a registry
==================================================================
  before the deploy: £449.99
  after the deploy:  £449.99
  after scaling up:  £449.99
      0ms ->     0ms  Registry         REGISTER  pricing-1, pricing-2, pricing-3
      0ms ->     0ms  Client           LOOKUP    3 Pricing instance(s) offered
      0ms ->    10ms  pricing-1        OK        £449.99
     10ms ->    10ms  Registry         DEREGISTER pricing-1 left cleanly
     10ms ->    10ms  Client           LOOKUP    2 Pricing instance(s) offered
     10ms ->    20ms  pricing-2        OK        £449.99
     20ms ->    20ms  Registry         REGISTER  pricing-4 (10.0.1.148:8084)
     20ms ->    20ms  Client           LOOKUP    3 Pricing instance(s) offered
     20ms ->    30ms  pricing-2        OK        £449.99

  no code changed, no restart, no configuration edit.""",
        narration=(
            "Now the same deployment, with a registry in place. [[slnc 300]] "
            "Follow the number of instances offered, because that number is the "
            "whole story. [[slnc 300]] The first lookup is offered three "
            "instances, and the price comes back in ten milliseconds. [[slnc 250]] "
            "Then the deployment happens. Pricing one shuts down politely this "
            "time, so on the way out it takes itself off the list. The next lookup "
            "is offered two, and pricing two answers. [[slnc 300]] Then a fourth "
            "instance starts up for a busy Friday and registers itself. The lookup "
            "after that is offered three again. [[slnc 400]] Three, then two, then "
            "three. A deployment and a scale-up, and the price came back correctly "
            "every single time. [[slnc 350]] And here is the line that is the "
            "actual return on the pattern: no code changed, no restart, no "
            "configuration edit. Nobody was paged. Nobody noticed. [[slnc 300]] "
            "The mechanical cost of all that is one extra message per call, the "
            "one that asks the registry who is running."
        ),
    ),
    dict(
        key="12-stale",
        kind="console",
        title="The Half That Gets Skipped: A Crash",
        body="""==================================================================
3. A crash: the registry is wrong for a few seconds
==================================================================
  price still answered: £449.99
      0ms ->     0ms  Pricing          CRASHED   pricing-1 died without deregistering
      0ms ->     0ms  Client           LOOKUP    2 Pricing instance(s) offered
      5ms ->     5ms  Client           STALE     pricing-1 was on the list but is not answering
      5ms ->    15ms  pricing-2        OK        £449.99

  a client that trusted the first address would have failed here.
  This one tried the next name on the list.""",
        narration=(
            "And now the half that usually gets skipped. [[slnc 300]] This time "
            "pricing one does not shut down politely. The process simply dies. No "
            "deregistration, because there is nobody left to send it. "
            "[[slnc 350]] So the client asks the registry who is running, and it "
            "is offered two instances. [[slnc 300]] Listen to that again. It is "
            "offered two instances, and the first one is dead. The registry is not "
            "wrong because somebody wrote it badly. It is wrong because it cannot "
            "be right. [[slnc 400]] The client calls that first instance, gets "
            "nothing, writes the word stale into its log, and moves down the list. "
            "Pricing two answers, and the shopper gets a price. [[slnc 350]] "
            "Count the cost of the crash: five milliseconds, and a line in a log. "
            "[[slnc 300]] Without that loop it would have cost an outage — the "
            "same outage we saw at the start, from the pattern that was supposed "
            "to have fixed it. [[slnc 350]] Which is why I said this is a pair "
            "rather than one idea. A registry without a caller that copes with "
            "stale entries fails every time an instance dies, and dying instances "
            "are precisely the situation it was introduced for."
        ),
    ),
    dict(
        key="13-lease",
        kind="console",
        title="The Lease Expires, and the List Corrects Itself",
        body="""==================================================================
4. The lease expires and the list corrects itself
==================================================================
  immediately after the crash: 2 listed
  1s later: 2 listed
  2s later: 2 listed
  3s later: 2 listed
  4s later: 1 listed
      0ms ->     0ms  Pricing          CRASHED   pricing-1 died without deregistering
   4000ms ->  4000ms  Registry         EXPIRED   pricing-1 missed its heartbeats

  the lease is 3000ms, so the wrong answer lasted a few seconds
  and then stopped. That window is the price of the pattern.""",
        narration=(
            "So how long is the registry wrong for? [[slnc 300]] This is the act "
            "with no caller in it at all. Time simply passes, one second at a "
            "time, and we ask the registry how many instances it lists. "
            "[[slnc 300]] Immediately after the crash: two. One second later: "
            "still two. Two seconds: two. Three seconds: two. Four seconds later: "
            "one. [[slnc 400]] For three full seconds the registry confidently "
            "names a dead process, because the living instance keeps renewing its "
            "lease and the dead one cannot. On the fourth second the dead lease "
            "expires unrenewed, the entry is dropped, and the list becomes true "
            "again. [[slnc 400]] That window is the honest price of this pattern, "
            "and I want to be straight about it, because every real registry has "
            "one. Eureka has it. Consul has it. The endpoints controller in "
            "Kubernetes has it. [[slnc 350]] You can make the window shorter by "
            "sending heartbeats more often, and then every instance spends more of "
            "its life telling a registry that it is alive. That is a real trade "
            "and you can pick either side of it. [[slnc 350]] What you cannot do "
            "is make it zero, because the only message that would close the window "
            "is the one a crashed process cannot send. [[slnc 300]] So the right "
            "response is not to tune the lease until the problem goes away. It is "
            "to write callers that expect to be handed a bad address now and then."
        ),
    ),
    dict(
        key="14-proof",
        kind="code",
        title="What the Tests Pin Down",
        body="""@Test void aNewInstanceIsFoundWithoutAnyCodeOrConfigurationChange()

@Test void aPoliteShutdownRemovesTheInstanceImmediately()

@Test void aCrashedInstanceStaysOnTheListBecauseItCouldNotSaySoItself()

@Test void aStaleEntryIsHandedOutAndTheClientCopesByTryingTheNextOne()

@Test void aLeaseIsStillGoodOnItsLastMillisecond()

@Test void theRegistryIsConsultedOnEveryCallRatherThanOnce()

@Test void andAnOrdinaryDeploymentTakesItDown()      // the naive client

// 19 tests, no Thread.sleep, and the clock is simulated""",
        narration=(
            "The tests are worth a minute, because of what they choose to assert. "
            "[[slnc 300]] Both clients return four hundred and forty nine pounds "
            "ninety nine. So a test that checked the price would pass on the "
            "hardcoded version too, and would prove nothing at all. [[slnc 350]] "
            "Instead the tests pin the behaviours that only discovery gives you. "
            "That a new instance is found with no code or configuration change. "
            "That a polite shutdown takes effect immediately. That a crashed "
            "instance stays on the list, because it could not say otherwise — yes, "
            "there is a test asserting that the registry is wrong, on purpose. "
            "[[slnc 350]] That a stale entry is handed out and the caller copes by "
            "trying the next one. That a lease is still good on its very last "
            "millisecond, which is the kind of boundary that quietly drifts. And "
            "that the registry is consulted on every call rather than once. "
            "[[slnc 350]] There is also a test pinning the naive client's failure, "
            "so the comparison cannot rot silently as the project changes. "
            "[[slnc 300]] Nineteen tests, and not one of them calls sleep, even "
            "the ones about a three second lease — because the clock is simulated "
            "and four seconds of waiting is a number added to a counter."
        ),
    ),
    dict(
        key="15-costs",
        kind="bullets",
        title="The Costs, Honestly",
        body=[
            "The registry is a new thing that has to be up.",
            "If nobody can look anything up, nothing can call anything —",
            "so it runs as a cluster, with a last-good list as fallback.",
            "",
            "One more call per request, usually served from a short-lived",
            "cache — staleness reintroduced on purpose, as the lesser evil.",
            "",
            "Nothing is where you left it: which instance answered is a",
            "runtime decision now, so the logs have to say.",
            "",
            "And with one instance that never moves, a constant is",
            "still the right answer.",
        ],
        narration=(
            "Now the costs, because a pattern presented without them is a sales "
            "pitch. [[slnc 350]] First, the registry is a new thing that has to be "
            "up. If it goes down and nobody can look anything up, then nothing can "
            "call anything, which is a worse failure than the one we started with. "
            "That is why real registries are run as a cluster of several nodes, and "
            "why real clients usually keep the last good list they were given as a "
            "fallback. [[slnc 350]] Which leads to the second cost, and it is an "
            "uncomfortable one. That fallback deliberately reintroduces staleness. "
            "Caching the list for a second or two is normal and sensible, and it "
            "means you are knowingly choosing to sometimes be wrong, because the "
            "alternative is being unavailable. The loop in the caller is what makes "
            "that choice affordable. [[slnc 400]] Third: nothing is where you left "
            "it. Which instance served a request is no longer something you can "
            "read out of a configuration file — it is a decision taken at runtime. "
            "That is the whole point, and it means your logs have to record which "
            "instance answered, or debugging becomes guesswork. [[slnc 400]] And "
            "finally, the honest one. If a service has exactly one instance, "
            "started by hand, that never moves, then a constant is the right answer "
            "and a registry is theatre. [[slnc 300]] The pattern earns its keep the "
            "moment the number of instances stops being one — or, in practice, the "
            "first time anybody wants to deploy without downtime."
        ),
    ),
    dict(
        key="16-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that deletes",
            "the loop from the caller, passes every deployment test,",
            "and falls over the first time something crashes.",
        ],
        narration=(
            "That's the service discovery pattern. [[slnc 250]] The full source, "
            "the written notes, the diagrams and an animated walkthrough are all in "
            "the repository, and everything runs offline with nothing installed but "
            "a Java development kit — no Docker, no Consul, no Kubernetes. "
            "[[slnc 300]] If you try one exercise, try this one. Delete the loop "
            "from the caller, so that it uses only the first instance the registry "
            "offers, and then run the tests. [[slnc 300]] Watch which ones fail. "
            "Every deployment test still passes. Only the crash tests break. "
            "[[slnc 350]] That is exactly the trap a real system falls into, "
            "because deployments happen constantly while you are testing, and "
            "crashes do not. You can ship a registry that looks perfect for months "
            "and fails the first night something dies badly. [[slnc 300]] It takes "
            "two minutes, and it is the moment that trying the next name stops "
            "being advice and becomes code. [[slnc 300]] If this helped, a like "
            "genuinely does help other people find it, and subscribe if you would "
            "like the rest of the series. [[slnc 250]] Thanks for watching, and "
            "I'll see you in the next one."
        ),
    ),
]
