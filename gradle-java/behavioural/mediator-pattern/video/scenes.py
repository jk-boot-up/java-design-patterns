"""Scene definitions for the Mediator teaching video.

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
        title="Mediator",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Mediator pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. "
            "[[slnc 300]] Let's start with the simple definition. When a group "
            "of objects all affect each other, you can either wire every one of "
            "them to every other one, or you can give them a single object to "
            "talk to and let that object hold the rules. The mediator is that "
            "single object. [[slnc 350]] That's the idea in a sentence. The "
            "rest of the video does it properly, by building a real working "
            "Java project: the checkout page of an online shop, where choosing "
            "a delivery country changes the couriers, the gift wrapping, the "
            "total, and whether you're allowed to place the order at all. "
            "[[slnc 250]] By the end you'll know why five controls can need "
            "nine references, what that costs you, and the one criticism of "
            "this pattern that is completely fair."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The checkout page of an online shop. Five controls:",
            "",
            "    Country          where the order is going",
            "    Shipping         a courier that serves that country",
            "    Gift wrap        hand-wrapped in London — domestic only",
            "    Total            the price, read-only",
            "    Place Order      pressable once it is all filled in",
            "",
            "Four rules connect them:",
            "",
            "  country  ->  which couriers exist",
            "  country  ->  whether gift wrap is offered at all",
            "  shipping + gift wrap  ->  the total",
            "  country + shipping    ->  can the button be pressed",
        ],
        narration=(
            "So, imagine an online shop. [[slnc 250]] This is its checkout "
            "page, and it has five controls. Where the order is going. Which "
            "courier. Whether to gift wrap it. The total. And the place order "
            "button. [[slnc 300]] Those five are not independent. Change the "
            "country and the courier list has to change with it, because the "
            "courier that delivers in the United Kingdom is not the one that "
            "ships to the States. Gift wrapping is done by hand in the London "
            "warehouse, so it's only offered on domestic orders. The total "
            "follows the courier and the wrapping. And the button may only be "
            "pressed when there's both a country and a courier. [[slnc 350]] "
            "Four rules. Write them down and they fit on a slide. [[slnc 250]] "
            "The difficulty is never the rules. It's where they live."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Look Closely at One Click",
        body=[
            "The shopper has a UK order: Express shipping, gift wrapped, £48.",
            "",
            "Then they change the country to US.",
            "",
            "    gift wrap:  offered = false      <- correctly withdrawn",
            "    gift wrap:  ticked  = true       <- nobody cleared it",
            "",
            "    Total: £42     — and £2 of that is wrapping",
            "                     the London warehouse will never do.",
            "",
            "Nothing throws. Nothing logs.",
            "The shopper is simply charged for a service they cannot receive.",
        ],
        narration=(
            "Before any code, look closely at one click. [[slnc 300]] The "
            "shopper has a UK order. Express shipping, gift wrapped, forty "
            "eight pounds. Then they change their mind and send it to the "
            "States instead. [[slnc 300]] The gift wrap box is correctly "
            "withdrawn — the warehouse can't reach this order. But the tick is "
            "still there, because withdrawing the offer and clearing the tick "
            "were two separate things and only one of them got written. [[slnc "
            "350]] So the shopper pays two pounds for gift wrapping that will "
            "never happen. [[slnc 300]] Sit with that for a second, because it "
            "is the reason this pattern exists. Nothing throws. Nothing gets "
            "logged. It is a perfectly ordinary looking checkout with two "
            "pounds of pure fiction in it, and it can stay that way for a year."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — Everyone Wires Everyone",
        body="""country.wire(shipping, giftWrap, total, placeOrder);   // 4
shipping.wire(giftWrap, total, placeOrder);            // 3
giftWrap.wire(shipping, total);                        // 2
                                                       // 9 references

