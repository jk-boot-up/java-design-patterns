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
            "Hello, and welcome. This video explains the Interpreter pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. "
            "[[slnc 300]] Let's start with the simple definition. The "
            "interpreter pattern means writing one small class for each kind of "
            "phrase in a little language, and letting a big phrase hold small "
            "ones. The tree of objects you end up with is the sentence, and "
            "running the sentence is calling one method on the top of that tree. "
            "[[slnc 350]] That's the idea in a sentence. The rest of the video "
            "does it properly, by building a real working Java project: the "
            "promotion rules of an online shop, written as text instead of as "
            "code. [[slnc 250]] By the end you'll know what a terminal and a "
            "non-terminal expression are, why a rule that can describe itself is "
            "worth more than a rule that merely works, and the honest limit of "
            "this pattern — which is the sentence people skip."
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
            "So, imagine an online shop. [[slnc 250]] It runs promotions, and a "
            "promotion is three things: a code, a percentage off, and a rule "
            "about who qualifies. [[slnc 300]] Save ten is ten percent for UK "
            "orders over fifty pounds. Save fifteen is fifteen percent over a "
            "hundred. Free ship is five percent for UK orders of three items or "
            "more. [[slnc 300]] Written in Java, the first one is four lines, "
            "and I want to be clear about this: there is nothing wrong with it. "
            "It's the right amount of code for the job. [[slnc 350]] The trouble "
            "is not the first promotion. The trouble is the fourth — because by "
            "then, each new offer is written by copying the one above it and "
            "changing the numbers, which is the fastest correct-looking thing "
            "anybody can do."
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
            "Here are the two copies that went wrong, and they went wrong in "
            "opposite directions. [[slnc 300]] Save fifteen gives money away. "
            "The ticket said fifteen percent on baskets over a hundred pounds. "
            "That the offer was UK only was in the paragraph above the sentence "
            "somebody actually read, so no line of code was ever written for it. "
            "[[slnc 300]] Every large overseas order now takes fifteen percent "
            "off. On a hundred and twenty pound order that's eighteen pounds, on "
            "every order, for as long as nobody adds it up. [[slnc 350]] Free "
            "ship withholds it. That branch was copied from a welcome offer that "
            "retired last spring, and the first-order check came along with it. "
            "So a returning UK shopper with three items is offered nothing. "
            "[[slnc 300]] And nobody reports that one. A missing discount looks "
            "exactly like a shopper who didn't qualify. [[slnc 300]] Neither bug "
            "throws. Neither is logged. Both are correct-looking Java that "
            "compiled, passed review, and shipped."
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
            "Here's the shape of it. [[slnc 250]] One method per promotion, one "
            "branch inside each, and a method at the top taking the best of "
            "them. [[slnc 300]] And honestly? For three offers this is fine. I "
            "wouldn't reject this in a review. [[slnc 350]] But look at what "
            "happens when marketing wants an offer live on Friday. That is now a "
            "branch, a pull request, a review, a merge and a release — and the "
            "person who writes the branch is not the person who understands the "
            "offer. [[slnc 300]] The gap between those two people is where both "
            "of the bugs we just saw came from. It isn't a skill problem. It's "
            "that the campaign brief has to be translated into Java by hand, "
            "every single time, and nothing anywhere checks the translation."
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
            "Let's be precise, because it's five separate costs. [[slnc 300]] "
            "One. Every rule change is a code change. Marketing wants seventy "
            "five pounds instead of fifty, and that's a release. [[slnc 300]] "
            "Two. The people who own the offers can't read the rules. Nobody "
            "outside the team can check that the code says what the campaign "
            "brief said, which means the one check that would have caught a "
            "misread ticket can't happen at all. [[slnc 300]] Three. Nothing can "
            "say why. When a shopper asks why they got fifteen percent off, the "
            "only answer available is, read the source. A number came out of a "
            "method, and the reasoning stayed behind in the shape of the Java it "
            "was made of. [[slnc 300]] Four. There's no place for a typo to be "
            "caught. A mistyped condition is valid Java. It compiles, it "
            "deploys, and it behaves — wrongly — at checkout. There is no "
            "earlier moment at which anything could have objected. [[slnc 350]] "
            "And five. It grows the wrong way. Every new promotion is a new "
            "branch in one growing method, and each one is a fresh chance to "
            "copy the wrong condition. The tenth promotion is riskier to add "
            "than the first, which is precisely backwards."
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
            "Here's the definition from the Gang of Four book. [[slnc 250]] "
            "Given a language, define a representation for its grammar, along "
            "with an interpreter that uses the representation to interpret "
            "sentences in the language. [[slnc 350]] That sentence puts people "
            "off, and it's the main reason this pattern has a reputation for "
            "being the hard one. It shouldn't. [[slnc 300]] Strip the vocabulary "
            "and it says: write one small class per kind of phrase, and let a "
            "big phrase hold small ones. That's it. The tree of objects you end "
            "up with is the sentence, and running the sentence is calling one "
            "method on the top of the tree. [[slnc 300]] In this project the "
            "language is promotion rules, a sentence is, country is UK and "
            "basket over fifty, and interpreting one is asking a tree of rule "
            "objects whether an order matches."
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
            "Here's the analogy to hold on to. [[slnc 250]] Think about how a "
            "sentence is put together. The man is a noun phrase. The tall man in "
            "the blue coat is also a noun phrase. One is more elaborate than the "
            "other, but both fit in the same slot — you can drop either of them "
            "into, dot dot dot bought a laptop, without rewriting the sentence "
            "around it. [[slnc 350]] A rule tree is exactly that idea. Basket "
            "over fifty is a rule. Country is UK and basket over fifty or first "
            "order is also a rule. Both fit wherever a rule fits. [[slnc 300]] "
            "The grammar composes, so the objects compose. And once you've seen "
            "that, the pattern stops being clever and starts being obvious — "
            "which is the point I'd most like to land."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So here are the pieces. [[slnc 250]] At the top there's rule: the "
            "abstract expression. Two methods, matches and describe, and every "
            "single rule class in the project is one of these. [[slnc 300]] "
            "Underneath it, two kinds of class, and only two. On the left, the "
            "terminal expressions — basket over, country is, items at least, "
            "first order. Each one is a leaf. One comparison, and no other rule "
            "inside it. [[slnc 300]] On the right, the non-terminal expressions "
            "— and, or, not. These hold other rules and answer by asking them. "
            "[[slnc 300]] Now look at the arrow that goes from and-rule back up "
            "into rule. That one loop in the picture is the whole recursion. "
            "Because it holds a rule and not a leaf, it can hold another "
            "and-rule, or an or-rule, or anything else — and it never finds out "
            "which. [[slnc 300]] And off to the side, order: the context. That's "
            "what a sentence gets interpreted against, and notice that only the "
            "leaves ever touch it."
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
            "And here is the entire pattern on one slide. [[slnc 300]] Rule at "
            "the top: two methods, no fields. Everything implements that. "
            "[[slnc 300]] Basket over is a terminal — a leaf. One comparison, "
            "one string, and that is the whole class. It doesn't need to be "
            "bigger. [[slnc 300]] And-rule is a non-terminal. It holds other "
            "rules and answers by asking them. [[slnc 350]] Now read and-rule "
            "again, and notice what is not in it. It does not know what its "
            "parts are. It does not know whether they're leaves or more "
            "and-rules. It does not know how many levels are below it, and it "
            "never finds out, because it only ever asks. [[slnc 300]] That is "
            "the whole trick. It's why a rule of any shape and any depth is used "
            "exactly like a rule with one comparison in it — and why you can put "
            "a whole nested tree into either of those slots without changing a "
            "line of this."
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
            "Two things this buys you that are easy to undersell. [[slnc 300]] "
            "The first is describe. Each node says its own piece and asks its "
            "parts for theirs, so the sentence comes back out of the tree. "
            "[[slnc 300]] And here's the bit that matters: that string is "
            "rebuilt from the objects the checkout actually obeys. It is not "
            "remembered from the line that was read in. If the two ever "
            "disagreed, this is the one telling the truth. [[slnc 300]] So, why "
            "did this order get fifteen percent off, becomes a question the code "
            "can answer, in the words the offer was written in — for the audit "
            "log and for the shopper alike. There's a round-trip test asserting "
            "that parsing a rule and describing it gives the line back "
            "unchanged, so that guarantee is checked rather than hoped for. "
            "[[slnc 350]] The second is that a rule language which guesses is "
            "worse than no rule language at all. Every phrase the parser can't "
            "read is refused, naming the phrase. [[slnc 300]] Which means the "
            "typo is caught while the promotion is being saved, on a Wednesday, "
            "when it is cheap. Not at a checkout on Friday."
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
            "Twenty one tests, and these three are the ones worth showing. "
            "[[slnc 300]] The first pins the precedence. The parser splits on "
            "or first and and second, which is what gives and the tighter grip, "
            "so A and B or C reads as, bracket A and B, or C — the way a person "
            "says it. Swap those two lines round and this test goes red. [[slnc "
            "350]] The second is the round trip, and it's my favourite test in "
            "the project. Parse a line, describe the tree, and you must get the "
            "same line back. [[slnc 300]] That's what stops the audit log and "
            "the code drifting apart. Change how or-rule joins its parts and the "
            "rule still evaluates perfectly correctly — and this test still "
            "fails, because the explanation and the decision are no longer the "
            "same sentence. [[slnc 350]] And the third asserts a wrong answer, "
            "deliberately. It pins the naive version handing fifteen percent to "
            "an American order, with a message explaining why. [[slnc 300]] Fix "
            "the naive version and its own tests go red. That's intentional. "
            "Being broken is its entire job, and the cost of that design should "
            "be something the build says out loud rather than something a README "
            "claims."
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
            "Run it, and the halves sit side by side. [[slnc 250]] Same three "
            "orders, both ways. [[slnc 300]] The Java branches give fifteen "
            "percent to an American order, and nothing at all to a UK shopper "
            "who qualifies. No exception was thrown for either. [[slnc 300]] The "
            "language version gets all three right, and every discount comes "
            "with a because line, in the words the offer was written in. [[slnc "
            "350]] Then the part I'd frame. It's Friday, and marketing wants one "
            "more offer: basket over two hundred, or items at least ten. [[slnc "
            "300]] Now that shape appears nowhere in this codebase. There is no "
            "promotion anywhere in the shop that uses an or. And adding it is "
            "one line of text — no new class, nothing recompiled, nothing "
            "deployed. [[slnc 300]] And last, a rule with a typo in it. Basket "
            "ovr fifty. It's refused, by name, at the moment the promotion is "
            "saved."
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
            "So, what to take away. [[slnc 300]] A rule written in code can only "
            "be run. A rule written in a language can be run, read, printed, "
            "checked, and changed by the person who owns it. [[slnc 350]] On the "
            "comparisons, because these get confused constantly. Interpreter is "
            "a tree of expressions for evaluating a sentence. Composite is a "
            "tree of parts for treating one thing and many things alike. [[slnc "
            "300]] And here's the honest answer: interpreter is a composite. The "
            "tree, the uniform interface, the leaves and containers looking "
            "alike — that's all composite's. The difference is intent. Composite "
            "is about structure; interpreter is about meaning. [[slnc 300]] "
            "Strategy is the third one people reach for, and a whole rule tree "
            "is often used as a strategy: the checkout holds a rule and doesn't "
            "care which one. That's strategy's shape wrapped around "
            "interpreter's insides. [[slnc 350]] Now the honest bill, and this "
            "one is important. One class per phrase is fine for seven phrases "
            "and unbearable for seventy. A grammar with real syntax wants a "
            "parser generator, not this pattern. The Gang of Four say exactly "
            "that, and it is the most commonly ignored sentence in the chapter. "
            "[[slnc 300]] Adding a terminal stays cheap forever. Adding brackets "
            "is a real parser, and that's a much bigger day's work than it "
            "looks. [[slnc 300]] And don't reach for this when the rules never "
            "change. If the shop has run the same two promotions for four years, "
            "two if statements are better code than a language is. This pattern "
            "earns its keep when shipping code is the bottleneck."
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
            "That's the interpreter pattern. [[slnc 250]] The full source, the "
            "written notes, the diagrams and an animated walkthrough are all in "
            "the repository — including the exercise I'd most recommend. Swap "
            "the two splits in the parser so that and binds looser than or, run "
            "the tests, and then work out which of the shop's promotions would "
            "have quietly changed meaning. [[slnc 300]] It takes a minute, and "
            "it's the moment precedence stops being a word from a compilers "
            "course and becomes money. [[slnc 300]] If this helped, a like "
            "genuinely does help other people find it, and subscribe if you'd "
            "like the rest of the behavioural series. [[slnc 250]] Thanks for "
            "watching, and I'll see you in the next one."
        ),
    ),
]
