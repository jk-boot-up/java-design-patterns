"""Scene definitions for the Active Record teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Active Record',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Active Record pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] An active record is an '
            'object that wraps one row of a database table. [[slnc 300]] '
            'It carries the rules about that row. [[slnc 300]] And it '
            'knows how to find itself, save itself, and change itself. '
            '[[slnc 600]] Think of a paper form that can file itself in '
            'the right drawer. [[slnc 300]] Convenient, but the form now '
            'has to know how the filing cabinet works. [[slnc 700]] In '
            'our online store, the thing that saves itself is an order. '
            '[[slnc 500]] In this video, an order finds and saves itself '
            'in three lines, with its rules right beside its data. [[slnc '
            '300]] Then we will hear three costs. [[slnc 300]] A rule you '
            'cannot test without the table, a class that is the table, '
            'and database queries you cannot see.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The store keeps orders in a table.', '', 'An order has a customer, a total', 'and a status.', '', 'Created, changed as a draft,', 'placed, looked up by customer.', '', 'Who does the saving?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The online store keeps '
            'its orders in a database table. [[slnc 300]] Each order has '
            'a customer, a total, and a status. [[slnc 500]] Orders are '
            'created, changed while they are still drafts, placed, and '
            'looked up by customer. [[slnc 500]] So here is the question. '
            '[[slnc 300]] Who does the saving?'
        ),
    ),
    dict(
        key='03-self', kind='console', title='A Record That Saves Itself',
        body="""ONE. Saves itself.
  order 1, customer 1,
  1600 pence, DRAFT.

  new, save, find.
  no repository, no mapper.""",
        narration=(
            'First demo: a record that saves itself. [[slnc 400]] An '
            'order is created, saved, and found again, in three lines. '
            '[[slnc 300]] Order one, for customer one, sixteen pounds, as '
            'a draft. [[slnc 500]] There is no repository, and no mapper. '
            '[[slnc 300]] The order is the row.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One class is one row of a table.', '', 'It finds itself and saves itself.', '', 'Finders are static methods on', 'the class.', '', 'The rules about the row are', 'written on the row.'],
        narration=(
            'Now, the pattern. [[slnc 400]] One class represents one row '
            'of a table. [[slnc 300]] It finds itself, and saves itself. '
            '[[slnc 300]] Methods for finding records are static methods '
            'on the class. [[slnc 300]] And the rules about the row are '
            'written on the row, right beside its data.'
        ),
    ),
    dict(
        key='05-finders', kind='console', title='Finders On The Class',
        body="""TWO. Finders.
  Order.forCustomer(2):
  3 orders,
  totals 500, 1000, 1500.""",
        narration=(
            'Second demo: finders on the class. [[slnc 400]] Ask the '
            "Order class for customer two's orders. [[slnc 300]] It "
            'returns three, with totals of five pounds, ten pounds, and '
            'fifteen pounds. [[slnc 500]] The same class you use to '
            'create an order is the class you use to look one up.'
        ),
    ),
    dict(
        key='06-rules', kind='console', title='The Rules Are On The Record',
        body="""THREE. The rules.
  a PLACED order cannot change.
  an empty order cannot be
  placed.

  what an order may do sits
  beside what an order is.""",
        narration=(
            'Third demo: the rules live on the record. [[slnc 400]] A '
            'placed order refuses a new line. [[slnc 300]] An empty order '
            'refuses to be placed. [[slnc 500]] What an order may do sits '
            'right beside what an order is. [[slnc 300]] That is the '
            'appeal. [[slnc 300]] One class, and everything about orders '
            'is in it.'
        ),
    ),
    dict(
        key='07-test', kind='console', title='The Bill: A Rule That Needs The Table',
        body="""FOUR. The first bill.
  is the order eligible?
  on the record: 1 table
  operation.

  the same rule on two numbers:
  0.

  testing it needs the table.""",
        narration=(
            'Fourth demo: the first cost. [[slnc 400]] Is a sixty pound '
            'order eligible for free delivery? [[slnc 500]] Written on '
            'the record, the rule loads the customer to find out. [[slnc '
            '300]] So it touches the database once. [[slnc 500]] The same '
            'rule, written as a plain function of two numbers, touches '
            'nothing. [[slnc 500]] So to test the rule on the record, a '
            'customers table must exist, and hold a customer.'
        ),
    ),
    dict(
        key='08-table', kind='console', title='The Bill: The Class Is The Table',
        body="""FIVE. The second bill.
  a column was renamed.
  loading an order fails:
  no column total_pence.

  the class is the table.""",
        narration=(
            'Fifth demo: the second cost. [[slnc 400]] A column in the '
            'table is renamed. [[slnc 300]] Loading an order now fails, '
            'because the table has no column called total pence. [[slnc '
            '500]] The fields of the class are the columns of the table. '
            '[[slnc 300]] One cannot change without the other.'
        ),
    ),
    dict(
        key='09-hidden', kind='console', title='The Bill: Queries You Cannot See',
        body="""SIX. The third bill.
  5 orders checked:
  5 table operations.

  each call looked innocent.
  each loaded the customer
  again.""",
        narration=(
            'Last demo: the third cost, queries you cannot see. [[slnc '
            '400]] Check five orders for free delivery. [[slnc 300]] That '
            'makes five database queries, because each check loads the '
            'customer again. [[slnc 500]] Each call looked innocent. '
            '[[slnc 300]] And nothing in the loop shows the queries. '
            '[[slnc 300]] With a hundred orders, it would be a hundred '
            'queries.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A class with save(), find() and', 'delete() on it.', '', "Ruby on Rails' ActiveRecord, and", "Laravel's Eloquent.", '', 'JPA entities with methods that', 'reach for the database themselves.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a class with save, find, and delete '
            "methods on it. [[slnc 300]] Look for Ruby on Rails' Active "
            "Record, or Laravel's Eloquent. [[slnc 300]] Look for entity "
            'classes with methods that reach into the database '
            'themselves. [[slnc 300]] And fields named exactly like the '
            "table's columns."
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use an active record when the', 'objects are close to the tables,', 'the rules are few, and speed of', 'writing matters: admin tools,', 'small services, the first version.', 'Move the rules that need no table', 'into plain functions or objects.', 'Move to a data mapper when the', 'model and the schema start to'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use an active record '
            'when your objects closely match your tables, the rules are '
            'few, and speed of writing matters. [[slnc 300]] Admin tools, '
            'small services, or the first version of something. [[slnc '
            '500]] Move any rule that does not need the database into a '
            'plain function or object. [[slnc 300]] And switch to a data '
            'mapper when the model and the tables start to differ, or '
            'when the logic grows.'
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
        body=['Active Record is rarely too much.', 'It is often too little once the', 'rules grow. Watch for rules that', 'need a table to test, and loops', 'that hide queries.'],
        narration=(
            'So, when is this too much? [[slnc 400]] Active Record is '
            'rarely too much. [[slnc 300]] It is more often too little, '
            'once the rules grow. [[slnc 400]] Watch for rules that need '
            'a database to test. [[slnc 300]] And loops that hide '
            'queries.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Active Record pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] An '
            'active record is the quickest way to get data in and out, '
            'and the price is that the class and the table become one '
            'thing. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Make the free delivery rule take a total, instead of '
            'loading a customer. [[slnc 300]] Then count the database '
            'queries again. [[slnc 500]] If this helped, a like really '
            'does help other people find it. [[slnc 300]] And subscribe, '
            "if you'd like the rest of the series. [[slnc 400]] Thanks "
            'for watching.'
        ),
    ),
]
