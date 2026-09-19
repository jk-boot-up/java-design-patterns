"""Scene definitions for the Template Method with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Template Method with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Template Method '
            'pattern with Spring Boot, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Template Method video. That one '
            "fixed the order of an order's fulfilment steps in one final "
            'method, and let three routes fill in the holes. This one '
            'shows the same idea inside Spring Boot. [[slnc 350]] The '
            'plain definition, in short: in Spring, a template owns the '
            'fixed steps of a task, and you hand it a small function for '
            'the one step that differs. [[slnc 300]] By the end you will '
            'see plain database code leak a connection, see the same '
            'query through JdbcTemplate never leak, and see a transaction '
            'template roll back a half-finished checkout.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Template Method, the hand-built video,', 'fixes the order of fulfilment steps', 'in one final method, and lets three', 'routes fill in the holes.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Template Method video. If you have '
            'not seen it, start there. It fixes the order of the '
            'fulfilment steps in one final method, and lets three routes '
            'fill in the holes, by inheritance. [[slnc 300]] This one '
            'uses the same example. It does not teach the pattern again. '
            'It shows what Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot,', 'with its JDBC support and an', 'in-memory H2 database.', '', 'JdbcTemplate is the template.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'is a framework whose core is a container that creates your '
            'objects. Its JDBC support has a template that owns opening, '
            'running and closing a database call, and asks you only for '
            'the part that differs. [[slnc 300]] And a promise: skipping '
            'this video loses none of the pattern. The hand-built one '
            'teaches all of it.'
        ),
    ),
    dict(
        key='04-leak', kind='console', title='Plain JDBC Leaks',
        body="""ONE. Plain JDBC.
  good query: 0 in use.
  typo: JdbcSQLSyntaxError,
  1 connection in use.

  two in the pool. two typos,
  and it is empty.""",
        narration=(
            'First, the problem the pattern solves. Plain database code '
            'opens a connection, runs the query, walks the rows, and '
            'closes, in that order. On a good query, no connection is '
            'left in use. [[slnc 300]] With one typo in the SQL, the code '
            'throws before it reaches the close. One connection stays in '
            'use. The pool has two. Two typos, and the pool is empty.'
        ),
    ),
    dict(
        key='05-template', kind='console', title='The Template Closes On Every Path',
        body="""TWO. The template.
  good query: 0 in use.

  the same typo, three times:
  0 in use.""",
        narration=(
            'Second, the same query through the template. A good query '
            'leaves none in use. The same typo, three times over, still '
            'leaves none in use. The template closes on every path, '
            'because closing is one of its fixed steps.'
        ),
    ),
    dict(
        key='06-ours', kind='console', title='What Is Ours',
        body="""THREE. What is ours.
  asha's orders: two.

  we wrote one lambda: a row
  becomes an Order.

  the template did the rest.""",
        narration=(
            "Third, what is ours. Ask for Asha's orders and you get two. "
            'The only code we wrote is one lambda, which turns a row into '
            'an order. The template opened the connection, prepared the '
            'statement, bound the customer, ran it, walked the rows, and '
            'closed everything. [[slnc 300]] That is the pattern. The '
            'template is the skeleton. The lambda is the hole.'
        ),
    ),
    dict(
        key='07-errors', kind='console', title='Exceptions, Translated',
        body="""FOUR. Exceptions.
  by hand: a checked exception,
  SQL state 42S02.

  template: BadSqlGrammar,
  unchecked.

  duplicate: DuplicateKey.""",
        narration=(
            'Fourth, exceptions. By hand, a typo gives a checked '
            "exception, with a vendor's state code. Through the template, "
            'it becomes a bad SQL grammar exception, unchecked, and the '
            'same on every database. A repeated order number becomes a '
            'duplicate key exception. You catch by meaning, not by vendor '
            'code.'
        ),
    ),
    dict(
        key='08-decides', kind='console', title='What The Template Decides',
        body="""FIVE. Decisions.
  one row expected, none:
  EmptyResultDataAccess.

  one row expected, two:
  IncorrectResultSize.

  the template decided.""",
        narration=(
            'Fifth, what the template decides for you. Ask for exactly '
            'one row. None found is an exception. Two found is an '
            'exception. [[slnc 300]] Nothing in your code says so. The '
            'template decided that a missing row is an error, not a null. '
            'That is fine, but you should know it, because it shapes '
            'every caller.'
        ),
    ),
    dict(
        key='09-tx', kind='console', title='A Transaction Is A Template Too',
        body="""SIX. A transaction.
  before: 3 orders, 3 mugs.
  good checkout: 4 orders,
  1 mug.

  a checkout for 4 mugs fails.
  4 orders, 1 mug: the order
  row was rolled back.""",
        narration=(
            'Last, a transaction is a template too. The transaction '
            'template owns begin, commit and roll back. A good checkout '
            'takes the orders from three to four and the mugs from three '
            'to one. A checkout for four mugs inserts an order first, '
            'then fails on the stock. [[slnc 300]] Afterwards there are '
            'still four orders, and one mug. The order row was rolled '
            'back. The template did that.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Use the template.', '', 'Learn what it decides for you.', '', 'Keep the lambda small.', '', 'Catch the translated exceptions.'],
        narration=(
            'My verdict, plainly. Use the template, not the raw API. '
            'Learn what it decides for you. Keep the lambda small. And '
            'catch the translated exceptions, not vendor codes.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['jdbcTemplate.query with a lambda.', '', 'transactionTemplate.execute.', '', 'Any Spring class ending in Template.'],
        narration=(
            'How do you recognise this in code you did not write? A call '
            'to the JDBC template with a lambda. A transaction template '
            'execute. Or any Spring class whose name ends in template.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every Spring class ending in', 'Template.', '', 'Each owns the fixed steps of talking', 'to something.'],
        narration=(
            'You have met this in every Spring class whose name ends in '
            'template. Each owns the fixed steps of talking to something, '
            'and asks for the step that differs.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1, with JDBC', 'and an in-memory H2 database.', '', 'No web server.'],
        narration=(
            'For the record. Spring Boot four point one point one, with '
            'JDBC and an in memory H2 database. No web server.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real pool,', 'a real database, real exceptions.', '', 'Connections are counted, never timed.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: a real pool, a real database, real '
            'exceptions. Connections are counted, never timed.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For one query in a script, plain JDBC', 'with try-with-resources is fine.'],
        narration=(
            'So when is it too much? For one query in a script, plain '
            'JDBC with try with resources is fine. The template earns its '
            'place when many callers repeat the fixed steps.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add try-with-resources to the', 'by-hand method and rerun act one.'],
        narration=(
            "That's Template Method with Spring. [[slnc 250]] If you take "
            'one sentence away, take this one: a Spring template owns the '
            'fixed steps, and quietly makes some decisions for you. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, add try '
            'with resources to the by hand method, and rerun act one. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
