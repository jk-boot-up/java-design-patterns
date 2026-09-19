"""Scene definitions for the Fluent Interface teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Fluent Interface',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Fluent Interface '
            'pattern in Java, and it is written and presented by '
            'Jayasekhar Konduru. [[slnc 300]] The plain definition: a '
            'fluent interface lets calls be chained, so that code reads '
            'like a sentence. Each call returns something that the next '
            'call can be made on. [[slnc 350]] This is another project in '
            'the foundational category, whose subject is how an object '
            'gets hold of another, and how small idioms shape everyday '
            'Java. In our online store, a product search takes five '
            'arguments, and two of them are booleans that are easy to '
            'swap. [[slnc 300]] By the end you will see a long argument '
            'list where swapped booleans still compile, see the same '
            'search as a sentence, see optional parts left out, see the '
            'difference between a query that changes itself and one that '
            'never does, see guided steps that refuse a wrong order, and '
            'see the bill, which is late errors and awkward debugging.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Search takes a category,', 'a price limit,', 'in stock only or not,', 'sorted or not,', 'and how many to show.', '', 'Two of the five are true or', 'false.', '', 'Can it read better?'],
        narration=(
            'Here is the scenario. The catalog search takes a category, a '
            'price limit, whether to show only what is in stock, whether '
            'to sort by price, and how many to show. Two of the five are '
            'true or false. [[slnc 300]] The question: can it read '
            'better?'
        ),
    ),
    dict(
        key='03-args', kind='console', title='A Long List Of Arguments',
        body="""ONE. A long argument list.
  mugs, 2500, true, true, 10:
  Blue Mug, Big Mug.
  two booleans swapped:
  3 mugs, one out of stock.

  both compile.""",
        narration=(
            'First, a long list of arguments. The find call with mugs, '
            'twenty five hundred, true, true and ten gives the blue mug '
            'and the big mug. With the two booleans the other way round, '
            'it gives three mugs, including one that is not in stock. '
            'Both compile. Which is in stock, and which is the sort? You '
            'must count the arguments to know.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Each call returns something to', 'call the next on.', '', 'Each call names the one thing', 'it sets.', '', 'The code reads like a sentence.'],
        narration=(
            'The pattern. Each call returns something to call the next '
            'on. Each call names the one thing it sets. The code reads '
            'like a sentence.'
        ),
    ),
    dict(
        key='05-sentence', kind='console', title='A Sentence',
        body="""TWO. A sentence.
  search, category mugs,
  under 2500, in stock,
  cheapest first, first 10:
  Blue Mug, Big Mug.

  every part names itself.""",
        narration=(
            'Second, a sentence. Search, category mugs, under twenty five '
            'hundred, in stock, cheapest first, first ten. The same '
            'answer as the long call, and every part names itself.'
        ),
    ),
    dict(
        key='06-optional', kind='console', title='Leave Out What You Do Not Need',
        body="""THREE. Leave out what you don't
  need.
  category only: Green Tea.
  under 1000, any category:
  Blue Mug, Green Tea.

  order of optional parts does
  not matter.""",
        narration=(
            'Third, leave out what you do not need. Category only: green '
            'tea. Under a thousand, any category: the blue mug, and green '
            'tea. And the order of the optional parts does not matter.'
        ),
    ),
    dict(
        key='07-mutable', kind='console', title='Does A Call Change The Query?',
        body="""FOUR. Does a call change it?
  never changing:
  cheap 1, dear 3, base 4.
  changing itself:
  cheap 3, dear 3.
  the same object.
  cheap was spoiled by dear.""",
        narration=(
            'Fourth, does a call change the query? A query that never '
            'changes: cheap gives the blue mug, dear gives three mugs, '
            'and the base still gives four. A query that changes itself: '
            'cheap and dear give the same three mugs. They are the same '
            'object. The cheap query was spoiled by the dear one.'
        ),
    ),
    dict(
        key='08-steps', kind='console', title='Guided Steps',
        body="""FIVE. Guided steps.
  at the start: category.
  then: under.
  then: cheapestFirst, inStock,
  run.

  a call out of order does not
  compile.""",
        narration=(
            'Fifth, guided steps. At the start, the only thing offered is '
            'category. Then, under. Then, cheapest first, in stock, or '
            'run. A call out of order does not compile.'
        ),
    ),
    dict(
        key='09-bill', kind='console', title='The Bill',
        body="""SIX. The bill.
  under(-5) was accepted.
  it failed later, at run().
  the mistake and the report are
  on different steps.

  a debugger cannot stop between
  the calls in a chain.

  a small language to keep:
  7 methods.""",
        narration=(
            'Last, the bill. Under minus five was accepted, and nothing '
            'complained. It failed at run, saying the price limit is '
            'below zero. The mistake and the report are on different '
            'steps of one long line. A debugger cannot stop between the '
            'calls of one chain, and a stack trace names the line, not '
            'the step. And it is a small language that someone designed: '
            'this one has seven methods to learn, and to keep.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Java streams: list.stream().filter', '(...).map(...).toList().', '', 'StringBuilder.append(...).append(.', '..).', '', 'jOOQ, QueryDSL, AssertJ and', "Mockito's"],
        narration=(
            'How do you recognise this in code you did not write? Java '
            'streams: list.stream().filter(...).map(...).toList(). '
            'StringBuilder.append(...).append(...). jOOQ, QueryDSL, '
            "AssertJ and Mockito's when(...).thenReturn(...). Builders "
            'with .name(...).age(...).build().'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a fluent interface where many', 'optional settings make a plain', 'call hard to read. Make each call', 'return a new object, unless the', 'object is a builder used once.', 'Check values in each call, not at', 'the end. Use staged types when', 'order matters. Keep it small,', 'since it is a language you must'],
        narration=(
            'Here is my verdict, plainly. Use a fluent interface where '
            'many optional settings make a plain call hard to read. Make '
            'each call return a new object, unless the object is a '
            'builder used once. Check values in each call, not at the '
            'end. Use staged types when order matters. Keep it small, '
            'since it is a language you must maintain.'
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
        body=['For two or three obvious', 'arguments, a plain call is', 'shorter. A fluent API costs a', 'class, a design and its upkeep.'],
        narration=(
            'So when is it too much? For two or three obvious arguments, '
            'a plain call is shorter. A fluent API costs a class, a '
            'design and its upkeep.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's Fluent Interface. [[slnc 250]] If you take one "
            'sentence away, take this one: a fluent interface makes calls '
            'read like a sentence, and the price is errors found late, '
            'debugging that is harder, and a small language to maintain. '
            '[[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository, running offline with nothing installed but a '
            'Java development kit. [[slnc 300]] If you try one exercise, '
            'add a step that limits results to one category, and decide '
            'where in the chain it may appear. [[slnc 300]] If this '
            'helped, a like genuinely does help other people find it, and '
            'subscribe if you would like the rest of the series. [[slnc '
            '250]] Thanks for watching.'
        ),
    ),
]
