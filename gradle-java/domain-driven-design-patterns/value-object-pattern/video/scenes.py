"""Scene definitions for the Value Object teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Value Object',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Value Object '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'value object is a small object that is defined entirely by '
            'what it holds, is never changed after it is made, and cannot '
            'be made wrong in the first place. [[slnc 350]] This is the '
            'first project in the domain-driven design category, whose '
            'subject is writing code that says what the business says. In '
            'our online store, the first thing to get right is money. '
            '[[slnc 300]] By the end you will see money as a bare number '
            'go wrong four ways, then see one small type close every one '
            'of them, and hear when I would not use it.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['The store adds up prices in pounds', 'and in dollars.', '', 'It shares bills between people.', '', "It stores customers' email addresses.", '', 'What should a price be?'],
        narration=(
            'Here is the scenario. The online store adds up prices, in '
            'pounds and in dollars. It shares a bill between people, and '
            "it stores each customer's email address. [[slnc 300]] The "
            'question: what should a price be? A number? A number and a '
            'string? Or something of its own?'
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
            'First, money as a double. Three stamps at one pound ten come '
            'to three point three, followed by a long tail of zeros and a '
            'three. Point one plus point two is not point three. And ten '
            'pounds added to ten dollars comes to twenty, with no '
            'complaint at all. [[slnc 300]] The number has no idea what '
            'it is a number of.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['A Money that holds whole pence', 'and a currency, together.', '', 'It never changes: every operation', 'returns a new one.', '', 'It refuses to be built wrong,', 'and refuses a mixed currency.'],
        narration=(
            'The pattern. A money object that holds whole pence and a '
            'currency, together, as one thing. It never changes: every '
            'operation returns a new one. It refuses to be built wrong. '
            'And it refuses to be added to money in another currency. '
            'Everything else in this video is a consequence of those four '
            'sentences.'
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
            'Second, the same sum with a value. Whole pence, times three, '
            'is exactly three pounds thirty. And ten pounds plus ten '
            'dollars is refused, with a message that says why. The amount '
            'and its currency travel together, so they cannot be '
            'separated.'
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
            'Third, equality. Three separate objects, each five pounds, '
            'in a set. The set holds one, because a value object is equal '
            'to any other with the same contents. A class that compares '
            'by identity keeps all three. And five pounds is not equal to '
            'five dollars, as it should be.'
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
            'Fourth, never changed. Two orders share one price object, '
            'and it can be changed. Order B takes five pounds off. Order '
            'A now costs fifteen pounds, and nobody touched order A. '
            "[[slnc 300]] With values, order B's discount makes a new "
            'amount. Order A still pays twenty pounds. Sharing is safe, '
            'because nothing can change.'
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
            'Fifth, valid from the start. Three methods take an email as '
            'a string. Two check it. The third, written last, does not, '
            'and a bad address is stored. [[slnc 300]] An email address '
            'type checks once, when it is made. If you are holding one, '
            'it is valid. No method that receives one ever needs to check '
            'again. That is the same lesson as the null object.'
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
            'Last, splitting. Ten pounds three ways, rounded, is three '
            'thirty three, three times, which is nine ninety nine. A '
            'penny vanished. [[slnc 300]] Allocation gives the odd penny '
            'to the first share. Three thirty four, three thirty three, '
            'three thirty three, which is exactly ten pounds. Somebody '
            'has to decide who gets the odd penny. Now that rule lives in '
            'one place.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['A record with no setters.', '', 'A constructor that throws.', '', 'Methods that return a new one:', 'plus, minus, withName.', '', 'java.time and BigDecimal.'],
        narration=(
            'How do you recognise this in code you did not write? A '
            'record, or a final class, with no setters. A constructor '
            'that throws on bad input. Methods that return a new '
            'instance, such as plus, or with name. And the Java time '
            'classes and big decimal, which are value objects the '
            'language gave you.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use it where a raw type', 'hides a meaning: money, email,', 'a date range.', '', 'A record, checked in its', 'constructor.', '', 'Do not wrap every string.'],
        narration=(
            'Here is my verdict, plainly. Use a value object where a raw '
            'type hides a meaning: money, an email address, a date range, '
            'a quantity with a unit. Make it a record, check it in the '
            'constructor, and give it the operations that belong to it. '
            'And do not wrap every string.'
        ),
    ),
    dict(
        key='12-real', kind='bullets', title='What Is Real Here',
        body=['Everything is plain Java.', '', 'The floating point error and the', 'lost penny are real output,', 'not staged.', '', 'Nothing here uses a clock.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is plain Java. The floating point error and the '
            'lost penny are real output, not staged. Nothing here uses a '
            'clock, so every run is the same.'
        ),
    ),
    dict(
        key='13-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a value that means nothing', 'beyond its raw type, a wrapper', 'is noise.', '', 'It earns its place where mistakes', 'are expensive.'],
        narration=(
            'So when is it too much? For a value that means nothing '
            'beyond its raw type, like a loop counter, a wrapper is '
            'noise. It earns its place where mistakes are expensive, and '
            'where rules exist.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Write a Quantity type that', 'refuses a negative number.'],
        narration=(
            "That's Value Object. [[slnc 250]] If you take one sentence "
            'away, take this one: a value object makes the wrong thing '
            'impossible to say, instead of something every caller must '
            'remember to avoid. [[slnc 350]] The full source, the written '
            'notes, the diagrams and an animated walkthrough are all in '
            'the repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'write a quantity type that refuses a negative number. [[slnc '
            '300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of '
            'the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
