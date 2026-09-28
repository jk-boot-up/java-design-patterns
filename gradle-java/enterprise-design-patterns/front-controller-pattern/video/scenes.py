"""Scene definitions for the Front Controller teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Front Controller',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Front Controller pattern, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A front controller is a '
            'single entry point that every request passes through. [[slnc '
            '300]] The shared work is done once, right there. [[slnc '
            '300]] Logging, checking who is asking, finding the right '
            'handler, and dealing with failures. [[slnc 600]] Think of '
            'the reception desk in an office building. [[slnc 300]] Every '
            'visitor signs in there, and is checked, before being sent to '
            'the right floor. [[slnc 700]] In our online store, every '
            "visitor's web request arrives here first. [[slnc 500]] In "
            'this video, handlers that look after themselves forget a '
            'security check. [[slnc 300]] Then one front door does that '
            'work once. [[slnc 300]] We will hear routing from a single '
            'table, logging of refused requests, and a failure hidden '
            'safely from the customer. [[slnc 300]] And then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=["The store's web app has pages:", 'products, orders, account.', '', 'Every request must be logged.', 'Every private page needs a', 'signed-in visitor.', '', 'Who does that work?'],
        narration=(
            "Here is the scenario. [[slnc 400]] The online store's web "
            'application has pages for products, orders, and the '
            "customer's account. [[slnc 500]] Every request must be "
            'logged. [[slnc 300]] And every private page needs the '
            'visitor to be signed in. [[slnc 500]] So here is the '
            'question. [[slnc 300]] Who does that work?'
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
            'First, the naive way: every handler looks after itself. '
            '[[slnc 400]] The orders handler was written in a hurry, and '
            'has no sign-in check. [[slnc 300]] So a visitor who is not '
            "signed in receives Ada's orders. [[slnc 500]] The account "
            'handler does check, and refuses with four hundred and one, '
            'meaning not signed in. [[slnc 300]] But it only logs '
            'requests it accepts. [[slnc 500]] So neither request left a '
            'log line.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One entry point for every', 'request.', '', 'Filters run first: log, check', 'who is asking.', '', 'A routing table finds the', 'handler.', '', 'Failure is answered once.'],
        narration=(
            'Now, the pattern. [[slnc 400]] One entry point for every '
            'request. [[slnc 500]] Filters run first. [[slnc 300]] One '
            'logs the request. [[slnc 300]] Another checks who is asking. '
            '[[slnc 500]] Then a routing table finds the right handler. '
            '[[slnc 300]] And any failure is answered once, in one place. '
            '[[slnc 500]] The handlers only do their own work.'
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
            'Second demo: one entry point. [[slnc 400]] Through the front '
            'controller, the orders page without signing in is refused, '
            'with four hundred and one. [[slnc 300]] The orders page, '
            'when signed in, is served, with two hundred, meaning OK. '
            '[[slnc 300]] The products page is marked as public, so it '
            'needs neither. [[slnc 500]] The sign-in check is written '
            'once. [[slnc 300]] No handler can forget it, because no '
            'handler has it.'
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
            'Third demo: routes in one table. [[slnc 400]] A page that '
            'does not exist gets four hundred and four, meaning not '
            'found. [[slnc 300]] A request with the wrong method gets '
            'four hundred and five, meaning not allowed. [[slnc 500]] '
            'Both come from the routing table, in one place. [[slnc 300]] '
            'So every unknown request is answered the same way.'
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
            'Fourth demo: everything is logged. [[slnc 400]] Three '
            'requests, and three log lines. [[slnc 300]] A refused '
            'request to orders. [[slnc 200]] An accepted request to '
            'orders. [[slnc 200]] And a request to a page that does not '
            'exist. [[slnc 500]] Logging is a filter that runs first. '
            '[[slnc 300]] So it sees everything, including requests that '
            'never reach a handler.'
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
            'Fifth demo: failures are handled once. [[slnc 400]] A '
            'handler throws an error, and its message happens to include '
            'a password. [[slnc 500]] The customer sees a plain five '
            'hundred: something went wrong. [[slnc 300]] The full detail '
            'goes to the log, and only the log. [[slnc 300]] The password '
            'never reaches the customer.'
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
            'Finally, the cost: one door. [[slnc 400]] One filter has a '
            'bug in it. [[slnc 500]] Now the products page, the orders '
            'page, and the account page all fail at once, with five '
            'hundred. [[slnc 500]] The front controller is the one place '
            'everything depends on. [[slnc 300]] Every request passes '
            'through it. [[slnc 300]] So a mistake in it is a mistake '
            'everywhere.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A single servlet or dispatcher', 'mapped to every path.', '', 'A filter chain, or middleware, in', 'front of the handlers.', '', 'A routing table or annotations', 'that map paths to methods.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a single servlet, or dispatcher, that '
            'receives every path. [[slnc 300]] Look for a chain of '
            'filters, or middleware, in front of the handlers. [[slnc '
            '300]] Look for a routing table, or annotations that map '
            'paths to methods. [[slnc 300]] In Spring, this is the '
            "Dispatcher Servlet. [[slnc 300]] In Node's Express, it is "
            'app dot use.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a front controller for any', 'application with several pages or', 'endpoints and shared concerns:', 'sign in, logging, error handling,', 'routing. Keep filters small,', 'ordered, and well tested, because', 'everything depends on them. Keep', 'handlers free of the shared work.', 'Most web frameworks give you one'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a front controller '
            'for any application with several pages, and shared work. '
            '[[slnc 300]] Such as signing in, logging, error handling, '
            'and routing. [[slnc 500]] Keep the filters small, in a clear '
            'order, and well tested, because everything depends on them. '
            '[[slnc 300]] Keep the handlers free of the shared work. '
            '[[slnc 500]] Most web frameworks already give you one. '
            '[[slnc 300]] So learn the one you have.'
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
        body=['For a program with one endpoint, a', 'front controller is a door in', 'front of a door. Its risk is being', 'a single point of failure, so keep', 'it simple and tested.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a program with '
            'just one endpoint, a front controller is a door in front of '
            'a door. [[slnc 400]] And its main risk is being a single '
            'point of failure. [[slnc 300]] So keep it simple, and '
            'tested.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Front Controller pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'front controller does the shared work of every request once, '
            'and becomes the one thing everything depends on. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Add a filter that '
            'limits how many requests a visitor can make. [[slnc 300]] '
            'And decide where in the order it should run. [[slnc 500]] If '
            'this helped, a like really does help other people find it. '
            "[[slnc 300]] And subscribe, if you'd like the rest of the "
            'series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
