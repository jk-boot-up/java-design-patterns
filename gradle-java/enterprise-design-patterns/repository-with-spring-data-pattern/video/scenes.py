"""Scene definitions for the Repository with Spring Data teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Repository with Spring Data',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Repository '
            'pattern with Spring Data, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Repository video. That one built '
            'two implementations by hand. This one has none. [[slnc 350]] '
            'The plain definition, in short: an interface that looks like '
            'a collection of your objects, so the code using it asks for '
            'objects, not for tables. [[slnc 300]] By the end you will '
            'see an interface with no class behind it that still works, a '
            "query written from a method's name, and a leak that comes "
            'with it: an entity handed to a caller that can change '
            'without a save.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Repository, the hand-built video,', 'built one interface and two', 'implementations by hand.', '', 'This video uses the same customers', 'and the same question:', 'London customers who ordered', 'last month.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'This video assumes the Repository video. If you have not '
            'seen it, start there. It builds one interface, and two '
            'implementations by hand: one over a list, one over a '
            'database. [[slnc 300]] This one uses the same six customers '
            'and the same question: London customers who ordered in the '
            'last month. It does not teach the pattern again. It shows '
            'what Spring Data does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['Three things are new:', 'Spring Boot, Spring Data, and H2.', '', 'Spring Data writes your repository', 'for you, from an interface.', 'H2 is a database that runs in memory.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first annotation, new things. Spring Boot creates '
            'and wires your objects. Spring Data writes your repository '
            'for you, from an interface. H two is a database that runs in '
            'memory, so nothing needs installing. [[slnc 300]] And a '
            'promise: skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it.'
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
            'Here is the first surprise. The customer repository is an '
            'interface. And this project has no class that implements it. '
            'Not one. [[slnc 300]] The object Spring injected is a '
            'generated proxy. Save works. Find by id works. Find all '
            'works. Delete works. None of them were written by anyone.'
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
            'Now the query from the last video, London customers who '
            'ordered in the last month. It was written by hand, twice. '
            'Here it is a method name: find distinct by city and orders '
            'day greater than. [[slnc 300]] Spring Data reads the name '
            'and builds the query. Ada and Grace, in one statement. '
            '[[slnc 300]] And the marketing service from the partner '
            'video, its body unchanged, gives the same answer. The two '
            'implementation classes it needed before are not in this '
            'project, and the application runs.'
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
            'Now the bill. Every question still needs a method, and the '
            'names grow. Find distinct by city and orders day greater '
            'than and orders status in. [[slnc 300]] And the name is now '
            'the query. A typo, find by c i i ty, is not caught by the '
            'compiler. It is caught only when Spring reads it: no '
            'property c i i ty found. [[slnc 300]] The compiler cannot '
            'check a name.'
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
            "Second cost. Counting every customer's orders. Six "
            'customers, and the orders are lazy. Seven statements: the '
            'same seven the hand-built version cost. [[slnc 300]] Add an '
            'entity graph annotation to the repository method, and it is '
            'one statement. The interface can now say join. But only by '
            'carrying a persistence hint, on a type that was meant to '
            'hide persistence.'
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
            "Now the failure of this project's own. An entity that a "
            'repository hands out is not a plain object. It is managed. '
            '[[slnc 300]] A caller, inside a transaction, gets all the '
            'customers, and changes one. Moves Ada to Manchester. It '
            "never calls save. At commit, Ada's city in the database is "
            'Manchester. Written, with no save anywhere. [[slnc 300]] The '
            "same change, with no transaction around it: Ada's city in "
            'the database is still London. The change is lost, and there '
            'is no error. [[slnc 300]] The interface looks like a '
            'collection. The objects in it are not plain.'
        ),
    ),
    dict(
        key='09-swap', kind='bullets', title='And The Swap?',
        body=['You can swap the database.', '', 'Still claimed far more often', 'than it is used.', '', 'The real benefit: callers speak', 'the language of the domain.'],
        narration=(
            'One more thing from the hand-built video, still true. A '
            'repository is often sold as a way to swap the database. That '
            'is claimed far more often than it is used. The real benefit '
            'is that callers speak the language of the domain.'
        ),
    ),
    dict(
        key='10-met', kind='bullets', title='Where You Have Met This',
        body=['Every JpaRepository is this pattern.', '', 'The framework supplies the', 'implementation you wrote by hand.'],
        narration=(
            'You have met this. Every J P A repository is this pattern. '
            'The framework supplies the implementation you wrote by hand, '
            'and writes the queries from the names. [[slnc 300]] Now you '
            'know what it is doing for you, and where it leaks.'
        ),
    ),
    dict(
        key='11-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', 'Spring Data, Hibernate and H2:', 'the versions that release manages.', '', 'No web server, no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. Spring '
            'Data, Hibernate and H two are whichever versions that '
            'release manages. There is no web server and no web starter '
            'in this project.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the generated', 'proxy, the query from the name,', "and the counts from Hibernate's", 'own statistics.', '', 'The database is H2 in memory.'],
        narration=(
            'The same honest admission as everywhere in this course, and '
            "again short. Everything is real. The proxy is Spring's. The "
            'query is built by Spring Data from the name. The counts come '
            "from Hibernate's own statistics. The only stand-in is the "
            'database, H two in memory.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a handful of queries in one place,', 'Spring Data still saves you two classes.', '', 'The cost is the leak, which needs to', 'be known about.'],
        narration=(
            'So when is it too much? For a handful of queries in one '
            'place, Spring Data still saves you two classes. The cost is '
            'the leak, and it needs to be known about.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a finder by name prefix,', 'and write no other code.'],
        narration=(
            "That's Repository with Spring Data. [[slnc 250]] If you take "
            'one sentence away, take this one: the interface hides the '
            'database, but the entity it returns does not hide the '
            'persistence context. [[slnc 350]] The full source, the '
            'written notes, the diagrams and an animated walkthrough are '
            'all in the repository. [[slnc 300]] If you try one exercise, '
            'add a finder by name prefix, and call it, without writing '
            'any other code. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
