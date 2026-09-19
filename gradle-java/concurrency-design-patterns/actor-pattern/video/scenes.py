"""Scene definitions for the Actor teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Actor',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Actor pattern in '
            'Java, and it is written and presented by Jayasekhar Konduru. '
            '[[slnc 300]] The plain definition: an actor is an object '
            'that owns some state, has a mailbox, and handles one message '
            'at a time on its own thread. Its state is never touched by '
            'two threads, and nothing can reach in except by sending it a '
            'message. [[slnc 350]] This is another project in the '
            'concurrency category, whose subject is how threads share '
            'work and state without corrupting either. In our online '
            'store, the state that many threads want to change is the '
            'stock of a product. [[slnc 300]] By the end you will see '
            'shared stock lose an update, see one actor own it and lose '
            'nothing, see answers come back as messages, see that nobody '
            'can reach inside, see a bad message restart the actor, and '
            'see the bill, which is a deadlock with no locks, and state '
            'that a restart forgets.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Many threads place orders.', '', 'Every order reserves stock.', '', 'The stock must never go wrong,', 'however many arrive together.', '', 'Locks, or something else?'],
        narration=(
            'Here is the scenario. Many threads place orders in the '
            'online store, and every order reserves stock. The stock must '
            'never go wrong, however many orders arrive at the same '
            'moment. [[slnc 300]] The question: do we guard it with '
            'locks, or with something else?'
        ),
    ),
    dict(
        key='03-shared', kind='console', title='State That Many Threads Can Reach',
        body="""ONE. Open state.
  10 in stock.
  orders for 3 and 4 read it at
  the same moment.
  it should be 3 left: false.

  one reservation was lost.""",
        narration=(
            'First, state that many threads can reach. Ten in stock. Two '
            'orders, for three and for four, read the stock at the same '
            'moment. It should be three left. It is not. One of the two '
            'reservations was lost. Every method looked correct. The '
            'state was open to anyone.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['An actor owns some state.', '', 'It has a mailbox, and one thread', 'that takes one message at a time.', '', 'Nobody else can touch the state.', '', 'Others send messages, and get a', 'reply message back.'],
        narration=(
            'The pattern. An actor owns some state. It has a mailbox, and '
            'one thread that takes one message at a time. Nobody else can '
            'touch the state. Everyone else sends messages, and, if they '
            'want an answer, gets a reply message back.'
        ),
    ),
    dict(
        key='05-own', kind='console', title='State That One Actor Owns',
        body="""TWO. One owner.
  4 threads, 1000 each, to an
  inventory of 4000.
  stock left: 0.

  no lock in the inventory.
  one message at a time.""",
        narration=(
            'Second, state that one actor owns. Four threads each send a '
            'thousand reservations, to an inventory of four thousand. '
            'Stock left: zero. There is no lock in the inventory. The '
            'actor handled one message at a time, so none was lost.'
        ),
    ),
    dict(
        key='06-ask', kind='console', title='Ask, And Be Answered By A Message',
        body="""THREE. Ask.
  reserve 3: Reserved.
  reserve 3 more: OutOfStock,
  2 left.

  the answer is a message, and
  can be a refusal.""",
        narration=(
            'Third, ask, and be answered by a message. Reserve three of '
            'five: the reply is reserved. Reserve three more: the reply '
            'is out of stock, with two left. The answer is a message too, '
            'and it can be a refusal. No exception crossed between the '
            'two.'
        ),
    ),
    dict(
        key='07-closed', kind='console', title='Nobody Can Reach In',
        body="""FOUR. Closed.
  a public method that returns
  the stock: false.

  the only way to learn it is to
  ask.
  the answer is a copy: 5.""",
        narration=(
            'Fourth, nobody can reach in. The inventory actor has no '
            'public method that returns its stock. The only way to learn '
            'the stock is to ask, and the answer is a copy. Nobody holds '
            "the real thing, so nobody can change it behind the actor's "
            'back.'
        ),
    ),
    dict(
        key='08-crash', kind='console', title='Let It Crash',
        body="""FIVE. Let it crash.
  stock 3 after reserving 2.
  a bad message: the sender is
  told.
  the actor restarts.
  the next message is handled.

  the stock went back to 5.""",
        narration=(
            'Fifth, let it crash. After reserving two, the stock is '
            'three. Then a message the actor cannot handle. The sender is '
            'told what went wrong, and the actor is restarted. The next '
            'message is handled as normal. One bad message did not stop '
            'the actor. But the restart put the stock back to five. The '
            'state was reset.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  two actors ask each other, and
  wait: no answer.
  no locks, and still a deadlock.

  a restart forgets its state.
  messages are copied.
  mailboxes can grow.""",
        narration=(
            'Last, the bill. Two actors that each ask the other, and wait '
            'for the answer, never get one. There are no locks, and still '
            'a deadlock: each is waiting for a message the other can '
            'never send. A restart forgets state, unless it was written '
            'somewhere else. Messages are copied. Mailboxes can grow. And '
            'finding where a message went takes tools.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A class with a mailbox, a receive', 'method and a single thread.', '', "Akka's ActorRef and tell and ask,", "Erlang processes, Elixir's", '', 'Message classes that are records', 'or case classes.'],
        narration=(
            'How do you recognise this in code you did not write? A class '
            "with a mailbox, a receive method and a single thread. Akka's "
            "ActorRef and tell and ask, Erlang processes, Elixir's "
            'GenServer. Message classes that are records or case classes. '
            'A supervisor strategy that says what to do when a child '
            'fails.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use actors for state that many', 'parts of a program need to change,', 'where one owner and messages are', 'clearer than locks: a stock count,', 'a session, a connection. Keep', 'messages small and immutable. Do', 'not wait for a reply inside a', 'handler. Decide what a restart', 'does to the state. Use a library'],
        narration=(
            'Here is my verdict, plainly. Use actors for state that many '
            'parts of a program need to change, where one owner and '
            'messages are clearer than locks: a stock count, a session, a '
            'connection. Keep messages small and immutable. Do not wait '
            'for a reply inside a handler. Decide what a restart does to '
            'the state. Use a library such as Akka or Pekko rather than '
            'writing the mailbox yourself.'
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
        body=['For a counter, an AtomicInteger is', 'simpler. Actors earn their place', 'when the state is more than one', 'number, and many parts of the', 'system need to change it.'],
        narration=(
            'So when is it too much? For a counter, an AtomicInteger is '
            'simpler. Actors earn their place when the state is more than '
            'one number, and many parts of the system need to change it.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Actor. [[slnc 250]] If you take one sentence away, "
            'take this one: an actor takes locks out of the story by '
            'giving state one owner, and the price is messages, and a '
            'restart that forgets. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, make the actor keep its stock across a '
            'restart, and decide where to keep it. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
