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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Service Discovery pattern, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Instead of writing a '
            "service's address into the code that calls it, you keep a "
            'shared list of who is running right now. [[slnc 300]] The '
            'caller asks that list every time it needs an address. [[slnc '
            '300]] Programs add themselves to the list when they start, '
            'and drop off it when they stop. [[slnc 600]] Think of a taxi '
            "rank. [[slnc 300]] You do not need to know any driver's "
            'name. [[slnc 300]] You just take whoever is at the front. '
            '[[slnc 700]] In our online store, the pricing service runs '
            'as several copies. [[slnc 300]] And checkout has to reach '
            'one of them. [[slnc 500]] By the end, you will know why a '
            'written-down address turns an ordinary release into an '
            'outage. [[slnc 300]] What a lease is, and why a registration '
            'must expire. [[slnc 300]] And why the list is always wrong '
            'for a few seconds at a time, and what a caller must do about '
            'it.'
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
            "Here is the scenario. [[slnc 400]] The shop's pricing "
            'service is busy. [[slnc 300]] So it runs as three copies of '
            'the same program, on three machines. [[slnc 600]] The three '
            'copies are interchangeable. [[slnc 300]] Any of them can '
            'answer any question. [[slnc 300]] And they all give the same '
            'answer. [[slnc 300]] The price of an espresso machine does '
            'not depend on which machine you ask. [[slnc 600]] Now '
            'checkout needs a price. [[slnc 300]] To ask for one, it '
            'needs an address. [[slnc 500]] So which of the three does it '
            'call? [[slnc 300]] And how does it find out?'
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
            'The obvious answer is to write the address down. [[slnc '
            '300]] Every system starts this way, and starting there is '
            'right. [[slnc 600]] The class in the project is called the '
            'hard-coded pricing client. [[slnc 300]] It holds one name, '
            'pricing one, and calls it. [[slnc 300]] That is the whole '
            'class. [[slnc 600]] There is no bug in it. [[slnc 300]] It '
            'is fast, simple, and cannot be misconfigured. [[slnc 300]] '
            'Every test you would write against it passes. [[slnc 300]] '
            'When the shop had one pricing copy, this was exactly right. '
            '[[slnc 600]] So keep that in mind as we break it. [[slnc '
            '300]] What goes wrong is not a mistake. [[slnc 300]] It is '
            'the world changing under a decision that was correct when it '
            'was made.'
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
            'First demo: somebody releases a new version of pricing. '
            '[[slnc 400]] A rolling release stops the first copy, so it '
            'can be replaced. [[slnc 300]] That is not a fault. [[slnc '
            '300]] It is an ordinary afternoon. [[slnc 600]] And checkout '
            'is now down. [[slnc 300]] Not slow. [[slnc 300]] Down. '
            '[[slnc 300]] It asks for a price, and gets nothing back. '
            '[[slnc 300]] And it will keep getting nothing, until '
            'somebody changes the code. [[slnc 600]] Here is the painful '
            'part. [[slnc 300]] At that exact moment, pricing two and '
            'pricing three are up, healthy, and idle. [[slnc 300]] The '
            'client cannot use either of them. [[slnc 500]] It was told '
            'about one machine, once. [[slnc 300]] And it has no way of '
            'ever learning about another.'
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
            'The damage is wider than one outage. [[slnc 500]] A routine '
            'release takes the caller down. [[slnc 300]] Adding capacity '
            'does nothing: start a fourth copy for a busy Friday, and no '
            'caller will ever use it. [[slnc 300]] And a crash has no '
            'fallback, because there is nothing to fall back to. [[slnc '
            '600]] But none of those is the real diagnosis. [[slnc 300]] '
            'Here it is. [[slnc 500]] The set of running copies changes '
            'several times a day. [[slnc 300]] With every release, every '
            "scale-up, and every crash. [[slnc 300]] But the callers' "
            'code only changes every couple of weeks. [[slnc 300]] A '
            'fast-changing fact has been stored in a slow-changing place. '
            '[[slnc 600]] That is why moving the address into a settings '
            'file does not really help. [[slnc 300]] A person still has '
            'to edit the file, restart the program, and most of all, '
            'notice.'
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
            'Here is the pattern, as it is usually stated. [[slnc 400]] '
            'Each copy registers itself with a registry when it starts. '
            '[[slnc 300]] It renews that registration regularly. [[slnc '
            '300]] And it removes itself when it stops. [[slnc 300]] '
            'Callers ask the registry for the current copies of a '
            'service. [[slnc 600]] In plain words: do not write the '
            'address down. [[slnc 300]] Ask, every time. [[slnc 600]] And '
            'there is a second half, which most descriptions leave out. '
            '[[slnc 300]] Be ready to be told something wrong. [[slnc '
            '600]] The first half fixes a lot. [[slnc 300]] A new copy is '
            'reachable the moment it starts. [[slnc 300]] A polite '
            'shutdown is invisible to callers. [[slnc 300]] Adding '
            'capacity works. [[slnc 300]] Nobody edits anything. [[slnc '
            '600]] But it cannot fix one thing. [[slnc 300]] A program '
            'that has crashed cannot send a message saying it has '
            'crashed. [[slnc 300]] So for a few seconds after a crash, '
            'the list will hand out the address of something that is '
            'gone. [[slnc 300]] That is not a flaw in any registry. '
            '[[slnc 300]] It is the nature of the problem.'
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
            'Here is the analogy: a taxi rank. [[slnc 500]] One way to '
            'get a taxi is to keep the phone number of a driver called '
            'Dave. [[slnc 300]] That works well, until the evening Dave '
            'is off. [[slnc 300]] Then it keeps not working, while eleven '
            'other drivers in town would happily take you. [[slnc 300]] '
            'Because your phone only knows about Dave. [[slnc 600]] The '
            "other way is a taxi rank. [[slnc 300]] You know no driver's "
            'name. [[slnc 300]] You just take whoever is at the front. '
            '[[slnc 300]] Drivers join the rank when their shift starts, '
            'and leave when it ends. [[slnc 300]] And you never need to '
            'learn anything. [[slnc 500]] The rank is the registry. '
            '[[slnc 300]] The drivers are the copies of the service. '
            '[[slnc 600]] And here is the detail that matters. [[slnc '
            '300]] What if you get into a car whose driver has just been '
            'called away? [[slnc 300]] You do not stand there insisting. '
            '[[slnc 300]] You take the next one. [[slnc 500]] Remember '
            'that. [[slnc 300]] In the code, it is a tiny loop, and '
            'without it the whole pattern fails exactly when you need it.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "Let's name the pieces. [[slnc 500]] First, the caller, "
            'called the discovering pricing client. [[slnc 300]] It holds '
            'the registry, not an address. [[slnc 300]] That one '
            'difference is the whole pattern. [[slnc 500]] Second, the '
            'registry. [[slnc 300]] It keeps one entry per running copy. '
            '[[slnc 300]] Each entry is a lease, with a timestamp. [[slnc '
            '500]] Third, that lease. [[slnc 300]] A tiny record of the '
            'copy, and the time of its last heartbeat. [[slnc 300]] A '
            'heartbeat is a regular message saying: I am still alive. '
            '[[slnc 300]] The lease is what lets the registry forget. '
            '[[slnc 500]] Fourth, the pricing copies themselves. [[slnc '
            '300]] Notice the direction. [[slnc 300]] The copies announce '
            'themselves to the registry. [[slnc 300]] Nothing ever calls '
            'out to a service to ask if it is alive. [[slnc 300]] Because '
            'to do that, the registry would need a list of everyone, '
            'which is the original problem again. [[slnc 600]] And kept '
            'beside the pattern, for comparison, is the hard-coded '
            'client.'
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
            'Now the registry, and most of it is deliberately boring. '
            '[[slnc 500]] Registering adds an entry to a list. [[slnc '
            '300]] Removing takes one out. [[slnc 300]] A heartbeat puts '
            'the same entry back, with a fresher time. [[slnc 300]] If it '
            'stopped there, it would just be a phone book. [[slnc 600]] '
            'What makes it a registry is one check. [[slnc 300]] When '
            'someone asks who is running, it looks at each entry. [[slnc '
            '300]] How long since its last heartbeat? [[slnc 300]] If it '
            'is longer than the lease, the entry is thrown away. [[slnc '
            '300]] In this project, the lease is three seconds. [[slnc '
            '600]] Why must a registration expire at all? [[slnc 300]] '
            'Copies remove themselves when they shut down, so why not '
            'trust them? [[slnc 500]] Because a crashed program cannot '
            'say it has crashed. [[slnc 300]] The registry cannot detect '
            'death. [[slnc 300]] It can only notice silence. [[slnc 300]] '
            'And a dead program is very reliable at being silent. [[slnc '
            '600]] One more detail. [[slnc 300]] The expiry check happens '
            'when someone asks, not on a timer. [[slnc 300]] So there is '
            'no background thread anywhere in this project.'
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
            'Here is the caller. [[slnc 300]] It has two separate '
            'behaviours. [[slnc 600]] The first is discovery. [[slnc '
            '300]] Ask the registry who is running, then call one of '
            'them. [[slnc 300]] And notice when it asks: on every single '
            'call, not once at startup. [[slnc 500]] That matters. [[slnc '
            '300]] A client that looks up the list once, and keeps it '
            'forever, has just rebuilt the hard-coded address with extra '
            'steps. [[slnc 600]] The second behaviour is the loop. [[slnc '
            '300]] If the copy it was given does not answer, it logs the '
            'word stale. [[slnc 300]] And it moves on to the next name on '
            'the list. [[slnc 500]] That is the taxi driver who has been '
            'called away. [[slnc 300]] It is a loop and a caught error. '
            '[[slnc 300]] And it is the difference between discovery that '
            'works, and discovery that only works on good days. [[slnc '
            '600]] And at the end, if every copy it was offered is dead, '
            'the client fails. [[slnc 300]] It does not hang, and it does '
            'not invent a price. [[slnc 300]] Everything is down is a '
            'real answer.'
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
            'Second demo: the same release, with a registry. [[slnc 400]] '
            'Listen to how many copies are offered each time. [[slnc '
            '300]] That number tells the whole story. [[slnc 600]] The '
            'first lookup is offered three copies. [[slnc 300]] The price '
            'comes back in ten milliseconds. [[slnc 500]] Then the '
            'release happens. [[slnc 300]] Pricing one shuts down '
            'politely, and removes itself from the list on the way out. '
            '[[slnc 300]] The next lookup is offered two, and pricing two '
            'answers. [[slnc 500]] Then a fourth copy starts for a busy '
            'Friday, and registers itself. [[slnc 300]] The next lookup '
            'is offered three again. [[slnc 600]] Three, then two, then '
            'three. [[slnc 300]] A release and a scale-up, and the price '
            'came back correctly every time. [[slnc 500]] No code '
            'changed. [[slnc 300]] No restart. [[slnc 300]] No settings '
            'edited. [[slnc 300]] Nobody was called out. [[slnc 300]] '
            'Nobody noticed.'
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
            'Third demo, and this is the half that usually gets skipped. '
            '[[slnc 400]] This time, pricing one does not shut down '
            'politely. [[slnc 300]] The program simply crashes. [[slnc '
            '300]] It does not remove itself, because there is nobody '
            'left to do it. [[slnc 600]] The client asks the registry who '
            'is running. [[slnc 300]] It is offered two copies. [[slnc '
            '300]] And the first one is dead. [[slnc 500]] The registry '
            'is not wrong because it was badly written. [[slnc 300]] It '
            'is wrong because it cannot be right. [[slnc 600]] The client '
            'calls the first copy, and gets nothing. [[slnc 300]] It logs '
            'the word stale, and moves on. [[slnc 300]] Pricing two '
            'answers, and the shopper gets a price. [[slnc 500]] The '
            'crash cost five milliseconds, and one line in a log. [[slnc '
            '300]] Without that loop, it would have cost an outage. '
            '[[slnc 600]] So a registry and a caller that copes with '
            'wrong entries are a pair. [[slnc 300]] Without the loop, the '
            'registry fails every time a copy dies. [[slnc 300]] Which is '
            'exactly the situation it was meant for.'
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
            'Fourth demo: how long is the registry wrong for? [[slnc '
            '400]] There is no caller in this demo. [[slnc 300]] Time '
            'just passes, one second at a time, and we ask how many '
            'copies the registry lists. [[slnc 600]] Right after the '
            'crash: two. [[slnc 300]] One second later: still two. [[slnc '
            '300]] Two seconds: two. [[slnc 300]] Three seconds: two. '
            '[[slnc 300]] Four seconds later: one. [[slnc 600]] For three '
            'whole seconds, the registry names a dead program. [[slnc '
            '300]] The living copy keeps renewing its lease, and the dead '
            'one cannot. [[slnc 300]] On the fourth second, the dead '
            'lease expires, and the list becomes true again. [[slnc 600]] '
            'That gap is the honest price of this pattern. [[slnc 300]] '
            'Every real registry has one: Eureka, Consul, and Kubernetes '
            'too. [[slnc 500]] You can shorten the gap by sending '
            'heartbeats more often. [[slnc 300]] But then every copy '
            'spends more time saying it is alive. [[slnc 300]] You cannot '
            'make it zero. [[slnc 300]] Because the one message that '
            'would close the gap is the one a crashed program cannot '
            'send. [[slnc 500]] So do not try to tune the problem away. '
            '[[slnc 300]] Write callers that expect a bad address now and '
            'then.'
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
            'The tests are worth a moment, because of what they choose to '
            'check. [[slnc 500]] Both clients return the same price. '
            '[[slnc 300]] So a test that only checked the price would '
            'pass on the hard-coded version too. [[slnc 300]] And prove '
            'nothing. [[slnc 600]] Instead, the tests check what only '
            'discovery gives you. [[slnc 300]] A new copy is found, with '
            'no code or settings change. [[slnc 300]] A polite shutdown '
            'takes effect at once. [[slnc 300]] A crashed copy stays on '
            'the list, because it could not say otherwise. [[slnc 300]] '
            'Yes, one test deliberately checks that the registry is '
            'wrong. [[slnc 500]] A wrong entry is handed out, and the '
            'caller copes by trying the next one. [[slnc 300]] A lease is '
            'still valid on its very last millisecond. [[slnc 300]] And '
            'the registry is asked on every call, not just once. [[slnc '
            '600]] Nineteen tests, and not one of them waits. [[slnc '
            '300]] Even the ones about a three-second lease. [[slnc 300]] '
            'Because the clock is simulated.'
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
            'Now the costs, because a pattern without its costs is a '
            'sales pitch. [[slnc 600]] First, the registry is a new thing '
            'that must stay up. [[slnc 300]] If nobody can look anything '
            'up, nothing can call anything. [[slnc 300]] That is worse '
            'than where we started. [[slnc 300]] So real registries run '
            'as several servers. [[slnc 300]] And real clients keep the '
            'last good list, as a fallback. [[slnc 600]] Second, that '
            'fallback deliberately brings back out-of-date answers. '
            '[[slnc 300]] Keeping the list for a second or two is normal '
            'and sensible. [[slnc 300]] You are choosing to be sometimes '
            "wrong, rather than unavailable. [[slnc 300]] The caller's "
            'loop is what makes that choice safe. [[slnc 600]] Third, '
            'nothing is where you left it. [[slnc 300]] Which copy served '
            'a request is decided while the program runs. [[slnc 300]] So '
            'your logs must record which copy answered, or debugging '
            'becomes guesswork. [[slnc 600]] And finally, the honest one. '
            '[[slnc 300]] If a service has exactly one copy, started by '
            'hand, that never moves, a written-down address is the right '
            'answer. [[slnc 300]] The pattern earns its keep the moment '
            'there is more than one copy. [[slnc 300]] Or the first time '
            'anyone wants to release without downtime.'
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
            "That's the Service Discovery pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Do not '
            'write the address down, ask every time, and be ready to be '
            'told wrong, by trying the next name on the list. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 300]] '
            'It runs offline, with nothing installed except a Java '
            'development kit. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Delete the loop from the caller, so it only '
            'uses the first copy it is offered. [[slnc 300]] Then run the '
            'tests. [[slnc 300]] Every release test still passes. [[slnc '
            '300]] Only the crash tests fail. [[slnc 500]] That is the '
            'real trap. [[slnc 300]] Releases happen all the time while '
            'you test, but crashes do not. [[slnc 300]] So a registry can '
            'look perfect for months, and fail the first night something '
            'crashes. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
