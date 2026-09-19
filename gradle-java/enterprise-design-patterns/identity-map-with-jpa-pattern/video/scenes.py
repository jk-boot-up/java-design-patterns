"""Scene definitions for the Identity Map with JPA teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Identity Map with JPA',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Identity Map '
            'pattern inside J P A, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Identity Map video. That one built '
            'the pattern by hand. This one shows the very same customer '
            'and order inside J P A, where you did not write the map. '
            '[[slnc 350]] The plain definition, in short: keep one object '
            'for each database row, for as long as one session lasts. '
            '[[slnc 300]] By the end you will see why loading the same '
            'customer twice gives the same object, why two sessions give '
            'two objects, and what happens to a change made to an object '
            'whose session has closed.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Identity Map, the hand-built video,', 'built the map from plain Java.', '', 'This video uses the same customer 7', 'and the same order 100,', 'and shows what JPA does with them.', '', 'If you have not seen that one,', 'start there.'],
        narration=(
            'This video assumes the Identity Map video. If you have not '
            'seen it, start there. It builds an identity map by hand, '
            'from plain Java, and shows why one row should be one object. '
            '[[slnc 300]] This one uses the very same customer, number '
            'seven, and the very same order, number one hundred. It does '
            'not teach the pattern again. It shows what J P A does with '
            'it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Annotation',
        body=['Two things are new: Hibernate and H2.', '', 'Hibernate turns operations on objects', 'into SQL. H2 is a database that runs', 'inside the test, so nothing is installed.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first annotation, two new things. Hibernate is '
            'the most widely used implementation of J P A. You mark your '
            'classes, and it turns operations on them into S Q L. [[slnc '
            '300]] H two is a database that runs inside the test, in '
            'memory, so nothing needs installing. [[slnc 300]] And a '
            'promise: skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it. This one only shows you '
            'where you have already met it.'
        ),
    ),
    dict(
        key='04-annotations', kind='bullets', title='Two Annotations',
        body=["The partner's Customer, plus:", '', '@Entity: this class is stored.', '@Id: this field is its identity.', '', 'Nothing else about the class', 'changed.'],
        narration=(
            'The customer class from the partner project gets two '
            'annotations. At entity says this class is stored. At id says '
            'which field is its identity. Nothing else about the class '
            'changed. Not one line of the logic.'
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
            'Here is the moment. Ask the entity manager for customer '
            'seven, twice. Are the two the same object? True. And only '
            'one S Q L statement was issued. [[slnc 300]] That is the '
            'identity map from the last project. You did not write it. It '
            'is called the persistence context, and every entity manager '
            'has one.'
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
            'Load order one hundred, and ask it for its customer. Then '
            'ask for customer seven by id. Same object again. True. '
            '[[slnc 300]] And one S Q L statement for the whole lot: the '
            'order and its customer, fetched once. Everything you saw in '
            'the hand-built project, now done for you.'
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
            'Now the bug from the hand-built project. One route moves her '
            'to York. Another changes her email. In the hand-built '
            'version, without a map, one of those changes vanished. '
            '[[slnc 300]] Here, both are kept. There is only one object, '
            'so the second change cannot overwrite the first. And at '
            'commit, Hibernate writes a single update carrying both.'
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
            "Now the failure of this project's own. The map belongs to "
            'one persistence context. Open a second one, and ask for '
            'customer seven. It has its own map. [[slnc 300]] Is it the '
            "same object as the first context's? False. Equal by I D, but "
            'two objects. Each is free to disagree. [[slnc 300]] The '
            'problem from the hand-built project, back again, just by '
            'opening a second context.'
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
            'And worse. Close a context, and every object it loaded is '
            'detached. Change one. Move the customer to nowhere in '
            'particular. [[slnc 300]] Then open a new context and look at '
            'the stored address. Still twelve Mill Lane, Leeds. The '
            'change was silently not saved. [[slnc 300]] Nothing tracks a '
            'detached object. And there was no error at all.'
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
            "The costs are the partner's, in framework clothes. First, "
            'the context is a cache. Another context commits a new email. '
            'This one still sees the old one, because it has no reason to '
            'look. [[slnc 300]] The cure is refresh, which reloads the '
            'object from the database.'
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
            'Second cost. The context holds every entity it loads. After '
            'loading one thousand customers, it holds one thousand '
            'entities, until clear is called. [[slnc 300]] So its scope '
            'matters. In a Spring application the context normally lives '
            'for one transaction, or one request, which is why it does '
            'not grow forever.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every JPA developer has used an', 'identity map without knowing.', '', 'If a second find did not hit the', 'database, or an entity missed', "another transaction's change:", 'this was why.'],
        narration=(
            'This is where you have already met it. Every J P A developer '
            'has used an identity map without knowing it. If a second '
            'find ever did not hit the database, or an entity failed to '
            "pick up another transaction's change, this was the reason."
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Hibernate ORM 7.4.5.', 'H2 2.4.240.', "Versions from Spring Boot 4.1.1's", 'bill of materials.', '', 'Spring Boot itself is not used.'],
        narration=(
            'For the record. Hibernate O R M seven point four point five, '
            'and H two two point four point two forty. The versions come '
            "from Spring Boot four point one point one's bill of "
            'materials, so they are ones that release was tested '
            'together. Spring Boot itself is not used in this video.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: Hibernate,', 'the context, the SQL count from', "Hibernate's own statistics.", '', 'The database is H2 in memory,', 'not a production database.'],
        narration=(
            'The same honest admission as everywhere in this course, and '
            'for once it is short. Everything here is real. The '
            "persistence context is Hibernate's. The S Q L counts come "
            "from Hibernate's own statistics. The only stand-in is the "
            'database, which is H two in memory.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['If you use JPA you already have it,', 'and cannot turn it off.', '', 'The lesson is knowing it is there.'],
        narration=(
            'So when is it too much? If you use J P A, you already have '
            'it, and cannot turn it off. The lesson is simply knowing it '
            'is there.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Use merge to save the detached', 'change, and see what it returns.'],
        narration=(
            "That's the Identity Map, in J P A. [[slnc 250]] If you take "
            'one sentence away, take this one: the persistence context is '
            'an identity map, and it belongs to one entity manager. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, use merge '
            'to save the detached change, and look at what it returns. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
