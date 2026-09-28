"""Scene definitions for the Blue-Green and Canary teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Blue-Green and Canary',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Blue-Green and Canary patterns, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Blue-green runs the '
            'old release and the new release side by side. [[slnc 300]] '
            'Then it switches all the traffic across at once. [[slnc '
            '500]] A canary sends only a small share of traffic to the '
            'new release first. [[slnc 300]] And it grows that share only '
            'while the new release stays healthy. [[slnc 600]] The name '
            'comes from coal mines, where a canary warned miners of '
            'danger before it reached everyone. [[slnc 700]] In our '
            'online store, a new release of checkout must go live without '
            'customers noticing, and without taking all the risk at once. '
            '[[slnc 500]] By the end, you will hear a release that fails '
            'requests while it is replaced. [[slnc 300]] A switch where '
            'none fail. [[slnc 300]] A quick way back. [[slnc 300]] A '
            'canary that meets only a few failures. [[slnc 300]] A gate '
            'that stops a bad release. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A new release of the checkout', 'is ready.', '', 'One order in ten is a big one.', '', 'The new release has a bug', 'with big orders,', 'and nobody knows yet.', '', 'How do we go live?'],
        narration=(
            'Here is the scenario. [[slnc 400]] A new release of checkout '
            'is ready. [[slnc 300]] One order in ten is a big one. [[slnc '
            '300]] And the new release has a bug with big orders, that '
            'nobody has found yet. [[slnc 500]] So here is the question. '
            '[[slnc 300]] How do we go live?'
        ),
    ),
    dict(
        key='03-inplace', kind='console', title='Replace It Where It Stands',
        body="""ONE. Replace it in place.
  stop v1, install v2, start v2.
  10 requests arrive while down.
  of 100 requests, failed: 10.""",
        narration=(
            'First demo: replace it where it stands. [[slnc 400]] Stop '
            'version one. [[slnc 200]] Install version two. [[slnc 200]] '
            'Start version two. [[slnc 500]] Ten requests arrive while it '
            'is down. [[slnc 300]] So, out of a hundred requests, ten '
            'failed.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Run the new release beside', 'the old one.', '', 'Blue-green: switch all traffic', 'at once, and back at once.', '', 'Canary: send a small share', 'first, and grow it while it', 'stays healthy.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Run the new release beside '
            'the old one. [[slnc 500]] With blue-green, switch all the '
            'traffic at once. [[slnc 300]] And switch it back at once, if '
            'needed. [[slnc 500]] With a canary, send a small share '
            'first. [[slnc 300]] And grow it while the new release stays '
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
            'Second demo: blue and green. [[slnc 400]] Version two is '
            'started beside version one. [[slnc 300]] It is tried with a '
            'test order, and it works. [[slnc 300]] Meanwhile, version '
            'one serves fifty real requests. [[slnc 500]] The switch is '
            'one setting. [[slnc 300]] After it, version two serves the '
            'next fifty. [[slnc 500]] Out of a hundred requests, none '
            'failed.'
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
            'Third demo: going back. [[slnc 400]] Version two has the bug '
            'with big orders. [[slnc 300]] Of fifty requests on version '
            'two, five failed. [[slnc 500]] One setting sends traffic '
            'back to version one. [[slnc 300]] Version one was never '
            'stopped, so it is ready at once. [[slnc 300]] The next fifty '
            'requests: none failed.'
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
            'Fourth demo: a canary. [[slnc 400]] Five percent of traffic '
            'goes to the buggy version two. [[slnc 500]] Out of two '
            'hundred requests, version two got ten. [[slnc 300]] And two '
            'of them failed. [[slnc 500]] If all two hundred had gone to '
            'version two, twenty would have failed. [[slnc 300]] A few '
            'customers met the bug, not everyone.'
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
            'Fifth demo: promote in steps, with a gate. [[slnc 400]] The '
            'steps are five, twenty-five, fifty, and a hundred percent. '
            '[[slnc 300]] The gate says: stop if more than five percent '
            'of requests fail. [[slnc 600]] The buggy version two is '
            'stopped after the first step, with twenty percent failing. '
            '[[slnc 300]] And traffic goes back to version one. [[slnc '
            '500]] A good version two passes all four steps, and ends up '
            'with all the traffic.'
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
            'Finally, the bill. [[slnc 400]] During the switch, two full '
            'copies are running. [[slnc 300]] So you pay for twice the '
            'capacity. [[slnc 600]] And there is a harder cost. [[slnc '
            '300]] Before we went back, version two saved five orders in '
            'a new format. [[slnc 300]] Version one cannot read any of '
            'them. [[slnc 500]] Both releases share one database. [[slnc '
            '300]] So a release that changes the shape of the data cannot '
            'be switched back safely.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Two deployments or target groups', 'behind a load balancer.', '', 'Traffic weights of 5, 25 and 100', 'percent.', '', 'Argo Rollouts, Flagger, AWS', 'CodeDeploy, Kubernetes with an'],
        narration=(
            'How can you spot this pattern in a system someone else '
            'built? [[slnc 400]] Look for two copies of a service, behind '
            'one load balancer. [[slnc 300]] Look for traffic weights, '
            'like five, twenty-five, and a hundred percent. [[slnc 300]] '
            'Look for tools like Argo Rollouts, Flagger, or Amazon '
            'CodeDeploy. [[slnc 300]] Or a rollout that pauses to check '
            'the error rate.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Release beside the old version,', 'never on top of it. Switch by a', 'setting, so that going back is a', 'setting. Use a canary for risky', 'changes, with a gate on failures.', 'Keep data changes compatible in', 'both directions, and pay for the', 'extra capacity for the time it', 'takes.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Release beside the old '
            'version, never on top of it. [[slnc 300]] Switch with a '
            'setting, so going back is also just a setting. [[slnc 500]] '
            'Use a canary for risky changes, with a gate on failures. '
            '[[slnc 300]] Keep data changes readable by both the old and '
            'new releases. [[slnc 300]] And accept paying for extra '
            'capacity while the switch happens.'
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
        body=['For an internal tool where a short', 'outage is fine, a plain restart is', 'enough. These methods pay off', 'where downtime or a bad release is', 'costly.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For an internal tool '
            'where a short outage is fine, a plain restart is enough. '
            '[[slnc 400]] These methods pay off where downtime, or a bad '
            'release, is costly.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Blue-Green and Canary. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Release beside '
            'the old version, and go back with one setting, but pay for '
            'double capacity, and keep the shared data readable by both. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 300]] It runs offline, with nothing installed except '
            'a Java development kit. [[slnc 500]] Here is one exercise to '
            'try. [[slnc 300]] Change the gate to two percent. [[slnc '
            '300]] Then see whether the buggy release is stopped sooner. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
