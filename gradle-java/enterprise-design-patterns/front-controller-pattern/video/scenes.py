"""Scene definitions for the Front Controller teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Front Controller',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Front Controller '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'front controller is a single entry point that every request '
            'passes through. The shared work, logging, checking who is '
            'asking, finding the right handler and handling failure, is '
            'done once, there. [[slnc 350]] This is another project in '
            'the enterprise category, whose subject is how a business '
            'application organises its logic, its data and its requests. '
            'In our online store, the thing every visitor reaches first '
            'is a web request. [[slnc 300]] By the end you will see '
            'handlers that each look after themselves and one that '
            'forgets to check who is asking, then see one door do that '
            'work once, route every request from a single table, log even '
            "refused requests, and hide a failure's detail from the "
            'customer, and then see the bill, which is that everything '
            'now depends on that door.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=["The store's web app has pages:", 'products, orders, account.', '', 'Every request must be logged.', 'Every private page needs a', 'signed-in visitor.', '', 'Who does that work?'],
        narration=(
            "Here is the scenario. The online store's web application has "
            "pages for products, for orders, and for the customer's "
            'account. Every request needs to be logged. Every private '
            'page needs the visitor to be signed in. [[slnc 300]] The '
            'question: who does that work?'
        ),
    ),
    dict(
        key='03-self', kind='console', title='Every Handler Looks After Itself',
        body="""ONE. Each on its own.
  /orders, not signed in:
  200, ada's orders.
  /account, not signed in: 401.

  requests logged: 0 of 2.""",
        narration=(
            'First, every handler looks after itself. The orders handler '
            'was written on a Friday, and has no sign in check. A visitor '
            "who is not signed in receives Ada's orders. The account "
            'handler does check, but it logs only what it accepts, so '
            'neither request left a log line.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One entry point for every', 'request.', '', 'Filters run first: log, check', 'who is asking.', '', 'A routing table finds the', 'handler.', '', 'Failure is answered once.'],
        narration=(
            'The pattern. One entry point for every request. Filters run '
            'first: log the request, check who is asking. A routing table '
            'then finds the handler. And a failure is answered once, in '
            'one place. The handlers do only their own work.'
        ),
    ),
    dict(
        key='05-door', kind='console', title='One Entry Point',
        body="""TWO. One door.
  /orders, no sign-in: 401.
  /orders, signed in: 200.
  /products, public: 200.

  the check is written once.""",
        narration=(
            'Second, one entry point. Through the front controller, '
            'orders without a sign in is refused with a four oh one. '
            'Orders with a sign in is served. Products, which is listed '
            'as public, needs neither. The check is written once, and no '
            'handler can forget it, because no handler has it.'
        ),
    ),
    dict(
        key='06-routes', kind='console', title='Routes In One Table',
        body="""THREE. Routes.
  /nowhere: 404.
  POST /products: 405.

  answered the same way, in
  one place.""",
        narration=(
            'Third, routes in one table. An unknown page gets a four oh '
            'four. A wrong method gets a four oh five. Both come from the '
            'routing table, in one place, so every unknown request is '
            'answered the same way.'
        ),
    ),
    dict(
        key='07-log', kind='console', title='Everything Is Logged',
        body="""FOUR. Logged.
  GET /orders -> 401
  GET /orders -> 200
  GET /nowhere -> 404

  the refused and the missing
  are in the log.""",
        narration=(
            'Fourth, everything is logged. Three requests, and three log '
            'lines. The refused request is in the log, and so is the '
            'missing page. Logging is a filter that runs first, so it '
            'sees everything, including what never reaches a handler.'
        ),
    ),
    dict(
        key='08-fail', kind='console', title='Failures Are Handled Once',
        body="""FIVE. One handler for failure.
  a handler throws.
  the customer: 500, something
  went wrong.

  the log has the detail.
  the password never left.""",
        narration=(
            'Fifth, failures handled once. A handler throws an error, and '
            'its message includes a password. The customer sees a plain '
            'five hundred: something went wrong. The detail goes to the '
            'log, and only the log. The password never reached the '
            'customer.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill: One Door',
        body="""SIX. The bill.
  one filter with a bug.
  /products: 500.
  /orders: 500.
  /account: 500.

  every page down at once.""",
        narration=(
            'Last, the bill. One filter has a bug in it. Now the products '
            'page, the orders page and the account page all return a five '
            'hundred at once. The front controller is the one place '
            'everything depends on. Every request passes through it, so a '
            'mistake in it is a mistake in everything.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A single servlet or dispatcher', 'mapped to every path.', '', 'A filter chain, or middleware, in', 'front of the handlers.', '', 'A routing table or annotations', 'that map paths to methods.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'single servlet or dispatcher mapped to every path. A filter '
            'chain, or middleware, in front of the handlers. A routing '
            'table or annotations that map paths to methods. '
            'DispatcherServlet in Spring, app.use(...) in Express, Rack '
            'middleware in Ruby.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a front controller for any', 'application with several pages or', 'endpoints and shared concerns:', 'sign in, logging, error handling,', 'routing. Keep filters small,', 'ordered, and well tested, because', 'everything depends on them. Keep', 'handlers free of the shared work.', 'Most web frameworks give you one'],
        narration=(
            'Here is my verdict, plainly. Use a front controller for any '
            'application with several pages or endpoints and shared '
            'concerns: sign in, logging, error handling, routing. Keep '
            'filters small, ordered, and well tested, because everything '
            'depends on them. Keep handlers free of the shared work. Most '
            'web frameworks give you one already, so learn the one you '
            'have.'
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
        body=['For a program with one endpoint, a', 'front controller is a door in', 'front of a door. Its risk is being', 'a single point of failure, so keep', 'it simple and tested.'],
        narration=(
            'So when is it too much? For a program with one endpoint, a '
            'front controller is a door in front of a door. Its risk is '
            'being a single point of failure, so keep it simple and '
            'tested.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Front Controller. [[slnc 250]] If you take one "
            'sentence away, take this one: a front controller does the '
            'shared work of a request once, and becomes the one thing '
            'everything depends on. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, add a rate limit filter, and decide where '
            'in the order it should run. [[slnc 300]] If this helped, a '
            'like genuinely does help other people find it, and subscribe '
            'if you would like the rest of the series. [[slnc 250]] '
            'Thanks for watching.'
        ),
    ),
]