public void select(String country) {           // inside NaiveCountry
    this.country = country;
    shipping.showOptions(...);                 // remembered
    giftWrap.setAvailable(...);                // remembered — half of it
    total.recalculate(shipping, giftWrap);     // remembered
                                               // button: forgotten
}""",
        narration=(
            "Here's why. [[slnc 250]] The obvious place for, when the country "
            "changes, refill the couriers, is inside the country widget, "
            "because that's where the country changes. So the country widget is "
            "given the shipping widget. [[slnc 300]] Then gift wrap depends on "
            "the country too, so it needs that. And the total moved, so it "
            "needs the total. And the button might need re-checking, so it "
            "needs the button. [[slnc 300]] Nine references, on a page with "
            "five controls. And look at the method. Three of the four things it "
            "had to remember, it remembered. The fourth — re-check the button — "
            "isn't there. [[slnc 350]] And I want to be precise about the "
            "lesson, because it isn't that somebody was careless. It's that the "
            "correctness of this page depends on a person holding all five "
            "controls in their head, every time they touch any one of them."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "1.  Nobody can see the whole form.",
            "    'What happens when the country changes?' is spread",
            "    across three files, and no file has the answer.",
            "",
            "2.  The bugs are OMISSIONS. You cannot review a line",
            "    that was never written.",
            "",
            "3.  The wiring grows faster than the form:",
            "        3 controls -> 6      5 controls -> 20",
            "                    10 controls -> 90",
            "",
            "4.  No widget can be built or tested on its own.",
            "    And shipping holds gift wrap, which holds shipping.",
        ],
        narration=(
            "Let's be precise, because it's four separate costs. [[slnc 300]] "
            "One. Nobody can see the whole form. To answer what happens when "
            "the country changes, you read one method, then everything it "
            "calls, then everything those call. There is no file you can open "
            "that tells you what the page does. [[slnc 300]] Two. The bugs are "
            "omissions. A missing line looks exactly like nothing, and you "
            "cannot review nothing. [[slnc 300]] Three. The wiring grows faster "
            "than the form. Three controls, six possible connections. Five "
            "controls, twenty. Ten controls, ninety. This is why a form like "
            "this is perfectly fine on the day it's written and unmaintainable "
            "eighteen months later. [[slnc 300]] And four. No widget can be "
            "built or tested alone — the country selector needs four other "
            "widgets just to exist — and shipping holds gift wrap while gift "
            "wrap holds shipping, so neither can be understood without the "
            "other."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Mediator Pattern",
        # One line per rendered line: kind_quote lays these out as-is.
        body=[
            "Define an object that encapsulates how a set of",
            "objects interact. Mediator promotes loose coupling",
            "by keeping objects from referring to each other",
            "explicitly, and it lets you vary their interaction",
            "independently.",
            "",
            "— Gang of Four",
            "",
            "In plain terms:",
            "the parts stop talking to each other,",
            "and the rules move somewhere you can read them.",
        ],
        narration=(
            "Here's the definition from the Gang of Four book. [[slnc 250]] "
            "Define an object that encapsulates how a set of objects interact. "
            "Mediator promotes loose coupling by keeping objects from referring "
            "to each other explicitly. [[slnc 350]] There are two halves there "
            "and they're worth separating. Keeping objects from referring to "
            "each other is the mechanism — it's the nine references becoming "
            "five. [[slnc 300]] Encapsulates how a set of objects interact is "
            "the payoff, and it's the bigger of the two. After this "
            "refactoring, there is one file you can open, and one method inside "
            "it, and reading that method tells you everything the page does. "
            "[[slnc 300]] Nothing is hiding anywhere else, because there is "
            "nowhere else."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="An Analogy",
        body=[
            "Aircraft near an airport.",
            "",
            "  They do not negotiate with each other.",
            "  They all talk to the tower.",
            "",
            "Not because pilots can't be trusted —",
            "because n aircraft talking to each other is n² conversations,",
            "and one of them will be missed.",
            "",
            "One tower is n conversations,",
            "and the rules of the airspace are in one head.",
        ],
        narration=(
            "Here's the analogy to hold on to, and with this one, if you take "
            "nothing else away, take this. [[slnc 250]] Aircraft near an "
            "airport. [[slnc 300]] There is no protocol by which the inbound "
            "seven three seven asks the departing A three twenty to wait a "
            "minute. They don't talk to each other at all. They all talk to the "
            "tower, the tower knows where everything is, and the tower tells "
            "each of them what to do. [[slnc 350]] And that is not because "
            "pilots can't be trusted. It's arithmetic. Ten aircraft negotiating "
            "with each other is ninety conversations, and sooner or later one "
            "of them doesn't happen. Ten aircraft talking to a tower is ten "
            "conversations, and the rules of the airspace are in one head. "
            "[[slnc 300]] That's the whole pattern. Our checkout form is the "
            "tower, and the five controls are the aircraft."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "So here are the pieces. [[slnc 250]] Checkout mediator is the "
            "mediator role, and it has exactly one method: changed, taking the "
            "widget that changed. That is not an abbreviation for teaching. A "
            "mediator interface really can be this small, because colleagues "
            "are meant to report, not to ask. [[slnc 300]] Form widget is the "
            "colleague role. It has two fields, a name and a mediator, and the "
            "important one is the one that isn't there. There is no field on a "
            "widget capable of holding another widget, so the tangle isn't "
            "merely discouraged — it's unrepresentable. [[slnc 300]] Then the "
            "five concrete colleagues: country, shipping, gift wrap, the total "
            "and the button. Each one holds the form. The form holds all five. "
            "[[slnc 250]] Five arrows, all pointing the same way. It's a star, "
            "not a web, and that shape is the entire result."
        ),
    ),
    dict(
        key="09-colleague",
        kind="code",
        title="The Colleague — Notice What Is Missing",
        body="""public abstract class FormWidget {
    private final String name;
    private final CheckoutMediator mediator;    // its ONLY reference

    protected void announceChange() {
        mediator.changed(this);
    }
}

