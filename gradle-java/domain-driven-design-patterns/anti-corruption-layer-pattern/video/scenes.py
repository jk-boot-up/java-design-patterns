"""Scene definitions for the Anti-Corruption Layer teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Anti-Corruption Layer',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Anti-Corruption Layer pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] An anti-corruption '
            'layer is a translator. [[slnc 300]] It sits between your own '
            "model, and another system's model. [[slnc 300]] So the other "
            "system's ideas, names, and codes never leak into yours. "
            '[[slnc 600]] Think of an interpreter at a business meeting. '
            '[[slnc 300]] Each side speaks its own language. [[slnc 300]] '
            'The interpreter makes sure neither side has to learn the '
            "other's. [[slnc 700]] In our online store, we must talk to "
            'an old inventory system that nobody is allowed to change. '
            "[[slnc 500]] In this video, the old system's codes spread "
            'through four features. [[slnc 300]] Then one layer '
            'translates them, once. [[slnc 300]] We will hear bad data '
            'stopped at the door, and the cost of keeping the layer.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Stock comes from an old system.', '', 'Every value is a string.', 'The codes are one letter.', 'It cannot be changed.', '', 'Its owners add new codes,', 'without telling anyone.', '', 'How should the shop use it?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The online store gets its '
            'stock levels from an old inventory system. [[slnc 400]] It '
            'sends every value as text. [[slnc 300]] It uses one-letter '
            'codes. [[slnc 300]] It cannot be changed. [[slnc 300]] And '
            'its owners sometimes add new codes, without telling anyone. '
            '[[slnc 500]] So here is the question. [[slnc 300]] How '
            'should the shop use it?'
        ),
    ),
    dict(
        key='03-leak', kind='console', title='Their Model, Everywhere',
        body="""ONE. Their model.
  the old system sends strings:
  QTY_ON_HND=0012,
  IN_STK_FLG=Y, ITM_STAT=A.

  places in the shop that have
  learnt those codes: 4.""",
        narration=(
            'First, the naive way: their model, everywhere. [[slnc 400]] '
            'The old system sends text. [[slnc 300]] A quantity written '
            'as zero zero one two. [[slnc 300]] A stock flag of Y. [[slnc '
            '300]] And a status code of A. [[slnc 500]] Four features in '
            'the shop read that record directly. [[slnc 300]] So four '
            'places have each learned what those codes mean. [[slnc 300]] '
            'It works, for today.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A layer between the shop and', 'the old system.', '', 'It is the only class that knows', 'their codes.', '', "It translates into the shop's", 'own model, and refuses what it', 'cannot translate.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Put a layer between the shop '
            'and the old system. [[slnc 300]] It is the only class that '
            'knows the old codes. [[slnc 400]] It translates them into '
            "the shop's own model. [[slnc 300]] And it refuses anything "
            'it cannot translate. [[slnc 300]] So bad data stops at the '
            'door.'
        ),
    ),
    dict(
        key='05-translate', kind='console', title='Their Model, Translated Once',
        body="""TWO. Translated.
  MUG-BLUE: 12, IN_STOCK.
  MUG-OLD: 0, DISCONTINUED.
  TEA-050: 240, IN_STOCK.

  no code crossed the layer.""",
        narration=(
            'Second demo: translated, once. [[slnc 400]] Each old record '
            'becomes a stock level, with a real number, and a clear '
            'meaning. [[slnc 500]] The blue mug: twelve, in stock. [[slnc '
            '300]] The old mug: none, discontinued. [[slnc 300]] The tea: '
            'two hundred and forty, in stock. [[slnc 500]] Not a single '
            'old code crossed the layer.'
        ),
    ),
    dict(
        key='06-bad', kind='console', title='Bad Data Stops At The Door',
        body="""THREE. Bad data.
  quantity 12X.
  the shortcut: a number format
  error, no sku.

  the layer: legacy data for
  MUG-BLUE: quantity 12X is not
  a number.""",
        narration=(
            'Third demo: bad data stops at the door. [[slnc 400]] The old '
            'system sends a quantity of twelve X. [[slnc 500]] Without '
            'the layer, the error happens deep inside a report. [[slnc '
            '300]] It says only that a number could not be read, and does '
            'not say which item. [[slnc 500]] With the layer, the record '
            'is refused at the door. [[slnc 300]] And the message says: '
            'legacy data for the blue mug, quantity twelve X is not a '
            'number.'
        ),
    ),
    dict(
        key='07-change', kind='console', title='The Other Side Changes',
        body="""FOUR. A new code, H.
  the shortcut: page says in
  stock, basket allows it.
  four private guesses.

  the layer: ON_HOLD, cannot be
  bought. one decision.""",
        narration=(
            'Fourth demo: the other side changes. [[slnc 400]] The old '
            'system starts sending a new status code, H, meaning on hold. '
            '[[slnc 300]] And it tells nobody. [[slnc 500]] Without the '
            'layer, the four features each guess. [[slnc 300]] The '
            'product page says, in stock. [[slnc 300]] And the basket '
            'lets a customer buy it. [[slnc 500]] With the layer, there '
            'is one decision, in one place. [[slnc 300]] On hold, and it '
            'cannot be bought.'
        ),
    ),
    dict(
        key='08-cost', kind='console', title='What The Layer Costs',
        body="""FIVE. The cost.
  7 fields from the old system.
  4 used.
  dropped: last count date,
  warehouse, unit.

  a new need means extending
  the layer.""",
        narration=(
            'Fifth demo: what the layer costs. [[slnc 400]] Each old '
            'record has seven fields. [[slnc 300]] The shop uses four. '
            '[[slnc 300]] The layer drops three: the last stock count '
            'date, the warehouse, and the unit. [[slnc 500]] The day a '
            'feature needs one of those, the layer must be extended. '
            "[[slnc 300]] And the shop's model with it. [[slnc 300]] That "
            'is the price of keeping your model clean.'
        ),
    ),
    dict(
        key='09-protect', kind='console', title='What The Layer Protects',
        body="""SIX. Protected.
  the shop's words: IN_STOCK,
  OUT_OF_STOCK, DISCONTINUED,
  ON_HOLD.

  replace the old system: one
  new adapter, nothing else.""",
        narration=(
            'Last demo: what the layer protects. [[slnc 400]] The shop '
            'has four availability words of its own. [[slnc 300]] In '
            'stock, out of stock, discontinued, and on hold. [[slnc 500]] '
            "The old system's codes stay behind the layer. [[slnc 300]] "
            'So if the old system is ever replaced, you write one new '
            'adapter. [[slnc 300]] Nothing else in the shop changes.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['An interface in your domain and an', 'adapter class that implements it', '', 'Mapping code between two sets of', 'types with different names for the', '', "A package for the other system's", 'types that nothing but one class'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for an interface in your own domain, with '
            'an adapter class that implements it, by calling another '
            'system. [[slnc 300]] Look for mapping code between two sets '
            'of types, with different names for the same idea. [[slnc '
            "300]] Look for a package of the other system's types, used "
            'by only one class. [[slnc 300]] And look for names like '
            'legacy adapter, translator, or facade, around an old '
            'service.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use an anti-corruption layer when', 'your model must stay clean against', 'a system you do not control:', 'legacy, third-party, or a very', 'different one. Put every', 'translation in one adapter, refuse', 'what cannot be translated, and', 'list what you drop. Do not build', 'one for a system whose model'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use an anti-corruption '
            'layer when your model must stay clean, next to a system you '
            "do not control. [[slnc 300]] An old system, a third party's "
            'system, or one with a very different model. [[slnc 500]] Put '
            'every translation in one adapter. [[slnc 300]] Refuse '
            'anything that cannot be translated. [[slnc 300]] And write '
            'down what you drop. [[slnc 500]] Do not build one for a '
            'system whose model already matches yours.'
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
        body=["When the other system's model", 'already matches yours, or when it', 'is small and stable, a direct call', 'is simpler. The layer earns its', 'place against a model that is', 'foreign, large or changing.'],
        narration=(
            'So, when is this too much? [[slnc 400]] When the other '
            "system's model already matches yours, or when it is small "
            'and never changes, a direct call is simpler. [[slnc 400]] '
            'The layer earns its place against a model that is foreign, '
            'large, or changing.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Anti-Corruption Layer. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] An '
            "anti-corruption layer keeps someone else's ideas out of your "
            'model, at the price of a translator you must maintain. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 500]] Here is one exercise to try. [[slnc 300]] Add a '
            'new status code to the old system. [[slnc 300]] Then decide '
            'what the layer should make of it. [[slnc 500]] If this '
            'helped, a like really does help other people find it. [[slnc '
            "300]] And subscribe, if you'd like the rest of the series. "
            '[[slnc 400]] Thanks for watching.'
        ),
    ),
]
