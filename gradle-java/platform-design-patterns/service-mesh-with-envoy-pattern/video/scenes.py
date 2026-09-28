"""Scene definitions for the Service Mesh with Envoy teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Mesh with Envoy',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Service Mesh pattern in Java, using a real proxy called '
            'Envoy. [[slnc 300]] This video is presented by Jayasekhar '
            'Konduru. [[slnc 600]] First, a simple definition. [[slnc '
            '300]] A service mesh puts a proxy beside every service. '
            '[[slnc 300]] The proxy handles retries, checks who is '
            'calling, and counts calls. [[slnc 300]] So the service '
            'itself needs none of that code. [[slnc 600]] With Envoy, all '
            "of this is described in the proxy's settings file. [[slnc "
            '700]] In our online store, three services call the payment '
            'service. [[slnc 500]] By the end, you will hear three '
            'callers behave three different ways. [[slnc 300]] One real '
            'proxy retry for a caller with no retry code. [[slnc 300]] '
            'The policy changed in one file. [[slnc 300]] An unknown '
            "caller refused. [[slnc 300]] The proxy's own counts. [[slnc "
            '300]] And the bill.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Service Mesh, the hand-built', 'video, shows one policy applied to', 'every call.', '', 'It shows retries, identity and', 'counts kept by proxies.', '', 'If you have not seen it, start', 'there.'],
        narration=(
            'This video builds on the plain Java Service Mesh video. '
            '[[slnc 300]] If you have not seen it, start there. [[slnc '
            '500]] That video shows one policy applied to every call. '
            '[[slnc 300]] With retries, caller checks, and counts kept by '
            'proxies, not by services. [[slnc 500]] This video uses the '
            'same example. [[slnc 300]] It does not teach the pattern '
            'again. [[slnc 300]] It shows what Envoy does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Two things are new: Envoy, and', 'Docker to run it.', '', 'You need Docker running. Without', 'it the demo says so and stops.', '', 'Skipping this video loses none of', 'the pattern.'],
        narration=(
            'Before any code, what is Envoy? [[slnc 400]] Envoy is a '
            'proxy. [[slnc 300]] It sits in front of a service, and '
            'passes each call on. [[slnc 300]] It can retry a call, '
            'refuse a caller, and count everything. [[slnc 300]] And it '
            'is told how, in a settings file. [[slnc 300]] Most service '
            'meshes are built on it. [[slnc 500]] You need Docker running '
            'to try it. [[slnc 300]] Without Docker, the demo says so, '
            'and stops. [[slnc 500]] And a promise. [[slnc 300]] Skipping '
            'this video loses none of the pattern. [[slnc 300]] The plain '
            'Java video teaches all of it.'
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
            'First demo: each service carries its own retry code. [[slnc '
            '400]] The payment service refuses its first two calls from '
            'each caller. [[slnc 500]] Checkout tries three times, and '
            'succeeds. [[slnc 300]] Refunds never retries, and fails. '
            '[[slnc 300]] Reports tries once more, and fails. [[slnc '
            '500]] Three services, three copies of the retry code, and '
            'three different behaviours.'
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
            'Second demo: a proxy beside the service. [[slnc 400]] Envoy '
            'is told to retry server errors, up to three times. [[slnc '
            '500]] Checkout has no retry code. [[slnc 300]] And the call '
            'works. [[slnc 500]] The payment service received three '
            'calls. [[slnc 300]] And Envoy counted two retries.'
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
            'Third demo: change the policy once. [[slnc 400]] One setting '
            "in Envoy's file is changed, from three retries to none. "
            '[[slnc 300]] And the same call fails. [[slnc 500]] No '
            'service was changed, or released again.'
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
            'Fourth demo: who is calling? [[slnc 400]] Only checkout and '
            "refunds are allowed. [[slnc 500]] Checkout's call succeeds. "
            "[[slnc 300]] A gift card service's call is refused as "
            'forbidden. [[slnc 500]] The payment service only received '
            'one call. [[slnc 300]] The proxy turned the other away '
            "before it got there. [[slnc 600]] Here, the caller's name is "
            'just sent as a label on the request. [[slnc 300]] A real '
            'mesh checks a security certificate instead, which a service '
            'cannot fake.'
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
            'Fifth demo: numbers for free. [[slnc 400]] These come from '
            'Envoy, not from any service. [[slnc 500]] Requests to '
            'payment: three. [[slnc 300]] Retries: two. [[slnc 300]] '
            'Retries that ended in success: one. [[slnc 500]] No service '
            'counted anything. [[slnc 300]] The proxy did.'
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
            'Finally, the bill. [[slnc 400]] One call, with two refusals, '
            'means the payment service received three calls. [[slnc 300]] '
            'Retrying multiplies the load on a service that is already '
            'struggling. [[slnc 600]] Every call now passes through a '
            'proxy. [[slnc 300]] That is a second process, and a second '
            'network hop. [[slnc 600]] And the policy lives in a settings '
            'file, about forty-five lines long. [[slnc 300]] Someone must '
            'read it, and keep it right.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Policy in the proxy, set in one', 'place.', '', 'Keep retries small.', '', 'Identity by certificate, not by', 'name.', '', 'Review the configuration.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Put retries, caller '
            'checks, and counting in the proxy, and set them in one '
            'place. [[slnc 300]] Keep retries small, because they '
            'multiply load. [[slnc 300]] Check callers with certificates, '
            'not names. [[slnc 500]] And keep the settings file under '
            'review. [[slnc 300]] Because it now decides how every call '
            'behaves.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['`retry_policy` and `num_retries`', 'in Envoy configuration.', '', 'A `/stats` page with', '`upstream_rq_retry` counters.', '', 'An RBAC filter with principals.'],
        narration=(
            'How can you spot this in a system someone else built? [[slnc '
            "400]] Look for a retry policy in Envoy's settings file. "
            '[[slnc 300]] Look for a statistics page with retry counters. '
            '[[slnc 300]] Or look for access rules that list which '
            'callers are allowed.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Istio, Consul Connect, AWS App', 'Mesh, and many gateways and load', 'balancers.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In Istio, '
            "Consul Connect, Amazon's App Mesh, and in many gateways and "
            'load balancers.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Envoy one point thirty seven.', '', 'Docker 24 or later.'],
        narration=(
            'For the record, here is what was used. [[slnc 300]] Envoy, '
            'version one point thirty-seven. [[slnc 300]] And Docker, '
            'version twenty-four or later.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real Envoy', 'in a container, a real HTTP', 'server, and real retries.', '', 'One thing is a stand-in: the', "caller's name is a header, not a", 'certificate.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is real: a real Envoy in a container, a real web '
            'server, and real retries. [[slnc 500]] One thing is a '
            "stand-in. [[slnc 300]] The caller's name is a label on the "
            'request, not a certificate.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a few services, a shared', 'library is simpler. A proxy for', 'each service is more processes to', 'run and understand.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a few services, '
            'a shared library is simpler. [[slnc 400]] A proxy for every '
            'service means more processes to run, and to understand.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Allow only checkout, and see refunds turned away..'],
        narration=(
            "That's Service Mesh, with Envoy. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A real '
            'proxy can retry, refuse, and count for a service, and the '
            'price is extra load, and a settings file that decides '
            'everything. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Allow only checkout to call payment. [[slnc 300]] Then '
            'see refunds turned away. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
