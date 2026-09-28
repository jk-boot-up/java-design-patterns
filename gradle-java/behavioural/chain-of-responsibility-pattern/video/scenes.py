"""Scene definitions for the Chain of Responsibility teaching video.

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
        title="Chain of Responsibility",
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Chain of Responsibility pattern, in Java. [[slnc 300]] This '
            'video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] You hand a request '
            'to a line of objects, one after another. [[slnc 300]] Each '
            'object either answers, and the request stops there. [[slnc '
            '300]] Or it stays quiet, and passes the request to the next '
            'one. [[slnc 600]] Think of calling a support line. [[slnc '
            '300]] The first person tries to help. [[slnc 300]] If they '
            "can't, they pass you on to someone more senior. [[slnc 300]] "
            'You make one call, and you never need to know who will '
            'finally answer. [[slnc 700]] In our online store, every '
            'order is checked before it is accepted. [[slnc 300]] Is the '
            'address one we deliver to? [[slnc 200]] Is the stock '
            'available? [[slnc 200]] Is the order risky? [[slnc 200]] And '
            'will the card cover the total? [[slnc 500]] By the end, you '
            'will know why the order of those checks should be easy to '
            'change. [[slnc 300]] And how this pattern differs from the '
            'Decorator pattern, which looks exactly the same on paper.'
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "Before an order is accepted, it is checked:",
            "",
            "  address        is this somewhere a courier goes?",
            "  stock          can the warehouse pick every line?",
            "  fraud-score    what does the risk model think?",
            "  payment-limit  does the card cover the total?",
            "",
            "Any check can reject the order.",
            "Otherwise it moves on to the next one.",
            "",
            "Which checks run, and in what order, needs to change.",
        ],
        narration=(
            'Here is the scenario. [[slnc 400]] Before an online shop '
            'accepts an order, it checks it in four ways. [[slnc 400]] '
            'One. [[slnc 200]] Is the address somewhere a courier '
            'actually delivers? [[slnc 300]] Two. [[slnc 200]] Can the '
            'warehouse supply every item in the basket? [[slnc 300]] '
            'Three. [[slnc 200]] What does the fraud model think of this '
            'customer? [[slnc 300]] Four. [[slnc 200]] Does the card '
            'cover the total? [[slnc 500]] Any one of those checks can '
            'reject the order. [[slnc 300]] If none objects, the order is '
            'accepted. [[slnc 500]] And here is the important part. '
            '[[slnc 300]] Which checks run, and in what order, must be '
            'easy to change. [[slnc 300]] For example, trade customers '
            'are invoiced at the end of the month. [[slnc 300]] So they '
            'skip the card check.'
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Look Closely at One Order",
        body=[
            "R2001:  a £329 monitor",
            "        on a card with a £250 limit",
            "        from an account the risk model scores 92 out of 100",
            "",
            "Two checks would reject this. Only one of them speaks.",
            "",
            "Which one? Whichever is written first.",
            "",
            "Nobody decided that. It is just where the line was typed.",
        ],
        narration=(
            "Before any code, let's look closely at one order. [[slnc "
            '400]] Someone buys a monitor for three hundred and '
            'twenty-nine pounds. [[slnc 300]] Their card has a limit of '
            'two hundred and fifty pounds. [[slnc 300]] And the fraud '
            'model scores the account ninety-two out of a hundred, which '
            'is very risky. [[slnc 500]] Two of our four checks would '
            'reject this order. [[slnc 300]] But only one gets to speak, '
            'because the first rejection ends the checking. [[slnc 400]] '
            'So which one speaks? [[slnc 300]] Whichever is written '
            'first. [[slnc 500]] Nobody decided that on purpose. [[slnc '
            '300]] Yet it matters a lot. [[slnc 300]] It is the '
            'difference between telling the customer to try another card, '
            'and alerting the fraud team.'
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — Four Checks, One Method",
        body="""public Result validate(CheckoutRequest request) {
    if (!deliverable(request))      return no("we do not deliver there");
    if (outOfStock(request))        return no("... is out of stock");
    if (overCardLimit(request))     return no("card limit exceeded");
    if (request.fraudScore() >= 80) return no("unable to process");
    return new Result(true, "nothing objected");
}

