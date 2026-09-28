"""Scene definitions for the Interpreter teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Interpreter",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Interpreter pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Interpreter pattern is '
            'for small languages. [[slnc 300]] You write one small class '
            'for each kind of phrase in the language. [[slnc 300]] And '
            'bigger phrases are built by holding smaller ones. [[slnc '
            '400]] The result is a tree of objects that represents a '
            'sentence. [[slnc 300]] To run the sentence, you call one '
            'method on the top of the tree. [[slnc 600]] Think of a '
            'recipe card. [[slnc 300]] Mix the flour and the eggs, then '
            'bake. [[slnc 300]] The cook does not need a new cookbook for '
            'every cake, just a few words that combine. [[slnc 700]] In '
            "this video, we write an online shop's promotion rules as "
            'simple text, instead of as code. [[slnc 400]] By the end, '
            'you will know why a rule that can explain itself is worth '
            'more than a rule that merely works. [[slnc 300]] And you '
            "will know this pattern's honest limit."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online shop runs promotions.",
            "",
            "A promotion is a code, a percentage, and a rule:",
            "",
            "    SAVE10     10%    UK orders over £50",
            "    SAVE15     15%    UK orders over £100",
            "    FREESHIP    5%    UK orders of 3 items or more",
            "",
            "Written in Java, the first one is four lines,",
            "and there is nothing wrong with it:",
            "",
            "    if (\"UK\".equals(order.country())",
            "            && order.basketPounds() > 50) { return 10; }",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] An online shop runs '
            'promotions. [[slnc 300]] Each promotion has a code, a '
            'percentage off, and a rule about who qualifies. [[slnc 500]] '
            'Save ten gives ten percent off for UK orders over fifty '
            'pounds. [[slnc 300]] Save fifteen gives fifteen percent off '
            'for UK orders over one hundred pounds. [[slnc 300]] Free '
            'ship gives five percent off for UK orders of three items or '
            'more. [[slnc 500]] In Java, the first promotion is four '
            'lines of code, and there is nothing wrong with that. [[slnc '
            '500]] The trouble starts later. [[slnc 300]] Each new offer '
            'gets written by copying the one above it, and changing the '
            'numbers. [[slnc 300]] That is quick, and it looks correct.'
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Two Copies, Two Bugs, No Exceptions",
        body=[
            "SAVE15 gives money away:",
            "",
            "    if (order.basketPounds() > 100) { return 15; }",
            "",
            "    The ticket said 'over £100'. That it was UK-only was in",
            "    the paragraph above. No line was ever written for it.",
            "",
            "FREESHIP withholds it:",
            "",
            "    if (order.firstOrder() && \"UK\".equals(...) && ...)",
            "",
            "    Copied from a welcome offer that retired last spring.",
            "    A returning UK shopper with 3 items gets nothing.",
        ],
        narration=(
            'Here are two copies that went wrong, in opposite directions. '
            '[[slnc 500]] Save fifteen gives money away. [[slnc 300]] The '
            'request said fifteen percent off baskets over one hundred '
            'pounds. [[slnc 300]] The fact that it was for UK customers '
            'only was mentioned in an earlier paragraph. [[slnc 300]] So '
            'nobody wrote the country check. [[slnc 400]] Now every large '
            'overseas order gets fifteen percent off. [[slnc 300]] On a '
            'one hundred and twenty pound order, that is eighteen pounds '
            'lost, every time. [[slnc 600]] Free ship does the opposite. '
            '[[slnc 300]] It was copied from an old welcome offer, and it '
            "kept that offer's first-order check. [[slnc 300]] So a "
            'returning UK customer with three items gets nothing. [[slnc '
            '300]] And nobody complains, because a missing discount looks '
            'like a customer who simply did not qualify. [[slnc 600]] '
            'Neither bug causes an error. [[slnc 300]] Both are '
            'correct-looking code that compiled, passed review, and '
            'shipped.'
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — Every Rule Is a Branch",
        body="""public int bestPercentFor(Order order) {
    int best = 0;
    best = Math.max(best, save10(order));
    best = Math.max(best, save15(order));
    best = Math.max(best, freeship(order));
    return best;
}

