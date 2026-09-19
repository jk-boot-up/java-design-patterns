"""Scene definitions for the Type Object teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Type Object',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Type Object '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'type object turns the kind of a thing into data. Instead of '
            'a subclass for each kind, there is one class, and each '
            'object points at a type object that holds what differs. '
            '[[slnc 350]] This is another project in the foundational '
            'category, whose subject is how an object gets hold of '
            'another, and how small idioms shape everyday Java. In our '
            'online store, books, laptops and groceries differ only in a '
            'few numbers, yet each has its own class. [[slnc 300]] By the '
            'end you will see a class for each kind that differs only in '
            'numbers, see one class with a type as data, see a new kind '
            'added at run time with no new class, see one change in a '
            'type reach every product, see a type inherit from another, '
            'and see the bill, which is typos found late and behaviour '
            'that data cannot hold.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Books: no tax, 3 pounds', 'to ship.', '', 'Laptops: 20 percent tax,', 'free shipping.', '', 'Groceries: 5 percent tax.', '', 'Next month: gift cards.'],
        narration=(
            'Here is the scenario. Books have no tax, and cost three '
            'pounds to ship. Laptops carry twenty percent tax, and ship '
            'free. Groceries have five percent tax. Next month, the shop '
            'will sell gift cards. [[slnc 300]] The question: is each '
            'kind a class?'
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
            'First, a class for each kind. Three kinds, three classes, '
            'and they differ only in three numbers. A novel totals '
            'thirteen hundred. A gift card is a fourth kind. That is a '
            'fourth class, a new build, and a release.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['One class for the thing.', '', 'A type object for its kind,', 'holding what differs.', '', 'Each thing points at its type.', 'A new kind is a new type object.'],
        narration=(
            'The pattern. One class for the thing. A type object for its '
            'kind, holding what differs. Each thing points at its type. A '
            'new kind is a new type object.'
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
            'Second, a type that is data. One product class. A novel '
            'totals thirteen hundred, a laptop ninety six thousand, and '
            'tea six twenty. Laptops can be returned after ten days, but '
            'not after twenty.'
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
            'Third, a new kind at run time. Types before: three. After: '
            'four. Classes added: none. A twenty five pound card totals '
            'twenty five hundred, and cannot be returned after one day.'
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
            'Fourth, change the type, change every product. Tax on tea is '
            'twenty, on coffee forty. Grocery tax is raised to ten '
            'percent, in one place. Tea is now forty, and coffee eighty.'
        ),
    ),
    dict(
        key='08-inherit', kind='console', title='A Type That Inherits',
        body="""FIVE. A type that inherits.
  ebook states its shipping: 0.
  its tax 0 and return days 30
  come from book.""",
        narration=(
            'Fifth, a type that inherits. An ebook states only its '
            'shipping: none. Its tax, zero, and its return days, thirty, '
            'come from book.'
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
            'Last, the bill. A typo, b o k, is found when the program '
            'runs. With a class for each kind, the typo would not '
            'compile. Laptops need a serial number checked, and a type '
            'holds data, not steps. A flag says so, but the code that '
            'checks it is still somewhere else. And every new difference '
            'between kinds is a new field, that the code must remember to '
            'read. The type has six fields already.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A Type, Kind or Category object', 'referenced by another.', '', 'Rows in a product_types table,', 'with a foreign key from products.', '', 'Card, unit or enemy types in', 'games, defined in data files.'],
        narration=(
            'How do you recognise this in code you did not write? A Type, '
            'Kind or Category object referenced by another. Rows in a '
            'product_types table, with a foreign key from products. Card, '
            'unit or enemy types in games, defined in data files. '
            'Currency, Locale and Charset, which describe things as data.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a type object when kinds', 'differ in data, and new kinds', 'should be added without new code.', 'Let types inherit defaults. Where', 'kinds differ in steps, use a', 'strategy or a subclass. Check the', 'name of a type early, and keep the', 'number of fields small.'],
        narration=(
            'Here is my verdict, plainly. Use a type object when kinds '
            'differ in data, and new kinds should be added without new '
            'code. Let types inherit defaults. Where kinds differ in '
            'steps, use a strategy or a subclass. Check the name of a '
            'type early, and keep the number of fields small.'
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
        body=['If the kinds are few, fixed, and', 'differ in behaviour, plain', 'subclasses are clearer. A type', 'object pays off when kinds are', 'many, or added by non-programmers.'],
        narration=(
            'So when is it too much? If the kinds are few, fixed, and '
            'differ in behaviour, plain subclasses are clearer. A type '
            'object pays off when kinds are many, or added by '
            'non-programmers.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Type Object. [[slnc 250]] If you take one sentence "
            'away, take this one: a type object makes kinds into data so '
            'that a new kind needs no new class, and the price is late '
            'errors and behaviour that data cannot hold. [[slnc 350]] The '
            'full source, the written notes, the diagrams and an animated '
            'walkthrough are all in the repository, running offline with '
            'nothing installed but a Java development kit. [[slnc 300]] '
            'If you try one exercise, add a type for frozen groceries '
            'that inherits from grocery but ships for more, and check its '
            'total. [[slnc 300]] If this helped, a like genuinely does '
            'help other people find it, and subscribe if you would like '
            'the rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
