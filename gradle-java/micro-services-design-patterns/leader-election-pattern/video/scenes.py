"""Scene definitions for the Leader Election teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Leader Election',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Leader Election pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Several identical copies of '
            'a service are running. [[slnc 300]] Leader election makes '
            'exactly one of them responsible for a job. [[slnc 300]] And '
            'if that leader disappears, the job passes to another copy. '
            '[[slnc 600]] Think of a relay race baton. [[slnc 300]] Only '
            'the runner holding the baton runs. [[slnc 300]] If that '
            'runner falls, the baton passes to someone else. [[slnc 700]] '
            'In our online store, the job that must happen exactly once '
            'is the nightly sales report. [[slnc 500]] By the end, you '
            'will hear three copies each send the same report. [[slnc '
            '300]] One copy holding a lease instead. [[slnc 300]] A dead '
            'leader replaced after its lease runs out. [[slnc 300]] Two '
            'copies both believing they lead. [[slnc 300]] A token that '
            'stops the old one. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Three copies of the reporting', 'service run, for reliability.', '', 'One sales report must go out', 'each night.', '', 'Not three.', '', 'Who sends it?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Three copies of the '
            'reporting service run, for reliability. [[slnc 300]] Every '
            'night, one sales report must go to the manager. [[slnc 300]] '
            'Not three. [[slnc 500]] So here is the question. [[slnc '
            '300]] Which copy sends it?'
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
            'First demo: three copies, and nobody in charge. [[slnc 400]] '
            'Each copy runs the same schedule, and knows nothing about '
            'the others. [[slnc 500]] The nightly sales report is sent by '
            'copy A. [[slnc 300]] And by copy B. [[slnc 300]] And by copy '
            'C. [[slnc 300]] The manager receives it three times.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A shared record says who leads,', 'and until when.', '', 'A copy takes the lease if it is', 'free, and renews it while it', 'lives.', '', 'Only the holder does the job.', '', 'If it stops renewing, another', 'takes over.'],
        narration=(
            'Now, the pattern. [[slnc 400]] A shared record says who '
            'leads, and until when. [[slnc 300]] That permission, with a '
            'time limit, is called a lease. [[slnc 500]] A copy takes the '
            'lease if it is free. [[slnc 300]] And it keeps renewing the '
            'lease while it is alive. [[slnc 300]] Only the holder does '
            'the job. [[slnc 500]] If the holder stops renewing, the '
            'lease runs out. [[slnc 300]] And another copy takes over.'
        ),
    ),
    dict(
        key='05-one', kind='console', title='One Holds The Lease',
        body="""TWO. One leader.
  all three ask for the lease.
  A gets it.

  the report was sent by: A.""",
        narration=(
            'Second demo: one leader. [[slnc 400]] All three copies ask '
            'for the lease. [[slnc 300]] Copy A gets it, and becomes the '
            'leader. [[slnc 300]] B and C are told no. [[slnc 500]] The '
            'report is sent by A, and only A. [[slnc 300]] The manager '
            'receives it once.'
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
            'Third demo: the leader dies. [[slnc 400]] Copy A dies, '
            'holding a lease with thirty seconds left. [[slnc 500]] After '
            'ten seconds, B asks for the lease. [[slnc 300]] It is '
            'refused, because the record still says A. [[slnc 500]] After '
            'thirty seconds, the lease has run out. [[slnc 300]] B asks '
            'first, and becomes the leader. [[slnc 600]] For those thirty '
            'seconds, nobody was really leading. [[slnc 300]] That is the '
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
            'Fourth demo: two copies that both think they lead. [[slnc '
            '400]] Copy A freezes for thirty-five seconds. [[slnc 300]] '
            'In Java, that can happen during a long memory clean-up. '
            '[[slnc 500]] Its lease runs out, and B takes it. [[slnc '
            '500]] Then A wakes up. [[slnc 300]] It still believes it is '
            'the leader. [[slnc 300]] So it sends the report. [[slnc '
            '300]] And so does B. [[slnc 500]] The report goes out twice. '
            '[[slnc 300]] A lease alone cannot stop a leader that does '
            'not know it has been replaced.'
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
            'Fifth demo: fencing. [[slnc 400]] Every lease now carries a '
            'number, called a token, that only ever goes up. [[slnc 300]] '
            "A's token was one. [[slnc 300]] B's token is two. [[slnc "
            '600]] When A wakes and tries to send, the report system '
            'checks the token. [[slnc 300]] It sees one, which is older '
            'than the newest it has seen, two. [[slnc 300]] So it '
            "refuses. [[slnc 300]] Only B's report is sent. [[slnc 600]] "
            'The thing being written to must do the check. [[slnc 300]] '
            'Because the old leader cannot be trusted to check itself.'
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
            'Finally, the bill. [[slnc 400]] A perfectly healthy leader '
            'renews its lease every seven seconds. [[slnc 500]] With a '
            'lease of five seconds, it loses leadership at second five. '
            '[[slnc 300]] With a lease of thirty seconds, it never does. '
            '[[slnc 600]] So choose carefully. [[slnc 300]] Too short, '
            'and healthy leaders are lost. [[slnc 300]] Too long, and a '
            'dead leader goes unnoticed for that long. [[slnc 600]] And '
            'everything now depends on one shared record. [[slnc 300]] If '
            'it is down, nobody can lead.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A lock or lease record with an', 'owner and an expiry time.', '', "ZooKeeper's ephemeral nodes, etcd", 'leases, Consul sessions,', '', 'A @Scheduled job wrapped in', 'something like ShedLock.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a lock or lease record, with an owner '
            'and an expiry time. [[slnc 300]] Look for tools built for '
            'this, like ZooKeeper, etcd, Consul, or Kubernetes leases. '
            '[[slnc 300]] Look for a scheduled job wrapped in a library '
            'such as ShedLock. [[slnc 300]] Or a token number passed '
            'along with every write.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use leader election when exactly', 'one copy must do a job: a', 'scheduler, a coordinator, a cache', 'warmer. Use a lease with a time', 'limit, renew it well inside that', 'limit, and use a fencing token', 'wherever a stale leader could do', 'harm. Prefer a store built for it,', 'such as ZooKeeper, etcd or Consul,'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use leader election '
            'when exactly one copy must do a job. [[slnc 300]] A '
            'scheduler, a coordinator, or a job that fills a cache. '
            '[[slnc 500]] Use a lease with a time limit, and renew it '
            'well inside that limit. [[slnc 300]] Use a fencing token '
            'wherever an old leader could do harm. [[slnc 300]] And '
            'prefer a store built for this, such as ZooKeeper, etcd, or '
            'Consul, over building your own. [[slnc 500]] And if the job '
            'can safely run twice, do not elect anyone.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] "
            'Nothing depends on a real clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If a job is safe to run twice, or', 'if a single instance is', 'acceptable, an election is', 'machinery for nothing. The', 'simplest leader is the only', 'instance.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If a job is safe to '
            'run twice, or a single copy of the service is acceptable, an '
            'election is machinery for nothing. [[slnc 400]] The simplest '
            'leader is the only copy.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Leader Election pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'lease gives one copy the job, and a token stops the copy '
            'that has been replaced, at the price of a delay and a shared '
            'record. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 300]] It runs offline, with nothing '
            'installed except a Java development kit. [[slnc 500]] Here '
            'is one exercise to try. [[slnc 300]] Make the leader renew '
            'at half its lease time. [[slnc 300]] Then see how it '
            'survives a pause shorter than that. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
