"""Scene definitions for the Leader Election with Kubernetes teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of Kubernetes' words in plain
language before using its name, and never points at a picture the listener
cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Leader Election with Kubernetes',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Leader Election pattern in Java, using a real Kubernetes '
            'cluster. [[slnc 300]] This video is presented by Jayasekhar '
            'Konduru. [[slnc 600]] First, a simple definition. [[slnc '
            '300]] When several copies of a program are running, leader '
            'election lets them agree that exactly one of them does a '
            'job. [[slnc 300]] One copy holds a lease: a claim that runs '
            'out unless it is renewed. [[slnc 300]] The others wait, and '
            'take the lease if the renewals stop. [[slnc 700]] In our '
            'online store, the shop runs three copies of its reporting '
            'service. [[slnc 300]] So one can crash without the service '
            'going away. [[slnc 300]] Every night, exactly one of them '
            'must send the manager the sales report. [[slnc 300]] Not '
            'three reports, and not none. [[slnc 500]] By the end, you '
            'will hear a real Kubernetes server refuse a write. [[slnc '
            '300]] A dead leader leave nobody in charge for a whole '
            'lease. [[slnc 300]] A frozen leader wake up and send the '
            'report after losing its lease. [[slnc 300]] And the one '
            'check that stops it.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Three copies of the reporting service.', 'Three separate processes.', '',
              'One nightly sales report.', 'Exactly one copy must send it.', '',
              'The plain-Java project kept the lease', 'in one object, with a pretend clock.', '',
              'This time the lease lives in a real', 'Kubernetes server, and time is real.'],
        narration=(
            'Here is the scenario. [[slnc 400]] The reporting service '
            'runs as three copies, called A, B, and C. [[slnc 300]] Each '
            'copy is a separate program. [[slnc 300]] Every night, '
            'exactly one of them must send the sales report. [[slnc 600]] '
            'The plain Java version already solved this with a lease. '
            '[[slnc 300]] But its lease was an object inside one program, '
            'with a clock that only moved when the program said so. '
            '[[slnc 500]] This time, the lease lives in a real Kubernetes '
            'server. [[slnc 300]] The copies are real programs. [[slnc '
            '300]] And the clock is the real one. [[slnc 300]] That '
            'changes three things.'
        ),
    ),
    dict(
        key='03-one', kind='console', title='Three Copies, Nobody In Charge',
        body="""ONE. Three copies, nobody in charge.
  3 separate processes.
  none of them asks who is in charge.

  the nightly sales report is sent by
  every copy: [A, B, C].

  the manager receives it 3 times.""",
        narration=(
            'First demo: three copies, and nobody in charge. [[slnc 400]] '
            'Three copies start, as three separate programs. [[slnc 300]] '
            'None of them asks who is in charge. [[slnc 500]] Each is '
            'told to send the nightly sales report. [[slnc 300]] And each '
            'one does. [[slnc 300]] A sends it, B sends it, and C sends '
            'it. [[slnc 500]] The manager receives the same report three '
            'times.'
        ),
    ),
    dict(
        key='04-words', kind='bullets', title="Kubernetes' Words",
        body=['A cluster: machines Kubernetes runs on.', 'The API server: the notice board.', '',
              'A Lease: one note on the board.', '  holder, 5 seconds, last renewal,',
              '  and how many times the holder changed.', '',
              'Every note has a version number.', 'A write from an old version is refused:',
              '  409 Conflict.', '',
              'The server never takes a note down.'],
        narration=(
            'Before the next demo, some words, through an everyday '
            'picture. [[slnc 400]] Imagine a staff room with a notice '
            'board. [[slnc 300]] On it is one note, saying who does '
            "tonight's job, and until when. [[slnc 300]] The person named "
            'on it rewrites the time every few minutes. [[slnc 300]] If '
            'the time on the note has passed, anyone else may cross the '
            'name out, and write their own. [[slnc 600]] In Kubernetes, '
            'the group of machines is called a cluster. [[slnc 300]] The '
            'notice board is a program called the A P I server. [[slnc '
            '300]] It stores records, and lets others read and write '
            'them. [[slnc 300]] The note is called a Lease. [[slnc 300]] '
            'The name on it is the holder. [[slnc 300]] And rewriting the '
            'time is called renewing. [[slnc 300]] Our lease lasts five '
            'seconds without a renewal. [[slnc 600]] Every note also has '
            'a version number, which goes up with each write. [[slnc '
            '300]] If you try to write based on an old version, the '
            'server refuses you. [[slnc 300]] That refusal is called a '
            'conflict. [[slnc 600]] And one thing the board never does. '
            '[[slnc 300]] It never takes a note down because it is old. '
            '[[slnc 300]] It does not look at the clock at all.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='One Holds The Lease',
        body="""TWO. One holds the lease.
  it says: holder A, lasts 5 seconds,
  holder changes 0.
  A renews it every 1 second.
  each is told the leader is A.

  the report was sent by: [A].

  two writes from the same version:
  the first is accepted, the second
  refused with 409 Conflict.""",
        narration=(
            'Second demo: one copy holds the lease. [[slnc 400]] A starts '
            'first, finds no lease, and writes one with its own name. '
            '[[slnc 300]] The lease says: holder A, lasting five seconds. '
            '[[slnc 300]] A renews it every second. [[slnc 500]] B and C '
            'start next. [[slnc 300]] They read the lease, see it is '
            'fresh, and are told the leader is A. [[slnc 500]] All three '
            'are asked to send the report. [[slnc 300]] Only A sends it. '
            '[[slnc 600]] Then two writes are made to the lease, both '
            'based on the same version. [[slnc 300]] The first is '
            'accepted. [[slnc 300]] The second is refused, with a '
            'conflict, because its version is out of date. [[slnc 500]] '
            'That refusal is what stops two copies winning at the same '
            'moment. [[slnc 300]] And it is the only rule the server '
            'enforces.'
        ),
    ),
    dict(
        key='06-config', kind='code', title="The Elector's Settings",
        body="""client.leaderElector()
  .withConfig(new LeaderElectionConfigBuilder()
    .withLock(new LeaseLock(
        "default", lease, name))
    .withLeaseDuration(ofSeconds(5))
    .withRenewDeadline(ofSeconds(4))
    .withRetryPeriod(ofSeconds(1))
    .withReleaseOnCancel(true)
    .withLeaderCallbacks(new LeaderCallbacks(
        onStart, onStop, onNewLeader))
    .build())
  .build().start();""",
        narration=(
            'The copies do not do this by hand. [[slnc 300]] They use a '
            'library called Fabric8, which talks to Kubernetes from Java. '
            '[[slnc 300]] It has a built-in elector: the part that keeps '
            'asking for the lease, and keeps renewing it. [[slnc 600]] It '
            'takes four settings. [[slnc 300]] The lease lasts five '
            'seconds. [[slnc 300]] The holder stops leading if it cannot '
            'renew for four seconds. [[slnc 300]] Everyone asks again '
            'every second. [[slnc 300]] And on a clean shutdown, the '
            'holder hands the lease back. [[slnc 500]] Then the elector '
            'tells the copy three things. [[slnc 300]] You now lead. '
            '[[slnc 200]] You no longer lead. [[slnc 200]] And someone '
            'new leads.'
        ),
    ),
    dict(
        key='07-three', kind='console', title='The Leader Stops',
        body="""THREE. The leader stops.
  A is shut down cleanly. its elector
  hands the lease back.
  one of B and C took over within a
  couple of seconds, well inside one
  5-second lease.

  now the new leader is killed outright.
  the last copy took over after about
  one whole 5-second lease.""",
        narration=(
            'Third demo: the leader stops. [[slnc 400]] A is shut down '
            'cleanly. [[slnc 300]] On its way out, its elector hands the '
            "lease back, by clearing the holder's name. [[slnc 300]] B or "
            'C sees the empty lease at its next check. [[slnc 300]] And '
            'takes over within a couple of seconds. [[slnc 600]] Then the '
            'new leader is killed outright. [[slnc 300]] It gets no '
            'chance to hand anything back. [[slnc 300]] So the lease '
            'still names the dead copy. [[slnc 500]] The last copy must '
            'wait until five seconds have passed since the last renewal, '
            'by its own clock. [[slnc 300]] So it takes over only after '
            'about one whole lease. [[slnc 500]] For that time, nobody '
            'leads. [[slnc 300]] The others cannot tell a dead leader '
            'from a slow one, so they wait. [[slnc 500]] Which copy wins, '
            'and exactly how long it takes, vary slightly from run to '
            'run. [[slnc 300]] So the demo describes them, rather than '
            'counting them.'
        ),
    ),
    dict(
        key='08-diagram', kind='diagram', title='Who Reads The Clock',
        body=None,
        narration=(
            'Here is how the pieces fit, in words. [[slnc 400]] Three '
            'copies, each its own program. [[slnc 300]] And one lease '
            'record in the A P I server, which they all read and write. '
            '[[slnc 600]] The leader, A, rewrites the lease every second. '
            "[[slnc 300]] The lease holds the holder's name, the five "
            'seconds, and the time of the last renewal. [[slnc 500]] B '
            'and C read it. [[slnc 300]] They add five seconds to the '
            'last renewal, and compare that with their own clocks. [[slnc '
            '600]] Notice who reads the clock. [[slnc 300]] Not the '
            'server. [[slnc 300]] Each copy. [[slnc 300]] The server only '
            'stores the note, and checks the version. [[slnc 500]] And '
            "the manager's inbox, where the report goes, sits outside "
            'Kubernetes altogether.'
        ),
    ),
    dict(
        key='09-four', kind='console', title='Two Who Think They Lead',
        body="""FOUR. Two who think they lead.
  A checks that it leads, and starts
  building the report. then A freezes.
  the lease runs out, and B takes it.
  the lease says: holder B,
  holder changes 1.

  the report was sent by: [B, A].
  when A sent, the lease named B,
  renewed after A's last renewal: yes.""",
        narration=(
            'Fourth demo, and this is the one to remember. [[slnc 400]] A '
            'leads, and B waits. [[slnc 300]] A is told to send the '
            'report. [[slnc 300]] It checks that it leads, and it does. '
            '[[slnc 300]] So it starts building the report. [[slnc 600]] '
            "At that moment, A's whole program freezes. [[slnc 300]] "
            'Every thread stops, including the one that renews the lease. '
            '[[slnc 300]] A long memory clean-up in Java can do exactly '
            'that. [[slnc 600]] No renewals arrive. [[slnc 300]] After '
            "five seconds, by B's clock, B takes the lease. [[slnc 300]] "
            'B sends the report. [[slnc 600]] Then A wakes up. [[slnc '
            '300]] It finishes the report it had started, and sends it. '
            '[[slnc 300]] Because when it checked, it was the leader. '
            '[[slnc 500]] The report was sent twice. [[slnc 300]] First '
            'B, then A.'
        ),
    ),
    dict(
        key='10-proof', kind='bullets', title="The Lease's Own Record",
        body=['When A sent, the lease named B.', '',
              "B had renewed it after A's", 'last renewal.', '',
              "A's elector did notice the loss,", 'but only once A woke up.', '',
              'A had checked before it froze.', 'A check is not a promise.'],
        narration=(
            "The lease's own record proves A was wrong. [[slnc 400]] When "
            'A sent its report, the lease already named B. [[slnc 300]] '
            "And B had renewed it after A's last renewal. [[slnc 600]] "
            "A's elector did notice, in the end. [[slnc 300]] When A woke "
            'up, it saw it had missed its deadline, and said A no longer '
            'leads. [[slnc 300]] But the check had already been made. '
            '[[slnc 300]] And the report was already on its way. [[slnc '
            '600]] Nothing on the server could have stopped this. [[slnc '
            '300]] The server never takes a lease away. [[slnc 300]] It '
            'only stores it. [[slnc 500]] A check is not a promise.'
        ),
    ),
    dict(
        key='11-five', kind='console', title='Fencing',
        body="""FIVE. Fencing.
  each report now carries a token:
  the lease's count of holder changes.

  A's token is 0, B's is 1.
  B sends first. A wakes up and tries:
  refused, token 0 is older than 1.

  the report was sent by: [B].""",
        narration=(
            'Fifth demo: fencing. [[slnc 400]] The answer is a number '
            'called a fencing token. [[slnc 500]] When a copy starts '
            "leading, it keeps the lease's count of how many times the "
            'holder has changed. [[slnc 300]] That count only ever goes '
            'up. [[slnc 300]] Every report carries it. [[slnc 300]] And '
            'the inbox remembers the highest one it has seen. [[slnc '
            "600]] A's token is zero. [[slnc 300]] B's token is one. "
            '[[slnc 500]] B sends first, with one. [[slnc 300]] When A '
            'wakes and sends with zero, the inbox refuses it. [[slnc '
            "300]] Zero is older than one. [[slnc 500]] Only B's report "
            'was sent. [[slnc 300]] The lease could not stop A. [[slnc '
            '300]] But the inbox, the thing being written to, could.'
        ),
    ),
    dict(
        key='12-six', kind='console', title='The Bill',
        body="""SIX. The bill.
  B is killed. A's elector gave up
  when it lost the lease.
  two whole leases later the lease still
  names B, and nobody leads.
  A starts a new elector: token 2.

  lease of 5 seconds, renewed every 1.
  judged by each copy's own clock.
  1 cluster, with 1 node, for 1 nightly report.""",
        narration=(
            'Sixth demo: the bill. [[slnc 400]] B is killed. [[slnc 300]] '
            "A is still running. [[slnc 300]] But Fabric8's elector "
            'cannot be restarted. [[slnc 300]] When A lost the lease '
            'earlier, its elector stopped for good. [[slnc 500]] Two '
            'whole leases later, the lease still names the dead B. [[slnc '
            '300]] And nobody leads. [[slnc 500]] A only leads again when '
            'it starts a brand-new elector, with token two. [[slnc 300]] '
            'In Kubernetes, the usual answer is simpler. [[slnc 300]] A '
            'copy that loses the lease exits, and Kubernetes starts it '
            'again. [[slnc 600]] Three more costs. [[slnc 400]] A '
            'five-second lease means a dead leader can go unnoticed for '
            'up to five seconds. [[slnc 300]] A shorter lease lets one '
            'slow moment cost a healthy leader its job. [[slnc 400]] Each '
            'copy judges the lease by its own clock. [[slnc 300]] So '
            'machines whose clocks disagree can take over too early. '
            '[[slnc 400]] And all of it needs a Kubernetes server, just '
            'for one nightly report.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['Right: one leader, the gap after a death,', 'the stale leader, and the token.', '',
              'Left out: nothing on the server', 'takes the lease away.', '',
              'Left out: a real version check,', '  409 Conflict.', '',
              'Left out: the loser leaves the race', 'for good.'],
        narration=(
            'So what did the plain Java version get right? [[slnc 400]] '
            'The whole shape. [[slnc 300]] One leader at a time. [[slnc '
            '200]] A gap when the leader dies. [[slnc 200]] A leader that '
            'wakes up, and acts on an old belief. [[slnc 200]] And a '
            'token as the answer. [[slnc 300]] All of that holds on a '
            'real server. [[slnc 600]] But it left out three things. '
            '[[slnc 500]] First, its lease decided for itself when it had '
            'expired. [[slnc 300]] A real Kubernetes lease never expires '
            'on the server. [[slnc 300]] Each copy decides, with its own '
            'clock. [[slnc 400]] Second, the real server checks the '
            'version on every write, and refuses an old one. [[slnc 400]] '
            'Third, a real elector that loses the lease leaves the race '
            'for good. [[slnc 300]] And someone has to start a new one.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Let the elector renew the lease.', '',
              'Fence every write the leader makes:', 'the receiver checks the token.', '',
              'A copy that loses the lease exits,', 'and Kubernetes restarts it.', '',
              'Pick the lease length on purpose:', 'fast to notice, or hard to lose.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a Kubernetes lease '
            'to pick one copy, and let the elector do the renewing. '
            '[[slnc 500]] Then settle three things, because Kubernetes '
            "will not. [[slnc 500]] One. [[slnc 200]] A leader's belief "
            'that it leads can be out of date at any moment. [[slnc 300]] '
            'So everything it writes must carry a token, and the receiver '
            'must check it. [[slnc 400]] Two. [[slnc 200]] A copy that '
            'loses the lease should exit, and be restarted. [[slnc 300]] '
            'Not stay alive with no way back. [[slnc 400]] Three. [[slnc '
            '200]] The lease length is a choice. [[slnc 300]] Short '
            'notices a dead leader quickly. [[slnc 300]] Long survives a '
            'slow moment. [[slnc 300]] You cannot have both.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['Kubernetes 1.37.0 in a kind cluster', 'the demo creates and deletes itself.',
              'Fabric8 client 8.0.0, three processes.', '',
              'Needs a container runtime and kind.', '',
              'Too much if the job is safe to run', 'twice, or one copy is enough.', '',
              'A cluster for one nightly report.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] This is a '
            'real Kubernetes server, version one point thirty-seven. '
            '[[slnc 300]] It runs in a one-machine cluster, made by a '
            'tool called kind, inside a single container. [[slnc 300]] '
            'The demo creates the cluster at the start, and deletes it at '
            'the end. [[slnc 300]] It never touches your own Kubernetes '
            'settings. [[slnc 300]] You need Docker switched on, and kind '
            'installed. [[slnc 300]] Every number you heard comes from '
            "the program's own output. [[slnc 600]] So, when is this too "
            'much? [[slnc 300]] If the job is safe to run twice, run it '
            'everywhere. [[slnc 300]] If one copy is enough, run one, and '
            'let Kubernetes restart it. [[slnc 300]] A lease only earns '
            'its keep when several copies must run, and exactly one may '
            'act.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Leader Election, with Kubernetes. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] The '
            'lease tells everyone else who leads, but only the thing a '
            'leader writes to can stop a leader that has already lost. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 500]] Here is one exercise to try. [[slnc 300]] Make '
            'a copy exit the moment it loses the lease. [[slnc 300]] Then '
            'work out what would bring it back. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
