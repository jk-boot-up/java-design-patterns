"""Scene definitions for the Value Object teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Value Object',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Value Object pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A value object is a small '
            'object defined entirely by what it holds. [[slnc 300]] It '
            'never changes after it is made. [[slnc 300]] And it cannot '
            'be made wrong in the first place. [[slnc 600]] Think of a '
            'banknote. [[slnc 300]] One ten pound note is as good as any '
            'other ten pound note. [[slnc 300]] You do not care which one '
            'you hold, only what it is worth. [[slnc 700]] In our online '
            'store, the first thing to get right is money. [[slnc 500]] '
            'In this video, money as a bare number goes wrong in four '
            'ways. [[slnc 300]] Then one small type fixes every one of '
            'them. [[slnc 300]] And we will hear when not to use it.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The store adds up prices in pounds', 'and in dollars.', '', 'It shares bills between people.', '', "It stores customers' email addresses.", '', 'What should a price be?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The online store adds up '
            'prices, in pounds, and in dollars. [[slnc 300]] It splits a '
            'bill between several people. [[slnc 300]] And it stores each '
            "customer's email address. [[slnc 500]] So here is the "
            'question. [[slnc 300]] What should a price be? [[slnc 300]] '
            'A number? [[slnc 200]] A number and some text? [[slnc 200]] '
            'Or something of its own?'
        ),
    ),
    dict(
        key='03-double', kind='console', title='Money As A Double',
        body="""ONE. A double.
  three stamps at 1.10:
  3.3000000000000003.

  0.1 + 0.2 == 0.3: false.

  10 pounds + 10 dollars:
  20.0.""",
        narration=(
            'First, money as a plain decimal number, a double. [[slnc '
            '400]] Three stamps at one pound ten each should cost three '
            'pounds thirty. [[slnc 300]] But the result is three point '
            'three, followed by a long tail of zeros and a three. [[slnc '
            '500]] Point one plus point two is not exactly point three. '
            '[[slnc 500]] And ten pounds plus ten dollars comes to '
            'twenty, with no complaint at all. [[slnc 500]] The number '
            'has no idea what it is a number of.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A Money that holds whole pence', 'and a currency, together.', '', 'It never changes: every operation', 'returns a new one.', '', 'It refuses to be built wrong,', 'and refuses a mixed currency.'],
        narration=(
            'Now, the pattern. [[slnc 400]] A Money object that holds '
            'whole pence, and a currency, together, as one thing. [[slnc '
            '500]] It never changes. [[slnc 300]] Every operation returns '
            'a new Money. [[slnc 300]] It refuses to be created with bad '
            'data. [[slnc 300]] And it refuses to be added to money in '
            'another currency. [[slnc 500]] Everything else in this video '
            'follows from those four rules.'
        ),
    ),
    dict(
        key='05-value', kind='console', title='Money As A Value',
        body="""TWO. A value.
  three stamps: GBP 3.30.

  10 pounds + 10 dollars:
  refused, cannot combine
  GBP with USD.""",
        narration=(
            'Second demo: the same sums, with a value object. [[slnc '
            '400]] One hundred and ten pence, times three, is exactly '
            'three pounds thirty. [[slnc 500]] And ten pounds plus ten '
            'dollars is refused. [[slnc 300]] The message says: cannot '
            'combine pounds with dollars. [[slnc 500]] The amount and its '
            'currency travel together, so they can never be separated.'
        ),
    ),
    dict(
        key='06-equal', kind='console', title='Equal By Value',
        body="""THREE. Equal by value.
  three 5.00s in a set: 1.
  by identity: 3.

  5.00 GBP equals 5.00 GBP.
  5.00 GBP is not 5.00 USD.""",
        narration=(
            'Third demo: equal by value. [[slnc 400]] Three separate '
            'Money objects, each worth five pounds, are put into a set. '
            '[[slnc 300]] The set holds just one. [[slnc 300]] Because a '
            'value object is equal to any other with the same contents. '
            '[[slnc 500]] A class that compares objects by identity would '
            'keep all three. [[slnc 500]] And five pounds is not equal to '
            'five dollars, exactly as it should be.'
        ),
    ),
    dict(
        key='07-immutable', kind='console', title='Never Changed',
        body="""FOUR. Never changed.
  a shared, mutable price.
  order B takes 5.00 off.
  order A now costs 1500.

  with values: A still 20.00.""",
        narration=(
            'Fourth demo: never changed. [[slnc 400]] Two orders share '
            'one price object, and that object can be changed. [[slnc '
            '300]] Order B takes five pounds off. [[slnc 300]] Now order '
            'A costs fifteen pounds too, and nobody touched order A. '
            "[[slnc 500]] With value objects, order B's discount creates "
            'a new amount. [[slnc 300]] Order A still costs twenty '
            'pounds. [[slnc 500]] Sharing is safe, because nothing can '
            'change.'
        ),
    ),
    dict(
        key='08-valid', kind='console', title='Valid From The Start',
        body="""FIVE. Valid from the start.
  strings: 2 methods check,
  the third did not.
  stored: not an email.

  an EmailAddress: refused
  at the door.""",
        narration=(
            'Fifth demo: valid from the start. [[slnc 400]] Three methods '
            'receive an email address as plain text. [[slnc 300]] Two of '
            'them check it. [[slnc 300]] The third, written last, does '
            'not. [[slnc 300]] So a bad address gets stored. [[slnc 500]] '
            'An Email Address type checks the address once, when it is '
            'created. [[slnc 300]] If you are holding one, it is valid. '
            '[[slnc 300]] No method that receives one ever needs to check '
            'it again.'
        ),
    ),
    dict(
        key='09-split', kind='console', title='Splitting Is A Decision',
        body="""SIX. Splitting.
  10 pounds, three ways,
  rounded: 9.99. a penny
  vanished.

  allocated: 3.34, 3.33, 3.33.
  adds up to 10.00.""",
        narration=(
            'Last demo: splitting is a decision. [[slnc 400]] Split ten '
            'pounds three ways, rounding each share. [[slnc 300]] You get '
            'three pounds thirty-three, three times. [[slnc 300]] That '
            'adds up to nine ninety-nine. [[slnc 300]] A penny has '
            "vanished. [[slnc 500]] Money's allocate method gives the odd "
            'penny to the first share. [[slnc 300]] Three thirty-four, '
            'three thirty-three, and three thirty-three. [[slnc 300]] '
            'Exactly ten pounds. [[slnc 500]] Someone has to decide who '
            'gets the odd penny. [[slnc 300]] Now that rule lives in one '
            'place.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A record with no setters.', '', 'A constructor that throws.', '', 'Methods that return a new one:', 'plus, minus, withName.', '', 'java.time and BigDecimal.'],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Look for a record, or a final class, with no '
            'setters. [[slnc 300]] A constructor that throws an error on '
            'bad input. [[slnc 300]] Methods that return a new object, '
            "such as plus, or with name. [[slnc 300]] And Java's own date "
            'and time classes, and Big Decimal, which are value objects '
            'built into the language.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use it where a raw type', 'hides a meaning: money, email,', 'a date range.', '', 'A record, checked in its', 'constructor.', '', 'Do not wrap every string.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a value object '
            'wherever a plain type hides a meaning. [[slnc 300]] Money, '
            'an email address, a date range, or a quantity with a unit. '
            '[[slnc 500]] Make it a record. [[slnc 300]] Check its data '
            'in the constructor. [[slnc 300]] And give it the operations '
            'that belong to it. [[slnc 500]] But do not wrap every '
            'string.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'The floating point error and the', 'lost penny are real output,', 'not staged.', '', 'Nothing here uses a clock.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything is plain Java. [[slnc 300]] The decimal error, '
            'and the lost penny, are real output, not staged. [[slnc '
            '300]] And nothing here uses the clock, so every run gives '
            'the same result.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a value that means nothing', 'beyond its raw type, a wrapper', 'is noise.', '', 'It earns its place where mistakes', 'are expensive.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a value that '
            'means nothing beyond its plain type, like a loop counter, a '
            'wrapper is just noise. [[slnc 400]] A value object earns its '
            'place where mistakes are expensive, and where rules exist.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Write a Quantity type that', 'refuses a negative number.'],
        narration=(
            "That's the Value Object pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'value object makes the wrong thing impossible to say, '
            'instead of something every caller must remember to avoid. '
            '[[slnc 500]] The full source code, written notes, diagrams, '
            'and an animated walkthrough are all in the repository. '
            '[[slnc 500]] Here is one exercise to try. [[slnc 300]] Write '
            'a Quantity type. [[slnc 300]] And make it refuse a negative '
            'number. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
