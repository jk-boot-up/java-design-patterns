"""Scene definitions for the Service Locator teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Locator',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Service Locator pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A service locator is a '
            'middleman. [[slnc 300]] You ask it for what you need, and it '
            'finds it, or creates it. [[slnc 600]] Think of a hotel '
            'concierge. [[slnc 300]] You ask for a taxi, and the '
            'concierge arranges one. [[slnc 300]] But nobody can tell, by '
            'looking at you, that you needed a taxi. [[slnc 700]] This is '
            'one of three related patterns about how an object gets hold '
            'of what it needs. [[slnc 300]] The others are Registry, and '
            'Dependency Injection, each with its own video. [[slnc 500]] '
            'Service Locator is often called an anti-pattern. [[slnc '
            '300]] This video shows why, with evidence. [[slnc 300]] But '
            'it is also fair, because it solved a real problem, and there '
            'are places where it is still right.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The same checkout: a discount policy,', 'a payment gateway, a notifier.', '', "The registry's problems are now felt:", 'invisible dependencies, shared state.', '', 'Can a smarter middleman fix them?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The same online checkout, '
            'with the same three helpers. [[slnc 300]] A discount policy, '
            'a payment gateway, and a notifier. [[slnc 500]] And the '
            'problems of a simple registry are now being felt. [[slnc '
            '300]] Dependencies you cannot see, and state shared between '
            'tests. [[slnc 500]] So here is the question. [[slnc 300]] '
            'Can a smarter middleman fix them?'
        ),
    ),
    dict(
        key='03-recipes', kind='console', title='The Advance: Recipes',
        body="""ONE. Recipes.
  nothing asked for yet:
  gateways made 0
  notifiers made 0

  three finds of each:
  gateways made 1 (singleton)
  notifiers made 3 (new each
  time)""",
        narration=(
            "First demo: the locator's first advance, recipes. [[slnc "
            '400]] A registry holds things. [[slnc 300]] A locator holds '
            'recipes for making them. [[slnc 500]] Before anything is '
            'asked for, nothing has been made. [[slnc 500]] Ask three '
            'times for the gateway, set up as one shared instance. [[slnc '
            '300]] It is made once. [[slnc 500]] Ask three times for the '
            'notifier, set up to be fresh each time. [[slnc 300]] It is '
            'made three times. [[slnc 500]] So it creates things only '
            'when needed, and decides how long each one lives. [[slnc '
            '300]] A registry can do neither.'
        ),
    ),
    dict(
        key='04-swap', kind='console', title='The Other Advance: Swap For A Test',
        body="""TWO. A test.
  configure a fake gateway.

  the checkout charged the
  fake: [9000]

  no change to the checkout.""",
        narration=(
            'Second demo: the other advance, swapping for a test. [[slnc '
            '400]] Set up the locator with a fake gateway. [[slnc 300]] '
            'And the very same checkout charges the fake one. [[slnc '
            '300]] With no change to the checkout at all. [[slnc 500]] '
            'That is a genuine step forward. [[slnc 300]] Service Locator '
            'was a real answer to a real problem.'
        ),
    ),
    dict(
        key='05-silent', kind='console', title='The Bill: The Compiler Says Nothing',
        body="""THREE. Silence.
  production is configured.
  somebody forgot the notifier.

  new LocatorCheckout()
  compiled. the build was
  green.

  at run time: no service for
  Notifier.
  the customer was already
  charged.""",
        narration=(
            'Third demo: now the cost, with evidence. [[slnc 400]] '
            'Production is set up, but someone forgets the notifier. '
            '[[slnc 500]] Creating a locator checkout compiles. [[slnc '
            '300]] It constructs. [[slnc 300]] The build is green. [[slnc '
            '300]] Nothing anywhere complains. [[slnc 500]] Then a real '
            'order arrives. [[slnc 300]] The checkout asks for the '
            'discount policy, and gets it. [[slnc 300]] It asks for the '
            'gateway, and charges the customer. [[slnc 300]] Then it asks '
            'for the notifier, and there is no recipe. [[slnc 300]] It '
            'fails. [[slnc 500]] The customer has already been charged. '
            '[[slnc 300]] The failure arrived in production, after the '
            'money moved, not in the build.'
        ),
    ),
    dict(
        key='06-everywhere', kind='console', title='The Bill: Every Class Depends On It',
        body="""FOUR. Everywhere.
  classes that call the locator:
  Auditor, LocatorCheckout,
  ReceiptPrinter

  each is otherwise pure domain
  logic.

  a unit test must configure the
  locator first.""",
        narration=(
            'Fourth demo: the second cost, every class depends on the '
            'locator. [[slnc 400]] Here, three classes call the locator: '
            'the auditor, the checkout, and the receipt printer. [[slnc '
            '300]] Each one would otherwise be pure business logic. '
            '[[slnc 300]] Now each is tied to infrastructure. [[slnc '
            '500]] And a unit test of any of them must set up the locator '
            'first, or it fails. [[slnc 300]] A unit test that needs '
            'global setup is never quite a unit test.'
        ),
    ),
    dict(
        key='07-serviceloader', kind='console', title='Where It Is Still Right',
        body="""FIVE. Plug-ins.
  java.util.ServiceLoader
  found: [card, bank transfer]

  listed in META-INF/services.

  what is available is not
  known until run time.""",
        narration=(
            'Fifth demo: where this pattern is still right. [[slnc 400]] '
            'A plug-in system, where what is available is genuinely not '
            'known until the program runs. [[slnc 500]] Java has one '
            'built in, called Service Loader. [[slnc 300]] It found two '
            'payment plug-ins: card, and bank transfer. [[slnc 300]] Both '
            'listed in a small file. [[slnc 300]] The application could '
            'not have known about them in advance. [[slnc 500]] Here, '
            'asking is the whole point. [[slnc 300]] Service Loader is '
            "this pattern, in Java's own library, and it is nobody's "
            'mistake.'
        ),
    ),
    dict(
        key='08-verdict', kind='bullets', title='The Verdict',
        body=['Prefer the alternative for business', 'logic: do not ask; be given.', '', 'Keep a locator for plug-in systems,', 'and for the composition root of a', 'small application.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] For business logic, '
            'prefer the alternative: do not ask, be given. [[slnc 500]] '
            'Keep a locator for plug-in systems. [[slnc 300]] And for the '
            'one place in a small application that wires everything '
            'together.'
        ),
    ),
    dict(
        key='09-ask', kind='bullets', title='The Word Is Ask',
        body=['The class asks.', '', 'So nobody outside it knows what', 'it needs.', '', 'The next video removes the asking.'],
        narration=(
            'The whole difficulty comes down to one word: ask. [[slnc '
            '400]] The class asks for what it needs. [[slnc 300]] So '
            'nobody outside it knows what it needs. [[slnc 300]] Not the '
            'compiler, not the constructor, and not the person writing a '
            'test. [[slnc 500]] Dependency Injection, in its own video, '
            'removes the asking.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['find, lookup, getBean, resolve,', 'called from inside business classes.', '', 'ServiceLoader.load, JNDI lookup.', '', 'getBean inside a class that is itself', 'a bean.', '', 'A no-argument constructor that plainly', 'needs several things.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for words like find, lookup, get bean, or '
            'resolve, called from inside business classes. [[slnc 300]] '
            'Look for Service Loader, or a J N D I lookup. [[slnc 300]] '
            'Look for get bean, inside a class that Spring itself '
            'created. [[slnc 500]] And the giveaway: a class with an '
            'empty constructor, that plainly needs several things to '
            'work.'
        ),
    ),
    dict(
        key='11-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', 'ServiceLoader is the real one from', 'the standard library.', '', 'The forgotten notifier is simulated,', 'but exactly how it happens.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] '
            'Everything is plain Java. [[slnc 300]] Service Loader is the '
            "real one, from Java's own library. [[slnc 300]] The "
            'forgotten notifier is simulated, but it happens exactly this '
            'way in real projects.'
        ),
    ),
    dict(
        key='12-too-much', kind='bullets', title='When This Is Too Much',
        body=['For business logic.', '', 'It is right for plug-ins, and for the', 'composition root.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For business logic. '
            '[[slnc 300]] It is right for plug-ins, and for the one place '
            'that wires the application together.'
        ),
    ),
    dict(
        key='13-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a third plug-in to the', 'services file, and run act five.'],
        narration=(
            "That's the Service Locator pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] The '
            'word that matters is ask, because a class that asks hides '
            'what it needs from everyone outside it. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Add a third payment '
            'plug-in to the services file. [[slnc 300]] Then run the '
            'plug-in demo again. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
