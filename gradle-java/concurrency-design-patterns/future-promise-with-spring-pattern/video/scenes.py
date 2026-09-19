"""Scene definitions for the Future/Promise with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Future/Promise with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Future/Promise '
            'pattern with Spring Boot, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Future/Promise video. That one '
            'built the future and promise handoff by hand, and showed '
            'three costs: an exception that surfaces later, a get with no '
            'timeout that is a hang, and a cancellation a task can '
            'ignore. This one shows the same idea inside Spring Boot. '
            '[[slnc 350]] The plain definition, in short: each piece of '
            'work is submitted and immediately returns a handle to a '
            'result that does not exist yet, so independent work can run '
            'at once. [[slnc 300]] By the end you will see that the pool, '
            'not the annotation, decides how concurrent a page is, watch '
            'an exception vanish from a void method, lose a thread-local '
            'across the thread boundary, and learn why a timeout and a '
            'cancel both leave the work running.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Future/Promise, the hand-built video,', 'built the handoff and showed three', 'costs: an exception that moves, a get', 'that hangs, a cancel that is a request.', '', 'This one uses the same product page:', 'price, stock and a review score.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Future/Promise video. If you have not '
            'seen it, start there. It builds the future and promise '
            'handoff by hand, and shows three costs: an exception that '
            'surfaces later, a get with no timeout that is a hang, and a '
            'cancellation a task can ignore. [[slnc 300]] This one uses '
            'the same example. It does not teach the pattern again. It '
            'shows what Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'Its @Async annotation runs a method on', 'a pool, and hands back a future that', 'the container completes.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'is a framework whose core is a container that creates your '
            'objects. Its async annotation runs a method on a thread pool '
            'it owns, and hands back a completable future, which the '
            'container completes when the method returns. [[slnc 300]] '
            'And a promise: skipping this video loses none of the '
            'pattern. The hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-pool', kind='console', title='The Pool Decides',
        body="""ONE. The pool decides.
  three independent lookups.

  default pool: 3 in flight
  at the same moment.

  a pool of one thread: 1.

  the annotation asked.
  the pool decided.""",
        narration=(
            'First, concurrency. Three independent lookups, price, stock '
            'and rating, each marked async. On the default pool, all '
            'three are in flight at the same moment. Three. On a pool of '
            'one thread, only one is. [[slnc 300]] The annotation asked '
            'for concurrency. The pool decided whether to give it. '
            'Concurrency is a property of the pool, not of the '
            'annotation.'
        ),
    ),
    dict(
        key='05-exceptions', kind='console', title='Exceptions',
        body="""TWO. Exceptions.
  returns a future: the caller
  sees CompletionException,
  cause: review service is down.

  a void method threw:
  the caller got nothing.

  it went only to a handler
  you had to register.""",
        narration=(
            'Second, exceptions. A method returning a future fails, and '
            'the caller sees a completion exception, with the real cause '
            'inside it. The stack trace belongs to a pool thread. The '
            'calling method appears nowhere in it. [[slnc 300]] Now a '
            'void method that throws. The caller gets nothing. The call '
            'returned normally. The exception went only to a handler that '
            'you have to register by hand. Without one, it is just '
            'logged. That is why the rule is: return a future, never '
            'void.'
        ),
    ),
    dict(
        key='06-context', kind='console', title='Thread-Locals',
        body="""THREE. Thread-locals.
  the caller works for
  customer 7.

  the async method asks whose
  order it is: customer null.

  with a TaskDecorator that
  copies it across:
  customer 7.""",
        narration=(
            'Third, context. The caller is working for customer seven. '
            'That is held in a thread-local, the way request context, '
            'security context, and logging context all are. The async '
            'method asks whose order it is. Customer null. [[slnc 300]] A '
            'thread-local does not cross to a pool thread. The fix is a '
            'task decorator, a small bean that copies it across. With it: '
            'customer seven. The fix is yours to write.'
        ),
    ),
    dict(
        key='07-timeout', kind='console', title='A Timeout Does Not Stop It',
        body="""FOUR. A timeout.
  the caller waited 200ms:
  TimeoutException.

  the task had not finished
  when the caller gave up.

  it ran to the end anyway.
  nobody was waiting.""",
        narration=(
            'Fourth, a timeout. The caller waits two hundred milliseconds '
            'for a slow task, and gets a timeout exception. The task had '
            'not finished. [[slnc 300]] Then the gate opens, and the task '
            'runs to the end anyway, and does its work. Nobody is waiting '
            'for the answer. A timeout is the caller giving up. It does '
            'not stop the work.'
        ),
    ),
    dict(
        key='08-cancel', kind='console', title='cancel(true) Interrupts Nothing',
        body="""FIVE. cancel(true).
  reported: true.
  isCancelled: true.

  the task ran to completion
  anyway.

  the flag was set on the
  future. the thread was never
  told.""",
        narration=(
            'Fifth, cancellation. Cancel true reports true. The future '
            'says it is cancelled. And the task ran to completion anyway. '
            '[[slnc 300]] On a completable future, cancel sets a flag on '
            'the future. It never interrupts the thread. The hand-built '
            'video showed a task that ignored an interrupt. Here, no '
            'interrupt is even sent.'
        ),
    ),
    dict(
        key='09-compose', kind='console', title='Composing The Page',
        body="""SIX. Composing.
  three futures, combined:
  price 129.99, stock 7,
  rating 4.6

  review service down, with a
  fallback at that step:
  rating unavailable.

  no fallback: the whole page
  fails.""",
        narration=(
            'Last, composing the page. Three futures combine into one, '
            'with no blocking until the very end. [[slnc 300]] Now the '
            'review service is down. With a fallback chosen at that one '
            'step, the page still assembles: rating unavailable. Without '
            'the fallback, one failing lookup fails the whole page. That '
            'is the callback depth cost from the hand-built video, in a '
            'real library.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Return a CompletableFuture, never void.', 'Choose the pool.', 'Carry the context on purpose.', 'A timeout is giving up, not stopping.', '', 'Design tasks that check for', 'cancellation themselves.'],
        narration=(
            'My verdict, plainly. Return a completable future, never '
            'void. Choose the pool. Carry the context across on purpose. '
            'A timeout is the caller giving up, not the work stopping. '
            'And design tasks that check for cancellation themselves.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Async returning CompletableFuture.', 'thenCombine, exceptionally, orTimeout.', 'A TaskDecorator bean.', 'MDC or SecurityContext copied by hand.'],
        narration=(
            'How do you recognise this in code you did not write? Async '
            'on a method returning a completable future. Chains of then '
            'combine, exceptionally, and or timeout. A task decorator '
            'bean. And logging or security context copied by hand across '
            'a thread.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Async method that returns a', 'CompletableFuture.', '', 'And every log line that lost its request', 'id on the way to a pool thread.'],
        narration=(
            'You have met this in every async method that returns a '
            'completable future, and in every log line that lost its '
            'request identifier on the way to a pool thread.'
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
        body=["Everything is real: Spring's executor,", 'its futures and its handlers.', '', 'Every wait is a latch, a gate,', 'or a bounded spin.'],
        narration=(
            'The same honest admission as everywhere in this course, and '
            "short. Everything is real: Spring's executor, its futures, "
            'and its handlers. Every wait is a latch, a gate, or a '
            'bounded spin, so every result is the same each run.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['Two lookups that are already fast,', 'or where the second needs the', 'first: a future is ceremony.'],
        narration=(
            'So when is it too much? For two lookups that are already '
            "fast, or where the second needs the first's result, a future "
            'around work that never overlaps is ceremony.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Make the slow task check for', 'interruption, and cancel it properly.'],
        narration=(
            "That's Future/Promise with Spring. [[slnc 250]] If you take "
            'one sentence away, take this one: a future is a promise '
            'about when a value will be ready, never a promise that the '
            'work can be stopped. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository. [[slnc 300]] If you try one exercise, '
            'make the slow task check for interruption in a loop, and '
            "cancel it through an executor's future, and see the "
            'difference. [[slnc 300]] If this helped, a like genuinely '
            'does help other people find it, and subscribe if you would '
            'like the rest of the series. [[slnc 250]] Thanks for '
            'watching.'
        ),
    ),
]
