"""Scene definitions for the Blue-Green and Canary with Kubernetes teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Blue-Green and Canary with Kubernetes',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Blue-Green and Canary patterns in Java, using Kubernetes. '
            '[[slnc 300]] This video is presented by Jayasekhar Konduru. '
            '[[slnc 600]] First, a simple definition. [[slnc 300]] '
            'Blue-green runs the old and new releases side by side, and '
            'switches all the traffic at once. [[slnc 300]] A canary '
            'sends a small share of traffic to the new release first, and '
            'grows it while it stays healthy. [[slnc 600]] On Kubernetes, '
            'blue-green is one change to which copies a service points '
            'at. [[slnc 300]] And a canary is a change to how many copies '
            'of each release are running. [[slnc 700]] In our online '
            'store, a new checkout release must go live safely. [[slnc '
            '500]] By the end, you will hear a real cluster fail every '
            'request while a release is replaced. [[slnc 300]] A real '
            'switch, and a real switch back. [[slnc 300]] A canary spread '
            'by the cluster itself. [[slnc 300]] A gate that stops a bad '
            'release. [[slnc 300]] And the bill.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Blue-Green and Canary, the hand-', 'built video, runs two releases', 'behind a router that is a rule.', '', 'It shows a switch, a switch back,', 'a canary and a gate.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'This video builds on the plain Java Blue-Green and Canary '
            'video. [[slnc 300]] If you have not seen it, start there. '
            '[[slnc 500]] That video runs two releases behind a simple '
            'routing rule. [[slnc 300]] And it shows a switch, a switch '
            'back, a canary, and a gate. [[slnc 500]] This video uses the '
            'same example. [[slnc 300]] It does not teach the pattern '
            'again. [[slnc 300]] It shows what Kubernetes does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new: Kubernetes,', 'kind, and Docker.', '', 'You need Docker running, with kind', 'and kubectl installed. Without', 'them the demo says so and stops.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before any code, what is Kubernetes? [[slnc 400]] Kubernetes '
            'runs containers in small groups, called pods. [[slnc 300]] '
            'And it keeps as many pods running as you ask for. [[slnc '
            '500]] A service gives those pods one address. [[slnc 300]] '
            'It picks which pods to send traffic to by their labels. '
            '[[slnc 500]] A tool called kind runs a whole Kubernetes '
            'cluster inside Docker, on your own machine. [[slnc 300]] You '
            'need Docker running, with kind and the kube control tool '
            'installed. [[slnc 300]] Without them, the demo says so, and '
            'stops. [[slnc 500]] And a promise. [[slnc 300]] Skipping '
            'this video loses none of the pattern. [[slnc 300]] The plain '
            'Java video teaches all of it.'
        ),
    ),
    dict(
        key='04-gap', kind='console', title='Replace It Where It Stands',
        body="""ONE. Replace it in place.
  v1 stopped to make room for v2.
  20 requests, nothing running:
  failed 20 of 20.""",
        narration=(
            'First demo: replace it where it stands. [[slnc 400]] Version '
            'one is stopped, to make room for version two. [[slnc 300]] '
            'Twenty requests arrive while nothing is running. [[slnc '
            '300]] And all twenty fail. [[slnc 500]] This is a real '
            'cluster, and it really refuses them.'
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
            'Second demo: blue and green. [[slnc 400]] Version two runs '
            'beside version one. [[slnc 300]] Only a separate test port '
            'can reach it. [[slnc 500]] Twenty requests before the switch '
            'are all answered by version one. [[slnc 300]] The switch is '
            'one change to the service. [[slnc 300]] Twenty requests '
            'after it are all answered by version two. [[slnc 300]] And '
            'none failed.'
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
            'Third demo: going back. [[slnc 400]] Version two has a bug '
            'with big orders. [[slnc 300]] Twenty big orders go to '
            'version two, and all twenty fail. [[slnc 500]] One change '
            'points the service back at version one. [[slnc 300]] Its '
            'pods never stopped. [[slnc 300]] Twenty big orders: none '
            'fail.'
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
            'Fourth demo: a canary. [[slnc 400]] Nine pods of version '
            'one, and one pod of version two, behind one service. [[slnc '
            '500]] Three hundred big orders are sent. [[slnc 300]] A few '
            'dozen fail: a small share, just as a canary should be. '
            '[[slnc 500]] The cluster itself decides how to spread the '
            'requests. [[slnc 300]] So the exact count changes from run '
            'to run. [[slnc 300]] If all three hundred had gone to '
            'version two, every one would have failed.'
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
            'Fifth demo: promote in steps, with a gate. [[slnc 400]] The '
            'steps are one, five, and ten pods of version two. [[slnc '
            '300]] The gate says: stop if more than five requests in a '
            'hundred fail. [[slnc 500]] The buggy release is stopped. '
            '[[slnc 300]] And every pod is version one again. [[slnc '
            '500]] One lesson: a first step with only a few requests can '
            'miss a bug. [[slnc 300]] The next step, with more traffic, '
            'is what catches it.'
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
            'Finally, the bill. [[slnc 400]] During a blue-green switch, '
            'both releases are fully running. [[slnc 300]] Four pods, '
            'where one release needs only two. [[slnc 500]] Both releases '
            'share one database. [[slnc 300]] So a release that changes '
            'the shape of the data cannot be switched back safely. [[slnc '
            '500]] And a whole cluster is a lot to run, just for a '
            'checkout.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Release beside the old version.', '', 'Switch by selector, go back by', 'selector.', '', 'Canary by replica counts, with a', 'gate.', '', 'Keep data compatible.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Release beside the old '
            'version. [[slnc 300]] On Kubernetes, switch by changing '
            'where the service points, and go back the same way. [[slnc '
            '300]] Use pod counts for a canary, with a gate on failures, '
            'and enough traffic at each step. [[slnc 300]] Use a rollout '
            'tool to automate it. [[slnc 300]] And keep data changes '
            'readable by both releases.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A Service whose `selector`', 'includes a `version` label.', '', 'Two Deployments of one app, with', 'different `version` labels.', '', 'Argo Rollouts or Flagger objects.'],
        narration=(
            'How can you spot this in a system someone else built? [[slnc '
            '400]] Look for a service that picks its pods by a version '
            'label. [[slnc 300]] Look for two deployments of one app, '
            'with different version labels. [[slnc 300]] Or look for '
            'rollout tools like Argo Rollouts or Flagger.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Kubernetes platforms and their', 'release tools.'],
        narration=(
            'Where have you met this before? [[slnc 300]] On Kubernetes '
            'platforms, and the release tools built for them.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Kubernetes via kind 0.33.', '', 'nginx alpine.', '', 'Docker 24 or later.'],
        narration=(
            'For the record, here is what was used. [[slnc 300]] '
            'Kubernetes, run through kind, version zero point '
            'thirty-three. [[slnc 300]] The nginx web server, as the '
            'stand-in service. [[slnc 300]] And Docker, version '
            'twenty-four or later.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real', 'cluster, real pods, and a real', 'Service.', '', "The canary's spread is the", "cluster's own, so its counts", 'change from run to run.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is real: a real cluster, real pods, and a real '
            "service. [[slnc 300]] The canary's spread is chosen by the "
            'cluster. [[slnc 300]] So its counts change from run to run.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For an internal tool where a short', 'outage is fine, a plain restart is', 'enough, and a cluster is a lot to', 'run for one service.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For an internal tool '
            'where a short outage is fine, a plain restart is enough. '
            '[[slnc 300]] And a cluster is a lot to run for one service.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Change the gate to two failures in a hundred, and rerun act five..'],
        narration=(
            "That's Blue-Green and Canary, with Kubernetes. [[slnc 400]] "
            'If you remember one sentence, make it this one. [[slnc 300]] '
            'On Kubernetes, a release is a label choice and some pod '
            'counts, and the cluster does the rest. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Change the gate to two '
            'failures in a hundred. [[slnc 300]] Then run the fifth demo '
            'again. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
