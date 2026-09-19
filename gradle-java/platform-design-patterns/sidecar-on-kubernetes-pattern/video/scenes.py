"""Scene definitions for the Sidecar on Kubernetes teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Sidecar on Kubernetes',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Sidecar pattern '
            'on Kubernetes, in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] It is the third of three '
            'Sidecar videos. The first taught the pattern: a helper '
            'process that runs beside a service and handles a concern for '
            'it. The second swapped the helper for one written in Java. '
            'This one is about where sidecars actually live. [[slnc 350]] '
            'The plain definition, in short: a Pod is two or more '
            'containers that share one network and one fate. [[slnc 300]] '
            'By the end you will know four things a Pod guarantees, one '
            'popular claim about crashes that is not true, and whether '
            'you need any of it yet.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='Read The First Video First',
        body=['Sidecar taught the pattern: why the', 'retry code left the service.', '', 'Sidecar with a Java proxy swapped the', 'helper for one written in Java.', '', 'This one asks: what changes when', 'Kubernetes runs the two containers?', '', 'If you have not seen the first,', 'start there.'],
        narration=(
            'This video assumes the first Sidecar video. If you have not '
            'seen it, start there. It explains what a sidecar is, why the '
            'retry code left the service, and what a second process '
            'costs. [[slnc 300]] This one takes the same two containers, '
            'the checkout service and the proxy beside it, and asks one '
            'question: what changes when Kubernetes runs them?'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before Any Command: What Kubernetes Is',
        body=['Kubernetes runs containers across', 'machines and keeps them running.', '', 'You describe what you want in a file.', 'It makes it true, and keeps it true.', '', 'Its unit is the Pod: containers placed', 'together, sharing a network, living', 'and dying as one.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before anything else, what Kubernetes is, because it is the '
            'heaviest thing in this course. Kubernetes runs containers '
            'across one or many machines, and keeps them running. You '
            'describe what you want in a file, for example, one copy of '
            'checkout with a proxy beside it. Kubernetes makes it true, '
            'and keeps making it true. If a container dies, it restarts '
            'it. [[slnc 300]] Its unit is the Pod: one or more '
            'containers, placed together, sharing one network, and living '
            'and dying as one. [[slnc 300]] And a promise: skipping this '
            'video loses none of the pattern. The first Sidecar video '
            'teaches all of it. The model in this video needs no cluster '
            'at all.'
        ),
    ),
    dict(
        key='04-analogy', kind='bullets', title='Two Ways To Share',
        body=['Two flatmates who share a phone line:', 'they agreed to it. If one moves out,', 'the line stays.', '', 'A couple who share a flat: nobody set', 'anything up. One address, one front', 'door, one lease. Give up the flat,', 'and both leave.', '', 'Compose is the first. A Pod is the', 'second.'],
        narration=(
            'An analogy, before the shop. Two flatmates who share a phone '
            'line have agreed to it. Either can ring the other from the '
            'hall, but only because they set it up, and if one moves out, '
            'the line stays. Now a couple who share a flat. Nobody set '
            'anything up. One address, one front door, one lease. Give up '
            'the flat, and both leave together. [[slnc 300]] Two '
            'containers in a Docker Compose file are the flatmates. Two '
            'containers in a Pod are the couple.'
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
            'First, the network. In Compose, one line, network mode, '
            "service checkout, makes the proxy share checkout's network. "
            'With it, checkout reaches local host eighty-eighty-one. '
            'True. Forget that one line, and it is false. Refused. [[slnc '
            '300]] In a Pod, checkout reaches the proxy, true, and there '
            'is no line to forget. Both containers are on one address, '
            'one network, because that is what a Pod is. Sharing by '
            'configuration can be forgotten. Sharing by definition '
            'cannot.'
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
            'Second, the lifecycle. In Compose, stop the checkout '
            'container, and the proxy is still running, on its own, '
            'beside nothing. In a Pod, delete it, and both containers go '
            'together. [[slnc 300]] The replacement is a new Pod, on a '
            'new address, with both containers new. The Pod is scheduled, '
            'evicted, and deleted as one unit.'
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
            'Now a correction, because it is a common thing to say. It is '
            'tempting to say, if one container in a Pod crashes, it takes '
            "the other with it. It does not. [[slnc 300]] The proxy's "
            'process dies. The Pod reads one of two. A payment now fails: '
            'connection refused. Then the kubelet, the agent on each '
            'machine, restarts the proxy, on its own. Two of two again. '
            "The proxy's restart count is one. Checkout's is zero. "
            'Checkout was never touched. [[slnc 300]] What is shared is '
            'the Pod: scheduling, eviction, and deletion. Not process '
            'death. The gap is real, though: while the proxy is down, the '
            "service's calls fail, exactly as in the first video."
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
            'Third, injection. The refunds team wrote a manifest with one '
            'container, refunds. The Pod that was created has two: '
            'refunds, and a sidecar proxy. The manifest the team wrote is '
            'unchanged. The sidecar arrived from outside. [[slnc 300]] '
            'That is the mechanism every service mesh is built on. As '
            'each Pod is created, an admission step adds a proxy to it, '
            'and no team wrote it. This project does it by hand. A real '
            'cluster does it with a webhook, which is named here, and not '
            'built.'
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
            'Fourth, what you see. Kubectl get pods prints two of two, '
            'for one logical service made of two containers. With the '
            'proxy down, it prints one of two, and the Pod stops '
            'receiving traffic. [[slnc 300]] And a subtle problem. Start '
            'the containers together, and the service can start, and call '
            'the proxy, before the proxy is listening. A native sidecar '
            'fixes it: an init container marked to keep running, started '
            'first, and required to be up before the service starts. '
            'Proxy first, then checkout.'
        ),
    ),
    dict(
        key='10-bill', kind='bullets', title='The Bill, And The Honest Question',
        body=['Everything Compose cost, plus a cluster:', 'a scheduler, a control plane,', 'a YAML dialect, a networking model.', '', 'For four services: do you need', 'Kubernetes yet? Almost certainly not.', '', 'For a fleet, this is the bargain.'],
        narration=(
            'Now the bill. Everything the Compose version cost, plus a '
            'cluster. A scheduler, a control plane, a YAML dialect, and a '
            'networking model, added to a shop that worked with two '
            'containers and a file. [[slnc 300]] For a fleet, that is a '
            'bargain. For four services, it is the reason do you need '
            'Kubernetes yet is a real question. And for four services, '
            'the honest answer is: almost certainly not.'
        ),
    ),
    dict(
        key='11-not-show', kind='bullets', title='What The Model Does Not Show',
        body=['A scheduler choosing a machine.', 'A control plane that fails.', 'Restart back-off.', '', 'A real cluster, kind, closes most of', 'this on one laptop. It is not a fleet.'],
        narration=(
            'What this model does not show. A scheduler choosing a '
            'machine. A control plane that can fail. Restart back-off: a '
            'real kubelet waits longer between each restart of a '
            'container that keeps crashing. [[slnc 300]] There is a '
            'second tier in the repository, that runs these same two '
            'containers on a real cluster, called kind, and it closes '
            'most of that gap. It does not close all of it. A cluster on '
            'one laptop is not a fleet.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every Pod in every cluster.', '', 'And the proxy a service mesh injects', 'beside your service.'],
        narration=(
            'You have met this in every Pod in every cluster, and in the '
            'proxy a service mesh injects beside your service. Now you '
            'know what the two-of-two means, and why the proxy is there.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['This video is a plain-Java model:', 'no cluster, no containers.', '', 'The claims are the ones a real', 'cluster makes, and the second tier', 'checks them against one.'],
        narration=(
            'The same honest admission as everywhere in this course. This '
            'video is a plain Java model. There is no cluster and no '
            'container. The claims are the ones a real cluster makes, and '
            'the second tier of the project checks them against one.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['For four services, or one team,', 'Docker Compose is cheaper, faster to', 'start, and has fewer ways to fail.'],
        narration=(
            'So when is Kubernetes too much? For four services, or one '
            'team, Docker Compose is cheaper, faster to start, and has '
            'fewer ways to fail.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a second sidecar to the', 'Pod, and see what it shares.'],
        narration=(
            "That's Sidecar on Kubernetes. [[slnc 250]] If you take one "
            'sentence away, take this one: a Pod shares its network and '
            'its fate by definition, but not its process deaths. [[slnc '
            '350]] The full source, the written notes, the diagrams and '
            'an animated walkthrough are all in the repository. [[slnc '
            '300]] If you try one exercise, add a second sidecar, a log '
            'shipper, to the Pod, and see what it shares. [[slnc 300]] If '
            'this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
