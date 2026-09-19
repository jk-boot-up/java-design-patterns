"""Scene definitions for the Dependency Injection teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Dependency Injection',
        body=None,
        narration=(
            'Hello, and welcome. This video explains Dependency Injection '
            'in Java, and it is written and presented by Jayasekhar '
            'Konduru. [[slnc 300]] The plain definition: a class says '
            'what it needs, in its constructor, and is given it. It never '
            'goes looking. [[slnc 350]] This is the last project in the '
            'foundational category, and it closes an argument the last '
            'two videos began. Registry put things in a known place. '
            'Service Locator made a middleman that could find them. '
            'Dependency Injection stops the class asking at all. All '
            'three used the same three collaborators in our online store, '
            'a discount policy, a payment gateway and a notifier. [[slnc '
            '300]] By the end you will have seen it done in plain Java '
            'first, in nine lines, and you will have seen a small '
            'container written from scratch, so that a container is '
            'something you have watched being built, not something you '
            'take on trust.'
        ),
    ),
    dict(
        key='02-recap', kind='bullets', title='The Argument So Far',
        body=['Registry: a known place to put things.', 'Invisible dependencies, shared state.', '', 'Service Locator: a middleman that', 'finds or creates them.', 'The compiler still says nothing.', '', 'The word that matters: ask.'],
        narration=(
            'A quick recap of the argument. The registry: a well-known '
            'place to put things. It left dependencies invisible, and '
            'state shared between tests. [[slnc 300]] The service '
            'locator: a middleman that finds or creates them. The '
            'compiler still said nothing while a dependency was missing. '
            '[[slnc 300]] The problem in both is one word: ask. The class '
            'asks, so nobody outside it knows what it needs.'
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
            'Here is the answer. The checkout service declares what it '
            'needs, in its constructor. Discount policy. Payment gateway. '
            'Notifier. That is the signature, and the signature is the '
            'dependency list. [[slnc 300]] It is complete. It is checked '
            'by the compiler. Try to build a checkout service with no '
            'arguments, and it does not compile. There is no way to '
            'forget a collaborator. [[slnc 300]] It never looks anything '
            'up, so nothing is hidden. And it is valid the moment it '
            'exists.'
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
            'Now the wiring, by hand, before any framework. Something has '
            'to build the objects, and hand them to each other. Here it '
            'is: nine lines of plain Java, in one place. Build the '
            'policy, the gateway and the notifier. Build the checkout '
            'service with those three. Build the printer and the auditor. '
            'Build the storefront with all of them. [[slnc 300]] It runs. '
            'Charged nine thousand pence. Three messages sent. [[slnc '
            '300]] That is what a container does for you. A container is '
            'an optimisation of something you can write yourself.'
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
            'There are three forms. Constructor injection, which you have '
            'seen. Setter injection: for things that are genuinely '
            'optional. Here the notifier has a setter and a do-nothing '
            'default, and the order works without one. [[slnc 300]] And '
            'field injection, where the fields are private, and something '
            'reaches in from outside. This one compiles with no '
            'arguments, and is invalid. Placing an order throws a null '
            'pointer exception. It only works once something reaches in '
            'with reflection. It cannot be built validly in a test '
            'without a framework. [[slnc 300]] My recommendation: '
            'constructor injection. Mandatory, visible, and valid on '
            'creation.'
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
            'Now a container, written here, so it is not magic. '
            "Eighty-six lines. It reads each constructor's parameter "
            'types. For each one, it finds or builds a matching object. '
            'Then it calls the constructor. [[slnc 300]] It builds the '
            'same graph as the hand wiring, and the same order is '
            'charged, nine thousand pence. [[slnc 300]] That is what '
            'Spring, Guice and Dagger do, plus scanning, lifetimes, and a '
            'great deal of polish.'
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
            'Now the bill. A container that cannot build the graph fails, '
            'and it fails when it starts. A bean missing: no bean for its '
            'parameter of type notifier. A circular dependency: chicken '
            'needs egg, and egg needs chicken. [[slnc 300]] That is '
            'better than the service locator, which failed on the first '
            'real order, after the money moved. But it is still not at '
            'compile time. [[slnc 300]] And a warning: a class whose '
            'constructor takes seven things has a design problem that no '
            'injection style fixes. The long constructor is telling you '
            'the class does too much.'
        ),
    ),
    dict(
        key='08-grows', kind='bullets', title='Also On The Bill',
        body=['By hand, the wiring grows with', 'the application.', '', 'A container solves that,', 'and costs you magic.', '', 'Constructors grow long: that is', 'a design signal.'],
        narration=(
            'Two more costs. First, by hand, the wiring grows with the '
            'application. Nine lines is fine. Nine hundred is not. That '
            'is what a container is for. And it costs you some magic, '
            'because now something else builds your objects. [[slnc 300]] '
            'Second, constructors grow long. When they do, do not blame '
            'the injection. Listen to what it is telling you.'
        ),
    ),
    dict(
        key='09-progression', kind='bullets', title='The Progression',
        body=['Registry put things in a known place.', '', 'Service Locator made a middleman that', 'could find them.', '', 'Dependency Injection stopped the class', 'asking at all.'],
        narration=(
            'Here is the whole argument, in three moves. The registry put '
            'things in a known place. The service locator made a '
            'middleman that could find them. Dependency injection stopped '
            'the class asking at all. [[slnc 300]] Each one solved the '
            'problem the one before it left. And the last one is the only '
            'one where the class tells you, in its signature, what it '
            'needs.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Use constructor injection.', '', 'By hand until the wiring hurts.', 'Then a container.', '', 'Dependency injection is not Spring.', 'You have just done it in plain Java.'],
        narration=(
            'My verdict, plainly. Use constructor injection. Wire by hand '
            'until the wiring hurts. Then use a container. [[slnc 300]] '
            'And remember: dependency injection is not Spring. You have '
            'just done it, in plain Java.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['A constructor of interfaces; a class', 'that never calls new on collaborators.', '', 'Spring: @Component, @Service, and', 'constructor parameters.', '', 'Guice and Dagger: @Inject.', '', 'A main method or Config class that', 'builds everything in order.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'constructor whose parameters are interfaces, in a class that '
            'never calls new on its collaborators. In Spring, the '
            'component or service annotation, with the collaborators as '
            'constructor parameters. In Guice and Dagger, the inject '
            'annotation. And a main method, or a config class, that '
            'builds everything in order. This project does not run '
            'Spring. The point is that you no longer need it to '
            'understand it.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java, including', 'the container.', '', 'The container is a teaching size:', 'no scanning, no scopes.', '', 'The failures it shows are the', 'real ones.'],
        narration=(
            'The same honest admission as everywhere in this course. It '
            'is all plain Java, including the container. The container is '
            'teaching size: no scanning, no scopes, no polish. But the '
            'failures it shows, a missing bean and a circular dependency, '
            'are the real ones.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['Never, for the idea.', '', 'A container is too much for a small', 'application that fits in main.'],
        narration=(
            'So when is it too much? Never, for the idea. A container is '
            'too much for a small application that fits in a main method.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Make two beans depend on each', 'other, and read the message.'],
        narration=(
            "That's Dependency Injection. [[slnc 250]] If you take one "
            'sentence away, take this one: stop asking, and be given, '
            'because a signature that lists what a class needs is worth '
            'more than any framework. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, make two beans depend on each other, and '
            'read the message the container gives you. [[slnc 300]] If '
            'this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
