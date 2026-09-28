"""Scene definitions for the Lazy Load with Hibernate teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Lazy Load with Hibernate',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Lazy Load pattern, in Java, using Hibernate. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A lazy field does '
            'not hold its data straight away. [[slnc 300]] It holds a '
            'stand-in, which loads the data the first time someone asks. '
            '[[slnc 600]] Think of a gift voucher. [[slnc 300]] It is not '
            'the gift itself. [[slnc 300]] It only turns into the gift if '
            'you redeem it while the shop is still open. [[slnc 700]] '
            'This is the framework version of the Lazy Load video. [[slnc '
            '300]] And it is about one of the most searched Java errors '
            'there is: the Lazy Initialization Exception. [[slnc 500]] By '
            'the end, you will know exactly what is in a lazy field. '
            '[[slnc 300]] Why asking after the session has closed fails. '
            '[[slnc 300]] And what each of the three usual fixes costs.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Lazy Load, the hand-built video,', 'built four lazy variants and a', 'session-closed failure from', 'plain Java.', '', 'This video uses the same store', 'and shows what Hibernate does.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Lazy Load video. [[slnc 400]] That '
            'one builds four ways of loading later, by hand, and shows a '
            'failure once the session has closed. [[slnc 500]] Here, we '
            'use the very same store. [[slnc 300]] Five customers, twenty '
            'orders, and four lines in each order. [[slnc 300]] We will '
            'not teach the pattern again. [[slnc 300]] Instead, we hear '
            'the real error, from Hibernate itself.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['Two things are new: Hibernate and H2.', '', 'Hibernate turns operations on objects', 'into SQL. H2 is a database that runs', 'inside the test, so nothing is installed.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Two things are new in this project. [[slnc 400]] First, '
            'Hibernate, the most widely used implementation of J P A, '
            "Java's standard for storing objects. [[slnc 300]] You mark "
            'your classes, and it turns work on those objects into '
            'database commands. [[slnc 500]] Second, H2, a database that '
            'runs in memory, inside the test, so nothing needs '
            'installing. [[slnc 500]] And one promise. [[slnc 300]] If '
            'you skip this video, you lose none of the pattern. [[slnc '
            '300]] This one explains an error.'
        ),
    ),
    dict(
        key='04-lazy-word', kind='bullets', title='One Word Makes It Lazy',
        body=['@ManyToOne(fetch = LAZY)', '', "An order's customer, and its lines,", 'are both declared lazy.', '', 'That one word is what this', 'whole video is about.'],
        narration=(
            'Here is the one word that matters. [[slnc 400]] On the order '
            "class, the customer, and the order's lines, are both marked "
            'with fetch type lazy. [[slnc 500]] That one word is what '
            'this whole video is about.'
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
            'First demo: the error, on purpose. [[slnc 400]] Load an '
            'order. [[slnc 300]] Close the session. [[slnc 300]] Then ask '
            "the order for its customer's name. [[slnc 500]] The order "
            'loaded fine. [[slnc 300]] But asking for the name threw a '
            'Lazy Initialization Exception. [[slnc 300]] The message '
            'says: could not initialise proxy, customer number one, no '
            'session. [[slnc 500]] Notice where it failed. [[slnc 300]] '
            'Not where the order was loaded, but where the customer was '
            'used. [[slnc 300]] That is why this error is so hard to '
            'track down.'
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
            'So what is actually in that field? [[slnc 400]] Not a '
            'customer. [[slnc 500]] Hibernate generated a subclass of the '
            'customer class. [[slnc 300]] It holds just two things: the '
            "customer's I D, and a link to the session. [[slnc 300]] It "
            'has not loaded anything yet. [[slnc 500]] Ask it for the '
            'name while the session is open, and it loads the customer. '
            '[[slnc 300]] Close the session first, and it has nothing to '
            'load with. [[slnc 500]] That is the error. [[slnc 300]] Not '
            'a bug, but a promise that needed something that is now gone.'
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
            'The first usual fix: keep the session open while the page is '
            'built. [[slnc 300]] It works. [[slnc 500]] Twenty orders, '
            "each showing its customer's name: six database queries, not "
            'twenty-one. [[slnc 300]] One for the orders, and one for '
            'each of the five different customers. [[slnc 300]] Because '
            'the session loads each customer only once. [[slnc 500]] But '
            'twenty orders, each showing how many lines it has: '
            'twenty-one queries. [[slnc 300]] One for the orders, then '
            "one for each order's lines. [[slnc 300]] That is the N plus "
            'one problem. [[slnc 500]] The cost: the session, and its '
            'database connection, stay open while the page is built. '
            '[[slnc 300]] And the extra queries hide inside the page '
            'code, where nobody looks.'
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
            'The second fix: fetch the related data in the same query, '
            'with a join fetch. [[slnc 500]] One query for the customers. '
            '[[slnc 300]] And one query for the lines. [[slnc 500]] But '
            'there is a hidden cost. [[slnc 300]] Fetching the lines '
            'makes the database send eighty rows for twenty orders. '
            '[[slnc 300]] Each order is repeated, once for each of its '
            'four lines. [[slnc 300]] Hibernate folds them back together '
            'for you. [[slnc 500]] And every caller of that query now '
            'gets the lines, whether it wanted them or not.'
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
            'The third fix: ask for exactly what the page needs. [[slnc '
            '300]] This is called a projection. [[slnc 500]] One query, '
            'twenty rows, each with just an order number and a customer '
            'name. [[slnc 300]] No entity, no stand-in, and nothing lazy '
            'left to fail. [[slnc 500]] The cost: a small class for every '
            'query. [[slnc 300]] And a row is not an object with '
            'behaviour. [[slnc 300]] This is the idea from the D T O '
            'video, arriving from the other direction.'
        ),
    ),
    dict(
        key='10-not-eager', kind='bullets', title='The Fix Not On The List',
        body=['Make the mapping EAGER.', '', 'That removes the exception.', '', 'And it brings back the first act', 'of the partner video: loading one', 'order loads the shop.'],
        narration=(
            'There is a fourth fix, which is not on the list, because it '
            'needs care. [[slnc 400]] Make the relationship eager, '
            'instead of lazy. [[slnc 300]] That removes the error. [[slnc '
            '500]] But it brings back the first problem from the Lazy '
            'Load video. [[slnc 300]] Load one order, and you load the '
            'whole shop.'
        ),
    ),
    dict(
        key='11-met', kind='bullets', title='Where You Have Met This',
        body=['In a Spring application it is almost', 'always a controller or a view using', 'a lazy field after the transaction', 'has ended.', '', 'Exactly act one.'],
        narration=(
            'You have very likely met this in a Spring application. '
            '[[slnc 400]] It is almost always a controller, or a page '
            'template, using a lazy field after the transaction has '
            'ended. [[slnc 300]] Exactly the first demo. [[slnc 500]] Now '
            'you know the cause, not just the workaround.'
        ),
    ),
    dict(
        key='12-versions', kind='bullets', title='What Was Used',
        body=['Hibernate ORM 7.4.5.', 'H2 2.4.240.', "Versions from Spring Boot 4.1.1's", 'bill of materials.', '', 'Spring Boot itself is not used.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] '
            'Hibernate seven point four point five. [[slnc 300]] And H2 '
            'two point four point two forty. [[slnc 400]] These versions '
            "come from Spring Boot four point one point one's list of "
            'tested libraries. [[slnc 300]] But Spring Boot itself is not '
            'used here.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the exception,', 'the proxy, and the statement counts', "from Hibernate's own statistics.", '', 'The database is H2 in memory.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything here is real. [[slnc 300]] The error is '
            "Hibernate's. [[slnc 300]] The stand-in is Hibernate's. "
            "[[slnc 300]] And the query counts come from Hibernate's own "
            'statistics. [[slnc 400]] The only stand-in is the database, '
            'which is H2, in memory.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['If you almost always need the related', 'data, lazy loading only adds queries.'],
        narration=(
            'So, when is lazy loading too much? [[slnc 400]] If you '
            'almost always need the related data, it only adds extra '
            'queries. [[slnc 400]] It earns its place when the related '
            'data is large, and rarely needed.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a batch size to the lines', 'and count the statements.'],
        narration=(
            "That's Lazy Load with Hibernate. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A lazy '
            'field is a promise, and it needs an open session to keep it. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 500]] Here is one exercise to try. [[slnc 300]] Add a '
            'batch size setting to the order lines. [[slnc 300]] Then '
            'count the queries again. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
