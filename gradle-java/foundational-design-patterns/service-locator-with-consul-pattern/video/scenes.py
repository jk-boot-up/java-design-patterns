"""Scene definitions for the Service Locator with Consul teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Locator with Consul',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Service Locator pattern, in Java, using Consul. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A service locator '
            'is a middleman. [[slnc 300]] You ask it for what you need, '
            'by name. [[slnc 600]] Think of a taxi dispatcher. [[slnc '
            '300]] You ask for a taxi, and the dispatcher knows which '
            'cars are free right now. [[slnc 700]] This is the framework '
            'version of the Service Locator video. [[slnc 300]] That one '
            'argued against the pattern. [[slnc 300]] But it said the '
            'pattern is still right when what is available is only known '
            'while the program runs. [[slnc 300]] Finding services across '
            'a network is exactly that. [[slnc 500]] By the end, you will '
            'hear a real service registry answer. [[slnc 300]] Services '
            "come and go, without the caller's code changing. [[slnc "
            '300]] The old costs return, a new one appears, and then we '
            'hear the alternative: be given an address, and never ask.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Service Locator, the hand-built', 'video, argued against the pattern:', 'invisible dependencies, a silent', 'compiler, everything coupled to it.', '', 'It also said: still right where', 'what is available is a run-time', 'fact.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Service Locator video. [[slnc 400]] '
            'That one argued against the pattern, with evidence. [[slnc '
            '300]] And it said where the pattern is still right. [[slnc '
            '500]] Here, we use the same checkout. [[slnc 300]] But its '
            'helpers now live on the other side of a network. [[slnc '
            '300]] We will not teach the pattern again.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new:', 'Consul, Docker and nginx.', '', 'Consul is a service registry: services', 'register, callers ask for the healthy', 'ones. It runs here as a local process.', '', 'nginx, in Docker, is a proxy.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Three things are new in this project. [[slnc 400]] First, '
            'Consul, a service registry. [[slnc 300]] Services register '
            'themselves, with a name, an address, and a health check. '
            '[[slnc 300]] Callers ask Consul for the healthy ones. [[slnc '
            '500]] Second and third, nginx, a web server that can forward '
            'requests, running inside Docker. [[slnc 500]] And one '
            'promise. [[slnc 300]] If you skip this video, you lose none '
            'of the pattern. [[slnc 300]] This one is about the tools.'
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
            'First demo: the locator asks Consul. [[slnc 400]] Here is '
            'the setup. [[slnc 300]] Two payment gateway services, and '
            'one notifier. [[slnc 300]] Each is a real web server, '
            'registered with Consul, with a health check. [[slnc 300]] '
            'Nothing is simulated. [[slnc 500]] The locator asks Consul '
            'for the healthy payment gateways. [[slnc 300]] There are '
            'two. [[slnc 300]] Four orders are placed, and shared, two to '
            'each. [[slnc 500]] The checkout never knew an address. '
            '[[slnc 300]] It only asked for payment gateway, by name.'
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
            "Second demo: the real advance. [[slnc 400]] Gateway one's "
            'health check is marked as failing. [[slnc 300]] Consul now '
            'reports one healthy gateway. [[slnc 500]] Four more orders. '
            '[[slnc 300]] Gateway one serves none. [[slnc 300]] Gateway '
            'two serves all four. [[slnc 500]] Then gateway one recovers, '
            "and it is used again. [[slnc 300]] The checkout's code never "
            'changed. [[slnc 500]] A registry with fixed entries could '
            'never do this. [[slnc 300]] And it is why this pattern earns '
            'its place here.'
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
            'Third demo: the old costs return. [[slnc 400]] Service names '
            'are just text. [[slnc 300]] A typo, payment gatway, compiles '
            'fine. [[slnc 300]] And fails only while running: no healthy '
            "service by that name. [[slnc 500]] Worse, the notifier's "
            'registration is lost. [[slnc 300]] And nothing in the '
            'checkout says it needs one. [[slnc 500]] A real order '
            'arrives. [[slnc 300]] The checkout asks for a gateway, and '
            'the payment goes through. [[slnc 300]] Then it asks for the '
            'notifier, and there is none. [[slnc 500]] The failure '
            'arrived in production, after the money moved. [[slnc 300]] '
            'The same cost as the hand-built locator.'
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
            'Fourth demo: a new cost, an out-of-date cache. [[slnc 400]] '
            'Asking Consul on every call is slow. [[slnc 300]] So it is '
            'tempting to remember the answer. [[slnc 500]] A caching '
            'locator asks Consul just once. [[slnc 300]] Then gateway one '
            'dies, and Consul is told. [[slnc 300]] But the cache is not '
            'told. [[slnc 500]] The locator keeps handing out the dead '
            'address. [[slnc 300]] And the call fails, with a connection '
            'error. [[slnc 300]] Faster, and wrong. [[slnc 500]] The '
            'locator without a cache recovers at once. [[slnc 300]] And '
            'after a refresh, the cache heals too. [[slnc 300]] But '
            'deciding when to refresh is now your problem.'
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
            'Fifth demo: the alternative, be given. [[slnc 400]] Nginx, '
            'in a Docker container, is given the list of healthy '
            'services, once, from Consul. [[slnc 300]] The calling code '
            "is given just one address: nginx's. [[slnc 300]] It asks "
            'nothing. [[slnc 500]] Four out of four requests succeed, '
            'shared across the two gateways. [[slnc 500]] Now stop one '
            'gateway. [[slnc 300]] Four more requests, and all four still '
            'succeed. [[slnc 300]] Nginx simply retried the one that was '
            'still running. [[slnc 500]] The calling code never knew, '
            'because it never looked anything up. [[slnc 300]] That is '
            "dependency injection's idea, applied to a network address."
        ),
    ),
    dict(
        key='09-verdict', kind='bullets', title='The Verdict',
        body=['Service discovery is the strongest', 'case for a locator: where instances', 'are is a run-time fact.', '', 'Even so, prefer to be given an address', 'by the platform, a proxy or DNS,', 'than to have every class ask.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Finding services on a '
            'network is the strongest case for a locator. [[slnc 300]] '
            'Because where the services are is only known while the '
            'program runs. [[slnc 500]] Even so, prefer to be given an '
            'address. [[slnc 300]] By the platform, a proxy, or D N S. '
            '[[slnc 300]] Rather than making every class ask.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['DiscoveryClient.getInstances in', 'Spring Cloud.', '', 'A Consul, Eureka or ZooKeeper client', 'inside business classes.', '', 'A service name as a string, turned', 'into a URL at call time.', '', 'A load-balanced client, where the', 'lookup is hidden by an annotation.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            "400]] Look for Spring Cloud's Discovery Client, and its get "
            'instances method. [[slnc 300]] Look for a Consul, Eureka, or '
            'ZooKeeper client, used inside business classes. [[slnc 300]] '
            'Look for a service name, written as text, turned into a web '
            'address at call time. [[slnc 300]] And a load-balanced '
            'client, where the lookup hides behind an annotation.'
        ),
    ),
    dict(
        key='11-met', kind='bullets', title='Where You Have Met This',
        body=["Spring Cloud's DiscoveryClient.", 'Netflix Eureka. Consul itself.', '', 'Kubernetes DNS is the given form.'],
        narration=(
            'Where have you met this before? [[slnc 400]] In Spring '
            "Cloud's discovery client. [[slnc 300]] In Netflix Eureka. "
            "[[slnc 300]] And in Consul itself. [[slnc 500]] Kubernetes' "
            'built-in D N S is the given form. [[slnc 300]] The platform '
            'hands your code an address, and your code never asks.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real Consul', 'agent, real HTTP servers, a real', 'nginx in a real container.', '', 'The demo instances listen only for', 'the length of the run.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] For once, '
            'nothing is simulated. [[slnc 300]] A real Consul service, '
            'real web servers, and a real nginx, in a real container. '
            '[[slnc 300]] The demo services only run for the length of '
            'the demo.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a fixed set of services with', 'fixed addresses, configuration is', 'simpler, and needs no registry.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a fixed set of '
            'services, at fixed addresses, simple configuration is '
            'easier. [[slnc 300]] And it needs no registry at all.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Give the caching locator a', 'time to live, and see what you decided.'],
        narration=(
            "That's the Service Locator, with Consul. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] '
            'Finding services is a fair use of a locator, but being given '
            'an address is better still. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Give the caching locator an expiry '
            'time. [[slnc 300]] And notice the decision you just had to '
            'make. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
