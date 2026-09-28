"""Scene definitions for the Layered Architecture with Spring Boot teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Layered Architecture with Spring Boot',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Layered Architecture pattern, in Java, using Spring Boot. '
            '[[slnc 300]] This video is presented by Jayasekhar Konduru. '
            '[[slnc 600]] First, a simple definition. [[slnc 300]] A '
            'layered architecture splits a program into stacked layers. '
            '[[slnc 300]] Each layer may only depend on the layer '
            'directly beneath it. [[slnc 500]] In Spring Boot, the usual '
            'layers are controllers, services, and repositories. [[slnc '
            '300]] But the rule about who may depend on whom is still '
            'yours to enforce. [[slnc 600]] Think of a restaurant again. '
            '[[slnc 300]] The waiter takes the order, the chef cooks it, '
            'and the store room holds the food. [[slnc 300]] Spring gives '
            'everyone a name badge. [[slnc 300]] But the badges do not '
            'stop the waiter walking into the store room. [[slnc 700]] '
            'This is the framework version of the Layered Architecture '
            'video, with the same online store. [[slnc 400]] We will send '
            'one real web request through four layers, inside a real '
            'transaction. [[slnc 300]] Then we will see a shortcut that '
            'Spring accepts without complaint, and the test that catches '
            'it.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Layered Architecture, the hand-built', 'video, arranges placing an order', 'into four layers with one rule.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Layered Architecture video. [[slnc '
            '400]] That one splits placing an order into four layers: '
            'presentation, application, domain, and infrastructure. '
            '[[slnc 300]] With one rule about who may depend on whom. '
            '[[slnc 500]] If you are new to the pattern, watch that one '
            'first. [[slnc 400]] Here, we keep the same example, and ask '
            'what Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new: Spring Boot,', 'a web server and an in-memory', 'database.', '', 'Plus ArchUnit, which checks the', 'layering rule.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Three things are new in this project. [[slnc 400]] One. '
            '[[slnc 200]] Spring Boot, a framework that assembles a web '
            'application. [[slnc 300]] Its controllers, services and '
            'repositories are the presentation, application and '
            'infrastructure layers. [[slnc 400]] Two. [[slnc 200]] A real '
            'web server, and an in-memory database. [[slnc 400]] Three. '
            '[[slnc 200]] ArchUnit, a library that checks the layering '
            'rule in a test. [[slnc 500]] And one promise. [[slnc 300]] '
            'If you skip this video, you lose none of the pattern. [[slnc '
            '300]] This one is about the tool.'
        ),
    ),
    dict(
        key='04-one', kind='console', title='Four Layers, One Real Request',
        body="""ONE. A real request.
  POST /orders: 201.
  stock: 4.

  controller, service,
  repository, record.""",
        narration=(
            'First demo: one real request. [[slnc 400]] A real web '
            'request asks the shop to create an order. [[slnc 300]] The '
            'answer is two hundred and one, meaning created, and the '
            'stock drops to four. [[slnc 500]] On its way, the request '
            'passed through each layer in turn. [[slnc 300]] The '
            'controller received it. [[slnc 300]] The service ran the '
            'checkout. [[slnc 300]] The repository stored the order. '
            '[[slnc 400]] Each of those is one layer, marked by a Spring '
            'annotation.'
        ),
    ),
    dict(
        key='05-tx', kind='console', title='One Transaction',
        body="""TWO. A transaction.
  card declined: 402.
  the stock reservation was
  rolled back.

  the service owns the
  transaction.""",
        narration=(
            'Second demo: a transaction. [[slnc 400]] This time, the '
            'stock is reserved first, and then the card is declined. '
            '[[slnc 400]] The customer gets four hundred and two, meaning '
            'payment required. [[slnc 300]] And the stock goes back to '
            'what it was. [[slnc 500]] Why? [[slnc 300]] Because the '
            'service wraps the whole checkout in a transaction. [[slnc '
            '300]] When the payment fails, the transaction undoes the '
            'reservation. [[slnc 400]] That is why the transaction '
            'belongs in the application layer, the service.'
        ),
    ),
    dict(
        key='06-map', kind='console', title='Failures Become Statuses In One Place',
        body="""THREE. Statuses.
  ten machines, four left:
  422.

  the domain named the reason.
  presentation chose the number.""",
        narration=(
            'Third demo: turning failures into status codes. [[slnc 400]] '
            'A customer asks for ten coffee machines, but only four are '
            'left. [[slnc 300]] The answer is four hundred and '
            'twenty-two, meaning the request cannot be processed. [[slnc '
            '500]] Notice who decided what. [[slnc 300]] The domain only '
            'said: out of stock. [[slnc 300]] One class in the '
            'presentation layer decided which number that becomes.'
        ),
    ),
    dict(
        key='07-short', kind='console', title='The Shortcut Runs',
        body="""FOUR. The shortcut.
  GET /raw-orders/...: 200.

  a controller reading the
  repository directly.

  Spring did not object.""",
        narration=(
            'Fourth demo: the shortcut. [[slnc 400]] Someone writes a '
            'controller that reads the repository directly, skipping the '
            'service. [[slnc 500]] The application starts. [[slnc 300]] '
            'The shortcut answers requests, with two hundred, meaning OK. '
            '[[slnc 400]] Spring connects objects by their type, and it '
            'does not mind at all. [[slnc 300]] Ten minutes to write, and '
            'nothing objects.'
        ),
    ),
    dict(
        key='08-leak', kind='console', title='It Also Leaks',
        body="""FIVE. A leak.
  shortcut: cost price shown.
  layered answer: hidden.

  the layer between them was
  doing a job.""",
        narration=(
            'Fifth demo: the shortcut also leaks data. [[slnc 400]] It '
            'returns the stored record exactly as it is. [[slnc 300]] And '
            'that record includes the cost price, what the shop paid for '
            'the item. [[slnc 500]] The proper, layered answer returns a '
            'response object instead. [[slnc 300]] And that object leaves '
            'the cost price out. [[slnc 500]] So the layer in the middle '
            'was doing a job you could not see, until it was skipped.'
        ),
    ),
    dict(
        key='09-rule', kind='console', title='A Rule The Container Does Not Have',
        body="""SIX. The rule.
  the layering rule: 3
  violations.

  all in ShortcutController.

  the real layers: none.""",
        narration=(
            'Last demo: a rule that Spring does not have. [[slnc 400]] A '
            'test states which layer may depend on which. [[slnc 400]] We '
            'run it over the whole project. [[slnc 300]] It finds three '
            'violations. [[slnc 300]] All three are in the shortcut '
            'controller. [[slnc 300]] The four real layers have none. '
            '[[slnc 600]] Spring connects objects by type. [[slnc 300]] '
            'Only a test can say that a dependency is not allowed.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Packages as layers.', '', 'The transaction in the service.', '', 'Response objects, not entities.', '', 'A layering test in the build.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Keep each layer in its '
            'own package. [[slnc 300]] Put the transaction in the '
            'service. [[slnc 300]] Return response objects, not stored '
            'records. [[slnc 300]] And run a layering test with every '
            'build.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['RestController, Service and', 'Repository in separate packages.', '', '@Transactional on a service.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for classes marked Rest Controller, Service, and '
            'Repository, in separate packages. [[slnc 300]] And look for '
            'the at Transactional annotation on a service method.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Most Spring Boot applications', 'you will ever open.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In most Spring '
            'Boot applications you will ever open.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1, H2 and', 'ArchUnit 1.5.0.', '', 'A real web server on a free port.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] The H2 database. '
            '[[slnc 300]] And ArchUnit one point five. [[slnc 300]] With '
            'a real web server, on a free port.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real web server,', 'real HTTP, a real database and a', 'real transaction.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything in it is real. [[slnc 300]] A real web server, '
            'real web requests, a real database, and a real transaction.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a small script with one table,', 'four layers are more ceremony', 'than help.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a small script '
            'with a single table, four layers are more ceremony than '
            'help.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a class that breaks the rule', 'and run the test.'],
        narration=(
            "That's Layered Architecture with Spring Boot. [[slnc 400]] "
            'If you remember one sentence, make it this one. [[slnc 300]] '
            'Spring names the layers, but only a test can say which '
            'dependencies are forbidden. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Add a class that breaks the layering '
            'rule. [[slnc 300]] Then run the test, and listen to what it '
            'reports. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
