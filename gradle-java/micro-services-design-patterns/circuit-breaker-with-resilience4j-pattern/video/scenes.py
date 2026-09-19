"""Scene definitions for the Circuit Breaker with Resilience4j teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Circuit Breaker with Resilience4j',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Circuit Breaker '
            'pattern with Resilience4j, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Circuit Breaker video. That one '
            'built a breaker with three states by hand, so a product page '
            'stopped waiting on a recommendations service that had gone '
            'quiet, and failed instantly instead. This one shows the same '
            'idea inside Resilience4j. [[slnc 350]] The plain definition, '
            'in short: in Resilience4j, a circuit breaker is an '
            'annotation on a method, and its thresholds are '
            'configuration. [[slnc 300]] By the end you will see the same '
            'breaker as an annotation and a few settings, then see how it '
            'can be bypassed, how it hides failures, and how a wrong '
            'setting trips it for the wrong reason.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Circuit Breaker, the hand-built video,', 'counts failures, opens, and lets one', 'probe through later.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Circuit Breaker video. If you have '
            'not seen it, start there. It counts failures, opens the '
            'breaker when there are too many, fails instantly while open, '
            'and lets one probe through later to see whether the service '
            'has recovered. [[slnc 300]] This one uses the same example. '
            'It does not teach the pattern again. It shows what '
            'Resilience4j does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Resilience4j.', '', 'It contains the breaker, with its', 'three states.', '', 'It runs inside Spring Boot,', 'through an annotation.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Resilience4j is. '
            'Resilience4j is a library of resilience patterns for Java. '
            'It contains a circuit breaker with three states, and a '
            'Spring Boot module that turns it into an annotation. [[slnc '
            '300]] And a promise: skipping this video loses none of the '
            'pattern. The hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-healthy', kind='console', title='Healthy',
        body="""ONE. Healthy.
  page shows two products.
  breaker: CLOSED.
  backend calls: 1.""",
        narration=(
            'First, the good day. The product page asks for '
            'recommendations, and gets two products. The breaker is '
            'closed, which means calls flow. One call reached the '
            'service.'
        ),
    ),
    dict(
        key='05-down', kind='console', title='The Service Goes Down',
        body="""TWO. Goes down.
  call 1: page shows nothing.
  call 2: same.
  call 3: OPEN.
  call 4: not sent to the
  service.""",
        narration=(
            'Second, the service goes down. The window holds the last '
            'four calls, and the healthy one from act one is still in it. '
            'Each failure shows an empty list on the page, not an error. '
            'At the third failure, three of the last four have failed, '
            'and the breaker opens. [[slnc 300]] The fourth call never '
            'reaches the service.'
        ),
    ),
    dict(
        key='06-open', kind='console', title='Open: Fail Fast',
        body="""THREE. Open.
  100 more page views.
  backend calls: 0 more.
  refused by the breaker: 100.

  the page never saw an error.""",
        narration=(
            'Third, the payoff. A hundred more page views, and not one '
            'reaches the service. The breaker refuses every one, '
            'instantly, and the fallback answers with an empty list. The '
            'struggling service gets a rest. [[slnc 300]] But notice: the '
            "page never saw an error. The only alarm is the breaker's "
            'state.'
        ),
    ),
    dict(
        key='07-probe', kind='console', title='Half-Open: One Probe',
        body="""FOUR. One probe.
  still down: 1 probe reached
  it. breaker: OPEN.

  service back: the probe
  works. breaker: CLOSED.""",
        narration=(
            'Fourth, the probe. The demo moves the breaker to half-open, '
            'which in production a wait duration does by itself. One call '
            'is let through. The service is still down, so it fails, and '
            'the breaker opens again. Then the service comes back. The '
            'next probe works, and the breaker closes.'
        ),
    ),
    dict(
        key='08-count', kind='console', title='What Counts As A Failure',
        body="""FIVE. What counts.
  8 requests for a product
  that does not exist.

  ignoring them: CLOSED.
  counting them: OPEN.""",
        narration=(
            'Fifth, what counts as a failure. Eight requests for a '
            "product that does not exist. That is the caller's mistake, "
            "not the service's. The breaker with an ignore list stays "
            'closed. The breaker that counts everything opens, and blocks '
            'good requests. [[slnc 300]] The ignore list is one line in '
            'the settings, and easy to forget.'
        ),
    ),
    dict(
        key='09-proxy', kind='console', title='The Annotation Is A Proxy',
        body="""SIX. A proxy.
  10 calls through this.
  errors that reached the
  caller: 10.
  backend calls: 10.

  breaker: CLOSED. it saw
  nothing.""",
        narration=(
            'Last, the annotation is a proxy. A method inside the client '
            'calls its own protected method, on this. That call skips the '
            'proxy, and so the breaker and the fallback. All ten errors '
            'reach the caller. All ten calls hit the struggling service. '
            'The breaker stays closed. [[slnc 300]] The same rule as '
            'every Spring proxy: call it from outside.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Configure the window on purpose.', '', 'List exceptions that are not failures.', '', 'Alert on the state, not the errors.', '', 'Call from outside the bean.'],
        narration=(
            'My verdict, plainly. Configure the window and the threshold '
            'on purpose. List the exceptions that are not failures. Alert '
            "on the breaker's state, because the fallback hides the "
            'errors. And call protected methods from outside the bean.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@CircuitBreaker with a name and a', 'fallback method.', '', 'resilience4j.circuitbreaker in', 'configuration.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'circuit breaker annotation with a name and a fallback '
            'method. And settings under resilience four j circuit breaker '
            'in the configuration.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Any Spring service that calls', 'another service over the network', 'and must keep serving.'],
        narration=(
            'You have met this in any Spring service that calls another '
            'service over the network, and must keep serving when it '
            'fails.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Resilience4j 2.4.0.', '', 'No web server, no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. '
            'Resilience four j two point four point zero. No web server, '
            'and no web starter.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the real breaker', 'and the real annotation.', '', 'The clock is not used: the probe', 'is started by the demo, not a timer.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: the real breaker and the real '
            'annotation. The clock is not used. The demo starts the probe '
            'itself, so the numbers are the same every run.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a local, fast, reliable call,', 'a breaker is only more code.'],
        narration=(
            'So when is it too much? For a call that is local, fast and '
            'reliable, a breaker is only more code.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Remove the ignore list and', 'rerun act five.'],
        narration=(
            "That's Circuit Breaker with Resilience4j. [[slnc 250]] If "
            'you take one sentence away, take this one: Resilience4j '
            'gives you the breaker as configuration, and the state is '
            'your only alarm. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository. [[slnc 300]] If you try one exercise, remove '
            'the ignore list, and rerun act five. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