private int save15(Order order) {
    if (order.basketPounds() > 100) {   // ...and the UK check?
        return 15;
    }
    return 0;
}""",
        narration=(
            'Here is the shape of the naive code. [[slnc 400]] One method '
            'per promotion, each with one if statement. [[slnc 300]] And '
            'one method at the top that picks the best discount. [[slnc '
            '500]] Honestly, for three offers, this is fine. [[slnc 500]] '
            'But think about what happens when marketing wants a new '
            'offer live by Friday. [[slnc 300]] It becomes a code change, '
            'a review, a merge, and a release. [[slnc 300]] And the '
            'person writing the code is not the person who understands '
            'the offer. [[slnc 500]] Both bugs came from that gap. [[slnc '
            '300]] Every offer must be translated into Java by hand. '
            '[[slnc 300]] And nothing ever checks the translation.'
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "1.  Every rule change is a code change.",
            "    A release, to say '£75 instead of £50'.",
            "",
            "2.  The people who own the offers cannot read them.",
            "    So the check that would catch a misread ticket",
            "    cannot happen at all.",
            "",
            "3.  Nothing can say WHY.",
            "    'Why did I get 15% off?'  —  'Read the source.'",
            "",
            "4.  There is no place for a typo to be caught.",
            "    A mistyped condition is valid Java. It compiles,",
            "    deploys, and misprices an order on Friday.",
            "",
            "5.  It grows the wrong way. The tenth promotion is",
            "    riskier to add than the first.",
        ],
        narration=(
            'So what exactly is wrong? [[slnc 300]] Five separate things. '
            '[[slnc 500]] One. [[slnc 200]] Every rule change is a code '
            'change. [[slnc 300]] Seventy-five pounds instead of fifty '
            'means a whole release. [[slnc 500]] Two. [[slnc 200]] The '
            'people who own the offers cannot read the rules. [[slnc '
            '300]] So nobody can check that the code matches the request. '
            '[[slnc 500]] Three. [[slnc 200]] Nothing can explain itself. '
            '[[slnc 300]] When a customer asks why they got fifteen '
            'percent off, the only answer is, read the source code. '
            '[[slnc 500]] Four. [[slnc 200]] There is no place to catch a '
            'typo. [[slnc 300]] A mistyped condition is still valid Java. '
            '[[slnc 300]] It compiles, deploys, and quietly does the '
            'wrong thing at checkout. [[slnc 500]] And five. [[slnc 200]] '
            'It gets worse over time. [[slnc 300]] Each new promotion is '
            'another chance to copy the wrong condition.'
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Interpreter Pattern",
        # One line per rendered line: kind_quote lays these out as-is.
        body=[
            "Given a language, define a representation for its",
            "grammar along with an interpreter that uses the",
            "representation to interpret sentences in the language.",
            "",
            "— Gang of Four",
            "",
            "Strip the vocabulary and it says:",
            "one small class per kind of phrase,",
            "and a big phrase holds small ones.",
        ],
        narration=(
            "Here is the pattern's definition, from the famous Gang of "
            'Four book. [[slnc 400]] Given a language, define a '
            'representation for its grammar, along with an interpreter '
            'that uses it to interpret sentences in the language. [[slnc '
            '600]] That sounds hard, but it is not. [[slnc 300]] In plain '
            'words: write one small class for each kind of phrase. [[slnc '
            '300]] And let big phrases hold small ones. [[slnc 500]] In '
            'this project, the language is promotion rules. [[slnc 300]] '
            'A sentence is something like: country is UK, and basket over '
            'fifty. [[slnc 300]] And interpreting it means asking a tree '
            'of rule objects whether an order matches.'
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="An Analogy",
        body=[
            "Think of how a sentence is put together.",
            "",
            "  'the man'",
            "  'the tall man in the blue coat'",
            "",
            "Both are noun phrases. One is more elaborate.",
            "Either drops into '... bought a laptop' unchanged.",
            "",
            "A rule tree is the same idea:",
            "",
            "  'basket over 50'",
            "  'country is UK and basket over 50 or first order'",
            "",
            "Both are a Rule. Both fit wherever a Rule fits.",
            "The grammar composes, so the objects compose.",
        ],
        narration=(
            'Here is an analogy from everyday English. [[slnc 500]] The '
            'phrase, the man, is a noun phrase. [[slnc 300]] The phrase, '
            'the tall man in the blue coat, is also a noun phrase. [[slnc '
            '300]] One is longer, but both fit in the same place in a '
            'sentence. [[slnc 300]] Either can be followed by, bought a '
            'laptop. [[slnc 600]] Rules work exactly the same way. [[slnc '
            '300]] Basket over fifty is a rule. [[slnc 300]] Country is '
            'UK, and basket over fifty, or first order, is also a rule. '
            '[[slnc 300]] Both fit anywhere a rule fits. [[slnc 500]] The '
            'grammar combines, so the objects combine.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            'So here are the pieces. [[slnc 500]] At the top is Rule, the '
            'shared interface. [[slnc 300]] It has two methods: matches, '
            'and describe. [[slnc 300]] Every rule class in the project '
            'is a Rule. [[slnc 500]] Below it are just two kinds of '
            'class. [[slnc 400]] The first kind are simple rules, called '
            'terminal expressions. [[slnc 300]] Basket over, country is, '
            'items at least, and first order. [[slnc 300]] Each makes one '
            'comparison, and holds no other rule. [[slnc 500]] The second '
            'kind combine other rules, called non-terminal expressions. '
            '[[slnc 300]] And, or, and not. [[slnc 300]] They hold other '
            'rules, and answer by asking them. [[slnc 500]] And one more '
            'piece: the order itself. [[slnc 300]] That is what a rule is '
            'checked against. [[slnc 300]] Only the simple rules ever '
            'look at it.'
        ),
    ),
    dict(
        key="09-two-kinds",
        kind="code",
        title="Two Kinds of Class, and That Is All",
        body="""public interface Rule {                    // abstract expression
    boolean matches(Order order);
    String describe();
}