public class CountrySelector extends FormWidget {
    public void select(String country) {
        this.country = country;
        announceChange();          // "something about me changed"
    }                              // ...and that is the whole class
}""",
        narration=(
            "This is the colleague, and I'd rather talk about what isn't here. "
            "[[slnc 250]] Two fields. A name, and a mediator. There is no field "
            "that can hold another widget, which means a widget could not reach "
            "across the form even if a future change wanted it to. [[slnc 350]] "
            "And then look at the country selector. Store the string, announce "
            "the change, stop. That is the whole class. [[slnc 300]] Put it next "
            "to the naive version we saw earlier — four statements about four "
            "other widgets, and still missing one. [[slnc 300]] The widget's "
            "entire vocabulary is now, something about me is different. What "
            "that means for the rest of the page is not its business, and, "
            "crucially, it has no reference with which to make it its business."
        ),
    ),
    dict(
        key="10-mediator",
        kind="code",
        title="The Mediator — The Whole Page, in One Method",
        body="""@Override
public void changed(FormWidget source) {

    if (source == country) {                  // the only branch
        shipping.showOptions(methodsFor(country.country()));
        giftWrap.setAvailable(isDomestic(country.country()));
    }

    refreshTotal();       // every time, whatever changed
    refreshButton();      // every time, whatever changed
}

void setAvailable(boolean available) {        // on GiftWrapCheckbox
    this.available = available;
    if (!available) this.ticked = false;      // one call, both facts
}""",
        narration=(
            "And here's the page. Once. [[slnc 300]] Read those six lines and "
            "you have read the behaviour of the checkout. [[slnc 300]] Two "
            "things are worth pausing on. First, the refresh calls run on every "
            "change, unconditionally. Nothing works out whether they need to. "
            "[[slnc 300]] That's what makes the second bug impossible here — "
            "the mediator never has to notice that clearing the courier affects "
            "the button, because it re-asks that question every single time, "
            "whatever the change was. Cheap and always right beats clever and "
            "sometimes stale. [[slnc 350]] Second, look at set available at the "
            "bottom. Withdrawing gift wrap clears the tick in the same method. "
            "And that is not, we remembered to also untick it. There is no "
            "method in the project that does only half of that, so there is "
            "nothing left to forget. [[slnc 300]] One if. That is the entire "
            "control flow of the page."
        ),
    ),
    dict(
        key="11-proof",
        kind="code",
        title="The Tests — Asserting the Structure, Not Just the Behaviour",
        body="""@Test void widgetsOnlyKnowTheMediator() {
    for (FormWidget widget : allFiveWidgets) {
        for (Field field : allFieldsOf(widget.getClass())) {
            if (FormWidget.class.isAssignableFrom(field.getType()))
                offenders.add(widget.name() + "." + field.getName());
        }
    }
    assertEquals(List.of(), offenders);      // no widget holds a widget
}

