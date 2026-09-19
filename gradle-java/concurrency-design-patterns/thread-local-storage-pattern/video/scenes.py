"""Scene definitions for the Thread-Local Storage teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Thread-Local Storage',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Thread-Local '
            'Storage pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: '
            'thread local storage gives each thread its own private copy '
            'of a variable, so code anywhere on that thread can read it '
            'without it being passed down, and other threads never see '
            'it. [[slnc 350]] This is another project in the concurrency '
            'category, whose subject is how threads share work and state '
            'without corrupting either. In our online store, the thing '
            'every layer of a request needs to know, but few care about, '
            'is which customer it is for. [[slnc 300]] By the end you '
            'will see a customer handed down through three methods that '
            'do not need it, see it kept in the thread instead, see two '
            'threads keep their own, see a reused pool thread leak one '
            'request into the next, see a value fail to cross to another '
            'thread, and see the bill, which is a hidden dependency.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A checkout request goes through', 'checkout, pricing and stock.', '', 'At the bottom, the audit log must', 'say which customer did it.', '', 'Only the door knows the customer.', '', 'How does the log find out?'],
        narration=(
            'Here is the scenario. A checkout request goes through '
            'checkout, pricing and stock. At the bottom, the audit log '
            'must say which customer did it. Only the door of the request '
            'knows who the customer is. [[slnc 300]] The question: how '
            'does the log find out?'
        ),
    ),
    dict(
        key='03-hand', kind='console', title='Hand It Down',
        body="""ONE. Hand it down.
  3 methods take a customer
  they never use.

  so that the last can log it.

  every new layer passes it on.""",
        narration=(
            'First, hand it down. Three methods each take a customer '
            'parameter that they never use, so that the last one can log '
            'it. Every new layer, and every new caller, has to pass it '
            'on. The parameter is noise in every signature, and one '
            'method forgetting it breaks the log.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Each thread has its own copy of', 'a variable.', '', 'Set it once, at the door.', '', 'Read it anywhere below, with no', 'parameter.', '', 'Clear it when the request is done.'],
        narration=(
            'The pattern. Each thread has its own copy of a variable. Set '
            'it once, at the door. Read it anywhere below, with no '
            'parameter. And clear it when the request is done.'
        ),
    ),
    dict(
        key='05-own', kind='console', title='A Value That Belongs To The Thread',
        body="""TWO. Thread-local.
  the customer is set at the door.
  checkout, price, stock take no
  customer.
  the log: ada.

  after the request: cleared.""",
        narration=(
            'Second, a value that belongs to the thread. The customer is '
            'set once, at the door. Checkout, price and stock take no '
            'customer at all, and the log still says ada. After the '
            'request, the context is cleared.'
        ),
    ),
    dict(
        key='06-threads', kind='console', title='Each Thread Has Its Own',
        body="""THREE. Own copies.
  two customers at once.
  both set before either reads.
  ada: reserved stock.
  ben: reserved stock.

  the same static field, two
  values.""",
        narration=(
            'Third, each thread has its own. Two customers are handled at '
            'the same moment, and both contexts are set before either is '
            'read. The log says ada for one, and ben for the other. They '
            'share the code, and the same static field, and they do not '
            'share the value.'
        ),
    ),
    dict(
        key='07-reuse', kind='console', title='A Thread That Is Reused',
        body="""FOUR. Reused.
  A sets ada, forgets to clear.
  B, anonymous, runs next on
  the same pool thread:
  logged as ada.

  with a finally block: null.""",
        narration=(
            'Fourth, a thread that is reused. Request A sets ada, and '
            'forgets to clear it. Request B, an anonymous visitor, runs '
            'next on the same pool thread. B is logged as ada. A pool '
            'reuses its threads, so what a request leaves behind, the '
            'next one finds. With the clear in a finally block, B is '
            'logged as nobody. This is the classic bug.'
        ),
    ),
    dict(
        key='08-new', kind='console', title='A New Thread Starts Empty',
        body="""FIVE. Another thread.
  ada's request hands work to
  another thread: null.

  a thread created by ada's
  thread inherits a copy.

  a pool thread does not have
  the current request's.""",
        narration=(
            "Fifth, a new thread starts empty. Ada's request hands the "
            'work to another thread, and the log says null. A thread that '
            "ada's thread creates can inherit a copy. But a pool thread "
            'is created once and reused, so it holds whatever was there '
            "when it was created, not the current request's. Handing work "
            'on means handing the context on, on purpose.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  a method that reads the
  context has a hidden
  dependency: none set, null.

  every test must set and clear
  it.

  a pool thread keeps what is
  left in it.""",
        narration=(
            'Last, the bill. A method that reads the context has a '
            'dependency its signature does not show. With none set, it '
            'logs null. Every test of the code below the door has to set '
            'the context first, and clear it after. And a long lived pool '
            'thread keeps whatever is left in it, for as long as the '
            'thread lives.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A private static final', 'ThreadLocal<...> field.', '', 'SecurityContextHolder,', 'TransactionSynchronizationManager,', '', 'try { set(...); ... } finally {', 'remove(); }.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'private static final ThreadLocal<...> field. '
            'SecurityContextHolder, TransactionSynchronizationManager, '
            'MDC from logging. try { set(...); ... } finally { remove(); '
            '}. A TaskDecorator or ContextSnapshot that copies context to '
            'another thread.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use thread-local storage for', 'context that is truly per-request', 'and crosses many layers, such as a', 'trace id, a security principal or', 'a transaction. Set it in one', 'place, clear it in a finally block', 'in the same place, pass it on by', 'hand when you hand work to another', 'thread, and keep the values small.'],
        narration=(
            'Here is my verdict, plainly. Use thread-local storage for '
            'context that is truly per-request and crosses many layers, '
            'such as a trace id, a security principal or a transaction. '
            'Set it in one place, clear it in a finally block in the same '
            'place, pass it on by hand when you hand work to another '
            'thread, and keep the values small. If a parameter is easy, '
            'pass the parameter.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. Every number quoted comes from '
            "this program's own output. Nothing depends on a clock, so "
            'every run is the same.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If a value is used in one or two', 'places, pass it as a parameter,', 'where it can be seen and tested.', 'Thread-local state is global state', "with a thread's name on it."],
        narration=(
            'So when is it too much? If a value is used in one or two '
            'places, pass it as a parameter, where it can be seen and '
            "tested. Thread-local state is global state with a thread's "
            'name on it.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Thread-Local Storage. [[slnc 250]] If you take one "
            'sentence away, take this one: thread-local storage saves '
            'passing a value down, and its price is a dependency you '
            'cannot see and a clear you must not forget. [[slnc 350]] The '
            'full source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, write a decorator that copies the '
            'context to a pool thread for one task, and clears it after. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
