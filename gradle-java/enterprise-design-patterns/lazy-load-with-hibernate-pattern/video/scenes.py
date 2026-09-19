"""Scene definitions for the Lazy Load with Hibernate teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Lazy Load with Hibernate',
        body=None,
        narration=(
            'Hello, and welcome. This video explains Lazy Load with '
            'Hibernate, in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] It is the framework version '
            'of the Lazy Load video. That one built the pattern by hand. '
            'This one is about the most searched Java error there is: '
            'lazy initialization exception. [[slnc 350]] The plain '
            'definition: a lazy field does not hold its data. It holds a '
            'stand-in, that loads the data the first time somebody asks. '
            '[[slnc 300]] By the end you will know exactly what is in '
            'that field, why asking after the session has closed fails, '
            'and what each of the three usual fixes costs.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Lazy Load, the hand-built video,', 'built four lazy variants and a', 'session-closed failure from', 'plain Java.', '', 'This video uses the same store', 'and shows what Hibernate does.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'This video assumes the Lazy Load video. If you have not seen '
            'it, start there. It builds four ways of loading later, by '
            'hand, and a failure when the session has closed. [[slnc '
            '300]] This one uses the very same store: five customers, '
            'twenty orders, four lines in each. It does not teach the '
            'pattern again. It shows the real exception, from Hibernate '
            'itself.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['Two things are new: Hibernate and H2.', '', 'Hibernate turns operations on objects', 'into SQL. H2 is a database that runs', 'inside the test, so nothing is installed.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first annotation, two new things. Hibernate is '
            'the most widely used implementation of J P A. You mark your '
            'classes, and it turns operations on them into S Q L. [[slnc '
            '300]] H two is a database that runs inside the test, in '
            'memory, so nothing needs installing. [[slnc 300]] And a '
            'promise: skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it. This one explains an '
            'exception.'
        ),
    ),
    dict(
        key='04-lazy-word', kind='bullets', title='One Word Makes It Lazy',
        body=['@ManyToOne(fetch = LAZY)', '', "An order's customer, and its lines,", 'are both declared lazy.', '', 'That one word is what this', 'whole video is about.'],
        narration=(
            'Here is the one word. On the order class, the customer, and '
            'the lines, are both declared with fetch type lazy. [[slnc '
            '300]] That one word is what this whole video is about.'
        ),
    ),
    dict(
        key='05-exception', kind='console', title='The Exception',
        body="""ONE. Load, close, use.
  the order loaded fine:
  order 1

  the customer's name threw
  LazyInitializationException:
  Could not initialize proxy
  Customer#1 - no session

  the failure is where it
  was used.""",
        narration=(
            'Now the failure, on purpose. Load an order. Close the '
            "session. Then ask the order for its customer's name. [[slnc "
            '300]] The order loaded fine. Asking for the name threw a '
            'lazy initialization exception. Could not initialize proxy, '
            'customer number one, no session. [[slnc 300]] Look where it '
            'failed. Not where the order was loaded. Where the customer '
            'was used. That is why it is so hard to find.'
        ),
    ),
    dict(
        key='06-proxy', kind='console', title='What Is In The Field',
        body="""TWO. The field.
  order.customer() is a
  generated subclass of
  Customer.
  initialised: false

  it holds only the id (1)
  and a reference to the
  session.

  ask for the name, inside
  the session: initialised.""",
        narration=(
            'So what is actually in that field? Not a customer. Hibernate '
            'generated a subclass of the customer class. It holds only '
            "two things: the customer's id, and a reference to the "
            'session. It has not loaded anything. Initialised: false. '
            '[[slnc 300]] Ask it for the name while the session is open, '
            'and it selects the customer, and becomes initialised. [[slnc '
            '300]] Close the session first, and it has nothing to load '
            'with. That is the exception. Not a bug. A promise that '
            'needed something that has gone.'
        ),
    ),
    dict(
        key='07-fix-one', kind='console', title='Fix One: Keep The Session Open',
        body="""THREE. Keep it open.
  customer names: 6
  statements.
  line counts: 21
  statements. that is N+1.

  the session and connection
  stay open while the page
  renders.""",
        narration=(
            'The first usual fix: keep the session open while the page '
            'renders. It works. [[slnc 300]] Twenty orders, each with its '
            "customer's name: six statements. Not twenty-one. One for the "
            'orders, and one for each of the five different customers, '
            'because the session loads each customer only once. That is '
            'the identity map from the earlier video, at work. [[slnc '
            '300]] But twenty orders, each with its line count: '
            'twenty-one statements. One for the orders, then one for '
            "every order's lines. That is N plus one. [[slnc 300]] The "
            'cost: the session, and its database connection, stay open '
            'while the page renders. And the extra queries are hidden '
            'inside the view, where nobody looks.'
        ),
    ),
    dict(
        key='08-fix-two', kind='console', title='Fix Two: Fetch It In The Same Query',
        body="""FOUR. Join fetch.
  the customer: 1 statement
  the lines:    1 statement

  but the database sends
  80 rows for 20 orders,
  each order repeated once
  per line.

  every caller gets the lines.""",
        narration=(
            'The second fix: fetch it in the same query, with a join '
            'fetch. One statement, for the customers. One statement, for '
            'the lines. [[slnc 300]] The cost is hidden in the middle. '
            'Fetching the lines makes the database send eighty rows for '
            'twenty orders, each order repeated once for each of its four '
            'lines. Hibernate folds them back together for you. [[slnc '
            '300]] And every caller of that query now gets the lines, '
            'whether it wanted them or not.'
        ),
    ),
    dict(
        key='09-fix-three', kind='console', title='Fix Three: Ask For What You Need',
        body="""FIVE. A projection.
  20 rows, 1 statement

  OrderRow[orderId=1,
   customerName=Customer 1]

  no entity, no proxy,
  nothing lazy to fail.

  a class for every query.""",
        narration=(
            'The third fix: ask for exactly what the page needs. A '
            'projection. One statement, twenty rows, each with just an '
            'order number and a customer name. [[slnc 300]] No entity. No '
            'proxy. Nothing lazy left to fail. [[slnc 300]] The cost: a '
            'class for every query, and a row is not an object with '
            'behaviour. This is the idea from the D T O video, arriving '
            'from the other direction.'
        ),
    ),
    dict(
        key='10-not-eager', kind='bullets', title='The Fix Not On The List',
        body=['Make the mapping EAGER.', '', 'That removes the exception.', '', 'And it brings back the first act', 'of the partner video: loading one', 'order loads the shop.'],
        narration=(
            'There is a fourth fix, that is not on the list, because it '
            'is the one to be careful of. Make the mapping eager. That '
            'removes the exception. [[slnc 300]] And it brings back the '
            'first act of the Lazy Load video: load one order, and you '
            'load the shop.'
        ),
    ),
    dict(
        key='11-met', kind='bullets', title='Where You Have Met This',
        body=['In a Spring application it is almost', 'always a controller or a view using', 'a lazy field after the transaction', 'has ended.', '', 'Exactly act one.'],
        narration=(
            'You have very likely met this in a Spring application. It is '
            'almost always a controller, or a view, using a lazy field '
            'after the transaction has ended. Exactly act one. [[slnc '
            '300]] Now you know the mechanism, not just the workaround.'
        ),
    ),
    dict(
        key='12-versions', kind='bullets', title='What Was Used',
        body=['Hibernate ORM 7.4.5.', 'H2 2.4.240.', "Versions from Spring Boot 4.1.1's", 'bill of materials.', '', 'Spring Boot itself is not used.'],
        narration=(
            'For the record. Hibernate O R M seven point four point five, '
            'and H two two point four point two forty. The versions come '
            "from Spring Boot four point one point one's bill of "
            'materials. Spring Boot itself is not used in this video.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the exception,', 'the proxy, and the statement counts', "from Hibernate's own statistics.", '', 'The database is H2 in memory.'],
        narration=(
            'The same honest admission as everywhere in this course, and '
            'again a short one. Everything is real. The exception is '
            "Hibernate's. The proxy is Hibernate's. The statement counts "
            "come from Hibernate's own statistics. The only stand-in is "
            'the database, which is H two in memory.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['If you almost always need the related', 'data, lazy loading only adds queries.'],
        narration=(
            'So when is lazy loading too much? If you almost always need '
            'the related data, it only adds queries. It earns its place '
            'when the related data is large, and rarely needed.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a batch size to the lines', 'and count the statements.'],
        narration=(
            "That's Lazy Load with Hibernate. [[slnc 250]] If you take "
            'one sentence away, take this one: a lazy field is a promise '
            'that needs a session to keep. [[slnc 350]] The full source, '
            'the written notes, the diagrams and an animated walkthrough '
            'are all in the repository. [[slnc 300]] If you try one '
            'exercise, add a batch size to the lines, and count the '
            'statements. [[slnc 300]] If this helped, a like genuinely '
            'does help other people find it, and subscribe if you would '
            'like the rest of the series. [[slnc 250]] Thanks for '
            'watching.'
        ),
    ),
]
