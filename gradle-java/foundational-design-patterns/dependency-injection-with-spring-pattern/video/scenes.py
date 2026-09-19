"""Scene definitions for the Dependency Injection with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Dependency Injection with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains Dependency Injection '
            'with Spring, in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] It is the framework version '
            'of the Dependency Injection video. That one wired an '
            'application by hand, in nine lines, and even wrote a small '
            'container. This one runs the very same classes through '
            'Spring. [[slnc 350]] The plain definition, in short: a class '
            'says what it needs in its constructor, and is given it. '
            '[[slnc 300]] By the end you will see what each Spring '
            'annotation replaced, read two of its real start-up errors, '
            'and know what the magic costs.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Dependency Injection, the hand-built', 'video, wired everything in nine lines', 'and wrote a container from scratch.', '', 'This video uses the same classes.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'This video assumes the Dependency Injection video. If you '
            'have not seen it, start there. It wires the application by '
            'hand and builds a small container from scratch. [[slnc 300]] '
            'This one uses the same classes: the checkout service, the '
            'printer, the auditor, the storefront. It does not teach the '
            'pattern again. It shows what Spring does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['One thing is new: Spring Boot.', '', 'Spring creates the objects of an', 'application and wires them together.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first annotation, one new thing. Spring is a '
            'framework whose core is a container. It creates the objects '
            'of an application and wires them together. Spring Boot '
            'configures it with sensible defaults. [[slnc 300]] And a '
            'promise: skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it, and writes a container.'
        ),
    ),
    dict(
        key='04-annotation', kind='bullets', title='One Annotation Per Class',
        body=['@Component on each class.', '', 'That is the only change to the', "partner's classes.", '', 'The constructors are untouched.'],
        narration=(
            "The only change to the partner's classes is one annotation "
            'on each: at component. It says, Spring should create this '
            'one. The constructors are untouched. Not a line of the logic '
            'changed.'
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
            'Here is the moment. The wiring class from the last video is '
            'gone. Spring built the graph from the constructors. [[slnc '
            '300]] The same order is charged: nine thousand pence. The '
            'same three messages are sent. Exactly as by hand.'
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
            'Seven classes, seven annotations. Spring built the auditor, '
            'the checkout service, the loyalty policy, the printer, the '
            'gateway, the notifier, and the storefront. [[slnc 300]] One '
            'annotation per class replaced one line of new. The '
            'constructor parameters tell Spring the rest, exactly as they '
            'told the container from the last video.'
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
            "Now Spring's own failures, which are the real ones. Leave "
            'the notifier out. The context refuses to start. Unsatisfied '
            'dependency exception. Error creating bean checkout service: '
            'constructor parameter two. [[slnc 300]] It is the same '
            'failure the hand-written container gave. And better than a '
            "service locator's, which failed on the first order, after "
            'the money moved. It fails at start-up. It is still not at '
            'compile time.'
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
            'A circular dependency. A chicken needs an egg, and the egg '
            'needs the chicken. Spring refuses, at start-up: bean '
            'currently in creation exception. Since Spring six, that is '
            'the default. [[slnc 300]] A cycle is usually a design '
            'signal, not a wiring problem.'
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
            'Field injection: at autowired, on private fields. Spring can '
            'fill them. Nothing else can. New field injected checkout '
            'compiles, and placing an order throws a null pointer '
            'exception. Inside Spring it works. [[slnc 300]] So it cannot '
            'be built validly in a test without Spring, or reflection. '
            "Spring's own guidance is constructor injection, for exactly "
            'that reason.'
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
            'What does the magic cost? Building the graph by hand takes '
            'hundreds of nanoseconds. A Spring context takes a few '
            'milliseconds, once, at start-up. It grows with the size of '
            'the application. Timings vary by machine. [[slnc 300]] There '
            'is a second cost, harder to measure: objects now come from '
            'somewhere that is not in your code.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Unchanged:', 'constructor injection,', 'by hand until the wiring hurts,', 'then a container.', '', 'Spring did not add the idea.', 'It removed the typing.'],
        narration=(
            'The verdict is unchanged. Constructor injection. By hand '
            'until the wiring hurts. Then a container. [[slnc 300]] '
            'Spring did not add the idea. It removed the typing.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['In every Spring Boot application.', '', 'This is where the annotations you', 'copy from tutorials come from.'],
        narration=(
            'You have met this in every Spring Boot application. This is '
            'where the annotations you copy from tutorials come from. Now '
            'you know what each one replaced.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. No web '
            'server, no database, and no web starter. Just the container.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's container", 'and its error messages.', '', 'The timings are measured, and vary.'],
        narration=(
            'The same honest admission as everywhere in this course, and '
            "short. Everything is real: Spring's container, and its error "
            'messages. The timings are measured, and vary by machine.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Delete component from the notifier', 'and read the new error.'],
        narration=(
            "That's Dependency Injection with Spring. [[slnc 250]] If you "
            'take one sentence away, take this one: Spring did not add '
            'the idea, it removed the typing. [[slnc 350]] The full '
            'source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository. [[slnc 300]] If you '
            'try one exercise, delete the component annotation from the '
            'notifier, and read the new error. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
