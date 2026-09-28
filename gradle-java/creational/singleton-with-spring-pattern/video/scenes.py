"""Scene definitions for the Singleton with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Singleton with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Singleton pattern, in Java, using Spring Boot. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] The Singleton '
            'pattern makes sure there is exactly one instance of a class, '
            'shared by everyone. [[slnc 500]] In Spring, singleton is a '
            'scope. [[slnc 300]] The container keeps one instance, and '
            'hands it to everyone who asks. [[slnc 600]] Think of a '
            'shared office printer. [[slnc 300]] Everyone on the floor '
            'sends their pages to the same machine. [[slnc 700]] This is '
            'the framework version of the Singleton video, with the same '
            'order number generator. [[slnc 400]] We will share the '
            'generator as a Spring bean, between three callers. [[slnc '
            '300]] Then we will hear how the guarantee weakens. [[slnc '
            '300]] A plain new, a second container, a changed scope, and '
            'a counter that is not thread-safe.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Singleton, the hand-built video,', 'shares one order number sequencer', 'between checkout, admin and retry.', '', 'It closed reflection and', 'serialization with an enum.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Singleton video. [[slnc 400]] That '
            'one shares one order number generator between checkout, the '
            'admin console, and a retry job. [[slnc 300]] And it closes '
            'the reflection and serialization tricks, using an enum. '
            '[[slnc 500]] If you are new to the pattern, watch that one '
            'first. [[slnc 400]] Here, we ask what Spring Boot does with '
            'the same idea.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'Spring keeps one instance of a', 'bean per container.', '', 'No private constructor, no static', 'field.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'One thing is new in this project: Spring Boot. [[slnc 400]] '
            'At its heart, Spring is a container that creates your '
            'objects, and hands them out. [[slnc 300]] By default, it '
            'keeps one instance of each bean, per container. [[slnc 500]] '
            'And one promise. [[slnc 300]] If you skip this video, you '
            'lose none of the pattern. [[slnc 300]] This one is about the '
            'tool.'
        ),
    ),
    dict(
        key='04-one', kind='console', title='One Bean, Shared',
        body="""ONE. One bean.
  checkout, admin, retry hold
  the same generator: true

  ORD-000001
  ORD-000002
  ORD-000003""",
        narration=(
            'First demo: one bean, shared. [[slnc 400]] Checkout, the '
            'admin console, and the retry job are each given a generator '
            'by the container. [[slnc 300]] And it is the very same '
            'object. [[slnc 500]] The order numbers run one, two, three, '
            'across all three callers. [[slnc 500]] Notice what is '
            'missing. [[slnc 300]] No private constructor. [[slnc 300]] '
            'No static field. [[slnc 300]] Spring did the sharing.'
        ),
    ),
    dict(
        key='05-new', kind='console', title='Nothing Stops new',
        body="""TWO. Nothing stops new.
  managed says ORD-000001
  a plain new says ORD-000001

  same object: false.
  the constructor is public.""",
        narration=(
            'Second demo: nothing stops a plain new. [[slnc 400]] The '
            "generator's constructor is public, because Spring needs it "
            'that way. [[slnc 300]] So anyone can create a second '
            'generator. [[slnc 300]] And it starts again at order one. '
            '[[slnc 500]] The hand-built enum singleton made this '
            'impossible. [[slnc 300]] Here, it is only a convention.'
        ),
    ),
    dict(
        key='06-containers', kind='console', title='One Per Container',
        body="""THREE. One per container.
  context A issues ORD-000001
  context B issues ORD-000001

  the same order number went
  to two customers: true""",
        narration=(
            'Third demo: singleton means one per container. [[slnc 400]] '
            'Start the application twice, inside one program. [[slnc '
            '300]] Each container has its own generator. [[slnc 500]] '
            'Container A issues order one. [[slnc 300]] Container B also '
            'issues order one. [[slnc 300]] The same order number goes to '
            'two customers. [[slnc 500]] An enum could never do that.'
        ),
    ),
    dict(
        key='07-scope', kind='console', title='A Scope Change',
        body="""FOUR. A scope change.
  with scope prototype:
  checkout: ORD-000001
  admin:    ORD-000001

  one word changed.""",
        narration=(
            'Fourth demo: a scope change. [[slnc 400]] Change one word in '
            'the bean definition, from singleton to prototype. [[slnc '
            '300]] Now each caller gets its own generator. [[slnc 500]] '
            'Checkout says order one. [[slnc 300]] The admin console also '
            'says order one. [[slnc 500]] Nothing fails, and the compiler '
            'says nothing. [[slnc 300]] The only sign is duplicate order '
            'numbers, in production.'
        ),
    ),
    dict(
        key='08-built', kind='console', title='When Is It Built?',
        body="""FIVE. When is it built?
  eager: built 1 at startup.
  lazy: built 0 after startup,
  built 1 after the first
  caller.""",
        narration=(
            'Fifth demo: when is the singleton created? [[slnc 400]] By '
            'default, at startup, before any caller asks. [[slnc 300]] '
            'The count of generators built is one. [[slnc 500]] With lazy '
            'creation switched on, the count is zero after startup. '
            '[[slnc 300]] And one after the first caller arrives. [[slnc '
            '500]] Eager creation finds a broken constructor at startup. '
            '[[slnc 300]] Lazy creation finds it in front of a customer.'
        ),
    ),
    dict(
        key='09-threads', kind='console', title='Shared Means Shared By Threads',
        body="""SIX. Threads.
  a plain long, held between
  read and write:
  ORD-000001 and ORD-000001

  an AtomicLong, 4 x 2500:
  10000 distinct numbers.""",
        narration=(
            'Last demo: shared means shared by threads. [[slnc 400]] A '
            'singleton is used by every thread, and Spring does not '
            'protect its fields. [[slnc 500]] With a plain number as the '
            'counter, two threads both read the same value. [[slnc 300]] '
            'So two customers both get order number one. [[slnc 500]] '
            'With an Atomic Long, four threads request two thousand five '
            'hundred numbers each. [[slnc 300]] And they get ten thousand '
            'different numbers. [[slnc 500]] Spring shares the bean. '
            '[[slnc 300]] Keeping its data safe is still your job.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Let the container own the instance.', '', 'Keep its state thread-safe.', '', 'Run only one container.', '', 'Use an enum when no container', 'is around.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Let the container own '
            'the single instance. [[slnc 300]] Keep the data inside it '
            'thread-safe. [[slnc 300]] Make sure only one container runs. '
            '[[slnc 300]] And use the enum singleton when there is no '
            'container around.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['No private constructor, no', 'getInstance, injected by constructor.', '', '@Component or @Service with no scope', 'named.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a class with no private constructor, and no '
            'get instance method, passed in through a constructor. [[slnc '
            '300]] And a component or service with no scope named. [[slnc '
            '300]] Because the default scope is singleton.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Service and @Repository', 'you have written.', '', 'The default scope is singleton.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In every '
            'service and repository class you have written. [[slnc 300]] '
            'The default scope is singleton, so most of them already are.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] No web server, '
            'no database, and no web library.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's", 'containers and scopes.', '', 'The thread collision is forced with', 'a gate, so it happens every time.'],
        narration=(
            "A quick, honest note about this demo. [[slnc 300]] Spring's "
            'containers and scopes are real. [[slnc 300]] The thread '
            'collision is forced with a gate, so it happens every time.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a class with no state, it hardly', 'matters.', '', 'It bites when the bean holds a', 'counter, a cache or a connection.'],
        narration=(
            'So, when does this matter? [[slnc 400]] For a class that '
            'holds no data, it hardly matters. [[slnc 300]] It bites when '
            'the bean holds a counter, a cache, or a connection.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Make the constructor private', 'and see what Spring says.'],
        narration=(
            "That's Singleton with Spring. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A Spring '
            'singleton is one per container, and only as safe as the data '
            'inside it. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            "300]] Make the generator's constructor private. [[slnc 300]] "
            'Then see what Spring does. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
