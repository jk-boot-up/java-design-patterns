"""Scene definitions for the Registry with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Registry with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Registry pattern '
            'with Spring, in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] It is the framework version '
            'of the Registry video. That one built a registry by hand, '
            "and showed its costs. Spring's application context is a "
            'registry too, built far better. [[slnc 350]] The plain '
            'definition, in short: a well-known place where things are '
            'kept, found by asking. [[slnc 300]] By the end you will see '
            'what Spring fixes about the hand-built registry, when asking '
            "it is a mistake, and the failure that is Spring's own: a "
            'cached context that remembers what earlier tests did.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Registry, the hand-built video,', 'built a static registry and showed', 'its costs: invisible dependencies,', 'order-dependent tests.', '', 'This video uses the same checkout.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'This video assumes the Registry video. If you have not seen '
            'it, start there. It builds a registry by hand, and shows '
            'four costs, among them invisible dependencies, and a test '
            'that fails because of the order the tests ran in. [[slnc '
            '300]] This one uses the same checkout. It does not teach the '
            'pattern again. It shows what Spring does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['One thing is new: Spring Boot.', '', 'Its core is a container, the', 'ApplicationContext, that creates', 'your objects and lets you find them.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            "Before the first annotation, one new thing. Spring's core is "
            'a container, called the application context. It creates your '
            'objects, and lets you find them by type. That is a registry. '
            '[[slnc 300]] And a promise: skipping this video loses none '
            'of the pattern. The hand-built one teaches all of it.'
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
            'Here is the first thing to see. Registry dot get, from the '
            'hand-built video, is context dot get bean here. It found the '
            'recording gateway. [[slnc 300]] But look at what changed. '
            'Nothing is registered by calling a method, from somewhere. '
            'Things are registered by declaration: a component annotation '
            'on a class. And a missing bean fails when the context '
            'starts, not on the first call.'
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
            'Now two ways to use it. The injected checkout is given its '
            'collaborators, and never calls the registry at all. That is '
            'the best use of a registry: never calling it. [[slnc 300]] '
            'The other checkout calls get bean, three times. Same result. '
            'But its constructor takes nothing, its dependencies are '
            'invisible again, and constructing one with new throws a null '
            'pointer exception, because it needs Spring to hand it the '
            'context. [[slnc 300]] That is the hand-built registry, '
            'inside Spring. A get bean inside a business class is a '
            'service locator.'
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
            "Now the failure of Spring's own. Spring's test support "
            'caches a context, and reuses it across tests with the same '
            'configuration. Starting Spring is slow, so it is a sensible '
            'thing to do. [[slnc 300]] But the gateway is a singleton, so '
            'it remembers. Test A charges it once. Test B, on the same '
            'cached context, starts by expecting a clean gateway. It sees '
            'nine thousand. [[slnc 300]] That is the hand-built '
            "registry's order-dependent test failure, in Spring. This "
            "project's own tests prove it: the second test passes only "
            'because the first ran before it. Run alone, it would fail. '
            'The fix is to throw the context away, which is correct, and '
            'costs a new context.'
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
            'Spring has a second registry, and this one is of strings: '
            'the environment. Ask it for checkout currency, and you get '
            'pounds. Ask with a typo, checkout curency, and you get null. '
            'No error. No warning. [[slnc 300]] A required value with the '
            'same typo, injected, fails when the context starts: could '
            'not resolve placeholder. The untyped lookup is silent. The '
            'injected one is not.'
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
            'One more. Ask the registry for the notifier, by type, when '
            'there are two. No unique bean definition exception. Two '
            'beans found. [[slnc 300]] It is a run-time error, at the '
            'call site, not a compile error. Asking by type is only '
            'unambiguous until the second one arrives.'
        ),
    ),
    dict(
        key='09-verdict', kind='bullets', title='The Verdict',
        body=["Spring's context is the registry", 'done well: declared, checked at', 'start-up, mostly never called.', '', 'In business code, inject.', 'getBean belongs in main, tests,', 'and framework glue.', '', 'Keep singleton state out of', 'anything tests share.'],
        narration=(
            "My verdict, plainly. Spring's context is the registry, done "
            'well: declared, checked at start-up, and mostly never '
            'called. In business code, inject. Keep get bean to main, to '
            'tests, and to framework glue. [[slnc 300]] And keep '
            'singleton state out of anything that tests share.'
        ),
    ),
    dict(
        key='10-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Autowired lookup goes', 'through it.', '', 'Every @SpringBootTest shares one.'],
        narration=(
            'You have met this. Every autowired lookup goes through it. '
            'And every Spring boot test shares one, unless you ask it not '
            'to.'
        ),
    ),
    dict(
        key='11-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. No web '
            'server, no database, and no web starter.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the context,', 'its errors, and the test cache.', '', 'The tests in the project run the', 'leak on real Spring.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: the context, its errors, and the test '
            'cache. The tests in the project run the leak on real Spring.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['Never, for the context itself:', 'you already have one.', '', 'The cost is in calling it.'],
        narration=(
            'So when is it too much? Never, for the context itself: you '
            'already have one. The cost is in calling it.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Run only the second leak test', 'and watch it fail.'],
        narration=(
            "That's the Registry with Spring. [[slnc 250]] If you take "
            'one sentence away, take this one: the registry done well is '
            'one you rarely call, and even then, whatever it holds is '
            'shared. [[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, run only '
            'the second leak test, on its own, and watch it fail. [[slnc '
            '300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of '
            'the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
