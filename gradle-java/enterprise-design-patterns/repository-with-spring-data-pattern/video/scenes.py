"""Scene definitions for the Repository with Spring Data teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Repository with Spring Data',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Repository pattern, in Java, using Spring Data. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] A repository is an '
            'interface that looks like a collection of your objects. '
            '[[slnc 300]] So the code using it asks for objects, not for '
            'database tables. [[slnc 600]] Think of ordering from a '
            'catalogue by item name. [[slnc 300]] You say what you want, '
            'and the warehouse works out how to find it. [[slnc 700]] '
            'This is the framework version of the Repository video. '
            '[[slnc 300]] That one built two implementations by hand. '
            '[[slnc 300]] This one has none at all. [[slnc 500]] By the '
            'end, you will hear an interface with no class behind it that '
            "still works. [[slnc 300]] A query built from a method's "
            'name. [[slnc 300]] And a surprising leak: objects that can '
            'change the database without anyone calling save.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Repository, the hand-built video,', 'built one interface and two', 'implementations by hand.', '', 'This video uses the same customers', 'and the same question:', 'London customers who ordered', 'last month.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Repository video. [[slnc 400]] That '
            'one builds one interface, and two implementations by hand. '
            '[[slnc 300]] One over a simple list, and one over a '
            'database. [[slnc 500]] Here, we use the same six customers, '
            'and the same question. [[slnc 300]] London customers who '
            'ordered in the last month. [[slnc 300]] We will not teach '
            'the pattern again. [[slnc 300]] Instead, we ask what Spring '
            'Data does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['Three things are new:', 'Spring Boot, Spring Data, and H2.', '', 'Spring Data writes your repository', 'for you, from an interface.', 'H2 is a database that runs in memory.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Three things are new in this project. [[slnc 400]] Spring '
            'Boot, which creates and connects your objects. [[slnc 300]] '
            'Spring Data, which writes your repository for you, from just '
            'an interface. [[slnc 300]] And H2, a database that runs in '
            'memory, so nothing needs installing. [[slnc 500]] And one '
            'promise. [[slnc 300]] If you skip this video, you lose none '
            'of the pattern. [[slnc 300]] This one is about the tool.'
        ),
    ),
    dict(
        key='04-no-impl', kind='console', title='An Interface With No Implementation',
        body="""ONE. No implementation.
  CustomerRepository is an
  interface. this project has
  no class that implements it.

  the object Spring injected:
  a generated proxy.

  save, findById, findAll,
  delete: all there.""",
        narration=(
            'First demo: an interface with no implementation. [[slnc '
            '400]] The customer repository is an interface. [[slnc 300]] '
            'And this project has no class that implements it. [[slnc '
            '300]] Not one. [[slnc 500]] The object Spring provides is a '
            'generated stand-in, called a proxy. [[slnc 300]] Save works. '
            '[[slnc 200]] Find by I D works. [[slnc 200]] Find all works. '
            '[[slnc 200]] Delete works. [[slnc 300]] And nobody wrote any '
            'of them.'
        ),
    ),
    dict(
        key='05-from-name', kind='console', title='A Query From A Name',
        body="""TWO. From a name.
  findDistinctByCity
  AndOrdersDayGreaterThan
  (London, 70):
  [Ada, Grace]

  statements: 1

  the partner's service,
  unchanged: [Ada, Grace].""",
        narration=(
            'Second demo: a query built from a name. [[slnc 400]] In the '
            'last video, the London query was written by hand, twice. '
            '[[slnc 500]] Here, it is just a method name. [[slnc 300]] '
            'Find distinct by city, and orders day greater than. [[slnc '
            '300]] Spring Data reads the name, and builds the query. '
            '[[slnc 500]] The answer is Ada and Grace, in one database '
            'query. [[slnc 300]] And the marketing service from the '
            'partner video, unchanged, gives the same answer. [[slnc '
            '300]] The two implementation classes it needed before simply '
            'do not exist here.'
        ),
    ),
    dict(
        key='06-names', kind='console', title='Cost: A Name Can Be Wrong',
        body="""THREE. The bill.
  findAllWithOrders
  findByCityAndOrderedAfter
  findDistinct...GreaterThan
  ...AndOrdersStatusIn

  findByCiity (a typo):
  PropertyReferenceException:
  No property ciity found

  the compiler cannot check
  a name.""",
        narration=(
            'Third demo: the costs, starting with names. [[slnc 400]] '
            'Every question still needs its own method. [[slnc 300]] And '
            'the names grow long. [[slnc 300]] Find distinct, by city, '
            'and orders day greater than, and orders status in. [[slnc '
            '500]] The name is now the query. [[slnc 300]] So a typo, '
            "like city spelled with two i's, is not caught by the "
            'compiler. [[slnc 300]] It is only caught when Spring reads '
            'it, and complains that no such property exists. [[slnc 500]] '
            'The compiler cannot check a name.'
        ),
    ),
    dict(
        key='07-n-plus-one', kind='console', title='Cost: The Leak On Speed',
        body="""FOUR. Speed.
  counting every customer's
  orders, lazily:
  7 orders, 7 statements

  with @EntityGraph:
  7 orders, 1 statement

  the interface can say join,
  by carrying a hint.""",
        narration=(
            'Fourth demo: the speed leak. [[slnc 400]] Count every '
            "customer's orders. [[slnc 300]] Six customers, and their "
            'orders are loaded lazily. [[slnc 300]] That costs seven '
            'queries, the same seven as the hand-built version. [[slnc '
            '500]] Add an entity graph annotation to the repository '
            'method. [[slnc 300]] And now it is one query. [[slnc 500]] '
            'So the interface can now say, fetch these together. [[slnc '
            '300]] But only by carrying a database hint, on a type that '
            'was meant to hide the database.'
        ),
    ),
    dict(
        key='08-leak', kind='console', title='The Managed Entity That Leaks',
        body="""FIVE. The leak.
  inside a transaction, a
  caller changed a customer
  from findAll(), never called
  save.
  Ada's city: Manchester

  the same change, outside a
  transaction.
  Ada's city: London""",
        narration=(
            "Fifth demo: this project's own failure. [[slnc 400]] An "
            'object that a Spring Data repository hands out is not a '
            'plain object. [[slnc 300]] It is managed, which means it is '
            'being watched. [[slnc 500]] Inside a transaction, some code '
            'gets all the customers, and moves Ada to Manchester. [[slnc '
            '300]] It never calls save. [[slnc 300]] Yet when the '
            "transaction ends, Ada's city in the database is Manchester. "
            '[[slnc 300]] Written, with no save anywhere. [[slnc 500]] '
            'Now the same change, with no transaction around it. [[slnc '
            "300]] Ada's city in the database stays London. [[slnc 300]] "
            'The change is lost, and there is no error. [[slnc 500]] The '
            'interface looks like a plain collection. [[slnc 300]] But '
            'the objects inside it are not plain.'
        ),
    ),
    dict(
        key='09-swap', kind='bullets', title='And The Swap?',
        body=['You can swap the database.', '', 'Still claimed far more often', 'than it is used.', '', 'The real benefit: callers speak', 'the language of the domain.'],
        narration=(
            'One more point from the hand-built video, which is still '
            'true. [[slnc 400]] A repository is often sold as a way to '
            'swap your database. [[slnc 300]] That is claimed far more '
            'often than it happens. [[slnc 500]] The real benefit is that '
            'your code speaks the language of the business.'
        ),
    ),
    dict(
        key='10-met', kind='bullets', title='Where You Have Met This',
        body=['Every JpaRepository is this pattern.', '', 'The framework supplies the', 'implementation you wrote by hand.'],
        narration=(
            'Where have you met this before? [[slnc 400]] Every J P A '
            'Repository in Spring is exactly this pattern. [[slnc 300]] '
            'The framework supplies the implementation you wrote by hand '
            'before. [[slnc 300]] And it builds queries from the method '
            'names. [[slnc 500]] Now you know what it does for you, and '
            'where it leaks.'
        ),
    ),
    dict(
        key='11-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', 'Spring Data, Hibernate and H2:', 'the versions that release manages.', '', 'No web server, no web starter.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] With whichever '
            'versions of Spring Data, Hibernate, and H2 that release '
            'includes. [[slnc 300]] There is no web server, and no web '
            'library, in this project.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the generated', 'proxy, the query from the name,', "and the counts from Hibernate's", 'own statistics.', '', 'The database is H2 in memory.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            "Everything here is real. [[slnc 300]] The proxy is Spring's. "
            '[[slnc 300]] The query is built by Spring Data, from the '
            "name. [[slnc 300]] And the counts come from Hibernate's own "
            'statistics. [[slnc 400]] The only stand-in is the database, '
            'H2, in memory.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a handful of queries in one place,', 'Spring Data still saves you two classes.', '', 'The cost is the leak, which needs to', 'be known about.'],
        narration=(
            'So, when is this too much? [[slnc 400]] Even for a few '
            'queries in one place, Spring Data still saves you two '
            'classes. [[slnc 300]] The cost is the leak, and it needs to '
            'be understood.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a finder by name prefix,', 'and write no other code.'],
        narration=(
            "That's Repository with Spring Data. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] The '
            'interface hides the database, but the objects it returns are '
            'still being watched by it. [[slnc 500]] The full source '
            'code, written notes, diagrams, and an animated walkthrough '
            'are all in the repository. [[slnc 500]] Here is one exercise '
            'to try. [[slnc 300]] Add a finder that searches by the start '
            "of a customer's name. [[slnc 300]] And call it, without "
            'writing any other code. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