public record BasketOver(int pounds) implements Rule {      // TERMINAL
    public boolean matches(Order o) { return o.basketPounds() > pounds; }
    public String describe()        { return "basket over " + pounds; }
}

public record AndRule(List<Rule> parts) implements Rule {   // NON-TERMINAL
    public boolean matches(Order order) {
        for (Rule part : parts)
            if (!part.matches(order)) { return false; }
        return true;
    }
}""",
        narration=(
            'Here is the whole pattern in code. [[slnc 500]] The Rule '
            'interface has two methods, and no fields. [[slnc 500]] '
            'Basket over is a simple rule. [[slnc 300]] It compares the '
            'basket total with a number, and describes itself as, basket '
            'over, and the number. [[slnc 300]] That is the whole class. '
            '[[slnc 500]] The And rule holds two other rules. [[slnc '
            '300]] It matches only when both parts match. [[slnc 600]] '
            'Notice what the And rule does not know. [[slnc 300]] It does '
            'not know what its parts are. [[slnc 300]] Simple rules, or '
            'more And rules? [[slnc 300]] How deep does the tree go? '
            '[[slnc 300]] It never finds out, because it only ever asks. '
            '[[slnc 500]] That is the whole trick. [[slnc 300]] A rule of '
            'any size and shape is used exactly like the simplest rule.'
        ),
    ),
    dict(
        key="10-explaining",
        kind="code",
        title="The Tree Can Explain Itself — and Refuse a Typo",
        body="""public String explain() {                      // on Promotion
    return code + " (" + percentOff + "% off) applies when "
            + rule.describe();
}

