"""Scene definitions for the Anti-Corruption Layer teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Anti-Corruption Layer',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Anti-Corruption '
            'Layer pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: an '
            'anti-corruption layer is a translator that sits between your '
            "own model and another system's model, so that the other "
            "system's ideas, names and codes never leak into yours. "
            '[[slnc 350]] This is the fifth project in the domain-driven '
            'design category, whose subject is writing code that says '
            'what the business says. In our online store, the thing we '
            'have to talk to is an old inventory system that nobody is '
            'allowed to change. [[slnc 300]] By the end you will see the '
            "old system's codes spread through four features, see one "
            'layer translate them once, see bad data stopped at the door, '
            'and see the cost of the layer, which is the bill.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Stock comes from an old system.', '', 'Every value is a string.', 'The codes are one letter.', 'It cannot be changed.', '', 'Its owners add new codes,', 'without telling anyone.', '', 'How should the shop use it?'],
        narration=(
            'Here is the scenario. The online store gets its stock levels '
            'from an old inventory system. It sends every value as a '
            'string. It uses one letter codes. It cannot be changed, and '
            'its owners add new codes now and then without telling '
            'anyone. [[slnc 300]] The question: how should the shop use '
            'it?'
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
            'First, their model, everywhere. The old system sends '
            'strings. A quantity of zero zero one two. A flag of Y. A '
            'status of A. Four features in the shop read that record '
            'directly, so four places have each learnt what those codes '
            'mean. It works, today.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A layer between the shop and', 'the old system.', '', 'It is the only class that knows', 'their codes.', '', "It translates into the shop's", 'own model, and refuses what it', 'cannot translate.'],
        narration=(
            'The pattern. A layer between the shop and the old system. It '
            'is the only class that knows the old codes. It translates '
            "them into the shop's own model. And it refuses anything it "
            'cannot translate, so bad data stops at the door.'
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
            'Second, translated once. Each old record becomes a stock '
            'level, with a real number and a meaning. The blue mug: '
            'twelve, in stock. The old mug: none, discontinued. The tea: '
            'two hundred and forty, in stock. No code has crossed the '
            'layer.'
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
            'Third, bad data. The old system sends a quantity of twelve '
            'X. The shortcut fails deep inside a report, with a number '
            'format exception, and no mention of which item. The layer '
            'refuses it at the door, and says: legacy data for the blue '
            'mug, quantity twelve X is not a number.'
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
            'Fourth, the other side changes. The old system starts '
            'sending H, for a product on hold, and tells nobody. The four '
            'features each guess. The page says in stock. The basket lets '
            'a customer buy it. [[slnc 300]] With the layer, there is one '
            'decision, in one place: on hold, and it cannot be bought.'
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
            'Fifth, the cost. The old row has seven fields, and the shop '
            'uses four. The layer drops three: the last count date, the '
            'warehouse and the unit. The day a feature needs one of them, '
            "the layer has to be extended, and the shop's model with it. "
            'That is the price of keeping the model clean.'
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
            'Last, what the layer protects. The shop has four '
            'availability words of its own: in stock, out of stock, '
            "discontinued, and on hold. The old system's words stay "
            'behind the layer. Replace the old system, and you write one '
            'new adapter. Nothing else changes.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['An interface in your domain and an', 'adapter class that implements it', '', 'Mapping code between two sets of', 'types with different names for the', '', "A package for the other system's", 'types that nothing but one class'],
        narration=(
            'How do you recognise this in code you did not write? An '
            'interface in your domain and an adapter class that '
            'implements it against another system. Mapping code between '
            'two sets of types with different names for the same idea. A '
            "package for the other system's types that nothing but one "
            'class imports. Names like LegacyXAdapter, Translator or '
            'Facade around an old service.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use an anti-corruption layer when', 'your model must stay clean against', 'a system you do not control:', 'legacy, third-party, or a very', 'different one. Put every', 'translation in one adapter, refuse', 'what cannot be translated, and', 'list what you drop. Do not build', 'one for a system whose model'],
        narration=(
            'Here is my verdict, plainly. Use an anti-corruption layer '
            'when your model must stay clean against a system you do not '
            'control: legacy, third-party, or a very different one. Put '
            'every translation in one adapter, refuse what cannot be '
            'translated, and list what you drop. Do not build one for a '
            'system whose model already matches yours.'
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
        body=["When the other system's model", 'already matches yours, or when it', 'is small and stable, a direct call', 'is simpler. The layer earns its', 'place against a model that is', 'foreign, large or changing.'],
        narration=(
            "So when is it too much? When the other system's model "
            'already matches yours, or when it is small and stable, a '
            'direct call is simpler. The layer earns its place against a '
            'model that is foreign, large or changing.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Anti-Corruption Layer. [[slnc 250]] If you take one "
            'sentence away, take this one: an anti-corruption layer keeps '
            "someone else's ideas out of yours, at the price of a "
            'translator you must maintain. [[slnc 350]] The full source, '
            'the written notes, the diagrams and an animated walkthrough '
            'are all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, add a new status to the old system, and '
            'decide what the layer should make of it. [[slnc 300]] If '
            'this helped, a like genuinely does help other people find '
            'it, and subscribe if you would like the rest of the series. '
            '[[slnc 250]] Thanks for watching.'
        ),
    ),
]
