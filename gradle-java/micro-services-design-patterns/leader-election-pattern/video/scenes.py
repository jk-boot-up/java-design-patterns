"""Scene definitions for the Leader Election teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Leader Election',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Leader Election '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'leader election makes exactly one of several identical '
            'copies of a service responsible for a job, and hands the job '
            'to another copy if the leader disappears. [[slnc 350]] This '
            'is another project in the microservices category, whose '
            'subject is how many small services stay reliable when they '
            'talk to each other. In our online store, the job that must '
            'happen exactly once is the nightly sales report. [[slnc '
            '300]] By the end you will see three copies each send the '
            'same report, see one holding a lease instead, watch a dead '
            'leader replaced after its lease runs out, see two copies '
            'believe they lead, see a fencing token stop the old one, and '
            'see the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Three copies of the reporting', 'service run, for reliability.', '', 'One sales report must go out', 'each night.', '', 'Not three.', '', 'Who sends it?'],
        narration=(
            'Here is the scenario. Three copies of the reporting service '
            'run, for reliability. Every night one sales report must go '
            'to the manager. Not three. [[slnc 300]] The question: which '
            'copy sends it?'
        ),
    ),
    dict(
        key='03-all', kind='console', title='Three Copies, Nobody In Charge',
        body="""ONE. Nobody in charge.
  the report is sent by every
  copy: A, B, C.

  the manager receives it
  three times.""",
        narration=(
            'First, three copies, and nobody in charge. Each one runs the '
            'same schedule and knows nothing about the others. The '
            'nightly sales report is sent by A, by B, and by C. The '
            'manager receives it three times.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A shared record says who leads,', 'and until when.', '', 'A copy takes the lease if it is', 'free, and renews it while it', 'lives.', '', 'Only the holder does the job.', '', 'If it stops renewing, another', 'takes over.'],
        narration=(
            'The pattern. A shared record says who leads, and until when. '
            'A copy takes the lease if it is free, and renews it while it '
            'is alive. Only the holder does the job. If the holder stops '
            'renewing, the lease runs out, and another copy takes over.'
        ),
    ),
    dict(
        key='05-one', kind='console', title='One Holds The Lease',
        body="""TWO. One leader.
  all three ask for the lease.
  A gets it.

  the report was sent by: A.""",
        narration=(
            'Second, one holds the lease. All three ask for it. A gets '
            'it, and is the leader. B and C are told no. The report is '
            'sent by A, and only A. The manager receives it once.'
        ),
    ),
    dict(
        key='06-die', kind='console', title='The Leader Dies',
        body="""THREE. The leader dies.
  A dies, lease has 30 s left.
  10 s: B asks, still A.
  30 s: expired, B takes it.

  for 30 seconds nobody was
  leading.""",
        narration=(
            'Third, the leader dies. A dies, holding a lease with thirty '
            'seconds to run. After ten seconds, B asks, and is refused: '
            'the store still says A. After thirty seconds the lease has '
            'expired, and B asks first and becomes leader. For those '
            'thirty seconds, nobody was actually leading. That is the '
            'price of not being sure that A was dead.'
        ),
    ),
    dict(
        key='07-split', kind='console', title='Two Who Think They Lead',
        body="""FOUR. Two leaders.
  A pauses for 35 s.
  its lease expires, B takes it.
  A wakes, still believing it
  leads, and sends.

  sent by: A, B.""",
        narration=(
            'Fourth, two who think they lead. A pauses for thirty five '
            'seconds, say in a long garbage collection. Its lease '
            'expires, and B takes it. A wakes up, still believing that it '
            'leads, and sends the report. So does B. The report goes out '
            'twice. A lease alone cannot stop a leader that does not know '
            'it has been replaced.'
        ),
    ),
    dict(
        key='08-fence', kind='console', title='Fencing',
        body="""FIVE. Fencing.
  every lease has a token that
  only goes up.
  A wakes: token 1, refused.
  B: token 2, sent.

  the sink checks the token.""",
        narration=(
            'Fifth, fencing. Every lease carries a token that only goes '
            "up. A's was one. B's is two. When A wakes and tries to send, "
            'the report sink sees a token older than the newest it has '
            "seen, and refuses. Only B's report is sent. The thing being "
            'written to has to do the check, because the old leader '
            'cannot be trusted to.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  lease 5 s, renew every 7 s:
  a healthy leader loses it at
  second 5.
  lease 30 s: never.

  too short: healthy leaders
  lost. too long: dead ones
  missed.

  one shared record.""",
        narration=(
            'Last, the bill. A perfectly healthy leader that renews every '
            'seven seconds, against a lease of five, loses leadership at '
            'second five. Against a lease of thirty, it never does. Too '
            'short, and healthy leaders are lost. Too long, and a dead '
            'one is missed for that long. And everything now depends on '
            'one shared record. If it is down, nobody can lead.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A lock or lease record with an', 'owner and an expiry time.', '', "ZooKeeper's ephemeral nodes, etcd", 'leases, Consul sessions,', '', 'A @Scheduled job wrapped in', 'something like ShedLock.'],
        narration=(
            'How do you recognise this in code you did not write? A lock '
            'or lease record with an owner and an expiry time. '
            "ZooKeeper's ephemeral nodes, etcd leases, Consul sessions, "
            'Kubernetes Lease objects. A @Scheduled job wrapped in '
            'something like ShedLock. A token or epoch number passed with '
            'every write.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use leader election when exactly', 'one copy must do a job: a', 'scheduler, a coordinator, a cache', 'warmer. Use a lease with a time', 'limit, renew it well inside that', 'limit, and use a fencing token', 'wherever a stale leader could do', 'harm. Prefer a store built for it,', 'such as ZooKeeper, etcd or Consul,'],
        narration=(
            'Here is my verdict, plainly. Use leader election when '
            'exactly one copy must do a job: a scheduler, a coordinator, '
            'a cache warmer. Use a lease with a time limit, renew it well '
            'inside that limit, and use a fencing token wherever a stale '
            'leader could do harm. Prefer a store built for it, such as '
            'ZooKeeper, etcd or Consul, over building your own. If the '
            'job can safely run twice, do not elect anyone.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. Every number quoted comes from '
            "this program's own output. Nothing depends on a clock, so "
            'every run is the same.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If a job is safe to run twice, or', 'if a single instance is', 'acceptable, an election is', 'machinery for nothing. The', 'simplest leader is the only', 'instance.'],
        narration=(
            'So when is it too much? If a job is safe to run twice, or if '
            'a single instance is acceptable, an election is machinery '
            'for nothing. The simplest leader is the only instance.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Leader Election. [[slnc 250]] If you take one "
            'sentence away, take this one: a lease gives one copy the job '
            'and a token stops the copy that has been replaced, at the '
            'price of a delay and a shared record. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, make the leader renew at half its '
            'lease, and see how a pause shorter than that is survived. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
