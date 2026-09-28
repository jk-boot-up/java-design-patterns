"""Scene definitions for the Service Mesh teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Mesh',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Service Mesh pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A service mesh puts a '
            'helper, called a proxy, beside every service. [[slnc 300]] '
            'The proxies handle retries, checking who is calling, and '
            'counting calls. [[slnc 300]] All under one policy, set in '
            'one place. [[slnc 600]] Think of an office where every '
            "department's post goes through one post room. [[slnc 300]] "
            'The post room applies the same rules to everyone, so no '
            'department has to. [[slnc 700]] In our online store, every '
            'service calls the payment service. [[slnc 300]] And each '
            'team wrote its own retry code, in its own way. [[slnc 500]] '
            'By the end, you will hear three services behave three '
            'different ways. [[slnc 300]] One policy give them all the '
            'same behaviour. [[slnc 300]] The policy changed once, for '
            'everyone. [[slnc 300]] An unknown caller turned away. [[slnc '
            '300]] Counts kept with no service code. [[slnc 300]] And the '
            'bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Checkout, refunds and reports', 'all call the payment service.', '', 'It is having a bad day:', 'it refuses its first 2 calls.', '', 'Each team wrote its own retry', 'code.', '', 'Who should retry?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Checkout, refunds, and '
            'reports all call the payment service. [[slnc 500]] Payment '
            'is having a bad day. [[slnc 300]] It refuses its first two '
            'calls. [[slnc 500]] Each team wrote its own retry code. '
            '[[slnc 500]] So here is the question. [[slnc 300]] Who '
            'should retry?'
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
            'First demo: each service carries its own retry code. [[slnc '
            '400]] Payment refuses its first two calls. [[slnc 500]] '
            'Checkout retries three times, and succeeds. [[slnc 300]] '
            'Refunds never retries, and fails. [[slnc 300]] Reports '
            'retries once, and fails. [[slnc 500]] Three services. [[slnc '
            '300]] Three copies of the retry code. [[slnc 300]] Three '
            'different behaviours.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A proxy beside every service.', '', 'The proxies do the retrying,', 'the identity check, and the', 'counting.', '', 'One policy, set in one place,', 'applies to every call.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Put a proxy beside every '
            'service. [[slnc 300]] Every call in and out goes through it. '
            '[[slnc 500]] The proxies do the retrying, the check on who '
            'is calling, and the counting. [[slnc 500]] One policy, set '
            'in one place, applies to every call.'
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
            'Second demo: a proxy beside each service. [[slnc 400]] The '
            'same bad day. [[slnc 300]] And the same policy for everyone. '
            '[[slnc 500]] The call works. [[slnc 300]] The proxy made '
            'three attempts. [[slnc 300]] And checkout has no retry code '
            'at all.'
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
            'Third demo: change the policy once. [[slnc 400]] With three '
            'retries, the call works. [[slnc 500]] One setting changed to '
            "zero retries, and it fails. [[slnc 500]] Every service's "
            'calls changed together. [[slnc 300]] And no service had to '
            'be released again.'
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
            'Fourth demo: who is calling? [[slnc 400]] Checkout calls '
            'payment, and it works. [[slnc 300]] An unknown service calls '
            'payment, and is refused. [[slnc 500]] The payment service '
            'only received one call. [[slnc 300]] The proxy turned the '
            'other caller away, before it ever got there.'
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
            'Fifth demo: numbers for free. [[slnc 400]] Checkout to '
            'payment: two calls, none failed, four attempts. [[slnc 300]] '
            'Refunds to payment: one call, none failed, one attempt. '
            '[[slnc 500]] No service counted anything. [[slnc 300]] The '
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
            'Finally, the bill. [[slnc 400]] One call, with two refusals, '
            'means the payment service received three calls. [[slnc 300]] '
            'Retrying multiplies the load on a service that is already '
            'struggling. [[slnc 600]] Going through the proxies is also '
            'slower. [[slnc 300]] One attempt takes three ticks of time '
            'through the proxies, and one tick directly. [[slnc 300]] '
            'This call took nine ticks. [[slnc 600]] And three services '
            'means three more processes to run, update, and understand.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Istio, Linkerd, Consul Connect or', 'Cilium.', '', 'Envoy proxies injected beside each', 'pod.', '', 'Policies written as YAML: retries,', 'timeouts, allowed callers.'],
        narration=(
            'How can you spot this in a system someone else built? [[slnc '
            '400]] Look for tools like Istio, Linkerd, Consul Connect, or '
            'Cilium. [[slnc 300]] Look for Envoy proxies added beside '
            'each running service. [[slnc 300]] Look for policies written '
            'in settings files: retries, timeouts, and allowed callers. '
            '[[slnc 300]] Or dashboards of calls between services, with '
            'no counting code in the services themselves.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a mesh when many services need', 'the same behaviour, and you want', 'it set in one place, not written', 'many times. Keep retries small,', 'since they multiply load. Accept', 'the extra hop and the extra', 'processes. Do not use one for a', 'handful of services that a library', 'can serve.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a mesh when many '
            'services need the same behaviour. [[slnc 300]] And you want '
            'it set in one place, not written many times. [[slnc 500]] '
            'Keep retries small, because they multiply load. [[slnc 300]] '
            'And accept the extra delay, and the extra processes. [[slnc '
            '500]] Do not use a mesh for a handful of services that a '
            'shared library can serve.'
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
        body=['For a few services, a shared', 'library, or none, is simpler. A', 'mesh is a system in itself, and', 'needs people who understand it.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a few services, '
            'a shared library, or nothing at all, is simpler. [[slnc '
            '400]] A mesh is a whole system in itself. [[slnc 300]] And '
            'it needs people who understand it.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Service Mesh pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'service mesh moves retries, caller checks, and counting out '
            'of every service and into proxies, and the price is extra '
            'delay, extra load, and extra processes. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 300]] It runs '
            'offline, with nothing installed except a Java development '
            'kit. [[slnc 500]] Here is one exercise to try. [[slnc 300]] '
            'Allow only checkout to call payment. [[slnc 300]] Then see '
            'refunds turned away. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
