"""Scene definitions for the Fluent Interface teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Fluent Interface',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Fluent Interface pattern, in Java. [[slnc 300]] This video '
            'is presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] A fluent interface lets '
            'method calls be chained together, so the code reads like a '
            'sentence. [[slnc 300]] Each call returns something that the '
            'next call can be made on. [[slnc 600]] Think of giving '
            'directions. [[slnc 300]] Go straight, then turn left, then '
            'stop at the bakery. [[slnc 300]] Each step follows naturally '
            'from the last. [[slnc 700]] In our online store, a product '
            'search takes five arguments. [[slnc 300]] And two of them '
            'are true-or-false values that are easy to swap. [[slnc 500]] '
            'In this video, swapped values still compile. [[slnc 300]] '
            'Then the same search becomes a sentence. [[slnc 300]] We '
            'will leave out optional parts, compare a query that changes '
            'itself with one that never does, and use guided steps that '
            'refuse a wrong order. [[slnc 300]] And then the cost.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['Search takes a category,', 'a price limit,', 'in stock only or not,', 'sorted or not,', 'and how many to show.', '', 'Two of the five are true or', 'false.', '', 'Can it read better?'],
        narration=(
            'Here is the scenario. [[slnc 400]] The catalogue search '
            'takes five things. [[slnc 300]] A category, a price limit, '
            'whether to show only items in stock, whether to sort by '
            'price, and how many results to show. [[slnc 500]] Two of '
            'those five are simply true or false. [[slnc 500]] So here is '
            'the question. [[slnc 300]] Can the call read better?'
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
            'First, the naive way: a long list of arguments. [[slnc 400]] '
            'Search for mugs, under twenty-five pounds, true, true, and '
            'ten. [[slnc 300]] The result is the blue mug and the big '
            'mug. [[slnc 500]] Now swap the two true-or-false values. '
            '[[slnc 300]] The result is three mugs, including one that is '
            'out of stock. [[slnc 500]] Both versions compile. [[slnc '
            '300]] Which true means in stock, and which means sorted? '
            '[[slnc 300]] You have to count the arguments to know.'
        ),
    ),
    dict(
        key='04-pattern', kind='bullets', title='The Pattern',
        body=['Each call returns something to', 'call the next on.', '', 'Each call names the one thing', 'it sets.', '', 'The code reads like a sentence.'],
        narration=(
            'Now, the pattern. [[slnc 400]] Each call returns something '
            'you can make the next call on. [[slnc 300]] Each call names '
            'the one thing it sets. [[slnc 300]] And the code reads like '
            'a sentence.'
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
            'Second demo: a sentence. [[slnc 400]] Search, category mugs, '
            'under twenty-five pounds, in stock, cheapest first, first '
            'ten. [[slnc 500]] The same answer as the long call. [[slnc '
            '300]] And every part names itself.'
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
            'Third demo: leave out what you do not need. [[slnc 400]] '
            'With only a category, the result is green tea. [[slnc 300]] '
            'With only a price limit of ten pounds, any category, the '
            'result is the blue mug, and green tea. [[slnc 500]] And the '
            'order of the optional parts does not matter.'
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
            'Fourth demo: does a call change the query? [[slnc 400]] '
            'First, a query that never changes. [[slnc 300]] Each call '
            'returns a new query. [[slnc 300]] The cheap search gives one '
            'mug. [[slnc 300]] The expensive search gives three. [[slnc '
            '300]] And the original base query still gives all four. '
            '[[slnc 600]] Now, a query that changes itself. [[slnc 300]] '
            'The cheap search and the expensive search both give the same '
            'three mugs. [[slnc 300]] Because they are the same object. '
            '[[slnc 300]] The cheap query was spoiled by the expensive '
            'one.'
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
            'Fifth demo: guided steps. [[slnc 400]] At the start, the '
            'only step offered is category. [[slnc 300]] After that, only '
            'a price limit is offered. [[slnc 300]] After that, cheapest '
            'first, in stock, or run. [[slnc 500]] A call made in the '
            'wrong order simply does not compile.'
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
            'Finally, the costs. [[slnc 400]] A price limit of minus five '
            'was accepted, and nothing complained. [[slnc 300]] It only '
            'failed at the end, when the search ran, saying the price '
            'limit is below zero. [[slnc 500]] The mistake and the report '
            'are on different steps of one long line. [[slnc 500]] A '
            'debugger cannot stop between the calls in one chain. [[slnc '
            '300]] And an error report names the line, not the step. '
            '[[slnc 500]] Finally, it is a small language someone '
            'designed. [[slnc 300]] This one has seven methods to learn, '
            'and to maintain.'
        ),
    ),
    dict(
        key='10-recognise', kind='bullets', title='How To Recognise It',
        body=['Java streams: list.stream().filter', '(...).map(...).toList().', '', 'StringBuilder.append(...).append(.', '..).', '', 'jOOQ, QueryDSL, AssertJ and', "Mockito's"],
        narration=(
            'How can you spot this pattern in code someone else wrote? '
            '[[slnc 400]] Java streams are fluent: stream, filter, map, '
            'and to list. [[slnc 300]] String Builder, with append after '
            'append. [[slnc 300]] Testing libraries, like AssertJ, and '
            "Mockito's when, then return. [[slnc 300]] And builders, "
            'where you set a name, then an age, then call build.'
        ),
    ),
    dict(
        key='11-verdict', kind='bullets', title='The Verdict',
        body=['Use a fluent interface where many', 'optional settings make a plain', 'call hard to read. Make each call', 'return a new object, unless the', 'object is a builder used once.', 'Check values in each call, not at', 'the end. Use staged types when', 'order matters. Keep it small,', 'since it is a language you must'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use a fluent interface '
            'where many optional settings make a plain call hard to read. '
            '[[slnc 500]] Make each call return a new object. [[slnc '
            '300]] Unless the object is a builder, used once. [[slnc '
            '300]] Check values in each call, not at the end. [[slnc '
            '300]] Use guided steps when the order matters. [[slnc 500]] '
            'And keep it small, because it is a language you must '
            'maintain.'
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
        body=['For two or three obvious', 'arguments, a plain call is', 'shorter. A fluent API costs a', 'class, a design and its upkeep.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For two or three '
            'obvious arguments, a plain call is shorter. [[slnc 400]] A '
            'fluent interface costs a class, a design, and ongoing '
            'upkeep.'
        ),
    ),
    dict(
        key='14-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the exercises in', 'the session guide.'],
        narration=(
            "That's the Fluent Interface pattern. [[slnc 400]] If you "
            'remember one sentence, make it this one. [[slnc 300]] A '
            'fluent interface makes calls read like a sentence, and the '
            'price is errors found late, harder debugging, and a small '
            'language to maintain. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Add a step that limits results to one brand. '
            '[[slnc 300]] And decide where in the chain it may appear. '
            '[[slnc 500]] If this helped, a like really does help other '
            "people find it. [[slnc 300]] And subscribe, if you'd like "
            'the rest of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
