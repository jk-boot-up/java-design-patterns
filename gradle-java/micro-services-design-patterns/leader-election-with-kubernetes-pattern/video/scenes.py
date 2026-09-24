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
            'Hello, and welcome. This video explains the Leader Election '
            'pattern in Java, using a real Kubernetes cluster. '
            '[[slnc 250]] It is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] Here is the plain definition, in '
            'general words. When several copies of a program are running, '
            'leader election lets them agree that exactly one of them does '
            'a particular job. One copy holds a lease, which is a claim '
            'that runs out unless it is renewed. The others wait, and take '
            'the lease if the renewals stop. [[slnc 350]] Now the same '
            'thing in our online store. The shop runs three copies of its '
            'reporting service, so that one can crash without the service '
            'going away. Every night, exactly one of them must send the '
            'store manager the sales report. Not three reports, and not '
            'none. [[slnc 300]] By the end you will have seen a real '
            'Kubernetes server refuse a write, a leader that dies leave '
            'nobody in charge for a whole lease, a leader that freezes '
            'wake up and send the report after it has lost the lease, and '
            'the one check that stops it.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Three copies of the reporting service.', 'Three separate processes.', '',
              'One nightly sales report.', 'Exactly one copy must send it.', '',
              'The plain-Java project kept the lease', 'in one object, with a pretend clock.', '',
              'This time the lease lives in a real', 'Kubernetes server, and time is real.'],
        narration=(
            'Here is the scenario. The reporting service runs as three '
            'copies, called A, B and C. Each copy is a separate program, '
            'running on its own. Every night, exactly one of them must send '
            'the sales report. [[slnc 300]] The plain-Java project in this '
            'course already solved this with a lease, but its lease was an '
            'object inside one program, with a clock that only moved when '
            'the program said so. This time the lease lives in a real '
            'Kubernetes server, the copies are real programs, and the clock '
            'is the real one. That changes three things.'
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
            'Act one. Three copies start, as three separate processes. '
            'None of them asks anyone who is in charge. Each is told to '
            'send the nightly sales report, and each one does. A sends it, '
            'B sends it, and C sends it. [[slnc 250]] The manager receives '
            'the same report three times.'
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
            'Before the next act, some words, through a picture from '
            'everyday life. Imagine a staff room with a notice board. On '
            'it is one note that says who is doing tonight\'s job, and '
            'until when. The person named on it rewrites the time every '
            'few minutes. If the time on the note has passed, anyone else '
            'may cross the name out and write their own. [[slnc 300]] In '
            'Kubernetes, the group of machines is called a cluster. The '
            'notice board is a program called the API server, which '
            'stores records and lets others read and write them. The note '
            'is called a Lease. The name on it is the holder. Rewriting '
            'the time is called renewing. Our lease lasts five seconds '
            'without a renewal. [[slnc 300]] Every note also has a '
            'version number that goes up with each write. If you try to '
            'write, and say which version you read, but someone has '
            'written since, the server refuses you. Kubernetes calls '
            'that refusal four oh nine, Conflict. [[slnc 250]] And one '
            'thing the board never does: it never takes a note down '
            'because it is old. It does not look at the clock at all.'
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
            'Act two. A starts first, finds no lease, and writes one with '
            'its own name in it. The lease says: holder A, lasts five '
            'seconds, holder changes zero. A renews it every one second. '
            'B and C start next. They read the lease, see it is fresh, '
            'and each is told that the leader is A. [[slnc 250]] All '
            'three are asked to send the report. Only A sends it. '
            '[[slnc 300]] Then two writes are made to the lease, both '
            'based on the same version of it. The first is accepted. The '
            'second is refused with four oh nine, Conflict, because the '
            'version it was based on is gone. That refusal is what stops '
            'two copies winning at the same moment, and it is the only '
            'rule the server enforces.'
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
            'Each copy does not do this by hand. It uses a library called '
            'Fabric8, which talks to the Kubernetes server from Java, and '
            'which has an elector built in. An elector is the part that '
            'keeps asking for the lease and keeps renewing it. [[slnc 250]] '
            'It takes four settings. The lease lasts five seconds. The '
            'holder gives up leading if it cannot renew for four seconds. '
            'Everyone asks again every one second. And on a clean '
            'shutdown, the holder hands the lease back. [[slnc 250]] Then '
            'three things the elector tells the copy: you now lead, you '
            'no longer lead, and someone new leads.'
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
            'Act three. A is shut down cleanly. On its way out, its '
            'elector hands the lease back by clearing the holder\'s name. '
            'One of B and C sees the empty lease at its next check, and '
            'takes over within a couple of seconds. [[slnc 300]] Then the '
            'new leader is killed outright. It gets no chance to hand '
            'anything back. The lease goes on naming the dead copy. The '
            'last copy has to wait until the last renewal time plus five '
            'seconds has passed on its own clock, so it takes over only '
            'after about one whole five-second lease. [[slnc 250]] For '
            'that time, nobody leads. The others cannot tell a dead leader '
            'from a slow one, so they wait. Which copy wins, and exactly '
            'how long it takes, change a little from run to run, so the '
            'demo describes them rather than counting them.'
        ),
    ),
    dict(
        key='08-diagram', kind='diagram', title='Who Reads The Clock',
        body=None,
        narration=(
            'Here is how the pieces fit, in words. Three copies, each its '
            'own process, and one record in the API server that they all '
            'read and write. [[slnc 250]] The leader, A, rewrites the '
            'lease every second. The lease holds the holder\'s name, the '
            'five seconds, and the time of the last renewal. B and C read '
            'it, add five seconds to the last renewal, and compare the '
            'answer with their own clocks. [[slnc 250]] Notice who reads '
            'the clock. Not the server. Each copy. The server only stores '
            'the note and checks the version. And the manager\'s inbox, '
            'where the report goes, sits outside Kubernetes altogether.'
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
            'Act four, and this is the one to remember. A leads, and B '
            'waits. A is told to send the report. It checks that it '
            'leads, and it does. It starts building the report. At that '
            'moment, A\'s whole process is frozen. Every thread stops, '
            'including the one that renews the lease. That is what a long '
            'pause while Java tidies up its memory can do to a real '
            'program. [[slnc 300]] No renewals arrive. After five seconds '
            'by B\'s clock, B takes the lease. The lease now says holder '
            'B, holder changes one. B sends the report. [[slnc 300]] Then '
            'A wakes up. It finishes the report it had started, and sends '
            'it, because when it checked, it was the leader. The report '
            'was sent twice. B, then A.'
        ),
    ),
    dict(
        key='10-proof', kind='bullets', title="The Lease's Own Record",
        body=['When A sent, the lease named B.', '',
              "B had renewed it after A's", 'last renewal.', '',
              "A's elector did notice the loss,", 'but only once A woke up.', '',
              'A had checked before it froze.', 'A check is not a promise.'],
        narration=(
            'The lease\'s own record proves A was wrong. At the moment A '
            'sent its report, the lease named B as holder, and B had '
            'renewed it after A\'s last renewal. [[slnc 300]] A\'s elector '
            'did notice. When A woke up, the elector saw by its own '
            'stopwatch that it had missed its deadline, and said A no '
            'longer leads. But the check had already been made, and the '
            'report was already on its way. [[slnc 250]] Nothing on the '
            'server could have stopped this. The server never takes a '
            'lease away. It only stores it.'
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
            'Act five. The answer is a number called a fencing token. '
            'When a copy starts leading, it keeps the lease\'s count of '
            'holder changes. That count only ever goes up. Every report '
            'carries it, and the inbox remembers the highest one it has '
            'seen. [[slnc 250]] A\'s token is zero. B\'s is one. B sends '
            'first, with one. When A wakes and sends with zero, the inbox '
            'refuses it: token zero is older than one. [[slnc 250]] The '
            'report was sent by B alone. The lease could not stop A. The '
            'inbox, the thing being written to, could.'
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
            'Act six, the bill. B is killed. A is still running, but '
            'Fabric8\'s elector cannot be restarted. When A lost the '
            'lease, its elector said so and stopped for good. Two whole '
            'leases later, the lease still names the dead B, and nobody '
            'leads. [[slnc 250]] A leads again only when it starts a '
            'brand-new elector, with token two. In Kubernetes the usual '
            'answer is simpler: a copy that loses the lease exits, and '
            'Kubernetes starts it again. [[slnc 300]] Three costs remain. '
            'A five-second lease means a dead leader goes unnoticed for up '
            'to five seconds, and a shorter one lets one slow moment cost '
            'a healthy leader its lease. Each copy judges the lease by its '
            'own clock, so machines whose clocks disagree can take over '
            'too early. And all of it needs a Kubernetes server: one '
            'cluster, with one node, for one nightly report.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['Right: one leader, the gap after a death,', 'the stale leader, and the token.', '',
              'Left out: nothing on the server', 'takes the lease away.', '',
              'Left out: a real version check,', '  409 Conflict.', '',
              'Left out: the loser leaves the race', 'for good.'],
        narration=(
            'So what did the plain-Java project get right? All of the '
            'shape. One leader at a time, a gap when the leader dies, a '
            'leader that wakes up and acts on an old belief, and a token '
            'as the answer. Every one of those holds on a real server. '
            '[[slnc 300]] What did it leave out? First, its lease record '
            'decided for itself when a lease had expired. A real '
            'Kubernetes lease never expires on the server. Each copy '
            'decides, with its own clock. Second, the real server checks '
            'the version on every write, and refuses a stale one. Third, a '
            'real elector that loses the lease leaves the race for good, '
            'and someone has to start a new one.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['Let the elector renew the lease.', '',
              'Fence every write the leader makes:', 'the receiver checks the token.', '',
              'A copy that loses the lease exits,', 'and Kubernetes restarts it.', '',
              'Pick the lease length on purpose:', 'fast to notice, or hard to lose.'],
        narration=(
            'The verdict. Use a Kubernetes lease to pick one copy, and let '
            'the elector do the renewing. Then say three things out loud, '
            'because Kubernetes will not. [[slnc 200]] One. A leader\'s '
            'belief that it leads can be stale at any moment, so '
            'everything it writes must carry a token, and the receiver '
            'must check it. [[slnc 200]] Two. A copy that loses the lease '
            'should exit and be restarted, not sit there alive and '
            'leaderless. [[slnc 200]] Three. The lease length is a choice. '
            'Short notices a dead leader quickly. Long survives a slow '
            'moment. You cannot have both.'
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
            'What is real here? A Kubernetes server, version one point '
            'thirty seven, in a one-node cluster made by a tool called '
            'kind. Kind runs a whole cluster inside one container. The '
            'demo creates the cluster at the start and deletes it at the '
            'end, and it never touches your own Kubernetes settings. The '
            'copies use the Fabric8 client, version eight. You need two '
            'things installed: a container runtime, such as Docker '
            'Desktop, switched on, and kind. Every number in this video '
            'comes from the program\'s own output, and two runs one after '
            'the other print the same thing. [[slnc 300]] So when is this '
            'too much? If the job is safe to run twice, run it everywhere. '
            'If one copy is enough, run one, and let Kubernetes restart '
            'it. A lease earns its keep only when several copies must be '
            'running and exactly one may act.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Leader Election with Kubernetes. [[slnc 250]] If you "
            'take one sentence away, take this one: the lease tells '
            'everyone else who leads, but only the thing a leader writes '
            'to can stop a leader that has already lost. [[slnc 350]] The '
            'full source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository. [[slnc 300]] If you '
            'try one exercise, make a copy exit the moment it loses the '
            'lease, and say what would bring it back. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
