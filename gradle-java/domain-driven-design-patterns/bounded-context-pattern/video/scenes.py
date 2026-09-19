"""Scene definitions for the Bounded Context teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Bounded Context',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Bounded Context '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'bounded context is a boundary inside which every word has '
            'exactly one meaning, and one model. The contexts around it '
            'have their own, and they are linked on purpose. [[slnc 350]] '
            'This is the sixth project in the domain-driven design '
            'category, whose subject is writing code that says what the '
            'business says. In our online store, the word that means '
            'three different things is customer. [[slnc 300]] By the end '
            'you will see one customer class try to serve three '
            'departments, see three small models that each mean what '
            'their department means, see the contexts talk by events, and '
            'see the bill, which is that everything is now stored and '
            'translated more than once.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Sales, Shipping and Support', 'all say customer.', '', 'Sales: a buyer, with a credit limit.', 'Shipping: an address.', 'Support: a person, with tickets.', '', 'One class for all three?'],
        narration=(
            'Here is the scenario. Sales, Shipping and Support all talk '
            'about the customer. To Sales, a customer is a buyer with a '
            'credit limit. To Shipping, it is an address to deliver to. '
            'To Support, it is a person with tickets. [[slnc 300]] The '
            'question: is that one class?'
        ),
    ),
    dict(
        key='03-god', kind='console', title='One Customer For Everyone',
        body="""ONE. One class.
  the company-wide Customer:
  12 fields.

  each department uses a
  handful, and depends on
  all of them.""",
        narration=(
            'First, one customer class for everyone. It has twelve '
            'fields, because every department added what it needed. Each '
            'department uses only a handful, but every one depends on all '
            "twelve. So any department's change is every department's "
            'change.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Draw a boundary.', '', 'Inside it, every word has one', 'meaning, and one model.', '', 'Each department gets its own', 'model of the customer.', '', 'They share only an id, and they', 'talk by events.'],
        narration=(
            'The pattern. Draw a boundary. Inside it, every word has one '
            'meaning and one model. Each department gets its own model of '
            'the customer. They share only an identity, and they talk to '
            'one another by events.'
        ),
    ),
    dict(
        key='05-meaning', kind='console', title='The Same Word, Three Meanings',
        body="""TWO. One word.
  is Ada active?
  Sales: true.
  Shipping: true.
  Support: false.

  each is right, in its own
  context.""",
        narration=(
            'Second, one word, three meanings. Is Ada an active customer? '
            'Sales says yes: she bought in the last ninety days. Shipping '
            'says yes: a parcel is on its way. Support says no: she has '
            'no open ticket. [[slnc 300]] One class cannot answer all '
            'three. Each answer is right, in its own context.'
        ),
    ),
    dict(
        key='06-models', kind='console', title='A Model For Each Context',
        body="""THREE. Three models.
  Sales: Buyer, 4 fields.
  Shipping: Recipient, 4.
  Support: Contact, 4.

  they share only the id.""",
        narration=(
            'Third, a model for each context. Sales has a buyer. Shipping '
            'has a recipient. Support has a contact. Four fields each, '
            'and each means what its department means. None of them knows '
            "the others' types. They share one thing: the customer id."
        ),
    ),
    dict(
        key='07-events', kind='console', title='The Contexts Talk By Events',
        body="""FOUR. Events.
  Sales renames Ada.
  Sales: Ada King.
  Shipping: Ada Lovelace,
  1 event waiting.

  delivered: Shipping: Ada King.""",
        narration=(
            'Fourth, the contexts talk by events. Sales renames Ada, and '
            'publishes a fact. For a moment, Sales says Ada King, and '
            'Shipping still says Ada Lovelace, with one event waiting. '
            'Then the event is delivered, and Shipping updates its own '
            'recipient. It never saw a buyer.'
        ),
    ),
    dict(
        key='08-check', kind='console', title='The Boundary Can Be Checked',
        body="""FIVE. Checked.
  imports of one context's
  types by another: 0.

  Shipping can add a field to
  Recipient, and nothing else
  changes.""",
        narration=(
            'Fifth, the boundary can be checked. A test scans the source, '
            "and finds no import of one context's types by another. So "
            'Shipping can add a field to its recipient, and nothing in '
            'Sales or Support needs to change.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  Ada's name: stored 3 times.

  between a rename and its
  delivery, two contexts
  disagree.

  a translator per event, per
  context.""",
        narration=(
            "Last, the bill. Ada's name is now stored three times. "
            'Between a rename and its delivery, two contexts disagree '
            'about it, and that gap has a name: eventual consistency. And '
            'every context needs its own translator for every event it '
            'cares about. That is the price of a clean boundary.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['The same word, such as Customer or', 'Product, defined by separate', '', 'Services or modules that each have', 'their own database and their own', '', 'Events carrying an id and a few', 'plain values, not whole objects.'],
        narration=(
            'How do you recognise this in code you did not write? The '
            'same word, such as Customer or Product, defined by separate '
            'classes in separate packages. Services or modules that each '
            'have their own database and their own idea of a customer. '
            'Events carrying an id and a few plain values, not whole '
            'objects. A context map, or a diagram of who is upstream of '
            'whom.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Draw a bounded context wherever', 'the same word starts to mean', 'different things, or where', 'different teams own the model.', 'Give each its own model, share', 'only ids and events, translate at', 'the border, and accept that copies', 'lag. Do not split a small system', 'that one team understands.'],
        narration=(
            'Here is my verdict, plainly. Draw a bounded context wherever '
            'the same word starts to mean different things, or where '
            'different teams own the model. Give each its own model, '
            'share only ids and events, translate at the border, and '
            'accept that copies lag. Do not split a small system that one '
            'team understands.'
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
        body=['In a small system that one team', 'understands, one model is simpler,', 'and translation is pure cost. A', 'boundary earns its place where', 'meanings really diverge.'],
        narration=(
            'So when is it too much? In a small system that one team '
            'understands, one model is simpler, and translation is pure '
            'cost. A boundary earns its place where meanings really '
            'diverge.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Bounded Context. [[slnc 250]] If you take one "
            'sentence away, take this one: a bounded context lets every '
            'word mean one thing, at the price of translating between the '
            'things it means. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'add a support context that reacts to the rename event, and '
            'write its translator. [[slnc 300]] If this helped, a like '
            'genuinely does help other people find it, and subscribe if '
            'you would like the rest of the series. [[slnc 250]] Thanks '
            'for watching.'
        ),
    ),
]
