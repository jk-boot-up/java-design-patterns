"""Scene definitions for the Registry teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Registry',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Registry pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A registry is a well-known '
            'place where things are kept. [[slnc 300]] So any object can '
            'find what it needs, just by asking. [[slnc 600]] Think of a '
            'noticeboard in an office. [[slnc 300]] Anyone can walk up '
            'and read the phone number they need. [[slnc 300]] But nobody '
            'knows who pinned what, or when. [[slnc 700]] This is one of '
            'three related patterns that answer one question. [[slnc '
            '300]] How does an object get hold of what it needs? [[slnc '
            '300]] The others are Service Locator, and Dependency '
            'Injection, each with its own video. [[slnc 500]] In our '
            'online store, the checkout needs a discount policy, a '
            'payment gateway, and a notifier. [[slnc 300]] By the end, '
            'you will hear, with evidence, why a registry is a global '
            'variable with better manners.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A checkout needs three things:', 'a discount policy,', 'a payment gateway,', 'and a notifier.', '', 'The payment gateway is needed six', 'classes down.'],
        narration=(
            'Here is the scenario. [[slnc 400]] The checkout needs three '
            'helpers. [[slnc 300]] A discount policy, a payment gateway, '
            'and a notifier. [[slnc 500]] And the payment gateway is '
            'needed six classes down, from where the checkout starts. '
            '[[slnc 500]] So here is the question. [[slnc 300]] How does '
            'it get there?'
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
            'First, the plain answer: pass it down. [[slnc 400]] The '
            'gateway goes into the storefront. [[slnc 300]] The '
            'storefront passes it to the cart service. [[slnc 300]] Then '
            'to the order coordinator, the pricing stage, the payment '
            'stage, and finally the charger. [[slnc 300]] Six '
            'constructors. [[slnc 500]] Only the last one actually uses '
            'it. [[slnc 300]] The other five just pass it along. [[slnc '
            '500]] To be fair, that is real friction. [[slnc 300]] But it '
            'is also honest. [[slnc 300]] Every dependency is visible, in '
            'a constructor.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A well-known object others can', 'find things in.', '', 'Registry.get(PaymentGateway.class)', '', 'The six constructors collapse.'],
        narration=(
            'Now, the pattern. [[slnc 400]] A well-known object that '
            'others can find things in. [[slnc 300]] Registry dot get, '
            'payment gateway. [[slnc 300]] From anywhere in the code. '
            '[[slnc 500]] The six constructors collapse. [[slnc 300]] The '
            "checkout's constructor takes nothing at all. [[slnc 300]] "
            'The friction is gone.'
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
            'Second demo: it works. [[slnc 400]] The registry checkout '
            'takes nothing in its constructor. [[slnc 300]] It asks the '
            'registry for the discount policy, the gateway, and the '
            'notifier, whenever it needs them. [[slnc 500]] Six '
            'constructors became none. [[slnc 300]] And that is exactly '
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
            'Third demo: the first cost, invisible dependencies. [[slnc '
            '400]] Creating a registry checkout compiles, and looks '
            'perfectly fine. [[slnc 300]] Its constructor says it needs '
            'nothing. [[slnc 500]] Then the first call fails. [[slnc '
            '300]] Nothing is registered for the discount policy. [[slnc '
            '500]] Three things had to be registered first. [[slnc 300]] '
            'And nothing in the class says so. [[slnc 300]] The compiler '
            'could not tell you, and neither could the constructor.'
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
            'Fourth demo: the second cost, and the one teams meet first. '
            '[[slnc 400]] Two tests share the registry. [[slnc 300]] One '
            'leaves a gateway behind, with a charge already on it. [[slnc '
            '300]] The other expects exactly one charge in total. [[slnc '
            '500]] Run them in one order, and both pass. [[slnc 300]] Run '
            'them in the other order, and the second test fails, because '
            'it saw two charges. [[slnc 500]] Neither test changed. '
            '[[slnc 300]] Only the order they ran in did. [[slnc 300]] '
            'This kind of failure can cost a team a whole day. [[slnc '
            '300]] And it comes from shared, global state.'
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
            'Fifth demo: the third cost. [[slnc 400]] What is in the '
            'registry, right now? [[slnc 500]] At start-up: nothing. '
            '[[slnc 300]] After one class has run: the discount policy. '
            '[[slnc 300]] After two more: all three. [[slnc 500]] That '
            'answer is not written in any one file. [[slnc 300]] It '
            'depends on what has run, and in what order. [[slnc 300]] And '
            'the registry is shared by every thread, so thread safety '
            'becomes a question too.'
        ),
    ),
    dict(
        key='09-where', kind='bullets', title='Where A Registry Is Right',
        body=['A very few things that are truly', 'application-wide,', '', 'set up once at start-up,', 'and never changed.'],
        narration=(
            'So, is a registry ever the right answer? [[slnc 400]] Yes. '
            '[[slnc 300]] For a very small number of things that are '
            'truly application-wide. [[slnc 300]] Set up once, at '
            'start-up, and never changed. [[slnc 500]] But not for '
            'helpers that vary. [[slnc 300]] And not for anything a test '
            'needs to replace.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Use a registry narrowly.', '', 'A very few application-wide things,', 'set up once.', '', 'Not for collaborators, and not for', 'anything that tests must replace.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a registry '
            'narrowly. [[slnc 300]] For a very few application-wide '
            'things, set up once. [[slnc 500]] Not for the helpers of '
            'your business logic. [[slnc 300]] And not for anything a '
            'test must replace. [[slnc 500]] The problem it leaves, '
            'invisible dependencies, is what the Service Locator pattern '
            'tries to fix.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['Static get, lookup, getInstance.', 'System.getProperties(),', 'Locale.getDefault().', '', 'A Context passed everywhere.', '', 'A BeforeEach that clears something', 'static, because tests leaked.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a class with static get, lookup, or '
            'get instance methods, keyed by type or by name. [[slnc 300]] '
            'In Java itself, System get properties, and Locale get '
            'default. [[slnc 300]] Look for a context object passed '
            'everywhere. [[slnc 500]] And the giveaway: a test setup '
            'method that clears something static, because tests were '
            'leaking into each other.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', 'The test order is simulated by running', 'two test bodies in both orders,', 'in one shared registry.', '', 'The failure is exactly the real one.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] '
            'Everything is plain Java. [[slnc 300]] The two test orders '
            'are simulated, by running two tests in each order, against '
            'one shared registry. [[slnc 500]] But the failure is exactly '
            "the real one. [[slnc 300]] And it is in the project's own "
            'tests.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For nearly everything that is not', 'truly application-wide.'],
        narration=(
            'So, when is a registry too much? [[slnc 400]] For nearly '
            'everything that is not truly application-wide.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Run the two tests in both', 'orders yourself, and see which one fails.'],
        narration=(
            "That's the Registry pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A registry '
            'removes the friction of passing things down, and pays for it '
            'by hiding what every class needs. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Run the two tests in both '
            'orders yourself. [[slnc 300]] And see which one fails. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
