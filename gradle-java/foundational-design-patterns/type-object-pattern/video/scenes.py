"""Scene definitions for the Type Object teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Type Object',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Type Object pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A type object turns the kind '
            'of a thing into data. [[slnc 300]] Instead of a subclass for '
            'each kind, there is one class. [[slnc 300]] And each object '
            'points to a type object, which holds whatever differs. '
            "[[slnc 600]] Think of a library's shelf labels. [[slnc 300]] "
            'The labels say how long each kind of book can be borrowed. '
            '[[slnc 300]] Change a label, and every book on that shelf '
            'follows the new rule. [[slnc 700]] In our online store, '
            'books, laptops, and groceries differ in only a few numbers. '
            '[[slnc 300]] Yet each one has its own class. [[slnc 500]] In '
            'this video, we replace those classes with one class and some '
            'data. [[slnc 300]] We will add a new kind while the program '
            'runs, change a rule in one place, and let one type inherit '
            'from another. [[slnc 300]] And then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Books: no tax, 3 pounds', 'to ship.', '', 'Laptops: 20 percent tax,', 'free shipping.', '', 'Groceries: 5 percent tax.', '', 'Next month: gift cards.'],
        narration=(
            'Here is the scenario. [[slnc 400]] Books have no tax, and '
            'cost three pounds to ship. [[slnc 300]] Laptops have twenty '
            'percent tax, and ship free. [[slnc 300]] Groceries have five '
            'percent tax. [[slnc 500]] And next month, the shop will '
            'start selling gift cards. [[slnc 500]] So here is the '
            'question. [[slnc 300]] Should each kind of product be its '
            'own class?'
        ),
    ),
    dict(
        key='03-class', kind='console', title='A Class For Each Kind',
        body="""ONE. A class for each kind.
  3 kinds, 3 classes,
  differing in three numbers.
  a novel: 1300.

  a gift card: a fourth class,
  a build, a release.""",
        narration=(
            'First, the naive way: a class for each kind. [[slnc 400]] '
            'Three kinds, three classes. [[slnc 300]] And they differ '
            'only in three numbers. [[slnc 500]] A novel costs thirteen '
            'pounds in total. [[slnc 500]] And a gift card is a fourth '
            'kind. [[slnc 300]] That means a fourth class, a new build, '
            'and a new release.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One class for the thing.', '', 'A type object for its kind,', 'holding what differs.', '', 'Each thing points at its type.', 'A new kind is a new type object.'],
        narration=(
            'Now, the pattern. [[slnc 400]] One class for the product. '
            '[[slnc 300]] A type object for its kind, which holds '
            'whatever differs. [[slnc 500]] Each product points to its '
            'type. [[slnc 300]] And a new kind is just a new type object.'
        ),
    ),
    dict(
        key='05-data', kind='console', title='A Type That Is Data',
        body="""TWO. A type that is data.
  one Product class.
  novel 1300, laptop 96000,
  tea 620.

  laptop return after 10 days:
  true; after 20: false.""",
        narration=(
            'Second demo: a type that is data. [[slnc 400]] Now there is '
            'just one product class. [[slnc 500]] A novel costs thirteen '
            'pounds. [[slnc 300]] A laptop costs nine hundred and sixty '
            'pounds. [[slnc 300]] And a pack of tea costs six pounds '
            'twenty. [[slnc 500]] A laptop can be returned after ten '
            'days. [[slnc 300]] But not after twenty.'
        ),
    ),
    dict(
        key='06-new', kind='console', title='A New Kind At Run Time',
        body="""THREE. A new kind.
  types: 3 before, 4 after.
  classes added: 0.
  a 25 pound card: 2500.
  can it be returned after 1
  day: false.""",
        narration=(
            'Third demo: a new kind, while the program runs. [[slnc 400]] '
            'Before, there are three product types. [[slnc 300]] After '
            'adding gift cards, there are four. [[slnc 300]] Classes '
            'added: none. [[slnc 500]] A twenty-five pound gift card '
            'costs exactly twenty-five pounds. [[slnc 300]] And it cannot '
            'be returned, even after one day.'
        ),
    ),
    dict(
        key='07-change', kind='console', title='Change The Type, Change Every Product',
        body="""FOUR. Change the type.
  tax: tea 20, coffee 40.
  grocery tax to 10 percent,
  in one place.
  tea 40, coffee 80.""",
        narration=(
            'Fourth demo: change the type, and every product follows. '
            '[[slnc 400]] The tax on a pack of tea is twenty pence. '
            '[[slnc 300]] On a bag of coffee, forty pence. [[slnc 500]] '
            'Now grocery tax is raised to ten percent, in one place. '
            "[[slnc 300]] The tea's tax becomes forty pence. [[slnc 300]] "
            "The coffee's becomes eighty pence."
        ),
    ),
    dict(
        key='08-inherit', kind='console', title='A Type That Inherits',
        body="""FIVE. A type that inherits.
  ebook states its shipping: 0.
  its tax 0 and return days 30
  come from book.""",
        narration=(
            'Fifth demo: a type that inherits. [[slnc 400]] An ebook type '
            'states only its shipping cost: nothing. [[slnc 500]] Its '
            'tax, which is zero, and its return period, thirty days, both '
            'come from the book type. [[slnc 300]] So the ebook only '
            'states what is different.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  a typo, bok: found when it
  runs; a class would not
  compile.

  a serial check is steps, not
  data: a flag, and code
  elsewhere.

  every difference: a new field.
  6 already.""",
        narration=(
            "Finally, the costs. [[slnc 400]] First, a typo in a type's "
            'name, like book spelled b o k, is only found when the '
            'program runs. [[slnc 300]] With a class for each kind, that '
            'typo would not even compile. [[slnc 500]] Second, laptops '
            'need their serial number checked. [[slnc 300]] But a type '
            'holds data, not steps. [[slnc 300]] A flag can say a check '
            'is needed, but the code that does the check lives somewhere '
            'else. [[slnc 500]] Third, every new difference between kinds '
            'becomes a new field. [[slnc 300]] And the code must remember '
            'to read it. [[slnc 300]] This type already has six fields.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A Type, Kind or Category object', 'referenced by another.', '', 'Rows in a product_types table,', 'with a foreign key from products.', '', 'Card, unit or enemy types in', 'games, defined in data files.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a Type, Kind, or Category object, '
            'pointed to by another object. [[slnc 300]] Look for a '
            'product types table in a database, with products linked to '
            'it. [[slnc 300]] Look for card types, unit types, or enemy '
            'types in games, defined in data files. [[slnc 300]] And '
            "Java's own Currency, Locale, and Charset classes, which "
            'describe things as data.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a type object when kinds', 'differ in data, and new kinds', 'should be added without new code.', 'Let types inherit defaults. Where', 'kinds differ in steps, use a', 'strategy or a subclass. Check the', 'name of a type early, and keep the', 'number of fields small.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a type object when '
            'kinds differ in data, and new kinds should be added without '
            'new code. [[slnc 300]] Let types inherit defaults from each '
            'other. [[slnc 500]] Where kinds differ in steps, use a '
            'strategy, or a subclass. [[slnc 300]] Check type names '
            'early. [[slnc 300]] And keep the number of fields small.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'Every number quoted comes from', "this program's own output.", '', 'Nothing depends on a clock,', 'so every run is the same.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] Every number you '
            "heard comes from the program's own output. [[slnc 300]] And "
            'nothing depends on the clock, so every run gives the same '
            'result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['If the kinds are few, fixed, and', 'differ in behaviour, plain', 'subclasses are clearer. A type', 'object pays off when kinds are', 'many, or added by non-programmers.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If the kinds are '
            'few, fixed, and differ in behaviour, plain subclasses are '
            'clearer. [[slnc 400]] A type object pays off when there are '
            'many kinds. [[slnc 300]] Or when new kinds are added by '
            'people who are not programmers.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Type Object pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] A type object '
            'turns kinds into data, so a new kind needs no new class, and '
            'the price is late errors, and behaviour that data cannot '
            'hold. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Add a type for frozen groceries. [[slnc 300]] Make it '
            'inherit from groceries, but cost more to ship. [[slnc 300]] '
            'Then check its total. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