@Test void chargesForWrappingItWillNotDo() {     // the NAIVE form
    naive.country().select("US");
    assertTrue(naive.giftWrap().isTicked());     // the wrong answer,
    assertEquals(42, naive.total().pounds());    // pinned on purpose
}""",
        narration=(
            "Fourteen tests, and these two are the ones that prove the pattern. "
            "[[slnc 300]] A test that says picking Express makes the total forty "
            "six passes against the tangled version just as happily. It proves "
            "nothing. [[slnc 300]] The first one asserts the structure. It walks "
            "every field of every widget by reflection, and fails if any of them "
            "has a widget type. [[slnc 300]] Because a comment saying, widgets "
            "must not reference each other, survives exactly as long as the "
            "first person who is in a hurry. This doesn't. [[slnc 350]] And the "
            "second one is the interesting one, because it asserts the wrong "
            "answer. It pins the naive form's bug in place — still ticked, "
            "forty two pounds — with a message saying so. [[slnc 300]] Fix the "
            "naive version and its own tests go red. That's deliberate. The "
            "cost of that design is meant to be something the build says out "
            "loud, not something a README claims."
        ),
    ),
    dict(
        key="12-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

=== every widget wired to every other ===
UK, Express, gift wrapped        Total: £48   place order: enabled
shopper changes the country to US
  shipping chosen : (none)
  gift wrap       : offered=false, ticked=true    <- still ticked
  Total: £42                     <- £2 of wrapping that won't happen
  place order     : enabled      <- no courier, and it lets them through

=== every widget wired to the mediator ===
UK, Express, gift wrapped        Total: £48   place order: enabled
shopper changes the country to US
  gift wrap       : offered=false, ticked=false   <- cleared with it
  Total: £40                     <- basket only, nothing chosen yet
  place order     : disabled     <- the form re-checked itself""",
        narration=(
            "Run it, and the two halves sit side by side. [[slnc 250]] Same "
            "page. Same three clicks. Same change of mind. [[slnc 300]] The top "
            "half is the tangled version: forty two pounds, two of them "
            "phantom, and a place order button that will happily take an order "
            "with no courier on it. [[slnc 300]] The bottom half is the "
            "mediated one. The tick went when the offer went. The courier was "
            "cleared, so the total is back to just the basket. And the button "
            "disabled itself. [[slnc 350]] And here's the part I'd frame. "
            "Nobody wrote a line of code that says, when the country changes, "
            "disable the button. It falls out, because there is one place where "
            "the reaction to a change is written, and that place re-checks "
            "everything every time."
        ),
    ),
    dict(
        key="13-wrapup",
        kind="bullets",
        title="What to Remember",
        body=[
            "When everything talks to everything, nobody sees the whole thing.",
            "Give them one place to talk to, and the rules have somewhere to live.",
            "",
            "  Mediator   colleagues know it; it knows all of them",
            "  Observer   the publisher knows NOTHING about its subscribers",
            "  Facade     faces outward, to simplify life for a caller",
            "",
            "A publisher could not disable a button because a",
            "drop-down was cleared. A mediator can. That is the job.",
            "",
            "The honest cost: everything you take out of the widgets",
            "goes INTO the mediator. Split it before it becomes",
            "the class nobody wants to open.",
        ],
        narration=(
            "So, what to take away. [[slnc 300]] When everything talks to "
            "everything, nobody can see the whole thing. Give them one place to "
            "talk to, and the rules have somewhere to live. [[slnc 350]] On the "
            "comparison, because this is the question I'd expect. Mediator and "
            "observer both remove direct references, and they get confused "
            "constantly. The difference is knowledge. An observer publisher "
            "deliberately knows nothing about its subscribers. A mediator knows "
            "all of its colleagues, on purpose, and that knowledge is exactly "
            "what lets it enforce a rule spanning several of them. [[slnc 300]] "
            "A publisher could not disable a button because a drop-down was "
            "cleared. A mediator can. That's the job. And a facade sits in "
            "front of several objects too, but it faces outwards — it exists to "
            "simplify life for a caller outside. A mediator faces inwards. "
            "[[slnc 350]] Now the honest bill, and this is the one pattern "
            "whose main criticism I think is completely fair. Everything you "
            "take out of the widgets goes into the mediator, and on a real form "
            "that class gets big. It becomes a god object if you let it. The "
            "answer isn't to deny that, it's to split it — one mediator per "
            "section of the page — before it becomes the class nobody wants to "
            "open. [[slnc 300]] And don't reach for it on a form with two "
            "controls. Two things that affect each other, and never will be "
            "three, are clearer wired directly. This earns its keep at about "
            "four or five interacting parts, which is exactly where it stops "
            "being possible to hold the wiring in your head."
        ),
    ),
    dict(
        key="14-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that gives",
            "one widget a reference to another, and watches a test name it.",
        ],
        narration=(
            "That's the mediator pattern. [[slnc 250]] The full source, the "
            "written notes, the diagrams and an animated walkthrough are all in "
            "the repository — including the exercise I'd most recommend. Give "
            "the country selector a field of type total label, run the tests, "
            "and watch the isolation test name the offending field back at you. "
            "It takes a minute, and it's the moment the structural promise stops "
            "being a comment. [[slnc 300]] If this helped, a like genuinely does "
            "help other people find it, and subscribe if you'd like the rest of "
            "the behavioural series. [[slnc 250]] Thanks for watching, and I'll "
            "see you in the next one."
        ),
    ),
]
