"""Scene definitions for the Identity Map with JPA teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Identity Map with JPA',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            "Identity Map pattern, in Java, using J P A, Java's standard "
            'for storing objects in databases. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] An identity map keeps one '
            'object for each database row, for as long as one session '
            "lasts. [[slnc 600]] Think of a hotel's key desk. [[slnc "
            '300]] While you are staying, there is one key for your room. '
            '[[slnc 300]] Ask again, and you are handed the same key, not '
            'a new one. [[slnc 700]] This is the framework version of the '
            'Identity Map video, with the same customer and order. [[slnc '
            '500]] We will hear why loading the same customer twice gives '
            'the same object. [[slnc 300]] Why two sessions give two '
            'objects. [[slnc 300]] And what happens to a change made to '
            'an object whose session has closed.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Identity Map, the hand-built video,', 'built the map from plain Java.', '', 'This video uses the same customer 7', 'and the same order 100,', 'and shows what JPA does with them.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Identity Map video. [[slnc 400]] '
            'That one builds the map by hand, in plain Java, and shows '
            'why one row should be one object. [[slnc 500]] Here, we use '
            'the very same customer, number seven, and the very same '
            'order, number one hundred. [[slnc 300]] We will not teach '
            'the pattern again. [[slnc 300]] Instead, we ask what J P A '
            'does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['Two things are new: Hibernate and H2.', '', 'Hibernate turns operations on objects', 'into SQL. H2 is a database that runs', 'inside the test, so nothing is installed.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Two things are new in this project. [[slnc 400]] First, '
            'Hibernate, the most widely used implementation of J P A. '
            '[[slnc 300]] You mark your classes with annotations, and it '
            'turns work on those objects into database commands. [[slnc '
            '500]] Second, H2, a database that runs in memory, inside the '
            'test, so nothing needs installing. [[slnc 500]] And one '
            'promise. [[slnc 300]] If you skip this video, you lose none '
            'of the pattern. [[slnc 300]] This one only shows you where '
            'you have already met it.'
        ),
    ),
    dict(
        key='04-annotations', kind='bullets', title='Two Annotations',
        body=["The partner's Customer, plus:", '', '@Entity: this class is stored.', '@Id: this field is its identity.', '', 'Nothing else about the class', 'changed.'],
        narration=(
            'The customer class from the partner project gets two '
            'annotations. [[slnc 400]] At Entity says: this class is '
            'stored in the database. [[slnc 300]] At Id says: this field '
            'is its identity. [[slnc 500]] Nothing else about the class '
            'changed. [[slnc 300]] Not one line of its logic.'
        ),
    ),
    dict(
        key='05-one-context', kind='console', title='One Persistence Context',
        body="""ONE. One context.
  first == second: true
  SQL statements: 1

  the identity map from the
  last project, and you did
  not write it.""",
        narration=(
            'First demo, and here is the key moment. [[slnc 400]] Ask the '
            'entity manager for customer seven, twice. [[slnc 300]] Are '
            'the two the same object? [[slnc 300]] Yes. [[slnc 300]] And '
            'only one database query was made. [[slnc 500]] That is the '
            'identity map from the hand-built project. [[slnc 300]] You '
            'did not write it. [[slnc 300]] It is called the persistence '
            'context, and every entity manager has one.'
        ),
    ),
    dict(
        key='06-order', kind='console', title="The Order's Customer",
        body="""TWO. The order.
  the order's customer ==
  customer 7 by id: true

  SQL statements: 1
  (the order and its
  customer, once)""",
        narration=(
            "Second demo: the order's customer. [[slnc 400]] Load order "
            'one hundred, and ask it for its customer. [[slnc 300]] Then '
            'ask for customer seven by I D. [[slnc 300]] The same object '
            'again. [[slnc 500]] And just one database query for all of '
            'it: the order, and its customer, fetched once. [[slnc 300]] '
            'Everything from the hand-built project, now done for you.'
        ),
    ),
    dict(
        key='07-both-kept', kind='console', title='Both Changes Are Kept',
        body="""THREE. One object.
  moved to York, and email
  changed.

  SQL statements at commit:
  1 (one UPDATE)

  nothing lost.""",
        narration=(
            'Third demo: both changes are kept. [[slnc 400]] Remember the '
            'bug from the hand-built project? [[slnc 300]] One route '
            'moves the customer to York. [[slnc 300]] Another changes her '
            'email. [[slnc 300]] Without a map, one of those changes '
            'vanished. [[slnc 500]] Here, both are kept. [[slnc 300]] '
            'There is only one object, so the second change cannot '
            'overwrite the first. [[slnc 300]] And when the transaction '
            'commits, Hibernate writes one single update, carrying both '
            'changes.'
        ),
    ),
    dict(
        key='08-two-contexts', kind='console', title='The Failure Of Its Own: Two Contexts',
        body="""FOUR. Two contexts.
  context one == context two:
  false

  equals: true. same customer,
  two objects.

  both contexts closed:
  detached.""",
        narration=(
            "Fourth demo: this project's own failure, two contexts. "
            '[[slnc 400]] The map belongs to one persistence context. '
            '[[slnc 300]] Open a second one, and ask for customer seven '
            'again. [[slnc 300]] It has its own map. [[slnc 500]] Is it '
            "the same object as the first context's? [[slnc 300]] No. "
            '[[slnc 300]] Equal by I D, but two separate objects, each '
            'free to disagree. [[slnc 500]] The problem from the '
            'hand-built project is back, just by opening a second '
            'context.'
        ),
    ),
    dict(
        key='09-detached', kind='console', title='A Detached Change Is Not Saved',
        body="""  a detached customer was
  changed.

  stored address is still:
  12 Mill Lane, Leeds

  nothing tracks a detached
  object. no error.""",
        narration=(
            'And worse. [[slnc 400]] When a context closes, every object '
            'it loaded becomes detached. [[slnc 500]] Now change a '
            "detached customer's address. [[slnc 300]] Then open a new "
            'context, and look at the stored address. [[slnc 300]] It '
            'still says twelve Mill Lane, Leeds. [[slnc 500]] The change '
            'was silently not saved. [[slnc 300]] Nothing tracks a '
            'detached object. [[slnc 300]] And there was no error at all.'
        ),
    ),
    dict(
        key='10-stale', kind='console', title='Cost: The Context Is A Cache',
        body="""FIVE. Stale.
  another context committed
  a new email.

  this context still sees:
  ada@example.com
  after refresh:
  ada@other.example""",
        narration=(
            'Fifth demo: the context is a cache. [[slnc 400]] Another '
            'context saves a new email address for the customer. [[slnc '
            '300]] This context still sees the old one. [[slnc 300]] It '
            'has no reason to look again. [[slnc 500]] The cure is a '
            'method called refresh, which reloads the object from the '
            'database. [[slnc 300]] After refresh, it sees the new email.'
        ),
    ),
    dict(
        key='11-growth', kind='console', title='Cost: It Holds References',
        body="""SIX. Growth.
  after loading 1000
  customers, the context
  holds 1000 entities.

  after clear(): 0.

  scope: one transaction,
  or one request.""",
        narration=(
            'Last demo: the context holds on to everything. [[slnc 400]] '
            'After loading one thousand customers, the context holds all '
            'one thousand. [[slnc 300]] Until a method called clear is '
            'called. [[slnc 500]] So how long a context lives really '
            'matters. [[slnc 300]] In a Spring application, it normally '
            'lives for one transaction, or one request. [[slnc 300]] That '
            'is why it does not grow forever.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every JPA developer has used an', 'identity map without knowing.', '', 'If a second find did not hit the', 'database, or an entity missed', "another transaction's change:", 'this was why.'],
        narration=(
            'Where have you met this before? [[slnc 400]] Every J P A '
            'developer has used an identity map, often without knowing '
            'it. [[slnc 500]] If a second lookup ever did not touch the '
            'database, this was why. [[slnc 300]] And if an entity ever '
            "failed to see another transaction's change, this was why "
            'too.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Hibernate ORM 7.4.5.', 'H2 2.4.240.', "Versions from Spring Boot 4.1.1's", 'bill of materials.', '', 'Spring Boot itself is not used.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] '
            'Hibernate seven point four point five. [[slnc 300]] And H2 '
            'two point four point two forty. [[slnc 400]] These versions '
            "come from Spring Boot four point one point one's list of "
            'tested libraries. [[slnc 300]] But Spring Boot itself is not '
            'used here.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: Hibernate,', 'the context, the SQL count from', "Hibernate's own statistics.", '', 'The database is H2 in memory,', 'not a production database.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything here is real. [[slnc 300]] The persistence '
            "context is Hibernate's own. [[slnc 300]] And the query "
            "counts come from Hibernate's own statistics. [[slnc 400]] "
            'The only stand-in is the database, which is H2, in memory.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['If you use JPA you already have it,', 'and cannot turn it off.', '', 'The lesson is knowing it is there.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If you use J P A, '
            'you already have an identity map, and you cannot turn it '
            'off. [[slnc 300]] The lesson is simply knowing that it is '
            'there.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Use merge to save the detached', 'change, and see what it returns.'],
        narration=(
            "That's the Identity Map, in J P A. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] The '
            'persistence context is an identity map, and it belongs to '
            'one entity manager. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Use the merge method to save the detached '
            'change. [[slnc 300]] And look closely at what merge returns. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
