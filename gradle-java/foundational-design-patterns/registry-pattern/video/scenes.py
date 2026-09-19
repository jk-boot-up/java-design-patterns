"""Scene definitions for the Registry teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Registry',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Registry pattern '
            'in Java, and it is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] The plain definition: a registry is a '
            'well-known place where things are kept, so any object can '
            'find what it needs by asking. [[slnc 350]] This is the third '
            'project in the foundational category, and the first of three '
            'that answer one question: how does an object get hold of '
            'what it needs? Registry is a well-known place. The next '
            'video, on Service Locator, adds a middleman. The one after, '
            'on Dependency Injection, stops the asking altogether. All '
            'three use the same three collaborators in our online store, '
            'a discount policy, a payment gateway and a notifier, so you '
            'can compare them. [[slnc 300]] By the end you will see why a '
            'registry is a global variable with better manners, with '
            'evidence.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A checkout needs three things:', 'a discount policy,', 'a payment gateway,', 'and a notifier.', '', 'The payment gateway is needed six', 'classes down.'],
        narration=(
            'Here is the scenario. The checkout needs three things: a '
            'discount policy, a payment gateway, and a notifier. [[slnc '
            '300]] And the payment gateway is needed six classes down '
            'from where the checkout starts. How does it get there?'
        ),
    ),
    dict(
        key='03-passed', kind='console', title='Pass It Down',
        body="""ONE. Pass it down.
  the gateway went through:
  Storefront, CartService,
  OrderCoordinator,
  PricingStage, PaymentStage,
  Charger.

  only the last one uses it.""",
        narration=(
            'The plain answer: pass it down. The gateway goes into the '
            'storefront, which passes it to the cart service, which '
            'passes it to the order coordinator, the pricing stage, the '
            'payment stage, and finally the charger. Six constructors. '
            '[[slnc 300]] Only the last one uses it. The other five '
            'forward it. [[slnc 300]] I want to be fair to this. It is '
            'real friction, and anyone who says otherwise has not had to '
            'add a parameter to six constructors. But it is also honest. '
            'Every dependency is visible, in a signature.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A well-known object others can', 'find things in.', '', 'Registry.get(PaymentGateway.class)', '', 'The six constructors collapse.'],
        narration=(
            'The pattern: a well-known object that others find things in. '
            'Registry dot get, payment gateway. From anywhere. [[slnc '
            "300]] The six constructors collapse. The checkout's "
            'constructor takes nothing at all. The friction is gone.'
        ),
    ),
    dict(
        key='05-works', kind='console', title='It Works',
        body="""TWO. The registry.
  RegistryCheckout's
  constructor takes nothing.

  six constructors became
  none.""",
        narration=(
            'And it works. The registry checkout takes nothing in its '
            'constructor. It asks the registry for the discount policy, '
            'the gateway and the notifier, when it needs them. [[slnc '
            '300]] Six constructors became none. And that is exactly '
            'where the trouble starts.'
        ),
    ),
    dict(
        key='06-invisible', kind='console', title='The Bill: Invisible',
        body="""THREE. Invisible.
  new RegistryCheckout()
  compiled and ran.

  its signature says it needs
  nothing.

  the first call failed:
  nothing is registered for
  DiscountPolicy.""",
        narration=(
            'First cost. The dependencies become invisible. New registry '
            'checkout compiles, and constructs, and looks perfectly fine. '
            'Its signature says it needs nothing. [[slnc 300]] Then the '
            'first call fails: nothing is registered for discount policy. '
            'Three things had to be registered first, and nothing in the '
            'class says so. The compiler could not tell you. Neither '
            'could the constructor.'
        ),
    ),
    dict(
        key='07-order', kind='console', title='The Bill: Order Dependence',
        body="""FOUR. Order.
  order one:
  both tests passed.
  order two:
  the checkout test FAILED,
  saw 2 charges.

  neither test changed.
  the order did.""",
        narration=(
            'Second cost, and the one teams meet first. Two tests share '
            'the registry. One leaves a gateway behind, with a charge '
            'already on it. The other expects exactly one charge in '
            'total. [[slnc 300]] In one order, both pass. In the other '
            'order, the second test fails: it saw two charges. [[slnc '
            '300]] Neither test changed. The order they ran in did. This '
            'is the kind of failure that costs a team a day, and it comes '
            'from global state.'
        ),
    ),
    dict(
        key='08-contents', kind='console', title='The Bill: What Is In It?',
        body="""FIVE. Contents.
  at start-up: []
  after one class ran:
  [DiscountPolicy]
  after two more:
  [DiscountPolicy, Notifier,
   PaymentGateway]

  in no one file.""",
        narration=(
            'Third cost. What is in the registry, right now? At start-up, '
            'nothing. After one class ran, the discount policy. After two '
            'more, all three. [[slnc 300]] That answer is not in any one '
            'file. It depends on what has run, and in what order. And it '
            'is a static map, shared by every thread, so thread safety is '
            'now a question too.'
        ),
    ),
    dict(
        key='09-where', kind='bullets', title='Where A Registry Is Right',
        body=['A very few things that are truly', 'application-wide,', '', 'set up once at start-up,', 'and never changed.'],
        narration=(
            'Is there a place where a registry is the right answer? Yes. '
            'A very small number of things that are truly '
            'application-wide, set up once at start-up, and never '
            'changed. [[slnc 300]] Not collaborators that vary. Not '
            'anything a test needs to replace.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Use a registry narrowly.', '', 'A very few application-wide things,', 'set up once.', '', 'Not for collaborators, and not for', 'anything that tests must replace.'],
        narration=(
            'My verdict, plainly. Use a registry narrowly. For a very few '
            'application-wide things, set up once. Not for the '
            'collaborators of your business logic, and not for anything a '
            'test must replace. [[slnc 300]] And the problem it leaves, '
            'invisible dependencies, is what the next video tries to fix, '
            'with a middleman that can find and create things.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['Static get, lookup, getInstance.', 'System.getProperties(),', 'Locale.getDefault().', '', 'A Context passed everywhere.', '', 'A BeforeEach that clears something', 'static, because tests leaked.'],
        narration=(
            'How do you recognise this in code you did not write? A class '
            'with static get, lookup, or get instance methods, keyed by '
            'type or by name. System dot get properties. Locale dot get '
            'default. A context object passed everywhere. And the '
            'giveaway: a before each method that clears something static, '
            'because tests were leaking into each other.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', 'The test order is simulated by running', 'two test bodies in both orders,', 'in one shared registry.', '', 'The failure is exactly the real one.'],
        narration=(
            'The same honest admission as everywhere in this course. It '
            'is all plain Java. The two orders are simulated by running '
            'two test bodies, in each order, against one shared registry. '
            'But the failure is exactly the real one, and it is in the '
            "project's own tests."
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For nearly everything that is not', 'truly application-wide.'],
        narration=(
            'So when is a registry too much? For nearly everything that '
            'is not truly application-wide.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Run the two tests in both', 'orders yourself, and see which one fails.'],
        narration=(
            "That's the Registry. [[slnc 250]] If you take one sentence "
            'away, take this one: a registry removes the friction of '
            'passing things down, and pays for it by hiding what every '
            'class needs. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'run the two tests in both orders yourself, and see which one '
            'fails. [[slnc 300]] If this helped, a like genuinely does '
            'help other people find it, and subscribe if you would like '
            'the rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
