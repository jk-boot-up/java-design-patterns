"""Scene definitions for the Dependency Injection with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Dependency Injection with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains '
            'Dependency Injection, in Java, using Spring. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] With dependency '
            'injection, a class says what it needs in its constructor, '
            'and is given it. [[slnc 600]] Think of a film set. [[slnc '
            '300]] The actors do not fetch their own props. [[slnc 300]] '
            'The crew places everything they need, ready for the scene. '
            '[[slnc 700]] This is the framework version of the Dependency '
            'Injection video. [[slnc 300]] That one wired the application '
            'by hand, in nine lines, and even wrote a small container. '
            '[[slnc 300]] This one runs the very same classes through '
            'Spring. [[slnc 500]] By the end, you will know what each '
            'Spring annotation replaced. [[slnc 300]] You will hear two '
            'of its real start-up errors. [[slnc 300]] And you will know '
            'what the magic costs.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Dependency Injection, the hand-built', 'video, wired everything in nine lines', 'and wrote a container from scratch.', '', 'This video uses the same classes.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Dependency Injection video. [[slnc '
            '400]] That one wires the application by hand, and builds a '
            'small container from scratch. [[slnc 500]] Here, we use the '
            'same classes. [[slnc 300]] The checkout service, the receipt '
            'printer, the auditor, and the storefront. [[slnc 300]] We '
            'will not teach the pattern again. [[slnc 300]] Instead, we '
            'ask what Spring does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['One thing is new: Spring Boot.', '', 'Spring creates the objects of an', 'application and wires them together.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'One thing is new in this project: Spring Boot. [[slnc 400]] '
            'At its heart, Spring is a container. [[slnc 300]] It creates '
            'the objects of an application, and connects them together. '
            '[[slnc 300]] Spring Boot sets it up with sensible defaults. '
            '[[slnc 500]] And one promise. [[slnc 300]] If you skip this '
            'video, you lose none of the pattern. [[slnc 300]] This one '
            'is about the tool.'
        ),
    ),
    dict(
        key='04-annotation', kind='bullets', title='One Annotation Per Class',
        body=['@Component on each class.', '', 'That is the only change to the', "partner's classes.", '', 'The constructors are untouched.'],
        narration=(
            "The only change to the partner's classes is one annotation "
            'on each. [[slnc 400]] The at Component annotation. [[slnc '
            '300]] It says: Spring should create this one. [[slnc 500]] '
            'The constructors are untouched. [[slnc 300]] Not a single '
            'line of logic changed.'
        ),
    ),
    dict(
        key='05-graph', kind='console', title='The Same Graph',
        body="""ONE. No wiring code.
  Wiring.build() is gone.
  Spring built the graph from
  the constructors.

  charged [9000],
  messages sent 3,
  exactly as by hand.""",
        narration=(
            'First demo, and here is the key moment. [[slnc 400]] The '
            'hand-written wiring code from the last video is gone. [[slnc '
            '300]] Spring built all the objects, and connected them, by '
            'reading the constructors. [[slnc 500]] The same order is '
            'charged ninety pounds. [[slnc 300]] The same three messages '
            'are sent. [[slnc 300]] Exactly as it was by hand.'
        ),
    ),
    dict(
        key='06-replaced', kind='console', title='What Each Annotation Replaced',
        body="""TWO. Replaced.
  beans: Auditor,
  CheckoutService,
  LoyaltyPolicy, ReceiptPrinter,
  RecordingGateway,
  RecordingNotifier, Storefront

  7 annotations replaced
  7 lines of new.""",
        narration=(
            'Second demo: what each annotation replaced. [[slnc 400]] '
            'Seven classes, and seven annotations. [[slnc 300]] Spring '
            'built the auditor, the checkout service, the loyalty policy, '
            'the printer, the payment gateway, the notifier, and the '
            'storefront. [[slnc 500]] Each annotation replaced one line '
            'that created an object by hand. [[slnc 300]] The constructor '
            'parameters told Spring the rest. [[slnc 300]] Exactly as '
            'they told the hand-written container.'
        ),
    ),
    dict(
        key='07-missing', kind='console', title='A Missing Bean',
        body="""THREE. Missing.
  UnsatisfiedDependency
  Exception, when the context
  starts:

  Error creating bean with name
  checkoutService:
  constructor parameter 2

  at start-up, not on the first
  order.""",
        narration=(
            "Third demo: Spring's own failures, starting with a missing "
            'object. [[slnc 400]] Leave out the notifier. [[slnc 300]] '
            'Spring refuses to start. [[slnc 300]] It reports an '
            'Unsatisfied Dependency Exception. [[slnc 300]] It cannot '
            'create the checkout service, because constructor parameter '
            'two has nothing to fill it. [[slnc 500]] That is the same '
            'failure the hand-written container gave. [[slnc 300]] It '
            'fails at start-up, before any order is taken. [[slnc 300]] '
            'But it is still not caught at compile time.'
        ),
    ),
    dict(
        key='08-cycle', kind='console', title='A Circular Dependency',
        body="""FOUR. A cycle.
  chicken needs egg,
  egg needs chicken.

  BeanCurrentlyInCreation
  Exception

  refused by default since
  Spring 6.""",
        narration=(
            'Fourth demo: a circle of needs. [[slnc 400]] A chicken needs '
            'an egg, and the egg needs the chicken. [[slnc 500]] Spring '
            'refuses to start, with a Bean Currently In Creation '
            'exception. [[slnc 300]] Since Spring six, refusing is the '
            'default. [[slnc 500]] A circle like this is usually a sign '
            'of a design problem, not a wiring problem.'
        ),
    ),
    dict(
        key='09-field', kind='console', title='Field Injection',
        body="""FIVE. Field injection.
  @Autowired on private
  fields.

  new FieldInjectedCheckout()
  compiled. placing an order:
  NullPointerException.

  inside Spring: works.""",
        narration=(
            'Fifth demo: field injection. [[slnc 400]] Here, the at '
            'Autowired annotation sits on private fields. [[slnc 300]] '
            'Spring can fill them in. [[slnc 300]] Nothing else can. '
            '[[slnc 500]] Creating this class with new compiles. [[slnc '
            '300]] But placing an order throws a null pointer exception, '
            'because the fields are empty. [[slnc 300]] Inside Spring, it '
            'works. [[slnc 500]] So it cannot be tested properly without '
            "Spring. [[slnc 300]] That is exactly why Spring's own "
            'guidance recommends constructor injection.'
        ),
    ),
    dict(
        key='10-cost', kind='console', title='What The Magic Costs',
        body="""SIX. The cost.
  by hand: hundreds of
  nanoseconds each.

  a Spring context: a few
  milliseconds, once.

  paid at start-up.
  timings vary by machine.""",
        narration=(
            'Last demo: what the magic costs. [[slnc 400]] Building the '
            'objects by hand takes a few hundred nanoseconds. [[slnc '
            '300]] Starting a Spring container takes a few milliseconds, '
            'once, at start-up. [[slnc 300]] And it grows with the size '
            'of the application. [[slnc 300]] The exact times vary by '
            'machine. [[slnc 500]] There is a second cost, which is '
            'harder to measure. [[slnc 300]] Your objects now come from '
            'somewhere that is not in your own code.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Unchanged:', 'constructor injection,', 'by hand until the wiring hurts,', 'then a container.', '', 'Spring did not add the idea.', 'It removed the typing.'],
        narration=(
            'So, here is the verdict, and it has not changed. [[slnc '
            '400]] Use constructor injection. [[slnc 300]] Wire by hand, '
            'until the wiring starts to hurt. [[slnc 300]] Then use a '
            'container. [[slnc 500]] Spring did not add the idea. [[slnc '
            '300]] It removed the typing.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['In every Spring Boot application.', '', 'This is where the annotations you', 'copy from tutorials come from.'],
        narration=(
            'Where have you met this before? [[slnc 400]] In every Spring '
            'Boot application. [[slnc 300]] This is where the annotations '
            'you copy from tutorials come from. [[slnc 300]] And now you '
            'know what each one replaced.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] No web server, '
            'no database, and no web library. [[slnc 300]] Just the '
            'container.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's container", 'and its error messages.', '', 'The timings are measured, and vary.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            "Everything here is real. [[slnc 300]] Spring's container, "
            'and its error messages. [[slnc 300]] The timings are real '
            'measurements, and they vary by machine.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Delete component from the notifier', 'and read the new error.'],
        narration=(
            "That's Dependency Injection with Spring. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Spring '
            'did not add the idea of dependency injection, it removed the '
            'typing. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Remove the at Component annotation from the notifier. '
            '[[slnc 300]] And read the error message that Spring gives '
            'you. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
