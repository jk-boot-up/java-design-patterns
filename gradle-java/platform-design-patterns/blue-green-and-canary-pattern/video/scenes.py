"""Scene definitions for the Blue-Green and Canary teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Blue-Green and Canary',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Blue-Green and '
            'Canary pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: blue '
            'green runs the old and the new release side by side, and '
            'switches traffic at once. A canary sends a small share of '
            'traffic to the new release first, and grows it only while it '
            'stays healthy. [[slnc 350]] This is another project in the '
            'platform category, whose subject is how software is shipped, '
            'run and operated. In our online store, a new release of the '
            'checkout must go live without customers noticing, and '
            'without taking the risk all at once. [[slnc 300]] By the end '
            'you will see a release that fails requests while it is '
            'replaced, see a switch with none failing, see a quick way '
            'back, see a canary meet only a few failures, see a gate halt '
            'a bad release and promote a good one, and see the bill, '
            'which is double capacity and a shared database.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A new release of the checkout', 'is ready.', '', 'One order in ten is a big one.', '', 'The new release has a bug', 'with big orders,', 'and nobody knows yet.', '', 'How do we go live?'],
        narration=(
            'Here is the scenario. A new release of the checkout is '
            'ready. One order in ten is a big one, and the new release '
            'has a bug with big orders that nobody has found yet. [[slnc '
            '300]] The question: how do we go live?'
        ),
    ),
    dict(
        key='03-inplace', kind='console', title='Replace It Where It Stands',
        body="""ONE. Replace it in place.
  stop v1, install v2, start v2.
  10 requests arrive while down.
  of 100 requests, failed: 10.""",
        narration=(
            'First, replace it where it stands. Stop version one, install '
            'version two, start version two. Ten requests arrive while it '
            'is down. Of a hundred requests, ten failed.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Run the new release beside', 'the old one.', '', 'Blue-green: switch all traffic', 'at once, and back at once.', '', 'Canary: send a small share', 'first, and grow it while it', 'stays healthy.'],
        narration=(
            'The pattern. Run the new release beside the old one. Blue '
            'green: switch all the traffic at once, and back at once. '
            'Canary: send a small share first, and grow it while it stays '
            'healthy.'
        ),
    ),
    dict(
        key='05-bg', kind='console', title='Blue And Green',
        body="""TWO. Blue and green.
  v2 started beside v1,
  tried with a test order: ok.
  the switch: one setting.
  of 100 requests, failed: 0.""",
        narration=(
            'Second, blue and green. Version two is started beside '
            'version one, and tried with a test order. It is fine. '
            'Version one served fifty requests meanwhile. The switch is '
            'one setting. After it, version two serves the next fifty. Of '
            'a hundred requests, none failed.'
        ),
    ),
    dict(
        key='06-back', kind='console', title='Going Back',
        body="""THREE. Going back.
  v2 has a bug with big orders.
  50 requests on v2: 5 failed.
  one setting back to v1, which
  was never stopped:
  the next 50: 0 failed.""",
        narration=(
            'Third, going back. Version two has a bug with big orders. '
            'Fifty requests on version two, five failed. One setting '
            'sends traffic back to version one, which was never stopped. '
            'The next fifty requests, none failed.'
        ),
    ),
    dict(
        key='07-canary', kind='console', title='A Canary',
        body="""FOUR. A canary.
  5% to the buggy v2.
  of 200 requests, v2 got 10,
  and failed 2.

  all 200 on v2: 20 would fail.
  a few customers found the bug,
  not everyone.""",
        narration=(
            'Fourth, a canary. Five percent of traffic goes to the buggy '
            'version two. Of two hundred requests, version two got ten, '
            'and failed two. Had all two hundred gone to version two, '
            'twenty would have failed. A few customers found the bug, not '
            'everyone.'
        ),
    ),
    dict(
        key='08-gate', kind='console', title='Promote In Steps, With A Gate',
        body="""FIVE. Steps, with a gate.
  5, 25, 50, 100 percent;
  gate at 5% failures.
  buggy v2: halted after 1 step,
  20% failing; back to v1.
  good v2: all 4 steps, at 100%.""",
        narration=(
            'Fifth, promote in steps, with a gate. Steps of five, twenty '
            'five, fifty and a hundred percent, with a gate at five '
            'percent failures. The buggy version two is halted after one '
            'step, with twenty percent failing, and traffic goes back to '
            'version one. The good version two goes through all four '
            'steps, and ends at a hundred percent.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  two full copies: capacity 20
  instead of 10.

  v2 wrote 5 orders in a new
  format. v1 can read: 0.

  both share one database, so a
  data change cannot go back.""",
        narration=(
            'Last, the bill. Two full copies run during the switch: '
            'capacity twenty instead of ten. And version two wrote five '
            'orders in a new format before we went back. Version one can '
            'read none of them. Both releases share one database, so a '
            'release that changes the data cannot be switched back '
            'safely.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Two deployments or target groups', 'behind a load balancer.', '', 'Traffic weights of 5, 25 and 100', 'percent.', '', 'Argo Rollouts, Flagger, AWS', 'CodeDeploy, Kubernetes with an'],
        narration=(
            'How do you recognise this in code you did not write? Two '
            'deployments or target groups behind a load balancer. Traffic '
            'weights of 5, 25 and 100 percent. Argo Rollouts, Flagger, '
            'AWS CodeDeploy, Kubernetes with an Istio route. A rollout '
            'that pauses on an error-rate check.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Release beside the old version,', 'never on top of it. Switch by a', 'setting, so that going back is a', 'setting. Use a canary for risky', 'changes, with a gate on failures.', 'Keep data changes compatible in', 'both directions, and pay for the', 'extra capacity for the time it', 'takes.'],
        narration=(
            'Here is my verdict, plainly. Release beside the old version, '
            'never on top of it. Switch by a setting, so that going back '
            'is a setting. Use a canary for risky changes, with a gate on '
            'failures. Keep data changes compatible in both directions, '
            'and pay for the extra capacity for the time it takes.'
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
        body=['For an internal tool where a short', 'outage is fine, a plain restart is', 'enough. These methods pay off', 'where downtime or a bad release is', 'costly.'],
        narration=(
            'So when is it too much? For an internal tool where a short '
            'outage is fine, a plain restart is enough. These methods pay '
            'off where downtime or a bad release is costly.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Blue-Green and Canary. [[slnc 250]] If you take one "
            'sentence away, take this one: blue green and canary let a '
            'release go live beside the old one and go back with one '
            'setting, and the price is double capacity and a shared '
            'database that both releases must understand. [[slnc 350]] '
            'The full source, the written notes, the diagrams and an '
            'animated walkthrough are all in the repository, running '
            'offline with nothing installed but a Java development kit. '
            '[[slnc 300]] If you try one exercise, change the gate to two '
            'percent, and see whether the buggy release is halted sooner. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
