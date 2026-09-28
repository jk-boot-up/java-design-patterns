"""Scene definitions for the Future/Promise with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Future/Promise with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Future and Promise pattern, in Java, using Spring Boot. '
            '[[slnc 300]] This video is presented by Jayasekhar Konduru. '
            '[[slnc 600]] First, a simple definition. [[slnc 300]] When '
            'you start a piece of work, you immediately get back a handle '
            'to a result that does not exist yet. [[slnc 300]] So '
            'independent pieces of work can run at the same time. [[slnc '
            '600]] Think of dropping clothes at a dry cleaner. [[slnc '
            '300]] You get a ticket straight away, and collect the '
            'clothes later. [[slnc 700]] This is the framework version of '
            'the Future and Promise video, with the same product page. '
            '[[slnc 500]] We will learn that the thread pool, not the '
            'annotation, decides how much runs at once. [[slnc 300]] We '
            'will hear an error vanish from a method that returns '
            "nothing. [[slnc 300]] Lose a customer's details between "
            'threads. [[slnc 300]] And learn why a timeout and a cancel '
            'both leave the work running.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Future/Promise, the hand-built video,', 'built the handoff and showed three', 'costs: an exception that moves, a get', 'that hangs, a cancel that is a request.', '', 'This one uses the same product page:', 'price, stock and a review score.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Future and Promise video. [[slnc '
            '400]] That one builds the handoff between a future and a '
            'promise by hand. [[slnc 300]] And it shows three costs: an '
            'error that appears later, a wait with no timeout that hangs, '
            'and a cancel that a task can ignore. [[slnc 500]] If you are '
            'new to the pattern, watch that one first. [[slnc 400]] Here, '
            'we keep the same product page, with its price, stock, and '
            'review score, and ask what Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'Its @Async annotation runs a method on', 'a pool, and hands back a future that', 'the container completes.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'One thing is new in this project: Spring Boot. [[slnc 400]] '
            'At its heart, Spring is a container that creates your '
            'objects. [[slnc 500]] Its at Async annotation runs a method '
            'on a thread pool that Spring owns. [[slnc 300]] And it hands '
            'back a Completable Future. [[slnc 300]] Spring completes '
            'that future when the method returns. [[slnc 500]] And one '
            'promise. [[slnc 300]] If you skip this video, you lose none '
            'of the pattern. [[slnc 300]] This one is about the tool.'
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
            'First demo: the pool decides. [[slnc 400]] Three independent '
            'lookups, for price, stock, and rating, each marked at Async. '
            '[[slnc 500]] On the default pool, all three run at the same '
            'moment. [[slnc 300]] On a pool with just one thread, only '
            'one runs at a time. [[slnc 500]] The annotation asked for '
            'things to run at once. [[slnc 300]] The pool decided whether '
            'to allow it. [[slnc 300]] How much runs at once is a '
            'property of the pool, not the annotation.'
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
            'Second demo: errors. [[slnc 400]] A method that returns a '
            'future fails. [[slnc 300]] The caller receives a Completion '
            'Exception, with the real cause inside: the review service is '
            'down. [[slnc 300]] And the stack trace belongs to a pool '
            'thread, not the caller. [[slnc 600]] Now a method that '
            'returns nothing, called a void method, throws an error. '
            '[[slnc 300]] The caller gets nothing at all. [[slnc 300]] '
            'The call returned normally. [[slnc 400]] The error only went '
            'to a special handler, which you must register yourself. '
            '[[slnc 300]] Without one, it is just written to a log. '
            '[[slnc 500]] That is why the rule is: return a future, never '
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
            'Third demo: thread-local data. [[slnc 400]] The caller is '
            'working for customer seven. [[slnc 300]] That fact is stored '
            'in a thread-local, which is where request details, security '
            'details, and logging details usually live. [[slnc 500]] The '
            'async method asks: whose order is this? [[slnc 300]] The '
            "answer is: nobody's. [[slnc 500]] A thread-local does not "
            'travel to a pool thread. [[slnc 300]] The fix is a Task '
            'Decorator, a small bean that copies the data across. [[slnc '
            '300]] With it, the answer is customer seven. [[slnc 300]] '
            'But you have to write that fix yourself.'
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
            'Fourth demo: a timeout does not stop the work. [[slnc 400]] '
            'The caller waits two hundred milliseconds for a slow task. '
            '[[slnc 300]] Then it gets a Timeout Exception. [[slnc 300]] '
            'The task had not finished. [[slnc 500]] Later, the task '
            'carries on, runs to the end, and does its work anyway. '
            '[[slnc 300]] Nobody is waiting for its answer any more. '
            '[[slnc 500]] A timeout means the caller gave up. [[slnc '
            '300]] It does not stop the work.'
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
            'Fifth demo: cancelling. [[slnc 400]] Calling cancel with '
            'true reports success. [[slnc 300]] The future says it is '
            'cancelled. [[slnc 300]] And the task runs to the end anyway. '
            '[[slnc 500]] Why? [[slnc 300]] On a Completable Future, '
            'cancel only sets a flag on the future. [[slnc 300]] It never '
            'interrupts the thread doing the work. [[slnc 400]] In the '
            'hand-built video, a task ignored an interruption. [[slnc '
            '300]] Here, no interruption is even sent.'
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
            'Last demo: building the page from futures. [[slnc 400]] '
            'Three futures are combined into one. [[slnc 300]] Nothing '
            'waits until the very end. [[slnc 300]] The page shows a '
            'price of one hundred and twenty-nine pounds ninety-nine, a '
            'stock of seven, and a rating of four point six. [[slnc 500]] '
            'Now the review service goes down. [[slnc 300]] With a '
            'fallback chosen at that one step, the page still appears, '
            'with the rating marked as unavailable. [[slnc 300]] Without '
            'the fallback, one failed lookup fails the whole page.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Return a CompletableFuture, never void.', 'Choose the pool.', 'Carry the context on purpose.', 'A timeout is giving up, not stopping.', '', 'Design tasks that check for', 'cancellation themselves.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Return a Completable '
            'Future, never void. [[slnc 300]] Choose your thread pool '
            'deliberately. [[slnc 300]] Carry thread-local data across on '
            'purpose. [[slnc 300]] Remember that a timeout is giving up, '
            'not stopping. [[slnc 300]] And design tasks that check for '
            'cancellation themselves.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Async returning CompletableFuture.', 'thenCombine, exceptionally, orTimeout.', 'A TaskDecorator bean.', 'MDC or SecurityContext copied by hand.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for at Async methods that return a Completable '
            'Future. [[slnc 300]] Look for chains of then combine, '
            'exceptionally, and or timeout. [[slnc 300]] Look for a Task '
            'Decorator bean. [[slnc 300]] And look for logging or '
            'security details, copied by hand between threads.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Async method that returns a', 'CompletableFuture.', '', 'And every log line that lost its request', 'id on the way to a pool thread.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In every at '
            'Async method that returns a future. [[slnc 300]] And in '
            'every log line that lost its request I D on the way to a '
            'pool thread.'
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
        body=["Everything is real: Spring's executor,", 'its futures and its handlers.', '', 'Every wait is a latch, a gate,', 'or a bounded spin.'],
        narration=(
            "A quick, honest note about this demo. [[slnc 300]] Spring's "
            'thread pool, its futures, and its error handlers are all '
            'real. [[slnc 300]] Every wait uses a latch, a gate, or a '
            'short, limited loop. [[slnc 300]] So every run gives the '
            'same result.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['Two lookups that are already fast,', 'or where the second needs the', 'first: a future is ceremony.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For lookups that are '
            "already fast, or where the second needs the first's result, "
            'a future adds ceremony and saves no time.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Make the slow task check for', 'interruption, and cancel it properly.'],
        narration=(
            "That's Future and Promise with Spring. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'future promises when a value will be ready, but never that '
            'the work behind it can be stopped. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Make the slow task check '
            'for interruption in its loop. [[slnc 300]] Then cancel it '
            "through a normal executor's future, and listen for the "
            'difference. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
