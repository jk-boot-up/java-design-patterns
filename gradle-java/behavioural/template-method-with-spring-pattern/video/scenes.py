"""Scene definitions for the Template Method with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Template Method with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Template Method pattern, in Java, using Spring Boot. [[slnc '
            '300]] This video is presented by Jayasekhar Konduru. [[slnc '
            '600]] First, a simple definition. [[slnc 300]] The Template '
            "Method pattern fixes the order of a task's steps in one "
            'place, and leaves only certain steps to be filled in. [[slnc '
            '500]] In Spring, a template class owns the fixed steps of a '
            'task. [[slnc 300]] You hand it a small function for the one '
            'step that differs. [[slnc 600]] Think of a car wash. [[slnc '
            '300]] It always soaps, rinses, and dries, in that order. '
            '[[slnc 300]] You only choose the extras, like wax. [[slnc '
            '700]] This is the framework version of the Template Method '
            'video, in the same online shop. [[slnc 400]] We will hear '
            'plain database code leak a connection. [[slnc 300]] Then the '
            "same query through Spring's JDBC template, which never "
            'leaks. [[slnc 300]] And a transaction template that undoes a '
            'half-finished checkout.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Template Method, the hand-built video,', 'fixes the order of fulfilment steps', 'in one final method, and lets three', 'routes fill in the holes.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Template Method video. [[slnc 400]] '
            "That one fixes the order of an order's fulfilment steps in "
            'one final method. [[slnc 300]] And three routes fill in the '
            'steps, through inheritance. [[slnc 500]] If you are new to '
            'the pattern, watch that one first. [[slnc 400]] Here, we ask '
            'what Spring Boot does with the same idea.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot,', 'with its JDBC support and an', 'in-memory H2 database.', '', 'JdbcTemplate is the template.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'One thing is new in this project: Spring Boot. [[slnc 400]] '
            'We use its database support, and a small in-memory database '
            "called H2. [[slnc 500]] Spring's JDBC template owns the "
            'fixed steps of a database call. [[slnc 300]] Opening a '
            'connection, running the query, and closing everything. '
            '[[slnc 300]] It asks you only for the part that differs. '
            '[[slnc 500]] And one promise. [[slnc 300]] If you skip this '
            'video, you lose none of the pattern. [[slnc 300]] This one '
            'is about the tool.'
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
            'First demo: the problem the pattern solves. [[slnc 400]] '
            'Plain database code opens a connection, runs the query, '
            'reads the rows, and then closes the connection. [[slnc 300]] '
            'In that order. [[slnc 500]] With a good query, no connection '
            'is left in use. [[slnc 400]] But with one typo in the query, '
            'the code fails before it reaches the close. [[slnc 300]] One '
            'connection is left in use, forever. [[slnc 400]] The pool '
            'only has two connections. [[slnc 300]] So after two typos, '
            'the pool is empty, and the whole shop stops.'
        ),
    ),
    dict(
        key='05-template', kind='console', title='The Template Closes On Every Path',
        body="""TWO. The template.
  good query: 0 in use.

  the same typo, three times:
  0 in use.""",
        narration=(
            'Second demo: the same query, through the template. [[slnc '
            '400]] With a good query, no connection is left in use. '
            '[[slnc 400]] With the same typo, three times over, still '
            'none are left in use. [[slnc 500]] The template closes the '
            'connection on every path, including failures. [[slnc 300]] '
            'Because closing is one of its fixed steps.'
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
            'Third demo: what is left for us to write. [[slnc 400]] We '
            "ask for Asha's orders, and get two. [[slnc 500]] The only "
            'code we wrote is one small function. [[slnc 300]] It turns '
            'one database row into one order. [[slnc 500]] The template '
            'did everything else. [[slnc 300]] It opened the connection, '
            'prepared the query, filled in the customer, ran it, walked '
            'through the rows, and closed everything. [[slnc 500]] That '
            'is the pattern. [[slnc 300]] The template is the fixed '
            'sequence. [[slnc 300]] Our small function fills the one gap.'
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
            'Fourth demo: errors, translated. [[slnc 400]] With plain '
            'code, a typo gives a checked error with a database-specific '
            'code. [[slnc 400]] Through the template, the same typo '
            'becomes a Bad SQL Grammar exception. [[slnc 300]] It is '
            'unchecked, and it is the same on every database. [[slnc '
            '400]] And a repeated order number becomes a Duplicate Key '
            'exception. [[slnc 500]] So you catch errors by their '
            "meaning, not by a vendor's code."
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
            'Fifth demo: what the template decides for you. [[slnc 400]] '
            'We ask for exactly one row. [[slnc 300]] If none is found, '
            'that is an error. [[slnc 300]] If two are found, that is '
            'also an error. [[slnc 500]] Nothing in our code said so. '
            '[[slnc 300]] The template decided that a missing row is an '
            'error, not an empty value. [[slnc 300]] That is fine, but '
            'you should know it, because it affects every caller.'
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
            'Last demo: a transaction is a template too. [[slnc 400]] The '
            'transaction template owns three fixed steps: begin, commit, '
            'and roll back. [[slnc 500]] At the start, there are three '
            'orders, and three mugs in stock. [[slnc 300]] A good '
            'checkout makes it four orders, and one mug. [[slnc 500]] '
            'Then a checkout for four mugs begins. [[slnc 300]] It saves '
            'the order first, and then fails, because there is not enough '
            'stock. [[slnc 500]] Afterwards, there are still four orders, '
            'and one mug. [[slnc 300]] The half-finished order was rolled '
            'back. [[slnc 300]] The template did that for us.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Use the template.', '', 'Learn what it decides for you.', '', 'Keep the lambda small.', '', 'Catch the translated exceptions.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use the template, not '
            'the raw database interface. [[slnc 300]] Learn what it '
            'decides for you. [[slnc 300]] Keep your small function '
            'small. [[slnc 300]] And catch the translated errors, not '
            'vendor codes.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['jdbcTemplate.query with a lambda.', '', 'transactionTemplate.execute.', '', 'Any Spring class ending in Template.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a JDBC template query, with a small function '
            "passed in. [[slnc 300]] Look for a transaction template's "
            'execute method. [[slnc 300]] Or any Spring class whose name '
            'ends in Template.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every Spring class ending in', 'Template.', '', 'Each owns the fixed steps of talking', 'to something.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In every Spring '
            'class whose name ends in Template. [[slnc 300]] Each one '
            'owns the fixed steps of talking to something, and asks you '
            'only for the step that differs.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1, with JDBC', 'and an in-memory H2 database.', '', 'No web server.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one, with its database support, '
            'and an in-memory H2 database. [[slnc 300]] No web server.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real pool,', 'a real database, real exceptions.', '', 'Connections are counted, never timed.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything in it is real. [[slnc 300]] A real connection '
            'pool, a real database, and real errors. [[slnc 300]] '
            'Connections are counted, never timed.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For one query in a script, plain JDBC', 'with try-with-resources is fine.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For one query in a '
            'small script, plain database code with try-with-resources is '
            'fine. [[slnc 300]] The template earns its place when many '
            'callers repeat the same fixed steps.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add try-with-resources to the', 'by-hand method and rerun act one.'],
        narration=(
            "That's Template Method with Spring. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'Spring template owns the fixed steps, and quietly makes some '
            'decisions for you. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Add try-with-resources to the plain database '
            'method. [[slnc 300]] Then run the first demo again, and '
            'count the connections left in use. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