// Trade accounts are invoiced, so somebody copied it and
// deleted the card check. The address check went too.
public Result validateTradeAccount(CheckoutRequest request) {
    if (outOfStock(request))        return no("... is out of stock");
    if (request.fraudScore() >= 80) return no("unable to process");
    return new Result(true, "nothing objected");
}""",
        narration=(
            'The obvious first approach is one method, with four checks, '
            'one after another. [[slnc 300]] Each check can return early '
            'with a rejection. [[slnc 500]] To be fair, this has real '
            'strengths. [[slnc 300]] It is short, and the whole policy is '
            'in one file. [[slnc 300]] For a shop with simple rules that '
            'never change, it is the right answer. [[slnc 600]] But in '
            'this method, the card check comes before the fraud check. '
            '[[slnc 300]] So our risky order is rejected as a card '
            'problem. [[slnc 300]] The customer tries another card, and '
            'it works. [[slnc 300]] There was never anything wrong with '
            'the cards. [[slnc 600]] Then there is a second method, for '
            'trade customers. [[slnc 300]] Someone copied the first '
            'method, and deleted the card check. [[slnc 300]] But in the '
            'same edit, the address check was deleted too. [[slnc 300]] '
            'So an order of two desks is now on its way to an island that '
            'no courier serves.'
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "1.  The ORDER is welded in.",
            "    Changing it means editing the file the rules live in.",
            "",
            "2.  A boolean has NO THIRD ANSWER.",
            "    Score 64 is the band risk asked us to review.",
            "    It gets accepted, because there is nowhere else to put it.",
            "",
            "3.  Variants are COPIES, and copies drift.",
            "",
            "4.  Testing the fraud rule means satisfying three checks",
            "    that have nothing to do with fraud.",
        ],
        narration=(
            'So what exactly is wrong? [[slnc 300]] Four separate things. '
            '[[slnc 500]] One. [[slnc 200]] The order of the checks is '
            'fixed inside the method. [[slnc 300]] Changing it means '
            'editing the file where the rules live. [[slnc 500]] Two. '
            '[[slnc 200]] Each check can only say yes or no. [[slnc 300]] '
            'But a fraud model gives a score, and the useful part is the '
            'middle band. [[slnc 300]] Those are the orders a person '
            'should review. [[slnc 300]] An order scoring sixty-four is '
            'simply accepted, because there is no third answer. [[slnc '
            '500]] Three. [[slnc 200]] Variations are copies, and copies '
            'drift apart. [[slnc 300]] We just heard that happen. [[slnc '
            '500]] And four. [[slnc 200]] To test the fraud rule, a test '
            'must first build an address, a basket and a card, that the '
            'fraud rule does not even care about.'
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Chain of Responsibility Pattern",
        # One line per rendered line: kind_quote lays these out as-is.
        body=[
            "Avoid coupling the sender of a request to its receiver",
            "by giving more than one object a chance to handle the",
            "request. Chain the receiving objects and pass the",
            "request along the chain until an object handles it.",
            "",
            "— Gang of Four",
            "",
            "In plain terms:",
            "the caller does not know which object will answer,",
            "and it never needs to find out.",
        ],
        narration=(
            "Here is the pattern's definition, from the famous Gang of "
            'Four book. [[slnc 400]] Avoid coupling the sender of a '
            'request to its receiver, by giving more than one object a '
            'chance to handle the request. [[slnc 500]] The key idea is '
            'not just running several checks in a row. [[slnc 300]] A '
            'simple loop can do that. [[slnc 300]] The key idea is that '
            'the caller does not know which check will answer. [[slnc '
            '500]] So here is the move. [[slnc 300]] Instead of one '
            'method that knows all four checks, write four objects. '
            '[[slnc 300]] Each one knows one check, and nothing about the '
            'others.'
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="An Analogy",
        body=[
            "An expenses claim.",
            "",
            "  a £40 lunch        your team lead approves it",
            "  £4,000 of laptops  goes up to their director",
            "  £400,000           goes to the board",
            "",
            "You submit once. You do not address it to whoever",
            "is allowed to approve that amount.",
            "",
            "The board never sees your lunch receipt —",
            "not because they'd object, but because nobody asked them.",
            "",
            "And a claim nobody can approve sits in a queue forever.",
        ],
        narration=(
            'Here is an analogy to hold on to: an expenses claim at work. '
            '[[slnc 500]] A forty pound lunch? [[slnc 200]] Your team '
            'lead approves it. [[slnc 300]] Four thousand pounds of '
            'laptops? [[slnc 200]] Your team lead cannot, so it goes up '
            'to their director. [[slnc 300]] Four hundred thousand '
            'pounds? [[slnc 200]] That goes to the board. [[slnc 500]] '
            'Three things about that office are the pattern. [[slnc 300]] '
            'You submit once, without knowing who can approve what. '
            '[[slnc 300]] Whoever can answer, answers, and it stops '
            'there. [[slnc 300]] The board never sees your lunch receipt. '
            '[[slnc 300]] And the chain of managers is not written on the '
            "claim form. [[slnc 500]] The pattern's risk is there too. "
            '[[slnc 300]] A claim that nobody is allowed to approve can '
            'sit in a queue forever.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            'So here are the pieces, and there are only a few. [[slnc '
            '500]] The client is the checkout. [[slnc 300]] It holds one '
            'screening chain, calls it once, and gets back a report. '
            '[[slnc 500]] The screening chain links the checks together. '
            '[[slnc 300]] It hands the order to the first check, and then '
            'waits until someone answers. [[slnc 500]] The screening '
            'handler is the shared base class for every check. [[slnc '
            '300]] It holds a link to the next check, and one method for '
            'each check to fill in. [[slnc 300]] Below it sit the four '
            'real checks. [[slnc 500]] And what comes back is a report. '
            '[[slnc 300]] It says the decision, which check made it, and '
            'which checks never ran.'
        ),
    ),
    dict(
        key="09-interface",
        kind="code",
        title="The Handler — And the Line That Is Written Once",
        body="""public abstract class ScreeningHandler {

    private ScreeningHandler next;

    public abstract String name();

    /** empty  = no opinion, pass it on
        present = I am answering, and the chain stops here */
    protected abstract Optional<Decision> check(CheckoutRequest request);

    final Optional<Decision> screen(CheckoutRequest request, List<String> consulted) {
        consulted.add(name());
        Optional<Decision> mine = check(request);
        if (mine.isPresent()) {
            return mine;
        }
        return next == null ? Optional.empty() : next.screen(request, consulted);
    }
}""",
        narration=(
            'The whole pattern fits in about twenty lines, in the base '
            'class. [[slnc 400]] It has one field, a link to the next '
            'check. [[slnc 300]] One method that each check writes, '
            'called check. [[slnc 300]] And one method that walks along '
            'the chain, called screen. [[slnc 600]] Listen to what check '
            'returns. [[slnc 300]] It returns an optional decision. '
            '[[slnc 300]] Empty means: I have no opinion, pass it on. '
            '[[slnc 300]] A decision means: I am answering, and the chain '
            'stops here. [[slnc 300]] Returning nothing does not mean no. '
            '[[slnc 300]] It means, not my call. [[slnc 600]] The screen '
            'method is marked final, so no check can change it. [[slnc '
            '300]] In textbook versions, every check writes its own '
            'pass-along code. [[slnc 300]] And a common bug is a check '
            'that forgets to pass the request on, so it silently '
            'vanishes. [[slnc 300]] Here, that logic is written exactly '
            'once, and no check ever touches the next link.'
        ),
    ),
    dict(
        key="10-context",
        kind="code",
        title="The Chain — And What Silence Means",
        body="""public ScreeningReport screen(CheckoutRequest request) {
    List<String> consulted = new ArrayList<>();
    Decision decision = first.screen(request, consulted).orElse(fallback);

    List<String> neverRan = new ArrayList<>(linkNames);
    neverRan.removeAll(consulted);
    return new ScreeningReport(name, decision, consulted, neverRan);
}

