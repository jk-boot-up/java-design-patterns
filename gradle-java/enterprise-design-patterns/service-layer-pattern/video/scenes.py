"""Scene definitions for the Service Layer teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Layer',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Service Layer pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A service layer puts the '
            'operations your application offers into one layer. [[slnc '
            '300]] So every way of reaching the application calls the '
            'same code. [[slnc 600]] Think of a bank. [[slnc 300]] '
            'Whether you use the app, the cash machine, or the counter, '
            'the same rules for a withdrawal apply. [[slnc 700]] In our '
            'online store, the question is: where should placing an order '
            'live? [[slnc 500]] By the end, you will know what goes wrong '
            'when a second way in appears. [[slnc 300]] What the service '
            'owns, and what the business objects own. [[slnc 300]] And '
            'where the line between them is hard to draw.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Placing an order:', 'validate the cart, check stock,', 'take payment, write the order,', 'send an email.', '', 'Where does that code live?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Placing an order takes '
            'five steps. [[slnc 300]] Check the cart. [[slnc 200]] Check '
            'the stock. [[slnc 200]] Take the payment. [[slnc 200]] Save '
            'the order. [[slnc 200]] And send the confirmation email. '
            '[[slnc 500]] So here is the question. [[slnc 300]] Where '
            'does that code live?'
        ),
    ),
    dict(
        key='03-controller', kind='console', title='The Logic In The Controller',
        body="""ONE. In the controller.
  a good order: placed
  charged: 20000 pence,
  emails sent: 1

  with one door, this is
  fine.""",
        narration=(
            'The natural place to start is the web controller. [[slnc '
            '400]] It checks the cart, reserves stock, takes payment, '
            'saves the order, and sends the email. [[slnc 500]] A good '
            'order is placed. [[slnc 300]] Two hundred pounds is charged. '
            '[[slnc 300]] One email is sent. [[slnc 500]] With only one '
            'way into the application, this is fine. [[slnc 300]] Nothing '
            'in this video says it is wrong.'
        ),
    ),
    dict(
        key='04-second-door', kind='console', title='A Second Door',
        body="""TWO. A second door.
  5 mice wanted, 3 in stock:

  web: refused, charged 0
  CLI: refused, charged 6000

  the web door was fixed.
  the copy was not.""",
        narration=(
            'Then support asks for a command-line tool, to place orders '
            'taken by phone. [[slnc 300]] The quickest thing is to copy '
            'the logic. [[slnc 500]] Later, someone fixes the web '
            'version. [[slnc 300]] Reserve the stock first, and only then '
            'take the payment. [[slnc 300]] Nobody remembers the copy. '
            '[[slnc 500]] Now, the same request: five mice, when only '
            'three are in stock. [[slnc 300]] Through the web, it is '
            'refused, and nothing is charged. [[slnc 300]] Through the '
            'command line, it is refused too. [[slnc 300]] But the '
            'customer was already charged sixty pounds. [[slnc 500]] '
            'Charged, or not, depending on which way they came in.'
        ),
    ),
    dict(
        key='05-domain-object', kind='console', title='Put It All In The Domain Object',
        body="""THREE. In the domain object.
  Order.place() needs:
  a payment gateway,
  an email service,
  a database, the products.

  its constructor takes 6
  things.""",
        narration=(
            'The other tempting answer is to put everything into the '
            'order object itself. [[slnc 300]] An order dot place method. '
            '[[slnc 300]] It looks tidy. [[slnc 500]] But now the order '
            'needs a payment gateway, an email service, a database, and '
            'the product list. [[slnc 300]] Its constructor takes six '
            'things. [[slnc 500]] It is no longer a business object. '
            '[[slnc 300]] It is a whole application, in disguise.'
        ),
    ),
    dict(
        key='06-pattern', kind='bullets', title='The Pattern',
        body=['One placeOrder.', '', 'Every door calls it.', '', 'It owns the order of the steps', 'and the transaction.', '', 'The domain owns the rules.'],
        narration=(
            'Now, the pattern: a service layer. [[slnc 400]] There is one '
            'place order operation. [[slnc 300]] And every way in calls '
            'it. [[slnc 500]] The service owns the order of the steps, '
            'and the transaction. [[slnc 300]] Begin, do the work, then '
            'commit or roll back. [[slnc 500]] The business objects keep '
            'the rules. [[slnc 300]] An order must not be empty. [[slnc '
            '300]] Stock must not go below zero.'
        ),
    ),
    dict(
        key='07-one-door', kind='console', title='One placeOrder, Two Doors',
        body="""FOUR. The pattern.
  web: refused, charged 0
  CLI: refused, charged 0

  the same answer, because
  there is one placeOrder.""",
        narration=(
            'Fourth demo: one place order, two ways in. [[slnc 400]] The '
            'same request: five mice, with three in stock. [[slnc 300]] '
            'Through the web: refused, and nothing charged. [[slnc 300]] '
            'Through the command line: refused, and nothing charged. '
            '[[slnc 500]] The same answer. [[slnc 300]] Not because '
            'anyone was careful. [[slnc 300]] Because both call the same '
            'place order operation, so they cannot disagree.'
        ),
    ),
    dict(
        key='08-anemic', kind='console', title='Cost One: The Anemic Domain',
        body="""FIVE. The anemic model.
  AnemicOrder: 8 methods,
  all getters and setters.

  push every rule into
  services and the domain
  becomes a bag of fields.""",
        narration=(
            'Now the costs. [[slnc 300]] The first needs a name: the '
            'anemic domain model. [[slnc 500]] Push too much into '
            'services, and the business objects become bags of getters '
            'and setters, with no behaviour of their own. [[slnc 300]] '
            'This anemic order has eight methods, and every single one is '
            'a getter or a setter. [[slnc 500]] It is the most common '
            'shape in business Java code. [[slnc 300]] And it is widely '
            'considered an anti-pattern.'
        ),
    ),
    dict(
        key='09-line', kind='bullets', title='Cost Two: The Line Is Hard To Draw',
        body=['Business rules: in the domain.', 'Orchestration: in the service.', '', 'But is free delivery over 50 pounds', 'a rule about the order,', 'or about shipping?', '', 'Reasonable teams differ.'],
        narration=(
            'The second cost: the line is hard to draw. [[slnc 400]] The '
            'honest rule is this. [[slnc 300]] Business rules go in the '
            'business objects. [[slnc 300]] The sequence of steps goes in '
            'the service. [[slnc 500]] But consider free delivery over '
            'fifty pounds. [[slnc 300]] Is that a rule about the order, '
            'or about shipping? [[slnc 500]] Here, it is on the order. '
            '[[slnc 300]] Another team could put it in a shipping '
            'service, and be just as right. [[slnc 300]] Reasonable teams '
            'draw the line differently.'
        ),
    ),
    dict(
        key='10-alternatives', kind='bullets', title='Other Ways To Organise It',
        body=['Transaction Script: one procedure', 'per operation. Roughly the naive', 'controller.', '', 'Table Module: one class per table.', '', 'Named here, not taught.'],
        narration=(
            'Two other ways of organising this logic are worth naming. '
            '[[slnc 500]] Transaction Script: one procedure for each '
            'operation. [[slnc 300]] That is roughly what the naive '
            'controller was. [[slnc 400]] Table Module: one class for '
            'each database table. [[slnc 500]] This video names them, but '
            'does not teach them. [[slnc 300]] Both are good answers, in '
            'the right place.'
        ),
    ),
    dict(
        key='11-toydb', kind='bullets', title='The Toy Database',
        body=['Rows, a counter, transactions.', '', 'The payment gateway and the email', 'service are fakes that remember', 'what they were asked to do.'],
        narration=(
            'A word about what is real in this demo. [[slnc 400]] The '
            'database is a toy, with transactions you can begin, and roll '
            'back. [[slnc 300]] The payment gateway and the email service '
            'are fakes. [[slnc 300]] They remember what they were asked '
            'to do. [[slnc 500]] That is how the demo can tell you '
            'exactly how much a customer was charged.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['A @Service class,', 'with @Transactional on placeOrder.', '', 'The annotation draws the transaction', 'boundary at the service.'],
        narration=(
            'You have met this pattern before. [[slnc 400]] A class '
            'marked with the at Service annotation. [[slnc 300]] With the '
            'at Transactional annotation on its place order method. '
            '[[slnc 500]] That annotation draws the transaction boundary '
            'at the service. [[slnc 300]] Exactly what this project does '
            'by hand.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The pattern is real.', 'The gateway and email are fakes.', 'The drift is real: it happens in', 'teams every day.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'pattern is real. [[slnc 300]] The payment gateway and the '
            'email service are fakes. [[slnc 500]] But the drift is real. '
            '[[slnc 300]] Copied logic drifting apart is one of the most '
            'ordinary things that happens in a team.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['One door, one operation: a service', 'layer is an extra class.', '', 'It earns its place the moment a', 'second door appears.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For one way in, and '
            'one operation, a service layer is just an extra class. '
            '[[slnc 400]] It earns its place the moment a second way in '
            'appears.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a third door, a batch import,', 'and count how many files change.'],
        narration=(
            "That's the Service Layer pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] Rules '
            'live in the business objects, the sequence of steps lives in '
            'the service, and every way in calls the service. [[slnc '
            '500]] The full source code, written notes, diagrams, and an '
            'animated walkthrough are all in the repository. [[slnc 500]] '
            'Here is one exercise to try. [[slnc 300]] Add a third way '
            'in: a batch import of orders. [[slnc 300]] And count how '
            'many files had to change. [[slnc 500]] If this helped, a '
            'like really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
