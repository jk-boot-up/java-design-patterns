"""Scene definitions for the Service Mesh with Envoy teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Mesh with Envoy',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Service Mesh '
            'pattern with Envoy, in Java, and it is written and presented '
            'by Jayasekhar Konduru. [[slnc 300]] It is the framework '
            'version of the Service Mesh video. That one showed three '
            'services with three different retry behaviours, then one '
            'mesh policy giving them all the same. It changed the policy '
            'in one place, turned an unknown caller away, and kept counts '
            'in the proxies. This one shows the same idea inside Envoy. '
            '[[slnc 350]] The plain definition, in short: with Envoy, the '
            'proxy in front of a service applies the retry, identity and '
            'counting policy from its configuration, and the service has '
            'none of that code. [[slnc 300]] By the end you will see '
            'three callers with three retry behaviours, see one real '
            'proxy retry for a caller that has no retry code, see the '
            'policy changed in one file, see an unknown caller refused '
            "before the payment service, see the proxy's own counters, "
            'and see the bill.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Service Mesh, the hand-built', 'video, shows one policy applied to', 'every call.', '', 'It shows retries, identity and', 'counts kept by proxies.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'This video assumes the Service Mesh video. If you have not '
            'seen it, start there. It shows one policy applied to every '
            'call, with retries, identity and counts kept by proxies '
            'instead of by services. [[slnc 300]] This one uses the same '
            'example. It does not teach the pattern again. It shows what '
            'Envoy does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: Envoy, and', 'Docker to run it.', '', 'You need Docker running. Without', 'it the demo says so and stops.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before the first line of code, what Envoy is. Envoy is a '
            'proxy. It sits in front of a service, and passes each call '
            'on. It can retry a call, refuse a caller, and count '
            'everything, and it is told how in a configuration file. Most '
            'service meshes are built on it. [[slnc 300]] And a promise: '
            'skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-own', kind='console', title='Each Service Carries Its Own',
        body="""ONE. Each carries its own.
  payments refuses 2 calls.
  retry code of 3, 0 and 1:
  checkout worked,
  refunds failed, reports failed.

  3 copies, 3 behaviours.""",
        narration=(
            'First, each service carries its own. The payment service '
            'refuses its first two calls, for each caller in turn. With '
            'retry code of three, none, and one tries: checkout worked, '
            'refunds failed, reports failed. Three services, three copies '
            'of the retry code, three different behaviours.'
        ),
    ),
    dict(
        key='05-proxy', kind='console', title='A Proxy Beside The Service',
        body="""TWO. A proxy beside it.
  Envoy retries 5xx, up to 3.
  the checkout has no retry code.
  the call worked.
  payments received 3 calls;
  Envoy counts 2 retries.""",
        narration=(
            'Second, a proxy beside the service. Envoy is told to retry '
            'server errors up to three times. The checkout has no retry '
            'code, and the call worked. The payment service received '
            'three calls, and Envoy counts two retries.'
        ),
    ),
    dict(
        key='06-policy', kind='console', title='Change The Policy Once',
        body="""THREE. One policy.
  one setting in Envoy's
  configuration: 3 retries to 0.
  the same call failed.

  services redeployed: 0.""",
        narration=(
            "Third, change the policy once. One setting in Envoy's "
            'configuration is changed, from three retries to none. The '
            'same call fails. Services changed or redeployed: none.'
        ),
    ),
    dict(
        key='07-who', kind='console', title='Who Is Calling',
        body="""FOUR. Who is calling.
  checkout: status 200.
  gift-cards: status 403.

  payments received 1 call.
  the proxy turned the other away.

  here the name is a header; a
  real mesh checks a certificate.""",
        narration=(
            'Fourth, who is calling. Only checkout and refunds are '
            'allowed. Checkout gets a 200. Gift cards gets a 403. The '
            'payment service received one call: the proxy turned the '
            "other away before it got there. Here the caller's name is a "
            'header. A real mesh checks a certificate instead, which a '
            'service cannot forge.'
        ),
    ),
    dict(
        key='08-num', kind='console', title='Numbers For Free',
        body="""FIVE. Numbers for free.
  read from Envoy:
  requests to payments 3,
  retries 2,
  retries that ended in success 1.

  no service counted anything.""",
        narration=(
            'Fifth, numbers for free. Read from Envoy, and not from any '
            'service: requests to payments, three; retries, two; retries '
            'that ended in success, one. No service counted anything. The '
            'proxy did.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  one call: payments received 3.
  retries multiply the load.

  every call crosses a proxy: a
  second process, a second hop.

  the policy is about 45 lines
  of configuration to keep right.""",
        narration=(
            'Last, the bill. One call, with two refusals: the payment '
            'service received three calls. Retrying multiplies the load '
            'on a service that is already struggling. Every call now '
            'crosses a proxy, which is a second process and a second '
            'network hop. And the policy is in a configuration file of '
            'about forty five lines, that someone must read, and keep '
            'right.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Policy in the proxy, set in one', 'place.', '', 'Keep retries small.', '', 'Identity by certificate, not by', 'name.', '', 'Review the configuration.'],
        narration=(
            'My verdict, plainly. Put retries, identity and counting in '
            'the proxy, and set them in one place. Keep retries small, '
            'since they multiply load. Check identity with certificates, '
            'not names. And keep the configuration under review, because '
            'it now decides how every call behaves.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['`retry_policy` and `num_retries`', 'in Envoy configuration.', '', 'A `/stats` page with', '`upstream_rq_retry` counters.', '', 'An RBAC filter with principals.'],
        narration=(
            'How do you recognise this in code you did not write? '
            'retry_policy and num_retries in Envoy configuration. A '
            '/stats page with upstream_rq_retry counters. An RBAC filter '
            'with principals.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Istio, Consul Connect, AWS App', 'Mesh, and many gateways and load', 'balancers.'],
        narration=(
            'You have met this in istio, consul connect, aws app mesh, '
            'and many gateways and load balancers.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Envoy one point thirty seven.', '', 'Docker 24 or later.'],
        narration=(
            'For the record. Envoy, one point thirty seven. Docker, 24 or '
            'later.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real Envoy', 'in a container, a real HTTP', 'server, and real retries.', '', 'One thing is a stand-in: the', "caller's name is a header, not a", 'certificate.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: a real Envoy in a container, a real HTTP '
            'server, and real retries. One thing is a stand in: the '
            "caller's name is a header, and not a certificate."
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a few services, a shared', 'library is simpler. A proxy for', 'each service is more processes to', 'run and understand.'],
        narration=(
            'So when is it too much? For a few services, a shared library '
            'is simpler. A proxy for each service is more processes to '
            'run and understand.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Allow only checkout, and see refunds turned away..'],
        narration=(
            "That's Service Mesh with Envoy. [[slnc 250]] If you take one "
            'sentence away, take this one: a real proxy can retry, refuse '
            'and count for a service, and the price is multiplied load '
            'and a configuration that decides everything. [[slnc 350]] '
            'The full source, the written notes, the diagrams and an '
            'animated walkthrough are all in the repository. [[slnc 300]] '
            'If you try one exercise, allow only checkout, and see '
            'refunds turned away. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
