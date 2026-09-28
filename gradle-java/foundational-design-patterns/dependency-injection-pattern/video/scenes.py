"""Scene definitions for the Dependency Injection teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Dependency Injection',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains '
            'Dependency Injection, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] With dependency injection, a '
            'class says what it needs, in its constructor. [[slnc 300]] '
            'And it is given those things. [[slnc 300]] It never goes '
            'looking for them. [[slnc 600]] Think of a chef in a '
            'restaurant kitchen. [[slnc 300]] The chef does not go '
            'shopping. [[slnc 300]] The ingredients are delivered to the '
            'station, ready to use. [[slnc 700]] In our online store, the '
            'checkout needs three helpers. [[slnc 300]] A discount '
            'policy, a payment gateway, and a notifier. [[slnc 500]] By '
            'the end, you will have heard it done in plain Java, in nine '
            'lines. [[slnc 300]] And a small container, built from '
            'scratch. [[slnc 300]] So a container becomes something you '
            'have watched being built, not something you take on trust.'
        ),
    ),
    dict(
        key='02-recap', kind='bullets', title='The Argument So Far',
        body=['Registry: a known place to put things.', 'Invisible dependencies, shared state.', '', 'Service Locator: a middleman that', 'finds or creates them.', 'The compiler still says nothing.', '', 'The word that matters: ask.'],
        narration=(
            'First, a quick recap of two related patterns. [[slnc 400]] '
            'The Registry puts shared objects in one well-known place. '
            '[[slnc 300]] But dependencies stay invisible, and state is '
            'shared between tests. [[slnc 500]] The Service Locator adds '
            'a middleman, which finds or creates the objects. [[slnc '
            '300]] But the compiler still cannot tell you when a '
            'dependency is missing. [[slnc 500]] The problem in both '
            'comes down to one word: ask. [[slnc 300]] The class asks for '
            'what it needs. [[slnc 300]] So nobody outside the class can '
            'see what it needs.'
        ),
    ),
    dict(
        key='03-signature', kind='console', title='The Signature Is The List',
        body="""ONE. The signature.
  CheckoutService(
    DiscountPolicy,
    PaymentGateway,
    Notifier)

  everything it needs:
  complete, and checked by
  the compiler.""",
        narration=(
            'Here is the answer. [[slnc 400]] The checkout service '
            'declares what it needs, in its constructor. [[slnc 300]] A '
            'discount policy, a payment gateway, and a notifier. [[slnc '
            "500]] The constructor's parameters are the complete list of "
            'what it depends on. [[slnc 300]] And the compiler checks it. '
            '[[slnc 500]] Try to create a checkout service with no '
            'arguments, and it will not compile. [[slnc 300]] There is no '
            'way to forget a helper. [[slnc 300]] It never looks anything '
            'up, so nothing is hidden. [[slnc 300]] And it is valid from '
            'the moment it exists.'
        ),
    ),
    dict(
        key='04-by-hand', kind='console', title='Wired By Hand',
        body="""TWO. By hand.
  the whole application is
  built in 9 lines of plain
  Java, in one place.

  charged [9000],
  3 messages sent.

  a container is an
  optimisation of something
  you can write yourself.""",
        narration=(
            'Second demo: wired by hand, before any framework. [[slnc '
            '400]] Something must create the objects, and hand them to '
            'each other. [[slnc 500]] Here, it is nine lines of plain '
            'Java, in one place. [[slnc 300]] Create the policy, the '
            'gateway, and the notifier. [[slnc 300]] Create the checkout '
            'service, giving it those three. [[slnc 300]] Then create the '
            'rest, and the storefront that uses them all. [[slnc 500]] It '
            'runs. [[slnc 300]] Ninety pounds is charged, and three '
            'messages are sent. [[slnc 500]] That is exactly what a '
            'container does for you. [[slnc 300]] A container is a '
            'shortcut for something you can write yourself.'
        ),
    ),
    dict(
        key='05-forms', kind='console', title='Three Forms',
        body="""THREE. Three forms.
  setter: for optional things.
  the order worked with no
  notifier.

  field: new ... compiled, and
  is invalid.
  NullPointerException.

  use constructor injection.""",
        narration=(
            'Third demo: three forms of injection. [[slnc 400]] '
            'Constructor injection, which you have just heard. [[slnc '
            '500]] Setter injection, for things that are truly optional. '
            '[[slnc 300]] Here, the notifier has a setter, and a '
            'do-nothing default. [[slnc 300]] So an order works, even '
            'with no notifier. [[slnc 500]] And field injection, where '
            'the fields are private, and something reaches in from '
            'outside to fill them. [[slnc 300]] This version compiles '
            'with no arguments, but it is not ready to use. [[slnc 300]] '
            'Placing an order throws a null pointer exception. [[slnc '
            '300]] It only works once a framework fills the fields. '
            '[[slnc 500]] The recommendation: constructor injection. '
            '[[slnc 300]] Required, visible, and valid from the start.'
        ),
    ),
    dict(
        key='06-container', kind='console', title='A Container, Written Here',
        body="""FOUR. A container.
  86 lines.

  it reads each constructor's
  parameter types, builds
  what each needs, calls it.

  the same graph as the hand
  wiring. charged [9000].""",
        narration=(
            'Fourth demo: a container, written right here, so it is not '
            'magic. [[slnc 400]] It is eighty-six lines long. [[slnc '
            "500]] It reads the types of each constructor's parameters. "
            '[[slnc 300]] For each one, it finds or builds a matching '
            'object. [[slnc 300]] Then it calls the constructor. [[slnc '
            '500]] It builds exactly the same set of objects as the hand '
            'wiring. [[slnc 300]] And the same order is charged ninety '
            'pounds. [[slnc 500]] That is what Spring, Guice, and Dagger '
            'do. [[slnc 300]] Plus scanning, lifetimes, and a great deal '
            'of polish.'
        ),
    ),
    dict(
        key='07-bill', kind='console', title='The Bill: It Fails At Start-Up',
        body="""FIVE. The bill.
  a bean missing:
  no bean for its parameter
  of type Notifier

  a circular dependency:
  Chicken -> Egg -> Chicken

  at start-up, not on the
  first order.""",
        narration=(
            'Fifth demo, and the cost. [[slnc 400]] A container that '
            'cannot build the objects fails, when it starts. [[slnc 500]] '
            'One object missing: it says there is nothing to supply the '
            'notifier. [[slnc 300]] A circle of needs: chicken needs egg, '
            'and egg needs chicken. [[slnc 500]] That is better than the '
            'service locator, which failed on the first real order, after '
            'the money moved. [[slnc 300]] But it is still not at compile '
            'time. [[slnc 500]] And a warning. [[slnc 300]] A class whose '
            'constructor needs seven things has a design problem. [[slnc '
            '300]] No injection style fixes that. [[slnc 300]] The long '
            'constructor is telling you the class does too much.'
        ),
    ),
    dict(
        key='08-grows', kind='bullets', title='Also On The Bill',
        body=['By hand, the wiring grows with', 'the application.', '', 'A container solves that,', 'and costs you magic.', '', 'Constructors grow long: that is', 'a design signal.'],
        narration=(
            'Two more costs. [[slnc 400]] First, when wiring by hand, the '
            'wiring grows with the application. [[slnc 300]] Nine lines '
            'is fine. [[slnc 300]] Nine hundred is not. [[slnc 300]] That '
            'is what a container is for. [[slnc 300]] And it costs you '
            'some magic, because something else now builds your objects. '
            '[[slnc 500]] Second, constructors can grow long. [[slnc '
            '300]] When they do, do not blame the injection. [[slnc 300]] '
            'Listen to what it is telling you.'
        ),
    ),
    dict(
        key='09-progression', kind='bullets', title='The Progression',
        body=['Registry put things in a known place.', '', 'Service Locator made a middleman that', 'could find them.', '', 'Dependency Injection stopped the class', 'asking at all.'],
        narration=(
            'Here is the whole idea, in three steps. [[slnc 400]] The '
            'Registry put things in a known place. [[slnc 300]] The '
            'Service Locator added a middleman that could find them. '
            '[[slnc 300]] Dependency injection stopped the class asking, '
            'at all. [[slnc 500]] Each step solved the problem left by '
            'the one before. [[slnc 300]] And only the last one lets a '
            'class tell you, in its constructor, what it needs.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Use constructor injection.', '', 'By hand until the wiring hurts.', 'Then a container.', '', 'Dependency injection is not Spring.', 'You have just done it in plain Java.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use constructor '
            'injection. [[slnc 300]] Wire things by hand, until the '
            'wiring starts to hurt. [[slnc 300]] Then use a container. '
            '[[slnc 500]] And remember: dependency injection is not the '
            'same thing as Spring. [[slnc 300]] You have just heard it '
            'done, in plain Java.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A constructor of interfaces; a class', 'that never calls new on collaborators.', '', 'Spring: @Component, @Service, and', 'constructor parameters.', '', 'Guice and Dagger: @Inject.', '', 'A main method or Config class that', 'builds everything in order.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a constructor whose parameters are '
            'interfaces, in a class that never creates its own helpers. '
            '[[slnc 300]] In Spring, look for the at Component or at '
            'Service annotations, with helpers as constructor parameters. '
            '[[slnc 300]] In Guice and Dagger, look for the at Inject '
            'annotation. [[slnc 300]] And look for a main method, or a '
            'configuration class, that builds everything in order.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java, including', 'the container.', '', 'The container is a teaching size:', 'no scanning, no scopes.', '', 'The failures it shows are the', 'real ones.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] '
            'Everything is plain Java, including the container. [[slnc '
            '300]] The container is a teaching size, with no scanning, '
            'and no lifetimes. [[slnc 500]] But the failures it shows, a '
            'missing object, and a circle of needs, are the real ones.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['Never, for the idea.', '', 'A container is too much for a small', 'application that fits in main.'],
        narration=(
            'So, when is this too much? [[slnc 400]] The idea itself, '
            'never. [[slnc 300]] But a container is too much for a small '
            'application that fits in one main method.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Make two beans depend on each', 'other, and read the message.'],
        narration=(
            "That's Dependency Injection. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Stop asking, '
            'and be given, because a constructor that lists what a class '
            'needs is worth more than any framework. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Make two objects depend on '
            'each other. [[slnc 300]] And read the message the container '
            'gives you. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