// SAVE15 (15% off) applies when country is UK and basket over 100
//   ^ rebuilt from the objects the checkout obeys.
//     NOT remembered from the line that was read in.

private Rule parseCondition(String text) {     // on RuleParser
    ...
    throw new IllegalArgumentException(
            "I do not understand \\"" + text + "\\"");
}""",
        narration=(
            'This buys two things that are easy to undervalue. [[slnc '
            '500]] The first is describe. [[slnc 300]] Each rule '
            'describes its own part, and asks its parts to describe '
            'theirs. [[slnc 300]] So the whole sentence can be rebuilt '
            'from the tree. [[slnc 400]] And that sentence comes from the '
            'very objects the checkout obeys. [[slnc 300]] Not from a '
            'copy of the text. [[slnc 400]] So when a customer asks why '
            'they got fifteen percent off, the code can answer in the '
            'words the offer was written in. [[slnc 300]] A test checks '
            'that reading a rule and describing it gives back the same '
            'line. [[slnc 600]] The second thing is refusing typos. '
            '[[slnc 300]] A rule language that guesses is worse than '
            'none. [[slnc 300]] So any phrase the reader cannot '
            'understand is refused, and the phrase is named. [[slnc 300]] '
            'The typo is caught when the promotion is saved, on a quiet '
            'Wednesday. [[slnc 300]] Not at a busy checkout on Friday.'
        ),
    ),
    dict(
        key="11-proof",
        kind="code",
        title="The Tests — Asserting the Grammar, Not Just the Answer",
        body="""@Test void andBindsTighterThanOr() {
    Rule rule = RuleParser.parse("country is UK and basket over 100 "
                                 + "or items at least 10");
    assertTrue(rule instanceof OrRule);        // (A and B) or C
}

@Test void parsingAndDescribingRoundTrip() {
    String line = "country is UK and basket over 50 or first order";
    assertEquals(line, RuleParser.parse(line).describe());
}

