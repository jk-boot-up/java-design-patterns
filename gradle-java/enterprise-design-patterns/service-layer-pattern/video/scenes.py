"""Scene definitions for the Service Layer teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Service Layer',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Service Layer '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: put '
            'the operations your application offers in one layer, so '
            'every way of reaching the application calls the same code. '
            '[[slnc 350]] This is the sixth project in the enterprise '
            'category. In our online store, the question is where placing '
            'an order should live. Put a business logic in a service is '
            'advice, not a pattern, so this video shows the problem it '
            'solves. [[slnc 300]] By the end you will know what goes '
            'wrong with a second entry point, what the service owns and '
            'what the domain owns, and where the line is hard to draw.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Placing an order:', 'validate the cart, check stock,', 'take payment, write the order,', 'send an email.', '', 'Where does that code live?'],
        narration=(
            'Here is the scenario. Placing an order has five steps. '
            'Validate the cart. Check the stock. Take the payment. Write '
            'the order. Send the confirmation email. [[slnc 300]] The '
            'question this video answers is simple: where does that code '
            'live?'
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
            'The natural place to start is the web controller. It '
            'validates, reserves stock, takes payment, writes the order, '
            'and sends the email. [[slnc 300]] A good order is placed. '
            'Twenty thousand pence is charged. One email is sent. [[slnc '
            '300]] With one door into the application, this is fine. '
            'Nothing in this video says it is wrong.'
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
            'Then support asks for a command line, to place orders by '
            'phone. The quickest thing is to copy the logic. [[slnc 300]] '
            'Later, someone fixes the web door: reserve the stock first, '
            'and only then take the payment. Nobody remembers the copy. '
            '[[slnc 300]] Now the same request, five mice when three are '
            'in stock. Through the web, it is refused, and charged '
            'nothing. Through the command line, it is refused too, but '
            'the customer was already charged six thousand pence. [[slnc '
            '300]] Charged, or not, depending on which door they came '
            'through.'
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
            'The other tempting answer is to put it all in the domain '
            'object. An order dot place method. It looks tidy. [[slnc '
            '300]] But the order now needs a payment gateway, an email '
            'service, a database and the products. Its constructor takes '
            'six things. [[slnc 300]] You can see it is no longer a '
            'domain object. It is an application, in disguise.'
        ),
    ),
    dict(
        key='06-pattern', kind='bullets', title='The Pattern',
        body=['One placeOrder.', '', 'Every door calls it.', '', 'It owns the order of the steps', 'and the transaction.', '', 'The domain owns the rules.'],
        narration=(
            'The pattern is a service layer. One place order operation, '
            'and every door calls it. [[slnc 300]] The service owns the '
            'order of the steps and the transaction: begin, do the work, '
            'commit or roll back. [[slnc 300]] The domain keeps the '
            'rules. An order must not be empty. Stock must not go below '
            'zero.'
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
            'Same request, five mice when three are in stock. Through the '
            'web door: refused, charged nothing. Through the command '
            'line: refused, charged nothing. [[slnc 300]] The same '
            'answer, and not because anyone was careful. Because both '
            'doors call the same place order. They cannot disagree.'
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
            'Now the bill. First, and it needs a name: the anemic domain '
            'model. [[slnc 300]] Push too much into services, and the '
            'domain objects become bags of getters and setters, with no '
            'behaviour of their own. This anemic order has eight methods, '
            'and every one is a getter or a setter. [[slnc 300]] It is '
            'the most common shape in enterprise Java, and widely '
            'considered an anti-pattern.'
        ),
    ),
    dict(
        key='09-line', kind='bullets', title='Cost Two: The Line Is Hard To Draw',
        body=['Business rules: in the domain.', 'Orchestration: in the service.', '', 'But is free delivery over 50 pounds', 'a rule about the order,', 'or about shipping?', '', 'Reasonable teams differ.'],
        narration=(
            'The honest dividing line is this. Business rules go in the '
            'domain. Orchestration goes in the service. [[slnc 300]] But '
            'the line is genuinely hard to draw. Free delivery over fifty '
            'pounds: is that a rule about the order, or about shipping? '
            '[[slnc 300]] Here it is on the order. Another team could put '
            'it in a shipping service, and be just as right. Reasonable '
            'teams draw it differently.'
        ),
    ),
    dict(
        key='10-alternatives', kind='bullets', title='Other Ways To Organise It',
        body=['Transaction Script: one procedure', 'per operation. Roughly the naive', 'controller.', '', 'Table Module: one class per table.', '', 'Named here, not taught.'],
        narration=(
            'Two other ways of organising this logic are worth naming. '
            'Transaction Script is one procedure per operation, which is '
            'roughly what the naive controller was. Table Module is one '
            'class for each table. [[slnc 300]] This video names them and '
            'teaches neither. Both are real answers, in the right place.'
        ),
    ),
    dict(
        key='11-toydb', kind='bullets', title='The Toy Database',
        body=['Rows, a counter, transactions.', '', 'The payment gateway and the email', 'service are fakes that remember', 'what they were asked to do.'],
        narration=(
            'A word about what is real here. The database is a toy, with '
            'a transaction you can begin and roll back. The payment '
            'gateway and the email service are fakes, that remember what '
            'they were asked to do. [[slnc 300]] That is how the demo can '
            'say a customer was charged six thousand pence.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['A @Service class,', 'with @Transactional on placeOrder.', '', 'The annotation draws the transaction', 'boundary at the service.'],
        narration=(
            'You have met this. A class marked as a service, with the '
            'transactional annotation on the place order method. [[slnc '
            '300]] The annotation draws the transaction boundary at the '
            'service, which is exactly what this project did by hand.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The pattern is real.', 'The gateway and email are fakes.', 'The drift is real: it happens in', 'teams every day.'],
        narration=(
            'The same honest admission as everywhere in this course. The '
            'pattern is real. The gateway and the email are fakes. [[slnc '
            '300]] The drift is real. Copied logic drifting apart is one '
            'of the most ordinary things that happens in a team.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['One door, one operation: a service', 'layer is an extra class.', '', 'It earns its place the moment a', 'second door appears.'],
        narration=(
            'So when is it too much? For one door and one operation, a '
            'service layer is just an extra class. [[slnc 300]] It earns '
            'its place the moment a second door appears.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a third door, a batch import,', 'and count how many files change.'],
        narration=(
            "That's the Service Layer. [[slnc 250]] If you take one "
            'sentence away, take this one: rules in the domain, '
            'orchestration in the service, and every door calls the '
            'service. [[slnc 350]] The full source, the written notes, '
            'the diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'add a third door, a batch import, and count how many files '
            'change. [[slnc 300]] If this helped, a like genuinely does '
            'help other people find it, and subscribe if you would like '
            'the rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
