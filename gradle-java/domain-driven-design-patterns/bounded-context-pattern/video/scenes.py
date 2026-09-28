"""Scene definitions for the Bounded Context teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Bounded Context',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Bounded Context pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A bounded context is a '
            'boundary, inside which every word has exactly one meaning, '
            'and one model. [[slnc 300]] The contexts around it have '
            'their own meanings. [[slnc 300]] And they are connected on '
            'purpose. [[slnc 600]] Think of the word, bank. [[slnc 300]] '
            'To a banker, it holds money. [[slnc 300]] To a fisherman, it '
            'is the edge of a river. [[slnc 300]] Both are right, in '
            'their own world. [[slnc 700]] In our online store, the word '
            'that means three different things is customer. [[slnc 500]] '
            'In this video, one customer class tries to serve three '
            'departments. [[slnc 300]] Then three small models each mean '
            'what their own department means. [[slnc 300]] We will hear '
            'them talk through events, and then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Sales, Shipping and Support', 'all say customer.', '', 'Sales: a buyer, with a credit limit.', 'Shipping: an address.', 'Support: a person, with tickets.', '', 'One class for all three?'],
        narration=(
            'Here is the scenario. [[slnc 400]] Sales, Shipping, and '
            'Support all talk about the customer. [[slnc 500]] To Sales, '
            'a customer is a buyer, with a credit limit. [[slnc 300]] To '
            'Shipping, a customer is an address to deliver to. [[slnc '
            '300]] To Support, a customer is a person, with support '
            'tickets. [[slnc 500]] So here is the question. [[slnc 300]] '
            'Is that really one class?'
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
            'First, the usual way: one customer class, for everyone. '
            '[[slnc 400]] It has twelve fields, because every department '
            'added what it needed. [[slnc 500]] Each department only uses '
            'a handful of them. [[slnc 300]] But every department depends '
            'on all twelve. [[slnc 300]] So a change for one department '
            'is a change for every department.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Draw a boundary.', '', 'Inside it, every word has one', 'meaning, and one model.', '', 'Each department gets its own', 'model of the customer.', '', 'They share only an id, and they', 'talk by events.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Draw a boundary. [[slnc 300]] '
            'Inside it, every word has one meaning, and one model. [[slnc '
            '500]] Each department gets its own model of the customer. '
            '[[slnc 300]] They share only an I D. [[slnc 300]] And they '
            'talk to each other through events.'
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
            'Second demo: one word, three meanings. [[slnc 400]] Is Ada '
            'an active customer? [[slnc 500]] Sales says yes, because she '
            'bought something in the last ninety days. [[slnc 300]] '
            'Shipping says yes, because a parcel is on its way to her. '
            '[[slnc 300]] Support says no, because she has no open '
            'ticket. [[slnc 500]] One class cannot give all three '
            'answers. [[slnc 300]] And each answer is right, in its own '
            'context.'
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
            'Third demo: a model for each context. [[slnc 400]] Sales has '
            'a Buyer. [[slnc 300]] Shipping has a Recipient. [[slnc 300]] '
            'Support has a Contact. [[slnc 500]] Each has four fields, '
            'and each means what its own department means. [[slnc 300]] '
            "None of them knows the others' types. [[slnc 300]] They "
            'share just one thing: the customer I D.'
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
            'Fourth demo: the contexts talk through events. [[slnc 400]] '
            'Sales renames Ada, from Ada Lovelace to Ada King. [[slnc '
            '300]] And it publishes that fact as an event. [[slnc 500]] '
            'For a moment, Sales says Ada King, and Shipping still says '
            'Ada Lovelace. [[slnc 300]] One event is waiting. [[slnc '
            '500]] Then the event is delivered. [[slnc 300]] Shipping '
            'updates its own recipient to Ada King. [[slnc 300]] It never '
            'saw the Sales buyer at all.'
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
            'Fifth demo: the boundary can be checked. [[slnc 400]] A test '
            'scans the source code. [[slnc 300]] It finds no place where '
            "one context uses another context's types. [[slnc 500]] So "
            'Shipping can add a field to its recipient. [[slnc 300]] And '
            'nothing in Sales or Support needs to change.'
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
            "Finally, the cost. [[slnc 400]] Ada's name is now stored "
            'three times. [[slnc 500]] Between a rename and its delivery, '
            'two contexts disagree about her name. [[slnc 300]] That gap '
            'has a name: eventual consistency. [[slnc 500]] And each '
            'context needs its own translator, for every event it cares '
            'about. [[slnc 300]] That is the price of a clean boundary.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['The same word, such as Customer or', 'Product, defined by separate', '', 'Services or modules that each have', 'their own database and their own', '', 'Events carrying an id and a few', 'plain values, not whole objects.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for the same word, such as customer or '
            'product, defined by separate classes, in separate packages. '
            '[[slnc 300]] Look for services or modules that each have '
            'their own database, and their own idea of a customer. [[slnc '
            '300]] Look for events that carry an I D and a few plain '
            'values, not whole objects. [[slnc 300]] And look for a '
            'context map, a diagram showing which context depends on '
            'which.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Draw a bounded context wherever', 'the same word starts to mean', 'different things, or where', 'different teams own the model.', 'Give each its own model, share', 'only ids and events, translate at', 'the border, and accept that copies', 'lag. Do not split a small system', 'that one team understands.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Draw a bounded context '
            'wherever the same word starts to mean different things. '
            '[[slnc 300]] Or wherever different teams own the model. '
            '[[slnc 500]] Give each context its own model. [[slnc 300]] '
            'Share only I Ds and events. [[slnc 300]] Translate at the '
            'border. [[slnc 300]] And accept that the copies will lag '
            'behind a little. [[slnc 500]] Do not split a small system '
            'that one team understands.'
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
        body=['In a small system that one team', 'understands, one model is simpler,', 'and translation is pure cost. A', 'boundary earns its place where', 'meanings really diverge.'],
        narration=(
            'So, when is this too much? [[slnc 400]] In a small system '
            'that one team understands, one model is simpler, and '
            'translation is pure cost. [[slnc 400]] A boundary earns its '
            'place where the meanings really do differ.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Bounded Context pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'bounded context lets every word mean one thing, at the price '
            'of translating between contexts. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try. [[slnc 300]] Make the support context '
            'react to the rename event. [[slnc 300]] And write its '
            'translator. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
