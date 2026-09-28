"""Scene definitions for the Sidecar on Kubernetes teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Sidecar on Kubernetes',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Sidecar pattern on Kubernetes, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A sidecar is a '
            'helper program that runs beside a service, and handles a job '
            'for it. [[slnc 300]] On Kubernetes, the service and its '
            'helper live together in a Pod. [[slnc 300]] A Pod is two or '
            'more containers that share one network, and one fate. [[slnc '
            '600]] This is the third of three Sidecar videos. [[slnc '
            '300]] The first taught the pattern. [[slnc 300]] The second '
            'swapped the helper for one written in Java. [[slnc 300]] '
            'This one is about where sidecars actually live. [[slnc 700]] '
            'In our online store, the checkout service and the proxy '
            'beside it run together. [[slnc 500]] By the end, you will '
            'know four things a Pod guarantees. [[slnc 300]] One popular '
            'claim about crashes that is not true. [[slnc 300]] And '
            'whether you need any of this yet.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='Read The First Video First',
        body=['Sidecar taught the pattern: why the', 'retry code left the service.', '', 'Sidecar with a Java proxy swapped the', 'helper for one written in Java.', '', 'This one asks: what changes when', 'Kubernetes runs the two containers?', '', 'If you have not seen the first,', 'start there.'],
        narration=(
            'This video builds on the first Sidecar video. [[slnc 300]] '
            'If you have not seen it, start there. [[slnc 500]] It '
            'explains what a sidecar is, why the retry code left the '
            'service, and what a second program costs. [[slnc 500]] This '
            'video takes the same two containers: the checkout service, '
            'and the proxy beside it. [[slnc 300]] And asks one question. '
            '[[slnc 300]] What changes when Kubernetes runs them?'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before Any Command: What Kubernetes Is',
        body=['Kubernetes runs containers across', 'machines and keeps them running.', '', 'You describe what you want in a file.', 'It makes it true, and keeps it true.', '', 'Its unit is the Pod: containers placed', 'together, sharing a network, living', 'and dying as one.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before anything else, what is Kubernetes? [[slnc 400]] '
            'Kubernetes runs containers across one or many machines, and '
            'keeps them running. [[slnc 500]] You describe what you want '
            'in a file. [[slnc 300]] For example: one copy of checkout, '
            'with a proxy beside it. [[slnc 300]] Kubernetes makes that '
            'true, and keeps it true. [[slnc 300]] If a container dies, '
            'it restarts it. [[slnc 600]] Its basic unit is the Pod. '
            '[[slnc 300]] One or more containers, placed together, '
            'sharing one network, living and dying as one. [[slnc 600]] '
            'And a promise. [[slnc 300]] Skipping this video loses none '
            'of the pattern. [[slnc 300]] The first Sidecar video teaches '
            'all of it. [[slnc 300]] And the model in this video needs no '
            'cluster at all.'
        ),
    ),
    dict(
        key='04-analogy', kind='bullets', title='Two Ways To Share',
        body=['Two flatmates who share a phone line:', 'they agreed to it. If one moves out,', 'the line stays.', '', 'A couple who share a flat: nobody set', 'anything up. One address, one front', 'door, one lease. Give up the flat,', 'and both leave.', '', 'Compose is the first. A Pod is the', 'second.'],
        narration=(
            'An analogy, before the shop. [[slnc 500]] Two flatmates who '
            'share a phone line have agreed to share it. [[slnc 300]] '
            'They set it up. [[slnc 300]] And if one moves out, the line '
            'stays. [[slnc 600]] Now think of a couple who share a flat. '
            '[[slnc 300]] Nobody set anything up. [[slnc 300]] One '
            'address, one front door, one lease. [[slnc 300]] Give up the '
            'flat, and both leave together. [[slnc 600]] Two containers '
            'in a Docker Compose file are like the flatmates. [[slnc '
            '300]] Two containers in a Pod are like the couple.'
        ),
    ),
    dict(
        key='05-shared', kind='console', title='Shared By Definition',
        body="""ONE. The network.
  Compose, with the line:
  reaches localhost:8081: true
  Compose, line forgotten:
  false

  a Pod: true. there is no
  line to forget.

  both on 10.244.0.10.""",
        narration=(
            'First demo: the network. [[slnc 400]] In Docker Compose, one '
            "line of settings makes the proxy share checkout's network. "
            '[[slnc 500]] With that line, checkout can reach the proxy. '
            '[[slnc 300]] Forget that one line, and the connection is '
            'refused. [[slnc 600]] In a Pod, checkout reaches the proxy. '
            '[[slnc 300]] And there is no line to forget. [[slnc 300]] '
            'Both containers share one address, because that is what a '
            'Pod is. [[slnc 600]] Sharing by settings can be forgotten. '
            '[[slnc 300]] Sharing by definition cannot.'
        ),
    ),
    dict(
        key='06-lifecycle', kind='console', title='One Lifecycle',
        body="""TWO. Lifecycle.
  Compose: checkout stopped.
  the proxy is still running.

  Pod: deleted.
  checkout: not running
  proxy: not running

  the replacement is a new
  Pod on a new address.""",
        narration=(
            'Second demo: living and dying together. [[slnc 400]] In '
            'Docker Compose, stop the checkout container. [[slnc 300]] '
            'The proxy keeps running, on its own, beside nothing. [[slnc '
            '600]] In a Pod, delete the Pod, and both containers go '
            'together. [[slnc 500]] The replacement is a brand new Pod, '
            'at a new address, with both containers new. [[slnc 300]] A '
            'Pod is placed, moved, and deleted as one unit.'
        ),
    ),
    dict(
        key='07-restarts', kind='console', title='But Restarts Are Per Container',
        body="""THREE. Restarts.
  the proxy's process dies.
  Pod: 1/2. a payment:
  connection refused.

  the kubelet restarts the
  proxy alone.
  Pod 2/2, proxy restarts 1,
  checkout restarts 0.

  a crash does not take a
  neighbour with it.""",
        narration=(
            'Third demo, and a correction to a common claim. [[slnc 400]] '
            'People often say: if one container in a Pod crashes, it '
            'takes the other with it. [[slnc 300]] It does not. [[slnc '
            "600]] The proxy's process dies. [[slnc 300]] The Pod now "
            'shows one of two containers ready. [[slnc 300]] A payment '
            'fails: connection refused. [[slnc 500]] Then the agent on '
            'each machine, called the kubelet, restarts the proxy, on its '
            'own. [[slnc 300]] Two of two again. [[slnc 300]] The proxy '
            'has restarted once. [[slnc 300]] Checkout has restarted zero '
            'times. [[slnc 300]] It was never touched. [[slnc 600]] What '
            "is shared is the Pod's placement, moving, and deletion. "
            '[[slnc 300]] Not a crash. [[slnc 500]] But the gap is real. '
            "[[slnc 300]] While the proxy is down, the service's calls "
            'fail, just as in the first video.'
        ),
    ),
    dict(
        key='08-injection', kind='console', title='Injection',
        body="""FOUR. Injection.
  the manifest the refunds team
  wrote: 1 container [refunds]

  the Pod that was created: 2
  [refunds, sidecar-proxy]

  the authored manifest is
  unchanged.
  the sidecar arrived from
  outside.""",
        narration=(
            'Fourth demo: injection. [[slnc 400]] The refunds team wrote '
            'a Pod description with one container: refunds. [[slnc 500]] '
            'But the Pod that was created has two containers. [[slnc '
            '300]] Refunds, and a sidecar proxy. [[slnc 500]] The '
            'description the team wrote is unchanged. [[slnc 300]] The '
            'sidecar was added from outside. [[slnc 600]] That is how '
            'every service mesh works. [[slnc 300]] As each Pod is '
            'created, an extra step adds a proxy to it. [[slnc 300]] No '
            'team wrote it. [[slnc 500]] This project does it by hand. '
            '[[slnc 300]] A real cluster does it with a hook called an '
            'admission webhook.'
        ),
    ),
    dict(
        key='09-ready', kind='console', title='READY 2/2',
        body="""FIVE. READY.
  checkout   READY 2/2

  with the proxy down: 1/2,
  and the Pod is not ready
  for traffic.

  started together, a race:
  [checkout, sidecar-proxy]

  a native sidecar starts first:
  [sidecar-proxy, checkout]""",
        narration=(
            "Fifth demo: what you see. [[slnc 400]] Kubernetes' "
            'command-line tool shows two of two, for one service made of '
            'two containers. [[slnc 500]] With the proxy down, it shows '
            'one of two. [[slnc 300]] And the Pod stops receiving '
            'traffic. [[slnc 600]] And one subtle problem. [[slnc 300]] '
            'If both containers start together, checkout may call the '
            'proxy before the proxy is listening. [[slnc 500]] A native '
            'sidecar fixes this. [[slnc 300]] It is a helper container '
            'that starts first, keeps running, and must be ready before '
            'the service starts. [[slnc 300]] Proxy first, then checkout.'
        ),
    ),
    dict(
        key='10-bill', kind='bullets', title='The Bill, And The Honest Question',
        body=['Everything Compose cost, plus a cluster:', 'a scheduler, a control plane,', 'a YAML dialect, a networking model.', '', 'For four services: do you need', 'Kubernetes yet? Almost certainly not.', '', 'For a fleet, this is the bargain.'],
        narration=(
            'Now the bill. [[slnc 400]] Everything the Docker Compose '
            'version cost, plus a whole cluster. [[slnc 300]] A '
            'scheduler, a control system, a settings language, and a '
            'networking model. [[slnc 300]] Added to a shop that already '
            'worked with two containers and one file. [[slnc 600]] For a '
            'large fleet of services, that is a bargain. [[slnc 300]] For '
            'four services, it raises a real question: do you need '
            'Kubernetes yet? [[slnc 300]] And for four services, the '
            'honest answer is: almost certainly not.'
        ),
    ),
    dict(
        key='11-not-show', kind='bullets', title='What The Model Does Not Show',
        body=['A scheduler choosing a machine.', 'A control plane that fails.', 'Restart back-off.', '', 'A real cluster, kind, closes most of', 'this on one laptop. It is not a fleet.'],
        narration=(
            'What this model does not show. [[slnc 400]] A scheduler '
            'choosing which machine to use. [[slnc 300]] A control system '
            'that can itself fail. [[slnc 300]] And restart back-off, '
            'where a real cluster waits longer between restarts of a '
            'container that keeps crashing. [[slnc 600]] A second version '
            'in the repository runs the same two containers on a real '
            'cluster, using a tool called kind. [[slnc 300]] It closes '
            'most of that gap. [[slnc 300]] But a cluster on one laptop '
            'is still not a fleet.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every Pod in every cluster.', '', 'And the proxy a service mesh injects', 'beside your service.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In every Pod, '
            'in every Kubernetes cluster. [[slnc 300]] And in the proxy a '
            'service mesh adds beside your service. [[slnc 300]] Now you '
            'know what two of two means, and why the proxy is there.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['This video is a plain-Java model:', 'no cluster, no containers.', '', 'The claims are the ones a real', 'cluster makes, and the second tier', 'checks them against one.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] It is a '
            'plain Java model. [[slnc 300]] There is no cluster, and no '
            'container. [[slnc 300]] But its claims are the ones a real '
            'cluster makes. [[slnc 300]] And the second version of the '
            'project checks them against a real one.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['For four services, or one team,', 'Docker Compose is cheaper, faster to', 'start, and has fewer ways to fail.'],
        narration=(
            'So, when is Kubernetes too much? [[slnc 400]] For four '
            'services, or one team, Docker Compose is cheaper, faster to '
            'start, and has fewer ways to fail.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a second sidecar to the', 'Pod, and see what it shares.'],
        narration=(
            "That's the Sidecar pattern, on Kubernetes. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] A '
            'Pod shares its network and its fate by definition, but a '
            'crash in one container does not take the other with it. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 500]] Here is one exercise to try. [[slnc 300]] Add a '
            'second sidecar to the Pod, a log shipper. [[slnc 300]] And '
            'see what it shares. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
