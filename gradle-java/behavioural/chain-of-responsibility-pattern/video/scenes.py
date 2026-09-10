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
            "Hello, and welcome. This video explains the Chain of Responsibility "
            "pattern in Java, and it is written and presented by Jayasekhar "
            "Konduru. [[slnc 300]] Let's start with the simple definition. You "
            "hand a request to a line of objects, one after another, until one of "
            "them takes it. Each one either answers, and everything stops there, "
            "or says nothing and passes the request along. [[slnc 350]] That's the "
            "idea in a sentence. The rest of the video does it properly, by "
            "building a real working Java project: the checks an online store runs "
            "before it accepts an order. Is the address deliverable, can the "
            "warehouse pick it, what does the fraud model think, will the card "
            "cover the total. [[slnc 250]] By the end you'll know why the order of "
            "those checks should be something you can change, and what separates a "
            "chain from a decorator — the pattern it is most often mistaken for."
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
            "So, imagine an online shop. [[slnc 250]] Before an order is accepted "
            "we check it four ways. Is the address somewhere a courier actually "
            "goes. Can the warehouse pick every line in the basket. What does the "
            "risk model think of this customer. And does the card cover the total. "
            "[[slnc 300]] Any one of those can reject the order. If none of them "
            "objects, we accept it. [[slnc 300]] And here is the part that "
            "matters. Which checks run, and in what order, is something we need to "
            "change. Trade accounts don't get a card check, because they're "
            "invoiced at the end of the month. That one sentence is the whole "
            "problem."
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
            "Before any code, look closely at one order. [[slnc 300]] A three "
            "hundred and twenty nine pound monitor, on a card with a two hundred "
            "and fifty pound limit, from an account the risk model scores ninety "
            "two out of a hundred. [[slnc 300]] Two of our four checks would "
            "reject this. Only one of them gets the chance, because the first "
            "rejection ends the screening. So which one? [[slnc 250]] Whichever is "
            "written first. [[slnc 350]] Nobody decided that. And the difference "
            "between the two answers is the difference between telling a customer "
            "to try another card, and telling the fraud team an account exists."
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
            "The obvious first move is one method with four checks in it and an "
            "early return on each. [[slnc 250]] I want to be fair to this, "
            "because the whole argument depends on it. It is short, the entire "
            "policy is in one file, and a new joiner can tell you what it does in "
            "thirty seconds. For a shop with one market and rules that never "
            "change, this is the right answer. [[slnc 350]] But look at the third "
            "line and the fourth. The card is checked above fraud. Our order is "
            "rejected as a card problem, the customer tries another card, and it "
            "works — because there was never anything wrong with the cards. "
            "[[slnc 350]] And then the second method. Trade accounts are "
            "invoiced, so somebody copied the first one and deleted the card "
            "check. In the same edit, the address check went too. Two desks are "
            "now on their way to Jersey."
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
            "Let's be precise, because it is four separate things. [[slnc 300]] "
            "One. The order of the checks is welded into the method, so changing "
            "it means editing the file the rules live in. [[slnc 300]] Two. The "
            "answer is a yes or a no, so there is no third answer. A risk model "
            "gives you a score, and the reason anybody pays for one is the band "
            "in the middle — the orders a human should look at. Sixty four gets "
            "accepted, because there is nowhere else to put it. [[slnc 300]] "
            "Three. Variants are copies, and copies drift. We just watched that "
            "happen. [[slnc 300]] And four. The fraud rule is the fourth "
            "statement, so to reach it a test has to build an address, a basket "
            "and a card that the fraud rule does not care about."
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
            "Here is the definition from the Gang of Four book, and the first half "
            "is the half everybody skips. [[slnc 250]] Avoid coupling the sender of "
            "a request to its receiver by giving more than one object a chance to "
            "handle the request. [[slnc 350]] The pattern is not really about "
            "running several checks in a row. You can do that with a loop. It is "
            "about the caller not knowing which of them will answer. [[slnc 300]] "
            "So the move is this. Stop writing one method that knows all four "
            "checks. Write four objects that each know one check, and none of the "
            "others."
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
            "Here's the analogy to hold on to. [[slnc 250]] An expenses claim. A "
            "forty pound lunch receipt, and your team lead approves it. Four "
            "thousand pounds of laptops, and your team lead cannot — that goes up "
            "to their director. Four hundred thousand goes to the board. [[slnc "
            "300]] Three things about that office are the pattern. You submit "
            "once, and you don't have to know the thresholds. [[slnc 250]] "
            "Whoever can answer, answers, and it stops there — the board never "
            "sees your lunch receipt. [[slnc 250]] And the hierarchy is not "
            "printed on the claim form. [[slnc 350]] The failure mode is the "
            "pattern's too. A claim nobody is allowed to approve sits in a queue "
            "forever."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So here are the pieces, and there aren't many. [[slnc 250]] The "
            "client is the checkout. It holds one thing, a screening chain, calls "
            "screen once, and gets back a report. [[slnc 300]] Screening chain is "
            "the wiring. It links the handlers together, hands the order to the "
            "first one, and then does nothing until somebody answers. [[slnc "
            "300]] Screening handler is the abstract link: one field pointing at "
            "the next link, and one method for subclasses to write. Underneath "
            "sit the four checks. [[slnc 250]] And coming back out is a report: "
            "the decision, who made it, and which links never ran."
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
            "This is the whole pattern, and it's about twenty lines. [[slnc 250]] "
            "One field, the next link. One method for subclasses to write, called "
            "check. And one method that walks the chain, called screen. [[slnc "
            "300]] Look at what check returns. An Optional of a decision. Empty "
            "means: I have no opinion, pass it on. A decision means: I am "
            "answering, and the chain stops here. Half the confusion about this "
            "pattern is people reading returns nothing as says no. [[slnc 350]] "
            "Now look at the word final in front of screen. In the textbook "
            "version every handler writes its own if-and-else, and the bug "
            "everybody hits is a handler that declines and forgets the else. The "
            "request vanishes, with no error. [[slnc 300]] Here there is one copy "
            "of that logic, and a link author never touches the next link at all."
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
            "Here's the chain itself, and two things are worth pointing at. "
            "[[slnc 250]] The first is what isn't here. No loop over the "
            "handlers, no index, no count. It hands the order to the first link "
            "and doesn't see it again until somebody answers. That's what makes "
            "reordering a wiring change. [[slnc 350]] The second is that or-else "
            "fallback. This is the expenses claim nobody can approve — an order "
            "really can pass every link with nobody deciding anything. [[slnc "
            "300]] So the fallback is a constructor argument, and there is no "
            "constructor without one. Approve by default, and you fail open. "
            "Refer by default, and you fail closed. Same links, opposite risk "
            "appetites, one argument apart."
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
            "Two of the links, on purpose different shapes. [[slnc 250]] Address "
            "check is the ordinary case. It rejects, and it names itself while "
            "doing it, so the answer carries the word address in a field rather "
            "than buried in a sentence. And when the address is fine it returns "
            "empty — no opinion. [[slnc 300]] Fraud score check is the one with "
            "three answers. Eighty and above, it rejects. Between fifty five and "
            "seventy nine it refers, so a human looks at it. Below that it says "
            "nothing. [[slnc 300]] That third answer costs the chain nothing, "
            "because the chain never looks inside the decision. A handler stops "
            "the chain whenever it is willing to own the answer — and the answer "
            "does not have to be no."
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
            "Twenty one tests, and these two make the point. [[slnc 300]] A test "
            "that says a Jersey order gets rejected passes against the naive "
            "method just as happily as against the chain. It proves nothing about "
            "the pattern. [[slnc 300]] The first one asserts that a link behind a "
            "decision never ran. Not that its answer was ignored — that it never "
            "ran at all. That's the risk model not being called, and not being "
            "billed for, written as an assertion. [[slnc 350]] The second is my "
            "favourite. Same four link classes, wired with payment above fraud, "
            "and the answer becomes the card again — the naive behaviour, "
            "reproduced exactly. It was never wrong. It was a setting you "
            "couldn't change without editing code."
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
            "Run it, and the two halves sit side by side. [[slnc 250]] Section "
            "one is the naive method: a fraud score of ninety two reported as a "
            "card problem, and a trade order accepted for delivery to an island "
            "no courier serves. [[slnc 300]] Section two is the same checks as "
            "links. Read the lines that begin never ran. On the monitor, fraud "
            "answers and the card link never runs. On the Jersey order, three "
            "links never ran — no warehouse query, no risk model call, nothing "
            "billed for. [[slnc 350]] That never-ran line is the real difference "
            "between this pattern and a validator that collects every problem. A "
            "chain gives you one answer, from one link, and stops. [[slnc 300]] "
            "And section four is the trade flow: the standard chain with one link "
            "left out of the wiring. Nothing was copied, so nothing could go "
            "missing, and Jersey is caught."
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
            "So, what to take away. [[slnc 300]] First, the confusion I promised "
            "to clear up. Chain of responsibility and decorator have the same "
            "class diagram. Not a similar one, the same one — so any explanation "
            "that separates them by structure is wrong. [[slnc 350]] The "
            "difference is one question you can ask before writing either. Does "
            "every layer have to run? [[slnc 250]] If yes, you want a decorator, "
            "and a layer that declined to pass the work on would be a bug. If no "
            "— a layer might settle the matter by itself — you want a chain. "
            "[[slnc 300]] In code that difference is one character deep. In a "
            "decorator, the call to the next object always happens. In a handler, "
            "it's inside an if. [[slnc 350]] Now the bill, honestly. A policy "
            "that read top to bottom in one method now lives across four check "
            "classes, a base class and a line of wiring. You need a report to see "
            "who decided. And an order can reach the end unanswered. [[slnc 300]] "
            "So if the checks and their order never change, write the four ifs. "
            "Reach for this when the order is something you need to change "
            "without editing any of them."
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
            "That's chain of responsibility. [[slnc 250]] The full source, the "
            "written notes, the diagrams and an animated walkthrough are all in "
            "the repository — including the exercise I'd most recommend. Take "
            "the standard chain, move the payment link above the fraud link, "
            "run the demo, and watch a customer get told something different "
            "about the same order. [[slnc 300]] If this helped, a like "
            "genuinely does help other people find it, and subscribe if you'd "
            "like the rest of the behavioural series. [[slnc 250]] Thanks for "
            "watching, and I'll see you in the next one."
        ),
    ),
]