@Test void save15GivesFifteenPercentToAnOverseasOrder() {   // NAIVE
    assertEquals(15, naive.bestPercentFor(
            new Order(120, "US", 2, false)));  // the wrong answer,
}                                              // pinned on purpose""",
        narration=(
            'The project has twenty-one tests. [[slnc 300]] Three are '
            'worth describing. [[slnc 500]] The first checks precedence, '
            'which means which word binds tighter. [[slnc 300]] A and B '
            'or C must mean: A and B together, or else C. [[slnc 300]] '
            'That is how a person would say it. [[slnc 300]] Swap two '
            'lines in the rule reader, and this test fails. [[slnc 500]] '
            'The second is the round trip. [[slnc 300]] Read a line, '
            'describe the tree, and you must get the same line back. '
            '[[slnc 300]] That keeps the explanation and the decision in '
            'step. [[slnc 500]] The third test checks a wrong answer, on '
            'purpose. [[slnc 300]] It confirms that the naive version '
            'gives fifteen percent to an American order. [[slnc 300]] '
            "Being broken is that version's whole job in this project, "
            'and the build says so out loud.'
        ),
    ),
    dict(
        key="12-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

=== rules written as Java branches ===
  £120, UK, 4 items, returning     discount: 15%
  £120, US, 2 items, returning     discount: 15%   <- overseas
  £30,  UK, 3 items, returning     discount:  0%   <- qualifies

=== the same rules, read as a language ===
  £120, UK, 4 items    15%   because SAVE15 applies when
                             country is UK and basket over 100
  £120, US, 2 items     0%
  £30,  UK, 3 items     5%   because FREESHIP applies when
                             country is UK and items at least 3

=== marketing wants one more, and it is Friday ===
  added: BIGBASKET | 20 | basket over 200 or items at least 10
  £90, UK, 12 items    20%       One line of text.

=== and a rule with a typo in it ===
  refused: I do not understand "basket ovr 50\"""",
        narration=(
            "Let's run the demo. [[slnc 400]] Three orders, checked both "
            'ways. [[slnc 500]] The Java version gives fifteen percent to '
            'an American order. [[slnc 300]] And nothing at all to a UK '
            'customer who qualifies. [[slnc 300]] No error for either. '
            '[[slnc 500]] The rule language gets all three right. [[slnc '
            '300]] And every discount comes with a reason, in the words '
            'the offer was written in. [[slnc 600]] Then it is Friday, '
            'and marketing wants one more offer. [[slnc 300]] Basket over '
            'two hundred, or items at least ten. [[slnc 300]] No '
            'promotion in the shop has ever used or before. [[slnc 300]] '
            'Yet adding it is one line of text. [[slnc 300]] No new '
            'class, nothing recompiled, nothing deployed. [[slnc 500]] '
            'And finally, a rule with a typo in it: basket ovr fifty. '
            '[[slnc 300]] It is refused, by name, the moment the '
            'promotion is saved.'
        ),
    ),
    dict(
        key="13-wrapup",
        kind="bullets",
        title="What to Remember",
        body=[
            "A rule written in code can only be run.",
            "A rule written in a language can be run, read, printed,",
            "checked, and changed by the person who owns it.",
            "",
            "  Interpreter  a tree of expressions — evaluating a sentence",
            "  Composite    the SAME tree — treating one and many alike",
            "  Strategy     one interchangeable behaviour",
            "",
            "Interpreter IS a Composite. The difference is intent:",
            "Composite is about structure, Interpreter is about meaning.",
            "",
            "The honest limit: one class per phrase is fine for seven",
            "phrases and unbearable for seventy. A real grammar wants a",
            "parser generator — and that is the sentence people skip.",
            "",
            "And if the rules never change, two if statements win.",
        ],
        narration=(
            'So, what should you remember? [[slnc 400]] A rule written in '
            'code can only be run. [[slnc 300]] A rule written in a '
            'language can be run, read, printed, checked, and changed by '
            'the person who owns it. [[slnc 600]] Now, two patterns '
            'people confuse with this one. [[slnc 300]] Composite is a '
            'tree of parts, where one thing and many things are treated '
            'alike. [[slnc 300]] Interpreter uses exactly that tree. '
            '[[slnc 300]] The difference is purpose. [[slnc 300]] '
            'Composite is about structure. [[slnc 300]] Interpreter is '
            'about meaning. [[slnc 500]] And Strategy. [[slnc 300]] The '
            'checkout holds a rule, and does not care which one. [[slnc '
            '300]] That is Strategy on the outside, with Interpreter on '
            'the inside. [[slnc 600]] Now the honest costs. [[slnc 300]] '
            'One class per phrase is fine for seven phrases, and painful '
            'for seventy. [[slnc 300]] A language with real syntax, like '
            'brackets, needs a proper parser tool, not this pattern. '
            '[[slnc 300]] The Gang of Four say exactly that. [[slnc 500]] '
            'And if the rules never change, two if statements beat a '
            'language. [[slnc 300]] This pattern pays off when releasing '
            'code is the bottleneck.'
        ),
    ),
    dict(
        key="14-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that swaps",
            "two lines in the parser, and quietly changes what every",
            "promotion in the shop means.",
        ],
        narration=(
            "That's the Interpreter pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Write one small '
            'class per kind of phrase, and your rules can be run, read, '
            'checked, and explained. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Swap the two splitting steps in the rule '
            'reader, so that and binds more loosely than or. [[slnc 300]] '
            'Run the tests. [[slnc 300]] Then work out which of the '
            "shop's promotions would quietly change their meaning. [[slnc "
            '500]] If this helped, a like really does help other people '
            "find it. [[slnc 300]] And subscribe, if you'd like the rest "
            'of the series. [[slnc 400]] Thanks for watching.'
        ),
    ),
]
