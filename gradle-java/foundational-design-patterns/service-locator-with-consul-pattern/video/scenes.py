"""Scene definitions for the Service Locator with Consul teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Locator with Consul',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Service Locator '
            'pattern with Consul, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Service Locator video. That one '
            'argued against the pattern, but said it is still right when '
            'what is available is a fact you only learn at run time. '
            'Service discovery is exactly that, over a network. [[slnc '
            '350]] The plain definition, in short: ask a middleman for '
            'what you need, by name. [[slnc 300]] By the end you will see '
            'a real service registry answer, instances come and go '
            "without the caller's code changing, the old costs return, "
            'one new cost appear, and the alternative: be given an '
            'address, and never ask.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Service Locator, the hand-built', 'video, argued against the pattern:', 'invisible dependencies, a silent', 'compiler, everything coupled to it.', '', 'It also said: still right where', 'what is available is a run-time', 'fact.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'This video assumes the Service Locator video. If you have '
            'not seen it, start there. It argued against the pattern, '
            'with evidence, and it also said where the pattern is still '
            'right: where what is available is a run-time fact. [[slnc '
            '300]] This one uses the same checkout, with its '
            'collaborators now on the other side of a network. It does '
            'not teach the pattern again.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new:', 'Consul, Docker and nginx.', '', 'Consul is a service registry: services', 'register, callers ask for the healthy', 'ones. It runs here as a local process.', '', 'nginx, in Docker, is a proxy.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line, three new things. Consul is a service '
            'registry. Services register themselves, with a name, an '
            'address, and a health check. Callers ask for the healthy '
            'ones. It runs here as a plain local process. [[slnc 300]] '
            'Nginx is a web server and proxy, and Docker runs it in a '
            'container. [[slnc 300]] And a promise: skipping this video '
            'loses none of the pattern. The hand-built one teaches all of '
            "it, including the standard library's own form."
        ),
    ),
    dict(
        key='04-asks', kind='console', title='The Locator Asks Consul',
        body="""ONE. Consul answers.
  two payment-gateway
  instances, one notifier:
  each a real HTTP server,
  each with a health check.

  healthy gateways: 2

  four orders: gateway-1: 2,
  gateway-2: 2""",
        narration=(
            'Here is the setup. Two payment gateway instances and one '
            'notifier, each a real H T T P server, each registered with '
            'Consul with a health check. Nothing is simulated. [[slnc '
            '300]] The locator asks Consul for the healthy payment '
            'gateways. Two. Four orders are placed, and they are shared: '
            'two to each. [[slnc 300]] The checkout never knew an '
            'address. It asked for payment gateway, by name.'
        ),
    ),
    dict(
        key='05-changes', kind='console', title='The Genuine Advance',
        body="""TWO. Instances change.
  gateway-1's check fails.
  healthy now: 1

  four orders: gateway-1: 0,
  gateway-2: 4

  gateway-1 recovers:
  healthy: 2

  no change to the checkout.""",
        narration=(
            "Now the genuine advance. Gateway one's health check is "
            'marked as failing. Consul reports one healthy gateway. Four '
            'more orders: gateway one served none, gateway two served all '
            'four. [[slnc 300]] Gateway one recovers, and it is used '
            "again. The checkout's code did not change. A registry with "
            'fixed entries could never do this, and it is the reason this '
            'pattern earns its place.'
        ),
    ),
    dict(
        key='06-strings', kind='console', title='The Old Costs Return',
        body="""THREE. Strings.
  a typo, payment-gatway,
  compiled.
  at run time: no healthy
  instance of it.

  the notifier's registration
  is lost. on a real order:
  no healthy instance of
  notifier.

  1 charge already went through.""",
        narration=(
            'Now the old costs, over a network. The service names are '
            'strings. A typo, payment gatway, compiles fine, and fails at '
            'run time: no healthy instance. [[slnc 300]] And worse, the '
            "notifier's registration is lost. Nothing in the checkout "
            'says it needs one. On a real order, the checkout asks for '
            'the gateway, and the payment goes through. Then it asks for '
            'the notifier, and there is none. [[slnc 300]] The failure '
            'arrived in production, after the money moved. It is the same '
            'bill as the hand-built locator.'
        ),
    ),
    dict(
        key='07-stale', kind='console', title='A New Cost: A Stale Cache',
        body="""FOUR. Stale.
  a caching locator asked
  Consul once.

  gateway-1 dies. Consul is
  told. the cache is not.

  the call fails:
  ConnectException

  faster, and wrong.""",
        narration=(
            'A new cost, from the network. Asking Consul on every call is '
            'slow, so it is tempting to remember the answer. A caching '
            'locator asks Consul once. [[slnc 300]] Then gateway one '
            'dies, and Consul is told. The cache is not. The locator '
            'keeps handing out the dead address, and the call fails with '
            'a connection exception. Consul was asked once, in total. '
            'Faster, and wrong. [[slnc 300]] The uncached locator '
            'recovers at once. And after a refresh, the cache heals too. '
            'But when to refresh is now your problem.'
        ),
    ),
    dict(
        key='08-given', kind='console', title='The Alternative: Be Given',
        body="""FIVE. Be given.
  nginx, in Docker, was given
  the healthy instances once.

  the caller asks nothing:
  4 of 4 succeeded.

  gateway-2 stopped:
  4 of 4 still succeed.

  nginx retried the next.""",
        narration=(
            'The alternative, and the point of the whole category: stop '
            'asking. Nginx, in a Docker container, is given the healthy '
            'instances once, from Consul. The caller is given one '
            "address, nginx's, and asks nothing. Four of four requests "
            'succeed, shared across two instances. [[slnc 300]] Now stop '
            'one instance. Four of four more still succeed, all served by '
            'the survivor, because nginx retried the next one. [[slnc '
            '300]] The class never knew, because it never looked anything '
            "up. This is dependency injection's idea, at the level of a "
            'network address.'
        ),
    ),
    dict(
        key='09-verdict', kind='bullets', title='The Verdict',
        body=['Service discovery is the strongest', 'case for a locator: where instances', 'are is a run-time fact.', '', 'Even so, prefer to be given an address', 'by the platform, a proxy or DNS,', 'than to have every class ask.'],
        narration=(
            'My verdict, plainly. Service discovery is the strongest case '
            'for a locator, because where instances are is a genuine '
            'run-time fact. [[slnc 300]] Even so, prefer to be given an '
            'address, by the platform, a proxy, or D N S, than to have '
            'every class ask.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['DiscoveryClient.getInstances in', 'Spring Cloud.', '', 'A Consul, Eureka or ZooKeeper client', 'inside business classes.', '', 'A service name as a string, turned', 'into a URL at call time.', '', 'A load-balanced client, where the', 'lookup is hidden by an annotation.'],
        narration=(
            'How do you recognise this in code you did not write? '
            'Discovery client, get instances, in Spring Cloud. A Consul, '
            'Eureka, or ZooKeeper client, used inside business classes. A '
            'service name as a string, turned into a U R L at call time. '
            'And a load balanced client, where the lookup is hidden '
            'behind an annotation.'
        ),
    ),
    dict(
        key='11-met', kind='bullets', title='Where You Have Met This',
        body=["Spring Cloud's DiscoveryClient.", 'Netflix Eureka. Consul itself.', '', 'Kubernetes DNS is the given form.'],
        narration=(
            "You have met this in Spring Cloud's discovery client, in "
            "Netflix Eureka, and in Consul itself. And Kubernetes' "
            'built-in D N S is the given form: the platform hands your '
            'code an address, and it never asks.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real Consul', 'agent, real HTTP servers, a real', 'nginx in a real container.', '', 'The demo instances listen only for', 'the length of the run.'],
        narration=(
            'The same honest admission as everywhere in this course, and '
            'for once nothing is simulated. A real Consul agent, real H T '
            'T P servers, and a real nginx in a real container. The demo '
            'instances only listen for the length of the run.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a fixed set of services with', 'fixed addresses, configuration is', 'simpler, and needs no registry.'],
        narration=(
            'So when is it too much? For a fixed set of services with '
            'fixed addresses, configuration is simpler, and needs no '
            'registry at all.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Give the caching locator a', 'time to live, and see what you decided.'],
        narration=(
            "That's the Service Locator with Consul. [[slnc 250]] If you "
            'take one sentence away, take this one: discovery is a '
            'legitimate locator, and being given an address is better '
            'still. [[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, give the '
            'caching locator a time to live, and notice the decision you '
            'just made. [[slnc 300]] If this helped, a like genuinely '
            'does help other people find it, and subscribe if you would '
            'like the rest of the series. [[slnc 250]] Thanks for '
            'watching.'
        ),
    ),
]