// The fallback is a constructor argument, and there is no
// constructor without one.
new ScreeningChain("standard", Decision.approved(...), links...);
new ScreeningChain("standard", Decision.referred(...), links...);""",
        narration=(
            'Now the chain itself, and two things are worth noticing. '
            '[[slnc 500]] First, what is missing. [[slnc 300]] There is '
            'no loop over the checks, and no counting. [[slnc 300]] The '
            'chain hands the order to the first check, and waits for an '
            'answer. [[slnc 300]] That is why reordering the checks is '
            'only a wiring change. [[slnc 600]] Second, the fallback. '
            '[[slnc 300]] An order really can pass every check, with '
            'nobody deciding anything. [[slnc 300]] Like the expenses '
            'claim nobody can approve. [[slnc 400]] So the chain must be '
            'given a fallback decision when it is built. [[slnc 300]] '
            'There is no way to build one without it. [[slnc 400]] '
            'Approve by default, and the chain fails open. [[slnc 300]] '
            'Refer to a person by default, and it fails closed. [[slnc '
            '300]] The same checks, with opposite attitudes to risk, '
            'decided by one setting.'
        ),
    ),
    dict(
        key="11-links",
        kind="code",
        title="Two Links — And the One With Three Answers",
        body="""// AddressCheck — the ordinary case: it rejects, and it names itself
