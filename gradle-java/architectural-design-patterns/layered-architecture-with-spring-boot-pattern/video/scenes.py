"""Scene definitions for the Layered Architecture with Spring Boot teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Layered Architecture with Spring Boot',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Layered '
            'Architecture pattern with Spring Boot, in Java, and it is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] It '
            'is the framework version of the Layered Architecture video. '
            'That one arranged placing an order into presentation, '
            'application, domain and infrastructure layers, with one rule '
            'about who may depend on whom, and counted the bill for a '
            'forced change. This one shows the same idea inside Spring '
            'Boot. [[slnc 350]] The plain definition, in short: in a '
            'Spring Boot application, the layers are controllers, '
            'services and repositories, and the layering rule is yours to '
            'enforce. [[slnc 300]] By the end you will see one real HTTP '
            'request go through four layers with a real transaction, then '
            'see the shortcut Spring accepts without complaint, and the '
            'test that catches it.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Layered Architecture, the hand-built', 'video, arranges placing an order', 'into four layers with one rule.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Layered Architecture video. If you '
            'have not seen it, start there. It arranges placing an order '
            'into presentation, application, domain and infrastructure '
            'layers, with one rule about who may depend on whom. [[slnc '
            '300]] This one uses the same example. It does not teach the '
            'pattern again. It shows what Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['Three things are new: Spring Boot,', 'a web server and an in-memory', 'database.', '', 'Plus ArchUnit, which checks the', 'layering rule.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'Boot is a framework that assembles a web application. '
            'Controllers, services and repositories are its names for the '
            'presentation, application and infrastructure layers. '
            'ArchUnit is a library that checks the layering rule. [[slnc '
            '300]] And a promise: skipping this video loses none of the '
            'pattern. The hand-built one teaches all of it.'
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
            'First, a real request over HTTP. It is created, and the '
            'stock drops to four. The controller took it, the service ran '
            'it, the repository stored it. Each is one layer, marked by a '
            'Spring annotation.'
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
            'Second, the transaction. The card is declined after the '
            'stock has been reserved. The customer gets a four oh two, '
            "and the stock is unchanged. The service's transaction undid "
            'the reservation. That is why the transaction belongs in the '
            'application layer.'
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
            'Third, statuses. Ten machines when four are left is refused '
            'with four twenty two. The domain only said out of stock. One '
            'class in the presentation layer decides what number that '
            'becomes.'
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
            'Fourth, the shortcut. A controller reads the repository '
            'directly, skipping the service. It starts. It answers. '
            'Spring wires by type, and it does not mind. Ten minutes to '
            'write, and nothing objects.'
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
            'Fifth, the shortcut also leaks. It returns the record as it '
            'is, and the record includes what the shop paid. The layered '
            'answer is a response object, with no cost. The layer in the '
            'middle was doing a job you could not see.'
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
            'Last, the rule. A test states which layer may depend on '
            'which. Run over the whole project, it finds three '
            'violations, and all of them are in the shortcut. The four '
            'real layers have none. [[slnc 300]] Spring wires by type. '
            'Only a test can say a layer is not allowed to be there.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Packages as layers.', '', 'The transaction in the service.', '', 'Response objects, not entities.', '', 'A layering test in the build.'],
        narration=(
            'My verdict, plainly. Keep the layers as packages. Put the '
            'transaction in the service. Return response objects, not '
            'entities. And run a layering test in the build.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['RestController, Service and', 'Repository in separate packages.', '', '@Transactional on a service.'],
        narration=(
            'How do you recognise this in code you did not write? A rest '
            'controller, a service and a repository, in separate '
            'packages. And a transactional annotation on a service '
            'method.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Most Spring Boot applications', 'you will ever open.'],
        narration=(
            'You have met this in most Spring Boot applications you will '
            'ever open.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1, H2 and', 'ArchUnit 1.5.0.', '', 'A real web server on a free port.'],
        narration=(
            'For the record. Spring Boot four point one point one, H2, '
            'and ArchUnit one point five. A real web server, on a free '
            'port.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: a real web server,', 'real HTTP, a real database and a', 'real transaction.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: a real web server, real HTTP, a real '
            'database and a real transaction.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a small script with one table,', 'four layers are more ceremony', 'than help.'],
        narration=(
            'So when is it too much? For a small script with one table, '
            'four layers are more ceremony than help.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a class that breaks the rule', 'and run the test.'],
        narration=(
            "That's Layered Architecture with Spring Boot. [[slnc 250]] "
            'If you take one sentence away, take this one: Spring names '
            'the layers, and only a test can say which dependencies are '
            'forbidden. [[slnc 350]] The full source, the written notes, '
            'the diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, add a '
            'class that breaks the rule, and run the test. [[slnc 300]] '
            'If this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
