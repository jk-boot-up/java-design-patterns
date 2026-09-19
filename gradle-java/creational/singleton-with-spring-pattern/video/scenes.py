"""Scene definitions for the Singleton with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Singleton with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Singleton '
            'pattern with Spring Boot, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Singleton video. That one built an '
            'order number sequencer that checkout, the admin console and '
            'a retry job all share, and closed the reflection and '
            'serialization holes with a single element enum. This one '
            'shows the same idea inside Spring Boot. [[slnc 350]] The '
            'plain definition, in short: in Spring, a singleton is a '
            'scope. The container keeps one instance, and hands it to '
            'everyone who asks. [[slnc 300]] By the end you will see the '
            'same sequencer as a Spring bean shared by three callers, '
            'then see how the guarantee weakens: a plain new, a second '
            'container, a changed scope, and a thread-unsafe counter.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Singleton, the hand-built video,', 'shares one order number sequencer', 'between checkout, admin and retry.', '', 'It closed reflection and', 'serialization with an enum.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Singleton video. If you have not seen '
            'it, start there. It shares one order number sequencer '
            'between checkout, the admin console and a retry job, and '
            'closes the reflection and serialization holes with an enum. '
            '[[slnc 300]] This one uses the same example. It does not '
            'teach the pattern again. It shows what Spring Boot does with '
            'it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'Spring keeps one instance of a', 'bean per container.', '', 'No private constructor, no static', 'field.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'is a framework whose core is a container that creates your '
            'objects and hands them out. By default it keeps one instance '
            'of each bean, per container. [[slnc 300]] And a promise: '
            'skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it.'
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
            'First, the good news. Checkout, the admin console and the '
            'retry job are each handed a generator by the container, and '
            'it is the same object. The numbers run one, two, three '
            'across all three callers. [[slnc 300]] Notice what is '
            'missing. No private constructor. No static field. Spring did '
            'the sharing.'
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
            'Second, nothing stops a plain new. The constructor is '
            'public, because Spring wants it that way. So anyone can '
            'build a second generator, and it starts again at order one. '
            '[[slnc 300]] The hand-built singleton made this impossible. '
            'Here it is only a convention.'
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
            'Third, the word singleton is per container. Start the '
            'application twice in one program, and each container has its '
            'own generator. Context A issues order one. Context B issues '
            'order one. [[slnc 300]] The same order number goes to two '
            'customers. An enum could not do that.'
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
            'Fourth, a scope change. Change one word in the bean '
            'definition, singleton to prototype, and each caller is '
            'handed its own generator. Checkout says order one. Admin '
            'says order one. [[slnc 300]] Nothing fails. The compiler is '
            'silent. The only sign is duplicate numbers in production.'
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
            'Fifth, when is it built. By default, at startup, before any '
            'caller asks. The count is one. With lazy initialization, the '
            'count is zero after startup, and one after the first caller. '
            '[[slnc 300]] Eager finds a broken constructor at startup. '
            'Lazy finds it in front of a customer.'
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
            'Last, threads. A singleton is shared by every thread, and '
            'Spring does not protect its fields. A plain long, held '
            'between the read and the write, gives two customers the same '
            'number. [[slnc 300]] An atomic long, hit by four threads, '
            'gives ten thousand distinct numbers. Spring shares the bean. '
            'Keeping its state safe is still your job.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Let the container own the instance.', '', 'Keep its state thread-safe.', '', 'Run only one container.', '', 'Use an enum when no container', 'is around.'],
        narration=(
            'My verdict, plainly. Let the container own the single '
            'instance. Keep the state inside it thread safe. Make sure '
            'only one container runs. And use the enum when no container '
            'is around.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['No private constructor, no', 'getInstance, injected by constructor.', '', '@Component or @Service with no scope', 'named.'],
        narration=(
            'How do you recognise this in code you did not write? A class '
            'with no private constructor and no getInstance method, '
            'passed in through a constructor. A component or service with '
            'no scope named, because the default is singleton.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Service and @Repository', 'you have written.', '', 'The default scope is singleton.'],
        narration=(
            'You have met this in every service and repository you have '
            'written. The default scope is singleton, so most of them '
            'already are.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. No web '
            'server, no database, and no web starter.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's", 'containers and scopes.', '', 'The thread collision is forced with', 'a gate, so it happens every time.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            "Everything is real: Spring's containers and scopes. The "
            'thread collision is forced with a gate, so it happens every '
            'time.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a class with no state, it hardly', 'matters.', '', 'It bites when the bean holds a', 'counter, a cache or a connection.'],
        narration=(
            'So when is it too much? For a class with no state, the '
            'question hardly matters. It bites when the bean holds a '
            'counter, a cache or a connection.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Make the constructor private', 'and see what Spring says.'],
        narration=(
            "That's Singleton with Spring. [[slnc 250]] If you take one "
            'sentence away, take this one: a Spring singleton is one per '
            'container, and only as safe as the state inside it. [[slnc '
            '350]] The full source, the written notes, the diagrams and '
            'an animated walkthrough are all in the repository. [[slnc '
            '300]] If you try one exercise, make the constructor private, '
            'and see what Spring does. [[slnc 300]] If this helped, a '
            'like genuinely does help other people find it, and subscribe '
            'if you would like the rest of the series. [[slnc 250]] '
            'Thanks for watching.'
        ),
    ),
]