if (!SERVED_COUNTRIES.contains(request.country())) {
    return Optional.of(Decision.rejected(name(),
            "we do not deliver to " + request.country()));
}
return Optional.empty();

// FraudScoreCheck — the only link with three answers
if (score >= REJECT_AT) return Optional.of(Decision.rejected(name(), ...));
if (score >= REFER_AT)  return Optional.of(Decision.referred(name(), ...));
return Optional.empty();""",
        narration=(
            "Let's look at two of the checks, which work differently on "
            'purpose. [[slnc 500]] The address check is the ordinary '
            'kind. [[slnc 300]] If the country is not one we deliver to, '
            'it rejects the order, and names itself as the one who '
            'decided. [[slnc 300]] If the address is fine, it returns '
            'empty, meaning no opinion. [[slnc 600]] The fraud score '
            'check has three possible answers. [[slnc 300]] A score of '
            'eighty or more, and it rejects. [[slnc 300]] Between '
            'fifty-five and seventy-nine, it refers the order to a '
            'person. [[slnc 300]] Below that, it says nothing. [[slnc '
            '500]] That third answer costs the chain nothing, because the '
            'chain never looks inside a decision. [[slnc 300]] A check '
            'stops the chain whenever it is willing to own the answer. '
            '[[slnc 300]] And that answer does not have to be no.'
        ),
    ),
    dict(
        key="12-proof",
        kind="code",
        title="The Tests — Asserting What Did NOT Happen",
        body="""@Test void linksBehindTheDecisionNeverRun() {
    ScreeningReport report = standardChain().screen(monitorOverLimit());

    assertEquals("fraud-score", report.decision().decidedBy());
    assertEquals(List.of("payment-limit"), report.neverRan());
}

