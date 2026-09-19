"""Scene definitions for the Interpreter with SpEL teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Interpreter with SpEL',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Interpreter '
            'pattern with Spring Expression Language, in Java, and it is '
            'written and presented by Jayasekhar Konduru. [[slnc 300]] It '
            'is the framework version of the Interpreter video. That one '
            'turned promotion rules written as text into a tree of small '
            'rule objects, and applied them to orders, with a parser '
            'written by hand. This one shows the same idea inside Spring '
            'Expression Language. [[slnc 350]] The plain definition, in '
            'short: SpEL is a ready made interpreter. A rule written as '
            'text becomes a tree, and the tree is evaluated against an '
            'object. [[slnc 300]] By the end you will see the same '
            'promotion rules run by a library instead of a hand-built '
            'parser, then see the costs: a bigger language than you '
            'wanted, errors that arrive late, and a safety choice you '
            'must make.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Interpreter, the hand-built video,', 'turns a promotion written as text', 'into a tree of small rules.', '', 'It writes its own parser.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Interpreter video. If you have not '
            'seen it, start there. It turns a promotion written as text '
            'into a tree of small rule objects, with a parser written by '
            'hand, and applies it to orders. [[slnc 300]] This one uses '
            'the same example. It does not teach the pattern again. It '
            'shows what Spring Expression Language does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: the expression', 'language library from Spring.', '', 'It replaces the parser and the', 'rule classes.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Expression '
            'Language is. Spring includes an expression language, called '
            'SpEL. It parses a line of text into a tree, and evaluates '
            'the tree against any object. [[slnc 300]] And a promise: '
            'skipping this video loses none of the pattern. The '
            'hand-built one teaches all of it.'
        ),
    ),
    dict(
        key='04-text', kind='console', title='The Rules Are Text',
        body="""ONE. The rules are text.
  UKBIG: country == UK and
  basketPence > 5000

  asha: UKBIG
  ben: WELCOME10, NOTUK
  carol: UKBIG, BULK""",
        narration=(
            'First, the rules are text. Welcome ten: first order. UK big: '
            'country is UK, and the basket is over fifty pounds. Bulk: '
            'five items or a basket over two hundred pounds. Not UK: '
            'everyone else. [[slnc 300]] Asha gets UK big. Ben gets '
            'welcome and not UK. Carol gets UK big and bulk. There is no '
            'parser in this project, and no rule class.'
        ),
    ),
    dict(
        key='05-free', kind='console', title='The Language Came Free',
        body="""TWO. Free features.
  a conditional, a pattern
  match and a remainder.

  nothing new was written.""",
        narration=(
            'Second, the language came free. A conditional, a pattern '
            'match against a voucher code, and a remainder all work, and '
            'we wrote none of them. In the hand built version, each one '
            'was a new class. [[slnc 300]] That is the gain. The cost is '
            'next.'
        ),
    ),
    dict(
        key='06-errors', kind='console', title='Two Kinds Of Typo',
        body="""THREE. Two typos.
  bad syntax: refused when the
  book is built.

  a misspelled name: accepted,
  fails when the first order
  arrives.""",
        narration=(
            'Third, two kinds of typo. A syntax error, two ands in a row, '
            'is refused when the book is built. Good. A misspelled '
            'property name is accepted, because nothing checks names '
            'until there is an order. It fails when the first order '
            'arrives. [[slnc 300]] The defence is a test that loads every '
            'rule against a sample order.'
        ),
    ),
    dict(
        key='07-open', kind='console', title='The Language Can Reach The Program',
        body="""FOUR. Reaching out.
  full context: a rule calls
  a static method.

  read-only: refused, and
  method calls too.

  a rule can only read
  properties.""",
        narration=(
            'Fourth, the danger. In the full context, a rule can call any '
            'static method in the program. Here it only reads a system '
            'property, but it could call anything. The read only context '
            'refuses it. It also refuses method calls. [[slnc 300]] Rules '
            'written by marketing are input, and input is not trusted. '
            'Use the read only context.'
        ),
    ),
    dict(
        key='08-null', kind='console', title='Missing Values',
        body="""FIVE. Missing values.
  asha has no voucher:
  voucher.empty fails.

  voucher?.empty: no match
  for asha, a match for ben.""",
        narration=(
            'Fifth, missing values. Asha has no voucher, so reading a '
            'property of it fails. Put a question mark before the dot, '
            'and the failure becomes no match. Asha gets nothing, and '
            'Ben, who has a voucher, gets his promotion.'
        ),
    ),
    dict(
        key='09-once', kind='console', title='Parsed Once',
        body="""SIX. Parsed once.
  1000 orders through the
  same four trees:
  1500 promotions.

  built 4 times, not 4000.""",
        narration=(
            'Last, the cost of parsing. The four rules are parsed once, '
            'when the book is built. A thousand orders then go through '
            'the same four trees, and fifteen hundred promotions apply. '
            'Parsing is the expensive part, so do it at startup, not per '
            'order.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Use it when rules change', 'without a release.', '', 'Parse once, at startup.', '', 'Read-only context for rules', 'from people.', '', 'Test every rule.'],
        narration=(
            'My verdict, plainly. Use it when rules change without a '
            'release. Parse once, at startup. Use the read only context '
            'for rules that come from people. And test every rule against '
            'real orders.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['SpelExpressionParser.', '', '@Value with a hash and braces.', '', '@PreAuthorize with a string.'],
        narration=(
            'How do you recognise this in code you did not write? A spel '
            'expression parser. A value annotation with a hash and '
            'braces. Or a pre authorize annotation with a string in it.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Value with a hash sign', 'and every @PreAuthorize.', '', 'Each is a SpEL expression.'],
        narration=(
            'You have met this in every value annotation with a hash '
            'sign, and every pre authorize. Each is a SpEL expression.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Framework 7,', 'spring-expression only.', '', 'No container, no Boot runtime.'],
        narration=(
            'For the record. The expression library from Spring Framework '
            'seven. No container, and no Boot runtime.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the real parser', 'and the real evaluation contexts.', '', 'Nothing depends on timing.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            'Everything is real: the real parser and the real evaluation '
            'contexts. Nothing depends on timing.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a fixed handful of rules,', 'plain Java is simpler and', 'checked by the compiler.'],
        narration=(
            'So when is it too much? For a fixed handful of rules, plain '
            'Java is simpler, and the compiler checks it.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the T operator in the', 'read-only context.'],
        narration=(
            "That's Interpreter with SpEL. [[slnc 250]] If you take one "
            'sentence away, take this one: SpEL is a ready-made '
            'interpreter, and the evaluation context is the safety '
            'choice. [[slnc 350]] The full source, the written notes, the '
            'diagrams and an animated walkthrough are all in the '
            'repository. [[slnc 300]] If you try one exercise, try the T '
            'operator in the read only context, and read the message. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
