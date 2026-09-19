"""Scene definitions for the Blue-Green and Canary with Kubernetes teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Blue-Green and Canary with Kubernetes',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Blue-Green and '
            'Canary pattern with Kubernetes, in Java, and it is written '
            'and presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Blue-Green and Canary video. That '
            'one ran two releases of the checkout behind a router that '
            'was a rule on the request number. It showed an in place '
            'upgrade failing requests, a switch and a switch back, a '
            'canary, and a gate that halts a bad release. This one shows '
            'the same idea inside Kubernetes. [[slnc 350]] The plain '
            'definition, in short: on Kubernetes, blue green is a change '
            "to a service's selector, between two deployments. A canary "
            'is a change to the replica counts of two deployments behind '
            'one service. [[slnc 300]] By the end you will see a real '
            'cluster fail every request while a release is replaced, see '
            'a real switch and a real switch back, see a canary spread by '
            'the cluster itself, see a gate halt a bad release, and see '
            'the bill: pods for two releases at once.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Blue-Green and Canary, the hand-', 'built video, runs two releases', 'behind a router that is a rule.', '', 'It shows a switch, a switch back,', 'a canary and a gate.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'This video assumes the Blue-Green and Canary video. If you '
            'have not seen it, start there. It runs two releases behind a '
            'router that is a rule on the request number, and shows a '
            'switch, a switch back, a canary and a gate. [[slnc 300]] '
            'This one uses the same example. It does not teach the '
            'pattern again. It shows what Kubernetes does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new: Kubernetes,', 'kind, and Docker.', '', 'You need Docker running, with kind', 'and kubectl installed. Without', 'them the demo says so and stops.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before the first line of code, what Kubernetes is. '
            'Kubernetes is a system that runs containers in groups called '
            'pods, and keeps as many as you ask for. A service gives them '
            'one address, and picks them by label. Kind runs a whole '
            'cluster inside Docker on your own machine. [[slnc 300]] And '
            'a promise: skipping this video loses none of the pattern. '
            'The hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-gap', kind='console', title='Replace It Where It Stands',
        body="""ONE. Replace it in place.
  v1 stopped to make room for v2.
  20 requests, nothing running:
  failed 20 of 20.""",
        narration=(
            'First, replace it where it stands. Version one is stopped to '
            'make room for version two. Twenty requests arrive while '
            'nothing is running, and all twenty fail. This is a real '
            'cluster, and it really refuses.'
        ),
    ),
    dict(
        key='05-bg', kind='console', title='Blue And Green',
        body="""TWO. Blue and green.
  v2 beside v1; a test port
  reaches only v2.
  before the switch: v1 x 20.
  one patch to the service.
  after: v2 x 20, failed 0.""",
        narration=(
            'Second, blue and green. Version two runs beside version one, '
            'and only a test port reaches it. Twenty requests before the '
            'switch are all answered by version one. The switch is one '
            'patch to the service. Twenty after are all answered by '
            'version two, and none failed.'
        ),
    ),
    dict(
        key='06-back', kind='console', title='Going Back',
        body="""THREE. Going back.
  v2 has a bug with big orders.
  20 big orders on v2: 20 failed.
  one patch back to v1, whose
  pods never stopped:
  20 big orders, failed 0.""",
        narration=(
            'Third, going back. Version two has a bug with big orders. '
            'Twenty big orders on version two: all twenty fail. One patch '
            'sends the service back to version one, whose pods never '
            'stopped. Twenty big orders: none fail.'
        ),
    ),
    dict(
        key='07-canary', kind='console', title='A Canary',
        body="""FOUR. A canary.
  9 pods of v1, 1 of v2, behind
  one service.
  300 big orders: a small share
  failed, as a canary should be.

  the exact count changes from
  run to run.""",
        narration=(
            'Fourth, a canary. Nine pods of version one and one of '
            'version two, behind one service. Three hundred big orders: a '
            'few dozen failed, a small share, as a canary should be. The '
            "spread is chosen by the cluster's own rules, so the exact "
            'count changes from run to run. Had all three hundred gone to '
            'version two, all would have failed.'
        ),
    ),
    dict(
        key='08-gate', kind='console', title='Promote In Steps, With A Gate',
        body="""FIVE. Steps, with a gate.
  1, 5, 10 pods of v2.
  a gate at 5 failures in 100.
  buggy v2: halted, and every pod
  is v1 again.

  a small first step can miss it.""",
        narration=(
            'Fifth, promote in steps, with a gate. Steps of one, five and '
            'ten pods of version two, with a gate at five failures in a '
            'hundred. The buggy release is halted, and every pod is '
            'version one again. A first step with few requests can miss a '
            'bug, and the next step, with more traffic, catches it.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  both releases running:
  4 pods, where one needs 2.

  both share one database:
  a data change cannot go back.

  a cluster is a lot for one
  service.""",
        narration=(
            'Last, the bill. During a blue-green switch both releases are '
            'fully running: four pods, where one release needs two. Both '
            'share one database, so a release that changes the data '
            'cannot be switched back safely. And a cluster is a lot to '
            'run for a checkout.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Release beside the old version.', '', 'Switch by selector, go back by', 'selector.', '', 'Canary by replica counts, with a', 'gate.', '', 'Keep data compatible.'],
        narration=(
            'My verdict, plainly. Release beside the old version. On '
            'Kubernetes, switch with a selector and go back with the '
            'same. Use replica counts for a canary, with a gate on '
            'failures and enough traffic per step. Automate it with a '
            'rollout tool, and keep data changes compatible in both '
            'directions.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A Service whose `selector`', 'includes a `version` label.', '', 'Two Deployments of one app, with', 'different `version` labels.', '', 'Argo Rollouts or Flagger objects.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'Service whose selector includes a version label. Two '
            'Deployments of one app, with different version labels. Argo '
            'Rollouts or Flagger objects.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Kubernetes platforms and their', 'release tools.'],
        narration=(
            'You have met this in kubernetes platforms and their release '
            'tools.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Kubernetes via kind 0.33.', '', 'nginx alpine.', '', 'Docker 24 or later.'],
        narration=(
            'For the record. Kubernetes, via kind 0.33. nginx, alpine. '
            'Docker, 24 or later.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real', 'cluster, real pods, and a real', 'Service.', '', "The canary's spread is the", "cluster's own, so its counts", 'change from run to run.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: a real cluster, real pods, and a real '
            "service. The canary's spread is the cluster's own, so its "
            'counts change from run to run.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For an internal tool where a short', 'outage is fine, a plain restart is', 'enough, and a cluster is a lot to', 'run for one service.'],
        narration=(
            'So when is it too much? For an internal tool where a short '
            'outage is fine, a plain restart is enough, and a cluster is '
            'a lot to run for one service.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Change the gate to two failures in a hundred, and rerun act five..'],
        narration=(
            "That's Blue-Green and Canary with Kubernetes. [[slnc 250]] "
            'If you take one sentence away, take this one: on Kubernetes '
            'a release is a selector and some replica counts, and the '
            'cluster does the rest. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository. [[slnc 300]] If you try one exercise, '
            'change the gate to two failures in a hundred, and rerun act '
            'five. [[slnc 300]] If this helped, a like genuinely does '
            'help other people find it, and subscribe if you would like '
            'the rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
