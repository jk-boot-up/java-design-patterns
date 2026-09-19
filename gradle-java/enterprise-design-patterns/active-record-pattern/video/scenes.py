"""Scene definitions for the Active Record teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Active Record',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Active Record '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: an '
            'active record is an object that wraps one row of a database '
            'table. It carries the rules about that row, and it knows how '
            'to find itself, save itself and change itself. [[slnc 350]] '
            'This is another project in the enterprise category, whose '
            'subject is how a business application organises its logic, '
            'its data and its requests. In our online store, the thing '
            'that saves itself is an order. [[slnc 300]] By the end you '
            'will see an order find and save itself in three lines, see '
            'its rules sit beside its data, and then see the three bills: '
            'a rule that cannot be tested without the table, a class that '
            'is the table, and queries you cannot see.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The store keeps orders in a table.', '', 'An order has a customer, a total', 'and a status.', '', 'Created, changed as a draft,', 'placed, looked up by customer.', '', 'Who does the saving?'],
        narration=(
            'Here is the scenario. The online store keeps orders in a '
            'table. Each order has a customer, a total and a status. '
            'Orders are created, changed while they are drafts, placed, '
            'and looked up by customer. [[slnc 300]] The question: who '
            'does the saving?'
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
            'First, a record that saves itself. An order is created, '
            'saved, and found again, in three lines. Order one, for '
            'customer one, sixteen hundred pence, a draft. There is no '
            'repository and no mapper. The order is the row.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One class is one row of a table.', '', 'It finds itself and saves itself.', '', 'Finders are static methods on', 'the class.', '', 'The rules about the row are', 'written on the row.'],
        narration=(
            'The pattern. One class is one row of a table. It finds '
            'itself and saves itself. The finders are static methods on '
            'the class. And the rules about the row are written on the '
            'row, right beside the data.'
        ),
    ),
    dict(
        key='05-finders', kind='console', title='Finders On The Class',
        body="""TWO. Finders.
  Order.forCustomer(2):
  3 orders,
  totals 500, 1000, 1500.""",
        narration=(
            'Second, finders on the class. Ask the order class for one '
            "customer's orders, and it returns three, with totals of five "
            'hundred, a thousand, and fifteen hundred. The class you use '
            'to make an order is the class you use to look one up.'
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
            'Third, the rules are on the record. A placed order refuses a '
            'new line. An empty order refuses to be placed. What an order '
            'may do sits right beside what an order is. That is the '
            'appeal: one class, and everything about orders is in it.'
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
            'Fourth, the first bill. Is a sixty pound order eligible for '
            'free delivery? Written on the record, the rule loads the '
            'customer to answer, so it touches the table once. The same '
            'rule on two numbers touches nothing. To test the rule on the '
            'record, a customers table has to exist, and hold a customer.'
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
            'Fifth, the second bill. A column in the table is renamed. '
            'Loading an order now fails: the table has no column total '
            'pence. The fields of the class are the columns of the table. '
            'One cannot change without the other.'
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
            'Last, the third bill. Check five orders for free delivery, '
            'and there are five table operations, because each call loads '
            'the customer again. Each call looked innocent, and nothing '
            'in the loop shows it. With a hundred orders, it is a hundred '
            'queries.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A class with save(), find() and', 'delete() on it.', '', "Ruby on Rails' ActiveRecord, and", "Laravel's Eloquent.", '', 'JPA entities with methods that', 'reach for the database themselves.'],
        narration=(
            'How do you recognise this in code you did not write? A class '
            "with save(), find() and delete() on it. Ruby on Rails' "
            "ActiveRecord, and Laravel's Eloquent. JPA entities with "
            'methods that reach for the database themselves. Fields named '
            'exactly like columns.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use an active record when the', 'objects are close to the tables,', 'the rules are few, and speed of', 'writing matters: admin tools,', 'small services, the first version.', 'Move the rules that need no table', 'into plain functions or objects.', 'Move to a data mapper when the', 'model and the schema start to'],
        narration=(
            'Here is my verdict, plainly. Use an active record when the '
            'objects are close to the tables, the rules are few, and '
            'speed of writing matters: admin tools, small services, the '
            'first version. Move the rules that need no table into plain '
            'functions or objects. Move to a data mapper when the model '
            'and the schema start to differ, or when the logic grows.'
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
        body=['Active Record is rarely too much.', 'It is often too little once the', 'rules grow. Watch for rules that', 'need a table to test, and loops', 'that hide queries.'],
        narration=(
            'So when is it too much? Active Record is rarely too much. It '
            'is often too little once the rules grow. Watch for rules '
            'that need a table to test, and loops that hide queries.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Active Record. [[slnc 250]] If you take one sentence "
            'away, take this one: an active record is the quickest way to '
            'get data in and out, and the price is that the class and the '
            'table become one thing. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, make the delivery rule take a total '
            'instead of loading a customer, and count the table '
            'operations again. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
