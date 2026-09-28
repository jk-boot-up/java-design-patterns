"""Scene definitions for the Event Sourcing with EventStoreDB teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks every count out loud, says each of KurrentDB's words in
plain language before using KurrentDB's name for it, and never points at a
picture the listener cannot see. Every figure is the output of `./gradlew run`.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Event Sourcing with EventStoreDB',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Event Sourcing pattern in Java, using a real database built '
            'for events. [[slnc 300]] It was called EventStoreDB, and has '
            'recently been renamed KurrentDB. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] Event sourcing means you '
            'never overwrite what you know. [[slnc 300]] You write down '
            'each thing that happened, in order, and never change it. '
            '[[slnc 300]] When you need the current state, you add the '
            'list up. [[slnc 600]] Think of a bank statement: a list of '
            'payments, with the total worked out from them. [[slnc 700]] '
            'In our online store, the loyalty scheme keeps every award, '
            'every spend, and every expiry. [[slnc 300]] And it adds them '
            'up to get the balance. [[slnc 500]] By the end, you will '
            'hear two checkouts spend the same points at the same moment. '
            '[[slnc 300]] A real database refuse the second one. [[slnc '
            '300]] A retry the database recognises. [[slnc 300]] A screen '
            'that catches up by reading the history. [[slnc 300]] And '
            'what deleting a customer really removes.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['One point per pound spent.', 'Points can be spent on later orders.',
              'Unused points expire.', '',
              'No balance is stored anywhere.', 'It is added up from the events.', '',
              'A customer can pay on the website', 'or in the phone app.', '',
              'This time the events live in a', 'real database, shared by both.'],
        narration=(
            'Here is the scenario. [[slnc 400]] The shop gives one '
            'loyalty point for every pound spent. [[slnc 300]] Customers '
            'can spend points on later orders. [[slnc 300]] And unused '
            'points expire. [[slnc 500]] No balance is stored anywhere. '
            '[[slnc 300]] Every award, spend, and expiry is written down. '
            '[[slnc 300]] And the balance is added up from them whenever '
            'someone asks. [[slnc 600]] The plain Java version kept those '
            'events in a simple list, inside one program, with one '
            'writer. [[slnc 300]] Here, the events live in a real '
            'database. [[slnc 300]] And two places can write to it at '
            'once: the website, and the phone app. [[slnc 300]] That is '
            'where the trouble starts.'
        ),
    ),
    dict(
        key='03-words', kind='bullets', title="KurrentDB's Words",
        body=['EventStoreDB is now named KurrentDB.', 'Same database, new name.', '',
              'A stream is one named list of events.', 'Here: loyalty-C-4417.', '',
              'Each event gets a number from 0.', 'That number is its revision.', '',
              'Append adds to the end. Nothing else', 'changes a stream, except deleting it.'],
        narration=(
            'This database brings a few words with it. [[slnc 400]] '
            'First, the name. [[slnc 300]] It was called EventStoreDB for '
            'many years. [[slnc 300]] Its makers renamed it KurrentDB. '
            '[[slnc 300]] Same database, new name. [[slnc 600]] Think of '
            'a paper ledger with numbered lines, one ledger per customer. '
            '[[slnc 300]] You may only write on the next empty line. '
            '[[slnc 300]] And you never rub anything out. [[slnc 600]] '
            'One ledger, one list of events for one customer, is called a '
            'stream. [[slnc 300]] Each line has a number, starting at '
            'zero, called its revision. [[slnc 300]] Writing on the next '
            'line is called an append. [[slnc 500]] There is no way to '
            'change a line. [[slnc 300]] The only other thing you can do '
            'is throw the whole ledger away.'
        ),
    ),
    dict(
        key='04-one', kind='console', title='A Real Log, Read Back',
        body="""ONE. A real log, read back from the start.
  4 events appended to loyalty-C-4417.
  KurrentDB numbered them revision 0 to 3.

  a second connection reads from the start:
  revision 0  earned 60      balance 60
  revision 1  spent 25       balance 35
  revision 2  earned 120     balance 155
  revision 3  lost 15        balance 140

  balance: 140 points, from 4 events.""",
        narration=(
            'First demo: a real log, read back. [[slnc 400]] The demo '
            'starts KurrentDB in a container, a small sealed box it '
            'switches on and off by itself. [[slnc 500]] It appends four '
            'things that happened to one customer in March. [[slnc 300]] '
            'KurrentDB numbers them, revision zero to three. [[slnc 600]] '
            'Then a second connection reads the stream from the start, '
            'and adds it up. [[slnc 300]] Sixty points earned: balance '
            'sixty. [[slnc 300]] Twenty-five spent: balance thirty-five. '
            '[[slnc 300]] A hundred and twenty earned: balance a hundred '
            'and fifty-five. [[slnc 300]] Fifteen expired: balance a '
            'hundred and forty. [[slnc 600]] Nothing stores a hundred and '
            'forty. [[slnc 300]] It was added up just now, from four '
            'events. [[slnc 300]] And the Java library has no way to '
            'change an event.'
        ),
    ),
    dict(
        key='05-two', kind='console', title='Two Checkouts, No Check',
        body="""TWO. Two checkouts at once, with no check.
  C-5120 has 140 points.
  the website and the phone app both look:
  140 points, at revision 3.

  both decide 100 is not more than 140.
  both append a redemption, check off.

  both appends accepted,
  at revisions 4 and 5.
  balance now: -60 points.""",
        narration=(
            'Second demo: two checkouts at once, with no check. [[slnc '
            '400]] A customer has a hundred and forty points. [[slnc '
            '300]] They pay for two orders at the same moment: one on the '
            'website, one in the phone app. [[slnc 600]] Paying with '
            'points has two steps. [[slnc 300]] First, look: read the '
            'stream, and add it up. [[slnc 300]] Then decide: if there '
            'are enough points, append a spend. [[slnc 600]] Both '
            'checkouts look, and both see a hundred and forty points, at '
            'revision three. [[slnc 300]] Both decide a hundred is less '
            'than a hundred and forty. [[slnc 300]] Both append a spend '
            'of a hundred points, with no check. [[slnc 600]] Both '
            'appends are accepted. [[slnc 300]] The balance is now minus '
            'sixty. [[slnc 300]] The customer spent two hundred points, '
            'but only had a hundred and forty.'
        ),
    ),
    dict(
        key='06-three', kind='console', title='The Expected Revision',
        body="""THREE. The same race, expected revision.
  C-5121 has 140 points. both look:
  140 points, at revision 3.
  both append, expecting revision 3.

  appends accepted: 1, at revision 4.
  appends refused: 1.
  WrongExpectedVersion: expected
  revision 3, but the stream is at 4.

  the refused one looks again: 40 points.
  100 is more than 40: it says no.""",
        narration=(
            'Third demo: the same race, with a check. [[slnc 400]] '
            'Another customer, with a hundred and forty points. [[slnc '
            '300]] This time, each checkout adds one condition to its '
            'append. [[slnc 300]] Only write this if the stream is still '
            'at the revision I looked at. [[slnc 300]] That is called the '
            'expected revision. [[slnc 600]] Both look, and see revision '
            'three. [[slnc 300]] Both append, expecting revision three. '
            '[[slnc 500]] One append is accepted, at revision four. '
            '[[slnc 300]] The other is refused. [[slnc 300]] The database '
            'says: you expected revision three, but the stream is now at '
            'four. [[slnc 600]] The refused checkout looks again. [[slnc '
            '300]] It sees forty points. [[slnc 300]] A hundred is more '
            'than forty, so it tells the customer no. [[slnc 500]] The '
            'balance is forty. [[slnc 300]] Nothing was locked. [[slnc '
            '300]] The database just compared one number.'
        ),
    ),
    dict(
        key='07-diagram', kind='diagram', title='One Number Decides',
        body=None,
        narration=(
            'Here is the whole setup, in words. [[slnc 400]] Two '
            'checkouts, one stream, one database. [[slnc 600]] Each '
            'checkout reads the stream, adds it up, and remembers the '
            'revision it saw. [[slnc 300]] Then it appends, and passes '
            'that revision along. [[slnc 500]] The database compares it '
            "with the stream's real last revision. [[slnc 300]] If they "
            'match, the event is written, and the stream moves on by one. '
            '[[slnc 300]] If they do not, someone else wrote in between, '
            'and the append is refused. [[slnc 600]] The rule to '
            'remember: whoever writes first moves the number. [[slnc '
            '300]] Everyone who looked before that has to look again.'
        ),
    ),
    dict(
        key='08-one-argument', kind='code', title='One Argument',
        body="""// the default: any state at all
