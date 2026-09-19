"""Scene definitions for the Thread Pool with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Thread Pool with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Thread Pool '
            'pattern with Spring Boot, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Thread Pool video. That one built a '
            'bounded thread pool by hand, and showed its costs: an '
            'unbounded queue is a trap, a refusal needs a decision, and a '
            'pool can starve itself. This one shows the same idea inside '
            'Spring Boot. [[slnc 350]] The plain definition, in short: '
            'run work on a small set of threads that are created once and '
            'reused, so a burst of work cannot create a burst of threads. '
            '[[slnc 300]] By the end you will see the pool Spring Boot '
            'gives you when you configure nothing, watch its queue grow '
            'without a bound, bound it and read the real refusal, and '
            'meet two failures that belong to Spring: an annotation that '
            'silently does nothing, and a pool that starves itself.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Thread Pool, the hand-built video,', 'built a bounded pool around a', 'ThreadPoolExecutor.', '', 'It showed: an unbounded queue is a', 'trap, a refusal needs a decision,', 'and a pool can starve itself.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Thread Pool video. If you have not '
            'seen it, start there. It builds a bounded pool by hand, and '
            'shows three costs: an unbounded queue is a trap, a refusal '
            'needs a decision, and a pool can starve itself. [[slnc 300]] '
            'This one uses the same example. It does not teach the '
            'pattern again. It shows what Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'Its @Async annotation sends a method', 'to a thread pool it creates and owns.', '', "The pool's size and queue are settings.", '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'is a framework whose core is a container that creates and '
            'wires your objects. Its async annotation sends a method to a '
            "thread pool it creates and owns, and the pool's size and "
            'queue are settings. [[slnc 300]] And a promise: skipping '
            'this video loses none of the pattern. The hand-built one '
            'teaches all of it.'
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
            'Start with no settings at all. Add the enable async '
            'annotation, and nothing else. What pool do you get? A thread '
            'pool task executor. Core threads: eight. Max threads: two '
            'billion, one hundred and forty-seven million. Queue '
            'capacity: the same number. [[slnc 300]] Eight workers, and a '
            "queue with no bound. That is the partner video's unbounded "
            'queue trap, and here it is not a mistake somebody made. It '
            'is the default.'
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
            'Now the annotation. Call the packing method, marked async. '
            'The caller is the main thread. The work ran on a thread '
            'called task one. A different thread. [[slnc 300]] One '
            'annotation replaced the whole hand-written pool class from '
            'the last video.'
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
            'Now make the workers busy. All eight are stuck on a slow '
            'step, held at a gate. A thousand more orders arrive. [[slnc '
            '300]] All thousand wait in the queue. Rejected: zero. Nobody '
            'was told. Submitting never blocks and never refuses, so the '
            'backlog just grows, until it is a heap dump instead of a '
            'decision.'
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
            'Now bound it, with three settings: two threads, and a queue '
            'of three. Two orders are running, and three are waiting. '
            '[[slnc 300]] The sixth order: a task rejected exception, '
            'thrown to the caller, at once. That is a decision. The '
            'caller learns the pool is full, instead of a queue growing '
            'in silence.'
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
            "A failure that is Spring's own. One method calls another "
            'async method, on the same object, through this. It ran on '
            "main, the caller's own thread. [[slnc 300]] Async works "
            'through a proxy, exactly as the transactional annotation '
            'does. A call on this skips the proxy, and nothing complains.'
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
            'Last failure. One thread. The packing task asks the same '
            'pool to print a label, and waits for the answer. [[slnc '
            '300]] The label task is queued behind the packing task, '
            'which is waiting for it. It starves. This demo is rescued by '
            'a timeout, so it can tell you. The same deadlock as the '
            'hand-built video.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Set the pool explicitly.', 'Bound the queue.', 'Decide what a refusal means.', 'Never wait on your own pool.', '', 'Do not rely on the default executor', 'for anything that can back up.'],
        narration=(
            'My verdict, plainly. Set the pool explicitly. Bound the '
            'queue. Decide what a refusal means. And never wait on your '
            'own pool. Do not rely on the default executor for anything '
            'that can back up.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@EnableAsync and @Async methods.', 'spring.task.execution.pool.* settings.', 'TaskRejectedException in a trace.', 'A CompletableFuture from a service.'],
        narration=(
            'How do you recognise this in code you did not write? Enable '
            'async, and methods marked async. Settings that begin spring '
            'dot task dot execution dot pool. A task rejected exception '
            'in a stack trace. And a service method that returns a '
            'completable future.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Async method.', '', "Spring Boot's applicationTaskExecutor.", '', 'Scheduled tasks, and async event', 'listeners, use the same kind of pool.'],
        narration=(
            'You have met this in every async method, and in Spring '
            "Boot's application task executor. Scheduled tasks and "
            'asynchronous event listeners use the same kind of pool.'
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
        body=["Everything is real: Spring's executor,", 'its defaults, and its exceptions.', '', 'Every wait is a latch or a gate,', 'so every count is the same each run.'],
        narration=(
            'The same honest admission as everywhere in this course, and '
            "short. Everything is real: Spring's executor, its defaults, "
            'and its exceptions. Every wait is a latch or a gate, so '
            'every count is the same on every run.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For work that is already fast, or', 'must finish before the caller', 'continues, a pool is only overhead.'],
        narration=(
            'So when is it too much? For work that is already fast, or '
            'that must finish before the caller continues, a thread pool '
            'is only overhead.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Turn on virtual threads and', 'see what the pool becomes.'],
        narration=(
            "That's Thread Pool with Spring. [[slnc 250]] If you take one "
            'sentence away, take this one: a thread pool you did not '
            'configure is a thread pool with a queue that never says no. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, turn on '
            'virtual threads, and print whether the work runs on one, and '
            'think about what the pool became. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
