"""Scene definitions for the Thread-Local Storage teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Thread-Local Storage',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Thread-Local Storage pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] Thread-local '
            'storage gives each thread its own private copy of a '
            'variable. [[slnc 300]] Code anywhere on that thread can read '
            'it, without it being passed down. [[slnc 300]] And other '
            'threads never see it. [[slnc 600]] Think of a name badge at '
            'a conference. [[slnc 300]] Anyone you meet can read your '
            'name from your badge. [[slnc 300]] You do not have to repeat '
            'it in every conversation. [[slnc 700]] In our online store, '
            'every layer of a request needs to know which customer it is '
            'for, but few of them care. [[slnc 500]] In this video, we '
            'pass the customer through three methods that do not need it. '
            '[[slnc 300]] Then keep it in the thread instead. [[slnc '
            '300]] We will hear a reused thread leak one request into the '
            'next, and a value that fails to reach another thread. [[slnc '
            '300]] And then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A checkout request goes through', 'checkout, pricing and stock.', '', 'At the bottom, the audit log must', 'say which customer did it.', '', 'Only the door knows the customer.', '', 'How does the log find out?'],
        narration=(
            'Here is the scenario. [[slnc 400]] A checkout request passes '
            'through three steps: checkout, pricing, and stock. [[slnc '
            '400]] At the very bottom, an audit log must record which '
            'customer did it. [[slnc 400]] But only the entry point of '
            'the request knows who the customer is. [[slnc 500]] So here '
            'is the question. [[slnc 300]] How does the log find out?'
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
            'First, the simple way: hand it down. [[slnc 400]] Three '
            'methods each take a customer parameter, which they never '
            'use. [[slnc 300]] They only pass it on, so the last one can '
            'log it. [[slnc 500]] Every new layer, and every new caller, '
            'must pass it on too. [[slnc 300]] The parameter clutters '
            'every method. [[slnc 300]] And if one method forgets it, the '
            'log breaks.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Each thread has its own copy of', 'a variable.', '', 'Set it once, at the door.', '', 'Read it anywhere below, with no', 'parameter.', '', 'Clear it when the request is done.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Each thread has its own copy '
            'of a variable. [[slnc 300]] Set it once, at the entry point '
            'of the request. [[slnc 300]] Read it anywhere below, with no '
            'parameter. [[slnc 300]] And clear it when the request is '
            'finished.'
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
            'Second demo: a value that belongs to the thread. [[slnc '
            '400]] The customer, Ada, is set once, at the entry point. '
            '[[slnc 300]] Checkout, pricing, and stock take no customer '
            'parameter at all. [[slnc 300]] And the log still says Ada. '
            '[[slnc 500]] When the request finishes, the value is '
            'cleared.'
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
            'Third demo: each thread has its own copy. [[slnc 400]] Two '
            'customers are served at the same moment. [[slnc 300]] Both '
            'values are set before either is read. [[slnc 500]] The log '
            'says Ada for one request, and Ben for the other. [[slnc '
            '400]] They run the same code, and use the same static field. '
            '[[slnc 300]] But they do not share the value.'
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
            'Fourth demo: a thread that is reused. [[slnc 400]] Request A '
            'sets the customer to Ada, and forgets to clear it. [[slnc '
            '500]] Then request B, from an anonymous visitor, runs next, '
            'on the same pool thread. [[slnc 300]] Request B is logged as '
            'Ada. [[slnc 500]] A thread pool reuses its threads. [[slnc '
            '300]] So whatever one request leaves behind, the next one '
            'finds. [[slnc 500]] With the clear placed in a finally '
            'block, request B is logged as nobody, which is correct. '
            '[[slnc 300]] This is the classic thread-local bug.'
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
            "Fifth demo: a new thread starts empty. [[slnc 400]] Ada's "
            'request hands some work to another thread. [[slnc 300]] And '
            "that thread's log says: nobody. [[slnc 500]] A thread "
            "created directly by Ada's thread can inherit a copy. [[slnc "
            '300]] But a pool thread was created long ago, and reused. '
            '[[slnc 300]] It holds whatever was there when it was made, '
            "not the current request's value. [[slnc 500]] So handing "
            'work to another thread means handing the value over too, on '
            'purpose.'
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
            'Finally, the cost. [[slnc 400]] A method that reads the '
            'thread-local value has a hidden dependency. [[slnc 300]] Its '
            'parameters do not show it. [[slnc 300]] If nobody set the '
            'value, it logs nothing. [[slnc 500]] Every test of the lower '
            'layers must set the value first, and clear it after. [[slnc '
            '400]] And a long-lived pool thread keeps whatever is left in '
            'it, for as long as the thread lives.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A private static final', 'ThreadLocal<...> field.', '', 'SecurityContextHolder,', 'TransactionSynchronizationManager,', '', 'try { set(...); ... } finally {', 'remove(); }.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a private static final Thread Local field. '
            "[[slnc 300]] Look for Spring's Security Context Holder, or "
            'the logging context, called M D C. [[slnc 300]] Look for a '
            'try block that sets a value, with a finally block that '
            'removes it. [[slnc 300]] And look for a Task Decorator that '
            'copies the value to another thread.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use thread-local storage for', 'context that is truly per-request', 'and crosses many layers, such as a', 'trace id, a security principal or', 'a transaction. Set it in one', 'place, clear it in a finally block', 'in the same place, pass it on by', 'hand when you hand work to another', 'thread, and keep the values small.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use thread-local '
            'storage for details that truly belong to one request, and '
            'cross many layers. [[slnc 300]] Such as a trace I D, the '
            'logged-in user, or a transaction. [[slnc 500]] Set it in one '
            'place. [[slnc 300]] Clear it in a finally block, in that '
            'same place. [[slnc 300]] Pass it on by hand when work moves '
            'to another thread. [[slnc 300]] And keep the values small. '
            '[[slnc 500]] And if passing a parameter is easy, just pass '
            'the parameter.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every result you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If a value is used in one or two', 'places, pass it as a parameter,', 'where it can be seen and tested.', 'Thread-local state is global state', "with a thread's name on it."],
        narration=(
            'So, when is this too much? [[slnc 400]] If a value is used '
            'in only one or two places, pass it as a parameter. [[slnc '
            '300]] There, it can be seen, and tested. [[slnc 400]] '
            "Thread-local data is really global data, with a thread's "
            'name on it.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Thread-Local Storage. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Thread-local '
            'storage saves passing a value down, and its price is a '
            'dependency you cannot see, and a clear you must never '
            'forget. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Write a decorator that copies the customer to a pool '
            'thread for one task. [[slnc 300]] And clears it again '
            'afterwards. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