@Test void reorderingChangesTheAnswer() {   // payment moved above fraud
    ScreeningReport report = paymentFirstChain().screen(monitorOverLimit());

    assertEquals("payment-limit", report.decision().decidedBy());
    assertEquals(List.of("fraud-score"), report.neverRan());
}""",
        narration=(
            'The project has twenty-one tests. [[slnc 300]] Two of them '
            'show the pattern best. [[slnc 500]] Note that a simple test '
            'like, an order to an island is rejected, passes for the '
            'naive method too. [[slnc 300]] So it proves nothing about '
            'the pattern. [[slnc 600]] The first special test checks that '
            'a check behind the decision never ran. [[slnc 300]] Not that '
            'its answer was ignored, but that it never ran at all. [[slnc '
            '300]] In real life, that means the payment service was never '
            'called, and never charged for. [[slnc 600]] The second test '
            'uses the same four checks, but wires the card check before '
            'the fraud check. [[slnc 300]] And the answer becomes the '
            'card problem again, exactly like the naive method. [[slnc '
            '400]] So the naive behaviour was not a bug in the checks. '
            '[[slnc 300]] It was a setting that nobody could change '
            'without editing code.'
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

=== 1.  The naive method — four checks in one method ===
   -> REJECTED — card limit exceeded, please try another card
   -> ACCEPTED — nothing objected        (two desks, to Jersey)

=== 2.  The same checks, as a chain ===
   -> REJECTED by fraud-score   score 92 is at or above 80
      never ran: payment-limit

   -> REJECTED by address       no courier covers JE3 8QX
      never ran: stock, fraud-score, payment-limit

=== 4.  A different policy, by wiring only ===
   trade-account: address -> stock -> fraud-score
   -> REJECTED by address       no courier covers JE2 3AB""",
        narration=(
            "Let's run the demo, and compare the two approaches. [[slnc "
            '500]] First, the naive method. [[slnc 300]] The risky order, '
            'with a fraud score of ninety-two, is rejected as a card '
            'problem. [[slnc 300]] And a trade order is accepted, for '
            'delivery to an island that no courier serves. [[slnc 600]] '
            'Second, the same checks as a chain. [[slnc 300]] For the '
            'monitor order, the fraud check answers, and the report says '
            'the card check never ran. [[slnc 300]] For the island order, '
            'the address check answers, and three checks never ran. '
            '[[slnc 300]] No warehouse lookup, no fraud model call, and '
            'nothing to pay for. [[slnc 600]] That never-ran list is the '
            'real difference between a chain and a validator that '
            'collects every problem. [[slnc 300]] A chain gives one '
            'answer, from one check, and stops. [[slnc 500]] Finally, the '
            'trade customers. [[slnc 300]] They use the standard chain, '
            'with the card check simply left out of the wiring. [[slnc '
            '300]] Nothing was copied, so nothing could go missing. '
            '[[slnc 300]] And the island order is caught.'
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="What to Remember",
        body=[
            "Chain of Responsibility and Decorator have the SAME class diagram.",
            "",
            "  Ask one question: does EVERY layer have to run?",
            "",
            "    yes -> Decorator. A layer that didn't delegate is a bug.",
            "    no  -> a chain. A layer that always delegated is pointless.",
            "",
            "In code the difference is one character deep:",
            "the call to next is inside an if.",
            "",
            "The cost, honestly:",
            "  the policy is no longer readable in one place",
            "  you need a report to see who decided",
            "  an order can reach the end unanswered",
            "",
            "Four checks that never change? Write the four ifs.",
        ],
        narration=(
            'So, what should you remember? [[slnc 500]] First, the '
            'confusion promised at the start. [[slnc 300]] Chain of '
            'Responsibility and Decorator have exactly the same class '
            'structure. [[slnc 300]] So you cannot tell them apart by '
            'their diagram. [[slnc 500]] Instead, ask one question. '
            '[[slnc 300]] Does every layer have to run? [[slnc 500]] If '
            'yes, you want a Decorator. [[slnc 300]] There, a layer that '
            'fails to pass the work on is a bug. [[slnc 400]] If no, '
            'because one layer might settle the matter alone, you want a '
            'chain. [[slnc 500]] In code, the difference is tiny. [[slnc '
            '300]] In a decorator, the call to the next object always '
            'happens. [[slnc 300]] In a chain, that call sits inside an '
            'if. [[slnc 600]] Now, the honest cost. [[slnc 300]] A policy '
            'that once read top to bottom in one method is now spread '
            'over four check classes, a base class, and some wiring. '
            '[[slnc 300]] You need a report to see who decided. [[slnc '
            '300]] And an order can reach the end with nobody answering. '
            '[[slnc 500]] So if the checks and their order never change, '
            'just write the four ifs. [[slnc 300]] Use a chain when you '
            'need to change the order, without editing any check.'
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that moves",
            "one link and watches the customer get a different answer.",
        ],
        narration=(
            "That's the Chain of Responsibility pattern. [[slnc 400]] If "
            'you remember one sentence, make it this one. [[slnc 300]] A '
            'chain passes a request along until one object is willing to '
            'answer, so the order of the checks becomes something you can '
            'change. [[slnc 500]] The full source code, written notes, '
            'diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Take the standard chain, and move the card check above '
            'the fraud check. [[slnc 300]] Run the demo, and listen to '
            'how the customer is told something different about the very '
            'same order. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
