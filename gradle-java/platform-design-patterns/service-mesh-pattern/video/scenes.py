"""Scene definitions for the Service Mesh teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Mesh',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Service Mesh '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'service mesh puts a proxy beside every service. The proxies '
            'handle retries, identity and measurement for all the calls, '
            'under one policy that is set in one place. [[slnc 350]] This '
            'is another project in the platform category, whose subject '
            'is how software is shipped, run and operated. In our online '
            'store, every service calls the payment service, and each '
            'team has written its own retry code, in its own way. [[slnc '
            '300]] By the end you will see three services with three '
            'different retry behaviours, see one policy give everyone the '
            'same behaviour, see the policy changed once, see an unknown '
            'caller turned away before the payment service, see counts '
            'kept with no service code, and see the bill, which is load, '
            'delay and more processes.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Checkout, refunds and reports', 'all call the payment service.', '', 'It is having a bad day:', 'it refuses its first 2 calls.', '', 'Each team wrote its own retry', 'code.', '', 'Who should retry?'],
        narration=(
            'Here is the scenario. The checkout, refunds and reports '
            'services all call the payment service. It is having a bad '
            'day, and refuses its first two calls. Each team wrote its '
            'own retry code. [[slnc 300]] The question: who should retry?'
        ),
    ),
    dict(
        key='03-lib', kind='console', title='Each Service Carries Its Own',
        body="""ONE. Each carries its own.
  payments refuses 2 calls.
  checkout retries 3: works.
  refunds never retries: fails.
  reports retries once: fails.

  3 copies, 3 behaviours.""",
        narration=(
            'First, each service carries its own. The payment service '
            'refuses its first two calls. Checkout retries three times, '
            'and succeeds. Refunds never retries, and fails. Reports '
            'retries once, and fails. Three services, three copies of the '
            'retry code, three different behaviours.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A proxy beside every service.', '', 'The proxies do the retrying,', 'the identity check, and the', 'counting.', '', 'One policy, set in one place,', 'applies to every call.'],
        narration=(
            'The pattern. A proxy beside every service. The proxies do '
            'the retrying, the identity check, and the counting. One '
            'policy, set in one place, applies to every call.'
        ),
    ),
    dict(
        key='05-proxy', kind='console', title='A Proxy Beside Each Service',
        body="""TWO. A proxy beside each.
  the same bad day, the same
  policy for everyone.
  the call worked: 3 attempts
  by the proxy.

  checkout has no retry code.""",
        narration=(
            'Second, a proxy beside each service. The same bad day, and '
            'the same policy for everyone. The call worked. The proxy '
            'made three attempts, and the checkout service has no retry '
            'code at all.'
        ),
    ),
    dict(
        key='06-policy', kind='console', title='Change The Policy Once',
        body="""THREE. One policy.
  retries 3: works.
  one setting to 0: fails.

  every service's calls changed.
  services redeployed: 0.""",
        narration=(
            'Third, change the policy once. With three retries, the call '
            'works. One setting changed to zero, and it fails. Every '
            "service's calls changed. Services redeployed: none."
        ),
    ),
    dict(
        key='07-who', kind='console', title='Who Is Calling',
        body="""FOUR. Who is calling.
  checkout: allowed.
  an unknown service: refused.

  payments received 1 call.
  the proxy turned the other
  away first.""",
        narration=(
            'Fourth, who is calling. Checkout calls payments, and it '
            'works. An unknown service calls payments, and is refused. '
            'The payment service received one call. The proxy turned the '
            'other away before it got there. Denied: one.'
        ),
    ),
    dict(
        key='08-num', kind='console', title='Numbers For Free',
        body="""FIVE. Numbers for free.
  checkout->payments:
  2 calls, 0 failed, 4 attempts.
  refunds->payments:
  1 call, 0 failed, 1 attempt.

  no service counted anything.""",
        narration=(
            'Fifth, numbers for free. Checkout to payments: two calls, '
            'none failed, four attempts. Refunds to payments: one call, '
            'none failed, one attempt. No service counted anything. The '
            'proxies did.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  one call: payments received 3.
  retrying multiplies load on a
  service that is struggling.

  one attempt: 3 ticks through
  proxies, 1 directly. this call:
  9 ticks.

  3 services: 3 more processes.""",
        narration=(
            'Last, the bill. One call, with two refusals: the payment '
            'service received three calls. Retrying multiplies the load '
            'on a service that is already struggling. One attempt takes '
            'three ticks through the proxies, and one directly. This call '
            'took nine ticks. And three services means three more '
            'processes to run, upgrade, and understand.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Istio, Linkerd, Consul Connect or', 'Cilium.', '', 'Envoy proxies injected beside each', 'pod.', '', 'Policies written as YAML: retries,', 'timeouts, allowed callers.'],
        narration=(
            'How do you recognise this in code you did not write? Istio, '
            'Linkerd, Consul Connect or Cilium. Envoy proxies injected '
            'beside each pod. Policies written as YAML: retries, '
            'timeouts, allowed callers. Dashboards of calls between '
            'services with no code in the services.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a mesh when many services need', 'the same behaviour, and you want', 'it set in one place, not written', 'many times. Keep retries small,', 'since they multiply load. Accept', 'the extra hop and the extra', 'processes. Do not use one for a', 'handful of services that a library', 'can serve.'],
        narration=(
            'Here is my verdict, plainly. Use a mesh when many services '
            'need the same behaviour, and you want it set in one place, '
            'not written many times. Keep retries small, since they '
            'multiply load. Accept the extra hop and the extra processes. '
            'Do not use one for a handful of services that a library can '
            'serve.'
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
        body=['For a few services, a shared', 'library, or none, is simpler. A', 'mesh is a system in itself, and', 'needs people who understand it.'],
        narration=(
            'So when is it too much? For a few services, a shared '
            'library, or none, is simpler. A mesh is a system in itself, '
            'and needs people who understand it.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Service Mesh. [[slnc 250]] If you take one sentence "
            'away, take this one: a service mesh moves retries, identity '
            'and counting out of every service into proxies, and the '
            'price is extra delay, extra load, and extra processes. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'allow only the checkout service to call payments, and see '
            'refunds turned away. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
