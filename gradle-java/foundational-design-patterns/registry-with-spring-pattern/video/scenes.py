"""Scene definitions for the Registry with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Registry with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Registry pattern, in Java, using Spring. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A registry is a '
            'well-known place where things are kept, and found by asking. '
            '[[slnc 600]] Think of a phone directory. [[slnc 300]] Anyone '
            'can look up a number, but everyone shares the same book. '
            '[[slnc 700]] This is the framework version of the Registry '
            'video. [[slnc 300]] That one built a registry by hand, and '
            "showed its costs. [[slnc 300]] Spring's application context "
            'is a registry too, but built far better. [[slnc 500]] By the '
            'end, you will know what Spring fixes. [[slnc 300]] When '
            'asking it for things is a mistake. [[slnc 300]] And the '
            "failure that is Spring's own: a cached context that "
            'remembers what earlier tests did.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Registry, the hand-built video,', 'built a static registry and showed', 'its costs: invisible dependencies,', 'order-dependent tests.', '', 'This video uses the same checkout.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Registry video. [[slnc 400]] That '
            'one builds a registry by hand, and shows its costs. [[slnc '
            '300]] Among them, invisible dependencies, and a test that '
            'fails depending on the order the tests run in. [[slnc 500]] '
            'Here, we use the same checkout. [[slnc 300]] We will not '
            'teach the pattern again. [[slnc 300]] Instead, we ask what '
            'Spring does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['One thing is new: Spring Boot.', '', 'Its core is a container, the', 'ApplicationContext, that creates', 'your objects and lets you find them.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'One thing is new in this project: Spring Boot. [[slnc 400]] '
            "Spring's core is a container, called the application "
            'context. [[slnc 300]] It creates your objects, and lets you '
            'find them by type. [[slnc 300]] That is a registry. [[slnc '
            '500]] And one promise. [[slnc 300]] If you skip this video, '
            'you lose none of the pattern. [[slnc 300]] This one is about '
            'the tool.'
        ),
    ),
    dict(
        key='04-is-registry', kind='console', title='The Context Is The Registry',
        body="""ONE. The registry.
  Registry.get(Gateway.class)
  is
  context.getBean(Gateway.class)

  registered by declaration:
  @Component on a class.

  a missing bean fails at
  start-up.""",
        narration=(
            'First demo: the application context is the registry. [[slnc '
            '400]] Registry dot get, from the hand-built video, becomes '
            'context dot get bean here. [[slnc 300]] And it finds the '
            'recording gateway. [[slnc 500]] But notice what changed. '
            '[[slnc 300]] Nothing is registered by calling a method, from '
            'somewhere. [[slnc 300]] Things are registered by declaring '
            'them, with an at Component annotation on a class. [[slnc '
            '500]] And a missing object makes Spring fail when it starts, '
            'not on the first call.'
        ),
    ),
    dict(
        key='05-well-badly', kind='console', title='Used Well, Or Badly',
        body="""TWO. Two checkouts.
  InjectedCheckout: given its
  collaborators.

  LocatorStyleCheckout: calls
  getBean three times.

  same result, but its
  constructor takes nothing.
  new: NullPointerException.""",
        narration=(
            'Second demo: using it well, or badly. [[slnc 400]] The first '
            'checkout is given its helpers, through its constructor. '
            '[[slnc 300]] It never asks the registry for anything. [[slnc '
            '300]] That is the best way to use a registry: never calling '
            'it. [[slnc 600]] The second checkout calls get bean, three '
            'times. [[slnc 300]] The result is the same. [[slnc 300]] But '
            'its constructor takes nothing, so its needs are invisible '
            'again. [[slnc 300]] And creating one with new throws a null '
            'pointer exception, because it needs Spring to give it the '
            'context. [[slnc 500]] That is the hand-built registry again, '
            'inside Spring. [[slnc 300]] A get bean call inside business '
            'code is really a service locator.'
        ),
    ),
    dict(
        key='06-cache', kind='console', title='The Failure Of Its Own',
        body="""THREE. The cache.
  test A charged the singleton
  gateway once: [9000]

  test B, same cached context:
  sees [9000]

  a fresh context sees: []
  at the price of starting
  Spring again.""",
        narration=(
            "Third demo: the failure that is Spring's own. [[slnc 400]] "
            "Spring's test support caches a context, and reuses it for "
            'tests with the same setup. [[slnc 300]] Starting Spring is '
            'slow, so this is sensible. [[slnc 500]] But the gateway is a '
            'singleton, so it remembers. [[slnc 300]] Test A charges it '
            'once, for ninety pounds. [[slnc 300]] Test B, on the same '
            'cached context, expects a clean gateway. [[slnc 300]] But it '
            'sees that ninety pound charge. [[slnc 500]] That is the '
            "hand-built registry's test order problem, now in Spring. "
            "[[slnc 300]] This project's tests prove it. [[slnc 300]] The "
            'fix is to throw that context away, which is correct, but '
            'costs starting a new one.'
        ),
    ),
    dict(
        key='07-strings', kind='console', title='A Registry Of Strings',
        body="""FOUR. The Environment.
  checkout.currency = GBP
  checkout.curency = null

  a typo: no error, no warning.

  a required @Value with the
  same typo fails at start-up:
  Could not resolve placeholder.""",
        narration=(
            'Fourth demo: a registry of text values. [[slnc 400]] Spring '
            'has a second registry: the environment, which holds settings '
            'as text. [[slnc 500]] Ask it for checkout currency, and you '
            'get pounds. [[slnc 300]] Ask with a typo, currency spelled '
            'with one r, and you get nothing. [[slnc 300]] No error, and '
            'no warning. [[slnc 500]] But a required setting injected '
            'with the same typo fails when Spring starts. [[slnc 300]] It '
            'says it could not resolve the placeholder. [[slnc 300]] The '
            'lookup is silent. [[slnc 300]] The injected one is not.'
        ),
    ),
    dict(
        key='08-ambiguous', kind='console', title='Two Of A Type',
        body="""FIVE. Ambiguity.
  two Notifiers registered.

  getBean(Notifier.class):
  NoUniqueBeanDefinition
  Exception

  a run-time error at the
  call site.""",
        narration=(
            'Fifth demo: two of the same type. [[slnc 400]] There are two '
            'notifiers registered. [[slnc 300]] Ask the registry for a '
            'notifier, by type. [[slnc 500]] It throws a No Unique Bean '
            'Definition exception, because it found two. [[slnc 300]] '
            'That is an error while running, at the point of the call. '
            '[[slnc 300]] Not a compile error. [[slnc 500]] Asking by '
            'type only works, until a second one arrives.'
        ),
    ),
    dict(
        key='09-verdict', kind='bullets', title='The Verdict',
        body=["Spring's context is the registry", 'done well: declared, checked at', 'start-up, mostly never called.', '', 'In business code, inject.', 'getBean belongs in main, tests,', 'and framework glue.', '', 'Keep singleton state out of', 'anything tests share.'],
        narration=(
            "So, here is the verdict. [[slnc 400]] Spring's context is "
            'the registry done well. [[slnc 300]] Declared, checked at '
            'start-up, and mostly never called. [[slnc 500]] In business '
            'code, have things injected. [[slnc 300]] Keep get bean for '
            'the main method, for tests, and for framework plumbing. '
            '[[slnc 500]] And keep changing state out of anything that '
            'tests share.'
        ),
    ),
    dict(
        key='10-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Autowired lookup goes', 'through it.', '', 'Every @SpringBootTest shares one.'],
        narration=(
            'Where have you met this before? [[slnc 400]] Every at '
            'Autowired injection goes through it. [[slnc 300]] And every '
            'at Spring Boot Test shares one, unless you ask it not to.'
        ),
    ),
    dict(
        key='11-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] No web server, '
            'no database, and no web library.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the context,', 'its errors, and the test cache.', '', 'The tests in the project run the', 'leak on real Spring.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything here is real. [[slnc 300]] The context, its '
            "errors, and the test cache. [[slnc 300]] The project's own "
            'tests reproduce the leak, on real Spring.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['Never, for the context itself:', 'you already have one.', '', 'The cost is in calling it.'],
        narration=(
            'So, when is this too much? [[slnc 400]] Never, for the '
            'context itself, because you already have one. [[slnc 300]] '
            'The cost is in calling it.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Run only the second leak test', 'and watch it fail.'],
        narration=(
            "That's the Registry, with Spring. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] The '
            'registry done well is one you rarely call, and even then, '
            'whatever it holds is shared. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Run only the second leak test, on its '
            'own. [[slnc 300]] And watch it fail. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
