"""Scene definitions for the Circuit Breaker with Resilience4j teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Circuit Breaker with Resilience4j',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Circuit Breaker pattern in Java, using a library called '
            'Resilience four J. [[slnc 300]] This video is presented by '
            'Jayasekhar Konduru. [[slnc 600]] First, a simple definition. '
            '[[slnc 300]] A circuit breaker stops calling a service that '
            'keeps failing. [[slnc 300]] It fails instantly for a while. '
            '[[slnc 300]] Then it lets one test call through, to see '
            'whether the service has recovered. [[slnc 500]] Think of the '
            'fuse box in a house. [[slnc 300]] It trips when there is a '
            'fault, stays off, and is switched back on once, to check. '
            '[[slnc 600]] In Resilience four J, the breaker is an '
            'annotation on a method, and its limits are settings. [[slnc '
            '700]] In our online store, a product page shows '
            'recommendations from a separate service. [[slnc 500]] By the '
            'end, you will hear the same breaker built from one '
            'annotation and a few settings. [[slnc 300]] Then how it can '
            'be skipped by accident. [[slnc 300]] How it hides failures. '
            '[[slnc 300]] And how a wrong setting trips it for the wrong '
            'reason.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Circuit Breaker, the hand-built video,', 'counts failures, opens, and lets one', 'probe through later.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video builds on the plain Java Circuit Breaker video. '
            '[[slnc 300]] If you have not seen it, start there. [[slnc '
            '500]] That video counts failures, and opens the breaker when '
            'there are too many. [[slnc 300]] While open, it fails '
            'instantly. [[slnc 300]] Later, it lets one test call '
            'through, to see whether the service has recovered. [[slnc '
            '500]] This video uses the same example. [[slnc 300]] It does '
            'not teach the pattern again. [[slnc 300]] It shows what '
            'Resilience four J does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Resilience4j.', '', 'It contains the breaker, with its', 'three states.', '', 'It runs inside Spring Boot,', 'through an annotation.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before any code, what is Resilience four J? [[slnc 400]] It '
            'is a library of resilience patterns for Java. [[slnc 300]] '
            'It includes a circuit breaker with three states. [[slnc '
            '300]] Closed, which means calls go through. [[slnc 300]] '
            'Open, which means calls are refused. [[slnc 300]] And '
            'half-open, which lets one test call through. [[slnc 500]] It '
            'also has a Spring Boot module that turns the breaker into an '
            'annotation. [[slnc 500]] And a promise. [[slnc 300]] '
            'Skipping this video loses none of the pattern. [[slnc 300]] '
            'The plain Java video teaches all of it.'
        ),
    ),
    dict(
        key='04-healthy', kind='console', title='Healthy',
        body="""ONE. Healthy.
  page shows two products.
  breaker: CLOSED.
  backend calls: 1.""",
        narration=(
            'First demo: a good day. [[slnc 400]] The product page asks '
            'for recommendations, and gets two products. [[slnc 300]] The '
            'breaker is closed, which means calls go through. [[slnc '
            '300]] One call reached the service.'
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
            'Second demo: the service goes down. [[slnc 400]] The breaker '
            'looks at the last four calls. [[slnc 300]] And the healthy '
            'call from the first demo is still one of them. [[slnc 500]] '
            'Each failure shows an empty list on the page, not an error. '
            '[[slnc 300]] At the third failure, three of the last four '
            'calls have failed. [[slnc 300]] So the breaker opens. [[slnc '
            '500]] The fourth call never reaches the service.'
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
            'Third demo: the payoff. [[slnc 400]] A hundred more page '
            'views. [[slnc 300]] And not one of them reaches the service. '
            '[[slnc 500]] The breaker refuses every call, instantly. '
            '[[slnc 300]] A fallback method, which is a backup answer, '
            'returns an empty list. [[slnc 300]] And the struggling '
            'service gets a rest. [[slnc 600]] But notice this. [[slnc '
            '300]] The page never saw an error. [[slnc 300]] So the only '
            "warning sign is the breaker's state."
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
            'Fourth demo: the test call. [[slnc 400]] The demo moves the '
            'breaker to half-open. [[slnc 300]] In a real system, a '
            'waiting time does that by itself. [[slnc 500]] One call is '
            'let through. [[slnc 300]] The service is still down, so it '
            'fails. [[slnc 300]] And the breaker opens again. [[slnc '
            '500]] Then the service comes back. [[slnc 300]] The next '
            'test call works. [[slnc 300]] And the breaker closes.'
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
            'Fifth demo: what counts as a failure? [[slnc 400]] Eight '
            'requests arrive, for a product that does not exist. [[slnc '
            "300]] That is the caller's mistake, not the service's. "
            '[[slnc 500]] One breaker has a list of errors to ignore, and '
            'it stays closed. [[slnc 300]] Another breaker counts every '
            'error. [[slnc 300]] It opens, and starts blocking good '
            'requests too. [[slnc 500]] That ignore list is one line in '
            'the settings. [[slnc 300]] And it is easy to forget.'
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
            'Last demo: a trap. [[slnc 400]] Spring adds the breaker by '
            'wrapping the object in a proxy. [[slnc 300]] A proxy is a '
            'stand-in that sits in front of the real object, and checks '
            'each call on the way in. [[slnc 500]] Here, a method inside '
            'the client calls its own protected method directly. [[slnc '
            '300]] That call never goes through the proxy. [[slnc 300]] '
            'So it skips both the breaker and the fallback. [[slnc 500]] '
            'All ten errors reach the caller. [[slnc 300]] All ten calls '
            'hit the struggling service. [[slnc 300]] And the breaker '
            'stays closed, because it saw nothing. [[slnc 500]] The rule '
            'is the same for every Spring proxy. [[slnc 300]] Call the '
            'protected method from outside the object.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Configure the window on purpose.', '', 'List exceptions that are not failures.', '', 'Alert on the state, not the errors.', '', 'Call from outside the bean.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Choose how many calls '
            'the breaker looks at, and its failure limit, on purpose. '
            '[[slnc 300]] List the errors that are not real failures. '
            "[[slnc 300]] Alert on the breaker's state, because the "
            'fallback hides the errors. [[slnc 300]] And call protected '
            'methods from outside the object.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@CircuitBreaker with a name and a', 'fallback method.', '', 'resilience4j.circuitbreaker in', 'configuration.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a circuit breaker annotation, with a name and '
            'a fallback method. [[slnc 300]] And look for circuit breaker '
            'settings in the configuration file.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Any Spring service that calls', 'another service over the network', 'and must keep serving.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In any Spring '
            'service that calls another service over the network. [[slnc '
            '300]] And must keep serving when that service fails.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'Resilience4j 2.4.0.', '', 'No web server, no web starter.'],
        narration=(
            'For the record, here is what was used. [[slnc 300]] Spring '
            'Boot, version four point one point one. [[slnc 300]] '
            'Resilience four J, version two point four point zero. [[slnc '
            '300]] There is no web server, and no web starter.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the real breaker', 'and the real annotation.', '', 'The clock is not used: the probe', 'is started by the demo, not a timer.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is real: the real breaker, and the real '
            'annotation. [[slnc 300]] The clock is not used. [[slnc 300]] '
            'The demo starts the test call itself, so the numbers are the '
            'same on every run.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a local, fast, reliable call,', 'a breaker is only more code.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a call that is '
            'local, fast, and reliable, a breaker is only more code.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Remove the ignore list and', 'rerun act five.'],
        narration=(
            "That's Circuit Breaker, with Resilience four J. [[slnc 400]] "
            'If you remember one sentence, make it this one. [[slnc 300]] '
            'Resilience four J gives you the breaker as settings, and its '
            'state is your only warning sign. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Remove the ignore list, '
            'and run the fifth demo again. [[slnc 300]] Guess first '
            'whether the breaker will open. [[slnc 500]] If this helped, '
            'a like really does help other people find it. [[slnc 300]] '
            "And subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
