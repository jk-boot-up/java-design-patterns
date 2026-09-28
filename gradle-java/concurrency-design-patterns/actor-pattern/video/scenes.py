"""Scene definitions for the Actor teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Actor',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Actor pattern, in Java. [[slnc 300]] This video is presented '
            'by Jayasekhar Konduru. [[slnc 600]] First, a simple '
            'definition. [[slnc 300]] An actor is an object that owns '
            'some data, has a mailbox, and handles one message at a time, '
            'on its own thread. [[slnc 400]] Its data is never touched by '
            'two threads at once. [[slnc 300]] And nobody can reach '
            'inside it, except by sending it a message. [[slnc 600]] '
            'Think of a bank teller behind a window. [[slnc 300]] '
            'Customers queue, and pass notes through the window. [[slnc '
            '300]] Only the teller ever touches the cash drawer. [[slnc '
            '700]] In our online store, many threads want to change the '
            'stock of a product. [[slnc 500]] In this video, shared stock '
            'will lose an update. [[slnc 300]] Then one actor will own '
            'it, and lose nothing. [[slnc 300]] We will hear answers come '
            'back as messages, and a bad message restart the actor. '
            '[[slnc 300]] And finally, the costs.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Many threads place orders.', '', 'Every order reserves stock.', '', 'The stock must never go wrong,', 'however many arrive together.', '', 'Locks, or something else?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Many threads place orders '
            'in an online store. [[slnc 300]] Every order reserves some '
            'stock. [[slnc 400]] The stock count must never go wrong, '
            'however many orders arrive at the same moment. [[slnc 500]] '
            'So here is the question. [[slnc 300]] Do we protect it with '
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
            'First demo: data that many threads can reach. [[slnc 400]] '
            'There are ten in stock. [[slnc 300]] Two orders arrive, for '
            'three and for four. [[slnc 300]] Both read the stock at the '
            'same moment. [[slnc 500]] There should be three left. [[slnc '
            '300]] But there are not. [[slnc 300]] One of the two '
            'reservations was lost. [[slnc 500]] Every method looked '
            'correct. [[slnc 300]] The problem was that the data was open '
            'to anyone.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['An actor owns some state.', '', 'It has a mailbox, and one thread', 'that takes one message at a time.', '', 'Nobody else can touch the state.', '', 'Others send messages, and get a', 'reply message back.'],
        narration=(
            'Now, the pattern. [[slnc 400]] An actor owns some data. '
            '[[slnc 300]] It has a mailbox, and one thread, which takes '
            'one message at a time. [[slnc 400]] Nobody else can touch '
            'the data. [[slnc 300]] Everyone else sends messages. [[slnc '
            '300]] And if they want an answer, they get a reply message '
            'back.'
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
            'Second demo: data that one actor owns. [[slnc 400]] An '
            'inventory actor starts with four thousand in stock. [[slnc '
            '300]] Four threads each send one thousand reservations. '
            '[[slnc 500]] Stock left: zero, exactly right. [[slnc 400]] '
            'There is no lock inside the inventory. [[slnc 300]] The '
            'actor handled one message at a time, so nothing was lost.'
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
            'Third demo: ask, and get a message back. [[slnc 400]] There '
            'are five in stock. [[slnc 300]] Reserve three, and the reply '
            'says: reserved. [[slnc 300]] Reserve three more, and the '
            'reply says: out of stock, only two left. [[slnc 500]] The '
            'answer is a message too. [[slnc 300]] And it can be a '
            'refusal. [[slnc 300]] No exception crosses between the two '
            'sides.'
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
            'Fourth demo: nobody can reach inside. [[slnc 400]] The '
            'inventory actor has no public method that returns its stock. '
            '[[slnc 400]] The only way to learn the stock is to ask. '
            '[[slnc 300]] And the answer is a copy. [[slnc 500]] Nobody '
            'holds the real value. [[slnc 300]] So nobody can change it '
            "behind the actor's back."
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
            'Fifth demo: let it crash. [[slnc 400]] After reserving two, '
            'the stock is three. [[slnc 300]] Then the actor receives a '
            'message it cannot handle. [[slnc 500]] The sender is told '
            'what went wrong. [[slnc 300]] The actor is restarted. [[slnc '
            '300]] And the next message is handled normally. [[slnc 400]] '
            'One bad message did not stop the actor. [[slnc 500]] But '
            'notice: after the restart, the stock went back to five. '
            '[[slnc 300]] The restart reset its data.'
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
            'Finally, the costs. [[slnc 400]] Two actors each ask the '
            'other a question, and wait for the answer. [[slnc 300]] '
            'Neither ever gets one. [[slnc 500]] There are no locks, and '
            'yet it is a deadlock. [[slnc 300]] Each is waiting for a '
            'message the other can never send. [[slnc 500]] Also, a '
            "restart forgets the actor's data, unless it was saved "
            'somewhere else. [[slnc 300]] Messages are copied. [[slnc '
            '300]] Mailboxes can grow. [[slnc 300]] And tracing where a '
            'message went needs special tools.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A class with a mailbox, a receive', 'method and a single thread.', '', "Akka's ActorRef and tell and ask,", "Erlang processes, Elixir's", '', 'Message classes that are records', 'or case classes.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a class with a mailbox, a receive method, and '
            "a single thread. [[slnc 300]] Look for Akka's actor "
            'references, with tell and ask. [[slnc 300]] Or Erlang '
            "processes, and Elixir's Gen Server. [[slnc 300]] Look for "
            'message classes that are records. [[slnc 300]] And a '
            'supervisor that decides what to do when an actor fails.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use actors for state that many', 'parts of a program need to change,', 'where one owner and messages are', 'clearer than locks: a stock count,', 'a session, a connection. Keep', 'messages small and immutable. Do', 'not wait for a reply inside a', 'handler. Decide what a restart', 'does to the state. Use a library'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use actors for data '
            'that many parts of a program need to change, where one owner '
            'and messages are clearer than locks. [[slnc 300]] A stock '
            'count, a user session, or a network connection. [[slnc 500]] '
            'Keep messages small, and unchangeable. [[slnc 300]] Never '
            'wait for a reply inside a message handler. [[slnc 300]] '
            'Decide what a restart should do to the data. [[slnc 300]] '
            'And use a library such as Akka or Pekko, rather than writing '
            'mailboxes yourself.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a counter, an AtomicInteger is', 'simpler. Actors earn their place', 'when the state is more than one', 'number, and many parts of the', 'system need to change it.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a simple '
            'counter, an Atomic Integer is easier. [[slnc 300]] Actors '
            'earn their place when the data is more than one number, and '
            'many parts of the system need to change it.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Actor pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] An actor removes '
            'locks by giving data one owner, and the price is messages, '
            'and a restart that forgets. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Make the actor keep its stock across a '
            'restart. [[slnc 300]] And decide where that stock should be '
            'kept. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