AppendToStreamOptions.get()
    .streamState(StreamState.any());

// only if the stream is still at 3
AppendToStreamOptions.get()
    .streamState(
        StreamState.streamRevision(3));""",
        narration=(
            'The difference between those two races is one setting. '
            '[[slnc 500]] The first append says: any. [[slnc 300]] Write '
            'this, whatever state the stream is in. [[slnc 500]] The '
            'second says: only if the stream is still at revision three. '
            '[[slnc 600]] And here is the part to remember. [[slnc 300]] '
            'In the Java library, any is the default. [[slnc 300]] An '
            'append that says nothing about revisions is always accepted. '
            '[[slnc 300]] The check is real, but it is off, until you '
            'turn it on.'
        ),
    ),
    dict(
        key='09-retry', kind='console', title='A Retry It Recognises',
        body="""FOUR. A retry the server recognises.
  C-5122 is awarded 45 points on
  ORD-9001. the reply is lost, and the
  award is sent again.

  with a new event id:
    2 awards for ORD-9001. balance 90.
  for C-5123, the same event id
  and the same expectation:
    the server answers revision 0 again,
    and writes nothing. balance 45.""",
        narration=(
            'Fourth demo: a retry. [[slnc 400]] The shop awards a '
            'customer forty-five points for an order. [[slnc 300]] The '
            'reply gets lost on the network. [[slnc 300]] So the shop '
            'does not know if the award was written, and sends it again. '
            '[[slnc 600]] Every event carries a random label chosen by '
            'the writer, called the event I D. [[slnc 500]] Sent again '
            'with a new event I D, the award is simply written twice. '
            '[[slnc 300]] Two awards for one order, and a balance of '
            'ninety. [[slnc 300]] That is the double-award bug, happening '
            'for real. [[slnc 600]] For another customer, the retry '
            'reuses the same event I D, and the same expected revision. '
            '[[slnc 300]] The database gives the same answer as the first '
            'time, and writes nothing. [[slnc 300]] One award, and a '
            'balance of forty-five. [[slnc 500]] The retry is recognised, '
            'not refused. [[slnc 300]] So the shop never has to guess.'
        ),
    ),
    dict(
        key='10-catch-up', kind='console', title='A Screen That Catches Up',
        body="""FIVE. A screen that catches up.
  the support dashboard starts last and
  asks for every loyalty stream from
  the start.

  it receives 18 events already stored,
  and is told it has caught up.
  C-4417 = 140, C-5120 = -60,
  C-5121 = 40, C-5122 = 90.

  a new award of 20 for C-4417:
  the dashboard shows C-4417 = 160.""",
        narration=(
            'Fifth demo: a screen that catches up. [[slnc 400]] The '
            "support team has a screen showing every customer's balance. "
            '[[slnc 300]] It starts last, after everything so far. [[slnc '
            '300]] And it asks the database for every loyalty stream, '
            'from the very first event. [[slnc 300]] That is called a '
            'catch-up subscription. [[slnc 600]] The database sends the '
            'eighteen events already stored. [[slnc 300]] Then it says: '
            'you have caught up. [[slnc 300]] The screen shows every '
            "customer's balance, including the minus sixty and the "
            'ninety. [[slnc 600]] Then a new order awards the first '
            'customer twenty points. [[slnc 300]] Nobody tells the '
            'screen. [[slnc 300]] Moments later, it shows a hundred and '
            'sixty. [[slnc 500]] A copy built like this is called a '
            'projection, or a read model. [[slnc 300]] Starting late lost '
            'nothing.'
        ),
    ),
    dict(
        key='11-delete', kind='console', title='The Bill: Deleting A Stream',
        body="""SIX. The bill: deleting a stream.
  C-5122 asks to be forgotten.
  the shop deletes loyalty-C-5122.

  reading the stream: stream not found.
  reading the whole log: 2 events of
  loyalty-C-5122 are still there.

  the dashboard still shows C-5122 = 90.
  a later order reuses the name:
  accepted at revision 2, not 0.""",
        narration=(
            'Sixth demo: the bill. [[slnc 400]] A customer asks to be '
            "forgotten. [[slnc 300]] So the shop deletes that customer's "
            'stream. [[slnc 600]] Reading the stream now gives: stream '
            'not found. [[slnc 500]] But KurrentDB also keeps one log of '
            'everything, every stream together, in the order written. '
            '[[slnc 300]] Reading that whole log still finds two of the '
            "deleted customer's events. [[slnc 300]] They stay on disk "
            'until a later clean-up, called a scavenge. [[slnc 600]] The '
            "support screen still shows that customer's ninety points. "
            '[[slnc 300]] The delete reached the stream, not the copies '
            'built from it. [[slnc 600]] And when a later order reuses '
            'the same stream name, it starts at revision two, not zero. '
            '[[slnc 300]] The numbering carries on from where the deleted '
            'events stopped.'
        ),
    ),
    dict(
        key='12-bill', kind='bullets', title='What Else It Costs',
        body=['Deleting hides; it does not erase.', 'Every copy must forget too.', '',
              'The check is off by default.', 'Every writer must turn it on.', '',
              'This demo ran with security off:', 'no TLS, no passwords, 1 container.',
              'Production must never run like that.', '',
              'One more database to run and watch.'],
        narration=(
            'So what else does this cost? [[slnc 500]] Deleting a stream '
            'hides it. [[slnc 300]] It does not erase it. [[slnc 300]] '
            'Real erasure needs the clean-up to run. [[slnc 300]] And '
            'every copy built from the stream must be told to forget too. '
            '[[slnc 600]] The revision check is off by default. [[slnc '
            '300]] So every piece of code that writes must remember to '
            'turn it on. [[slnc 600]] This demo ran the database with '
            'security switched off. [[slnc 300]] No network encryption, '
            'and no passwords. [[slnc 300]] A real production server must '
            'never run like that. [[slnc 600]] And it is one more '
            'database to run, back up, and watch.'
        ),
    ),
    dict(
        key='13-contrast', kind='bullets', title='What The Simulation Left Out',
        body=['Got right: the whole idea.', 'Append only, add up, 140 from 4 events.', '',
              'Left out: two writers at once.', 'Its list had one writer and no check.', '',
              'Left out: a retry, a late reader,', 'and a delete that only hides.', '',
              'Headline: with no check, -60.', 'With the expected revision, refused.'],
        narration=(
            'So what did the plain Java version get right? [[slnc 400]] '
            'The whole idea. [[slnc 300]] Events are only ever added. '
            '[[slnc 300]] The balance is added up, never stored. [[slnc '
            '300]] A hundred and forty points, from the same four events. '
            '[[slnc 300]] All of that holds here. [[slnc 600]] What it '
            'left out was everything that needs two programs. [[slnc '
            '300]] Its list had one writer, so two checkouts could never '
            'race. [[slnc 300]] It had no lost replies, no screen '
            'starting late, and its delete really removed things. [[slnc '
            '600]] And the headline. [[slnc 300]] Two checkouts spending '
            'the same points at once. [[slnc 300]] With no check, both '
            'are accepted, and the balance goes to minus sixty. [[slnc '
            '300]] With the expected revision, the second one is refused.'
        ),
    ),
    dict(
        key='14-verdict', kind='bullets', title='The Verdict',
        body=['One stream per thing that must', 'stay consistent: one customer.', '',
              'Look, decide, then append with', 'the revision you looked at.', '',
              'On a refusal, look again and', 'decide again. Never retry blind.', '',
              'Choose each event id once,', 'and reuse it on a retry.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Give each thing that '
            'must stay consistent its own stream. [[slnc 300]] Here, one '
            "customer's points. [[slnc 600]] Look, decide, and then "
            'append with the revision you looked at. [[slnc 300]] If the '
            'append is refused, do not just send it again. [[slnc 300]] '
            'Look again, and decide again, because the answer may now be '
            "no. [[slnc 600]] And choose each event's I D once, when you "
            'first decide. [[slnc 300]] Reuse it on every retry. [[slnc '
            '300]] So a lost reply can never become a second award.'
        ),
    ),
    dict(
        key='15-real', kind='bullets', title='What Is Real, And When Not',
        body=['Real: KurrentDB 26.1.2 in a container', 'the demo starts and stops.',
              'kurrentdb-client 1.2.1,', 'Testcontainers 2.0.5.', '',
              'Real: two connections racing.', 'Real: a catch-up subscription.', '',
              'Too much: one writer, no audit.', 'A row with a number is simpler.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'database is KurrentDB, version twenty-six point one point '
            'two, the newest release. [[slnc 300]] It runs in a container '
            'that the demo starts and stops by itself. [[slnc 300]] You '
            'just need Docker switched on first. [[slnc 300]] The two '
            'checkouts are two real connections, really racing. [[slnc '
            '300]] And the support screen is a real subscription. [[slnc '
            '600]] So, when is this too much? [[slnc 300]] If only one '
            'program ever writes, and nobody will ever ask how a number '
            'got there, a row holding the number is simpler. [[slnc 300]] '
            'And much cheaper to run.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough',
              'are in the repository. Try the exercises in',
              'the session guide.'],
        narration=(
            "That's Event Sourcing, with EventStoreDB, now called "
            'KurrentDB. [[slnc 400]] If you remember one sentence, make '
            'it this one. [[slnc 300]] Append with the revision you '
            'looked at, because without it, the database accepts whatever '
            'arrives. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Give the first race the expected revision. [[slnc '
            '300]] Guess which result will change, and then run it. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
