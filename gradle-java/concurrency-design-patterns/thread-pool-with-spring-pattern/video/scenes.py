"""Scene definitions for the Thread Pool with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Thread Pool with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Thread Pool pattern, in Java, using Spring Boot. [[slnc '
            '300]] This video is presented by Jayasekhar Konduru. [[slnc '
            '600]] First, a simple definition. [[slnc 300]] A thread pool '
            'runs work on a small set of threads that are created once, '
            'and reused. [[slnc 300]] So a burst of work cannot create a '
            'burst of threads. [[slnc 600]] Think of a restaurant with a '
            'fixed team of waiters. [[slnc 300]] A rush of customers does '
            'not hire new waiters on the spot. [[slnc 300]] The customers '
            'wait for a free one. [[slnc 700]] This is the framework '
            'version of the Thread Pool video, with the same order '
            'packing. [[slnc 500]] We will hear the pool Spring Boot '
            'gives you when you configure nothing, and watch its queue '
            'grow without limit. [[slnc 300]] Then we will limit it, and '
            'hear a real refusal. [[slnc 300]] And we will meet two '
            'failures that belong to Spring: an annotation that silently '
            'does nothing, and a pool that starves itself.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Thread Pool, the hand-built video,', 'built a bounded pool around a', 'ThreadPoolExecutor.', '', 'It showed: an unbounded queue is a', 'trap, a refusal needs a decision,', 'and a pool can starve itself.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Thread Pool video. [[slnc 400]] That '
            'one builds a limited pool by hand. [[slnc 300]] And it shows '
            'three costs: a queue with no limit is a trap, a refusal '
            'needs a decision, and a pool can starve itself. [[slnc 500]] '
            'If you are new to the pattern, watch that one first. [[slnc '
            '400]] Here, we ask what Spring Boot does with the same idea.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'Its @Async annotation sends a method', 'to a thread pool it creates and owns.', '', "The pool's size and queue are settings.", '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'One thing is new in this project: Spring Boot. [[slnc 400]] '
            'At its heart, Spring is a container that creates and '
            'connects your objects. [[slnc 500]] Its at Async annotation '
            'sends a method to a thread pool that Spring creates and '
            "owns. [[slnc 300]] The pool's size and queue are just "
            'settings. [[slnc 500]] And one promise. [[slnc 300]] If you '
            'skip this video, you lose none of the pattern. [[slnc 300]] '
            'This one is about the tool.'
        ),
    ),
    dict(
        key='04-defaults', kind='console', title='What You Get By Default',
        body="""ONE. The defaults.
  @EnableAsync, no settings.

  core threads 8
  max threads 2147483647
  queue capacity 2147483647

  eight workers, and a queue
  with no bound.""",
        narration=(
            'First demo: what you get by default. [[slnc 400]] Add the '
            'enable async annotation, and no settings at all. [[slnc '
            '300]] What pool do you get? [[slnc 500]] Eight core threads. '
            '[[slnc 300]] A maximum of more than two billion threads. '
            '[[slnc 300]] And a queue that holds more than two billion '
            'tasks. [[slnc 500]] In practice, that is eight workers, and '
            'a queue with no limit. [[slnc 300]] The trap from the '
            "hand-built video is not someone's mistake here. [[slnc 300]] "
            'It is the default.'
        ),
    ),
    dict(
        key='05-async', kind='console', title='@Async Moves The Work',
        body="""TWO. @Async.
  the caller is thread main.
  the work ran on task-1.

  one annotation replaced the
  partner's BoundedPackingPool
  class.""",
        narration=(
            'Second demo: at Async moves the work. [[slnc 400]] We call '
            'the packing method, which is marked at Async. [[slnc 300]] '
            'The caller is the main thread. [[slnc 300]] The work runs on '
            'a different thread, called task one. [[slnc 500]] One '
            'annotation replaced the whole hand-written pool class from '
            'the other video.'
        ),
    ),
    dict(
        key='06-backlog', kind='console', title='The Unbounded Queue',
        body="""THREE. The backlog.
  all 8 workers stuck.
  1000 more orders arrive.

  waiting in the queue: 1000
  rejected: 0

  nobody was told.""",
        narration=(
            'Third demo: the queue with no limit. [[slnc 400]] All eight '
            'workers are made busy, held on a slow step. [[slnc 300]] '
            'Then a thousand more orders arrive. [[slnc 500]] All one '
            'thousand wait in the queue. [[slnc 300]] How many were '
            'refused? [[slnc 300]] Zero. [[slnc 300]] Nobody was told '
            'anything. [[slnc 500]] Submitting never waits, and never '
            'refuses. [[slnc 300]] So the backlog just grows, until the '
            'application runs out of memory.'
        ),
    ),
    dict(
        key='07-bounded', kind='console', title='Bound It',
        body="""FOUR. Bound it.
  2 threads, a queue of 3.
  2 running, 3 waiting.

  the sixth order:
  TaskRejectedException,
  thrown at once.

  a decision, not a silence.""",
        narration=(
            'Fourth demo: add a limit. [[slnc 400]] Three settings: two '
            'threads, and a queue that holds three. [[slnc 500]] Two '
            'orders are running. [[slnc 300]] Three are waiting. [[slnc '
            '300]] Then a sixth order arrives. [[slnc 500]] It is refused '
            'at once, with a Task Rejected exception. [[slnc 300]] That '
            'is a decision. [[slnc 300]] The caller learns that the pool '
            'is full, instead of a queue growing in silence.'
        ),
    ),
    dict(
        key='08-this', kind='console', title='The Annotation That Does Nothing',
        body="""FIVE. A call on this.
  packThroughThis() called
  pack(), which is @Async.

  it ran on main, the caller's
  own thread.

  nothing complained.""",
        narration=(
            'Fifth demo: the annotation that does nothing. [[slnc 400]] '
            'One method calls the at Async packing method on the same '
            'object, directly, through this. [[slnc 500]] The packing ran '
            "on the main thread, the caller's own thread. [[slnc 300]] "
            'Not on the pool. [[slnc 300]] And nothing complained. [[slnc '
            '500]] At Async works through a proxy that Spring wraps '
            'around the object. [[slnc 300]] A call on this skips the '
            'proxy completely.'
        ),
    ),
    dict(
        key='09-starve', kind='console', title='Pool Starvation',
        body="""SIX. Starvation.
  one thread.
  the packing task asks the pool
  to print a label, and waits.

  starved: the label task never
  got a thread.""",
        narration=(
            'Last demo: pool starvation. [[slnc 400]] The pool has one '
            'thread. [[slnc 300]] The packing task asks the same pool to '
            'print a label, and waits for the answer. [[slnc 500]] But '
            'the label task is queued behind the packing task. [[slnc '
            '300]] And the packing task is waiting for the label. [[slnc '
            '300]] So the label task never gets a thread. [[slnc 500]] '
            'The demo is rescued by a timeout, so it can tell you what '
            'happened. [[slnc 300]] It is the same deadlock as in the '
            'hand-built video.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Set the pool explicitly.', 'Bound the queue.', 'Decide what a refusal means.', 'Never wait on your own pool.', '', 'Do not rely on the default executor', 'for anything that can back up.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Configure the pool '
            'yourself. [[slnc 300]] Put a limit on the queue. [[slnc '
            '300]] Decide what a refusal should mean. [[slnc 300]] Never '
            'make a task wait on its own pool. [[slnc 300]] And do not '
            'rely on the default pool for any work that can pile up.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@EnableAsync and @Async methods.', 'spring.task.execution.pool.* settings.', 'TaskRejectedException in a trace.', 'A CompletableFuture from a service.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for the enable async annotation, and methods '
            'marked at Async. [[slnc 300]] Look for settings starting '
            'with spring dot task dot execution dot pool. [[slnc 300]] '
            'Look for a Task Rejected exception in an error report. '
            '[[slnc 300]] And a service method that returns a Completable '
            'Future.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Async method.', '', "Spring Boot's applicationTaskExecutor.", '', 'Scheduled tasks, and async event', 'listeners, use the same kind of pool.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In every at '
            "Async method, and in Spring Boot's application task "
            'executor. [[slnc 300]] Scheduled tasks and asynchronous '
            'event listeners use the same kind of pool.'
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
        body=["Everything is real: Spring's executor,", 'its defaults, and its exceptions.', '', 'Every wait is a latch or a gate,', 'so every count is the same each run.'],
        narration=(
            "A quick, honest note about this demo. [[slnc 300]] Spring's "
            'thread pool, its defaults, and its errors are all real. '
            '[[slnc 300]] Every wait uses a latch or a gate, so every '
            'count is the same on every run.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For work that is already fast, or', 'must finish before the caller', 'continues, a pool is only overhead.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For work that is '
            'already fast, or work that must finish before the caller '
            'continues, a thread pool is only overhead.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Turn on virtual threads and', 'see what the pool becomes.'],
        narration=(
            "That's Thread Pool with Spring. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A thread pool '
            'you did not configure has a queue that never says no. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Turn on virtual '
            'threads in the settings. [[slnc 300]] Print whether the work '
            'now runs on one. [[slnc 300]] And think about what the pool '
            'has become. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
