"""Scene definitions for the Interpreter with SpEL teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Interpreter with SpEL',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Interpreter pattern, in Java, using the Spring Expression '
            'Language. [[slnc 300]] This video is presented by Jayasekhar '
            'Konduru. [[slnc 600]] First, a simple definition. [[slnc '
            '300]] The Interpreter pattern turns sentences in a small '
            'language into a tree of objects, and then runs that tree. '
            '[[slnc 500]] The Spring Expression Language, called SpEL, is '
            'a ready-made interpreter. [[slnc 300]] You give it a rule '
            'written as text. [[slnc 300]] It turns the text into a tree, '
            'and checks the tree against an object. [[slnc 600]] Think of '
            'a calculator. [[slnc 300]] You type a sum as text, and it '
            'works out the answer. [[slnc 300]] You never have to build '
            'the calculator yourself. [[slnc 700]] This is the framework '
            'version of the Interpreter video, with the same promotion '
            'rules for an online shop. [[slnc 400]] This time, a library '
            'runs the rules, instead of a hand-built reader. [[slnc 300]] '
            'Then we look at the costs: a bigger language than you '
            'wanted, errors that show up late, and a safety choice you '
            'must make.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Interpreter, the hand-built video,', 'turns a promotion written as text', 'into a tree of small rules.', '', 'It writes its own parser.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Interpreter video. [[slnc 400]] That '
            'one turns a promotion written as text into a tree of small '
            'rule objects. [[slnc 300]] And it writes its own reader for '
            'the text. [[slnc 500]] If you are new to the pattern, watch '
            'that one first. [[slnc 400]] Here, we keep the same example, '
            'and ask what SpEL does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: the expression', 'language library from Spring.', '', 'It replaces the parser and the', 'rule classes.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            "One thing is new in this project: Spring's expression "
            'language library. [[slnc 400]] It reads a line of text, '
            'turns it into a tree, and evaluates that tree against any '
            'object. [[slnc 400]] It replaces both the hand-written '
            'reader and all the rule classes. [[slnc 500]] And one '
            'promise. [[slnc 300]] If you skip this video, you lose none '
            'of the pattern. [[slnc 300]] This one is about the tool.'
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
            'First demo: the rules are plain text. [[slnc 400]] Welcome '
            "ten: the customer's first order. [[slnc 300]] UK big: the "
            'country is UK, and the basket is over fifty pounds. [[slnc '
            '300]] Bulk: five items or more, or a basket over two hundred '
            'pounds. [[slnc 300]] Not UK: everyone outside the UK. [[slnc '
            '500]] Asha gets UK big. [[slnc 300]] Ben gets welcome ten, '
            'and not UK. [[slnc 300]] Carol gets UK big, and bulk. [[slnc '
            '500]] There is no reader in this project, and no rule '
            'classes. [[slnc 300]] The library does it all.'
        ),
    ),
    dict(
        key='05-free', kind='console', title='The Language Came Free',
        body="""TWO. Free features.
  a conditional, a pattern
  match and a remainder.

  nothing new was written.""",
        narration=(
            'Second demo: the language comes free. [[slnc 400]] A rule '
            'can use an if-then-else, a pattern match on a voucher code, '
            'and a remainder calculation. [[slnc 300]] All of them just '
            'work, and we wrote none of them. [[slnc 400]] In the '
            'hand-built version, each one would have been a new class. '
            '[[slnc 500]] That is the gain. [[slnc 300]] Now for the '
            'costs.'
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
            'Third demo: two kinds of typo. [[slnc 400]] First, a grammar '
            'mistake, like two ands in a row. [[slnc 300]] That is '
            'refused as soon as the rule book is built. [[slnc 300]] '
            'Good. [[slnc 500]] Second, a misspelled property name. '
            '[[slnc 300]] That is accepted, because nothing checks names '
            'until an order arrives. [[slnc 300]] So it fails later, when '
            'the first real order comes in. [[slnc 500]] The defence is a '
            'test that loads every rule, and checks it against a sample '
            'order.'
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
            'Fourth demo: the danger. [[slnc 400]] With the full '
            'evaluation context, a rule can call any static method in the '
            'whole program. [[slnc 300]] Here, it only reads a system '
            'setting. [[slnc 300]] But it could call anything. [[slnc '
            '500]] The read-only context refuses that. [[slnc 300]] It '
            'refuses method calls too. [[slnc 300]] A rule can only read '
            'properties. [[slnc 500]] Rules written by the marketing team '
            'are input. [[slnc 300]] And input must never be trusted. '
            '[[slnc 300]] So use the read-only context.'
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
            'Fifth demo: missing values. [[slnc 400]] Asha has no '
            'voucher. [[slnc 300]] So a rule that reads a property of her '
            'voucher fails with an error. [[slnc 500]] Add a question '
            'mark before the dot, and a missing voucher simply means no '
            'match. [[slnc 400]] Now Asha gets nothing, without an error. '
            '[[slnc 300]] And Ben, who does have a voucher, gets his '
            'promotion.'
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
            'Last demo: the cost of reading rules. [[slnc 400]] The four '
            'rules are read and turned into trees once, when the rule '
            'book is built. [[slnc 400]] Then a thousand orders go '
            'through those same four trees. [[slnc 300]] Fifteen hundred '
            'promotions apply. [[slnc 500]] The trees were built four '
            'times, not four thousand. [[slnc 300]] Reading the text is '
            'the expensive part, so do it at startup, not for every '
            'order.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Use it when rules change', 'without a release.', '', 'Parse once, at startup.', '', 'Read-only context for rules', 'from people.', '', 'Test every rule.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use it when rules must '
            'change without a release. [[slnc 300]] Read the rules once, '
            'at startup. [[slnc 300]] Use the read-only context for any '
            'rule written by people. [[slnc 300]] And test every rule '
            'against real orders.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['SpelExpressionParser.', '', '@Value with a hash and braces.', '', '@PreAuthorize with a string.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for the SpEL Expression Parser class. [[slnc '
            '300]] Look for an at Value annotation with a hash sign and '
            'curly braces. [[slnc 300]] Or an at Pre Authorize annotation '
            'with a text rule inside it.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Every @Value with a hash sign', 'and every @PreAuthorize.', '', 'Each is a SpEL expression.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In every at '
            'Value annotation that uses a hash sign. [[slnc 300]] And in '
            'every at Pre Authorize annotation. [[slnc 300]] Each of '
            'those holds a SpEL expression.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Framework 7,', 'spring-expression only.', '', 'No container, no Boot runtime.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Just the '
            'expression library, from Spring Framework seven. [[slnc '
            '300]] No container, and no Spring Boot.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=['Everything is real: the real parser', 'and the real evaluation contexts.', '', 'Nothing depends on timing.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 300]] '
            'Everything in it is real. [[slnc 300]] The real expression '
            'reader, and the real evaluation contexts. [[slnc 300]] And '
            'nothing depends on timing.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['For a fixed handful of rules,', 'plain Java is simpler and', 'checked by the compiler.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a small, fixed '
            'set of rules, plain Java is simpler. [[slnc 300]] And the '
            'compiler checks it for you.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Try the T operator in the', 'read-only context.'],
        narration=(
            "That's Interpreter with SpEL. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] SpEL is a '
            'ready-made interpreter, and choosing the evaluation context '
            'is your safety decision. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] In the read-only context, try a rule that calls '
            'a static method. [[slnc 300]] Then read the message it gives '
            'you. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
