"""Scene definitions for the Service Locator teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Locator',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Service Locator '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'service locator is a middleman. You ask it for what you '
            'need, and it finds it, or creates it. [[slnc 350]] This is '
            'the fourth project in the foundational category, and the '
            'second of three that answer one question: how does an object '
            'get hold of what it needs? The last video showed a registry, '
            'a bag of things someone remembered to put in. This one adds '
            'a middleman. The next one stops the asking. All three use '
            'the same three collaborators in our online store. [[slnc '
            '300]] Service Locator is widely called an anti-pattern. I '
            'will show you why, with evidence. But I will also be fair, '
            'because it was a reasonable answer to a real problem, and '
            'there are places it is still right.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The same checkout: a discount policy,', 'a payment gateway, a notifier.', '', "The registry's problems are now felt:", 'invisible dependencies, shared state.', '', 'Can a smarter middleman fix them?'],
        narration=(
            'Here is the scenario. The same checkout, with the same three '
            "collaborators. And the registry's problems are now felt: "
            'dependencies you cannot see, and state shared between tests. '
            '[[slnc 300]] Can a smarter middleman fix them?'
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
            'Here is what a locator does better than a registry. A '
            'registry holds things. A locator holds recipes for making '
            'them. [[slnc 300]] Before anything is asked for, nothing has '
            'been made. Ask three times for the gateway, configured as a '
            'singleton: it is made once. Ask three times for the '
            'notifier, configured as a prototype: it is made three times. '
            '[[slnc 300]] It creates lazily, and it decides how long each '
            'thing lives. A registry can do neither.'
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
            'The second advance. Configure a fake gateway, and the same '
            'checkout charges the fake. No change to the checkout at all. '
            '[[slnc 300]] That is a genuine step forward, and I want to '
            'say so. Service Locator was a real answer to a real problem.'
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
            'Now the bill, as evidence. Production is configured, and '
            'somebody forgets the notifier. [[slnc 300]] New locator '
            'checkout compiles. It constructs. The build is green. '
            'Nothing anywhere complains. [[slnc 300]] Then a real order '
            'arrives. The checkout asks for the discount policy, and gets '
            'it. It asks for the gateway, and charges the customer. Then '
            'it asks for the notifier, and there is no recipe. It fails. '
            'The customer has already been charged. [[slnc 300]] The '
            'failure arrived in production, after the money moved, not in '
            'the build.'
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
            'Second cost. Every class that needs a collaborator now '
            'depends on the locator. Here, three of them: the auditor, '
            'the checkout, and the receipt printer. Each is otherwise '
            'pure domain logic, now coupled to infrastructure. [[slnc '
            '300]] And a unit test of any of them must configure the '
            'locator first, or it fails. A unit test that needs global '
            'set-up is never quite a unit test.'
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
            'Now to be fair. There is a place this pattern is still '
            'right. A plug-in system, where what is available is '
            'genuinely not known until run time. [[slnc 300]] Java has '
            'one built in: service loader. It found two payment plug-ins, '
            'card, and bank transfer, listed in a file. The application '
            'could not have known about them in advance. Asking is the '
            'whole point. [[slnc 300]] Service loader is this pattern, in '
            "the standard library, and it is nobody's mistake."
        ),
    ),
    dict(
        key='08-verdict', kind='bullets', title='The Verdict',
        body=['Prefer the alternative for business', 'logic: do not ask; be given.', '', 'Keep a locator for plug-in systems,', 'and for the composition root of a', 'small application.'],
        narration=(
            'My verdict, plainly. For business logic, prefer the '
            'alternative: do not ask, be given. Keep a locator for '
            'plug-in systems, and for the composition root of a small '
            'application, the one place that wires things together.'
        ),
    ),
    dict(
        key='09-ask', kind='bullets', title='The Word Is Ask',
        body=['The class asks.', '', 'So nobody outside it knows what', 'it needs.', '', 'The next video removes the asking.'],
        narration=(
            'The whole difficulty is one word. Ask. The class asks, so '
            'nobody outside it knows what it needs. Not the compiler, not '
            'the constructor, not the person writing a test. [[slnc 300]] '
            'The next video removes the asking.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['find, lookup, getBean, resolve,', 'called from inside business classes.', '', 'ServiceLoader.load, JNDI lookup.', '', 'getBean inside a class that is itself', 'a bean.', '', 'A no-argument constructor that plainly', 'needs several things.'],
        narration=(
            'How do you recognise this in code you did not write? The '
            'words find, lookup, get bean, or resolve, called from inside '
            'business classes. Service loader, or a J N D I lookup. Get '
            'bean, inside a class that is itself a bean: a locator, '
            'inside a container. And the giveaway: a class with a '
            'no-argument constructor, that plainly needs several things '
            'to work.'
        ),
    ),
    dict(
        key='11-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', 'ServiceLoader is the real one from', 'the standard library.', '', 'The forgotten notifier is simulated,', 'but exactly how it happens.'],
        narration=(
            'The same honest admission as everywhere in this course. It '
            'is all plain Java. Service loader is the real one from the '
            'standard library. The forgotten notifier is simulated, but '
            'it happens exactly this way in real projects.'
        ),
    ),
    dict(
        key='12-too-much', kind='bullets', title='When This Is Too Much',
        body=['For business logic.', '', 'It is right for plug-ins, and for the', 'composition root.'],
        narration=(
            'So when is it too much? For business logic. It is right for '
            'plug-ins, and for the composition root.'
        ),
    ),
    dict(
        key='13-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a third plug-in to the', 'services file, and run act five.'],
        narration=(
            "That's the Service Locator. [[slnc 250]] If you take one "
            'sentence away, take this one: the word that matters is ask, '
            'because a class that asks hides what it needs from everyone '
            'who is not inside it. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, add a third plug-in to the services file, '
            'and run act five. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
